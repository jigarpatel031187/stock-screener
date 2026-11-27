"""
Trade Plan Agent Engine for AntiGravity Smart Money Dual Track Radar.

Combines:
  1. Market Regime & Cap-Tier Budget Allocator (Swing % / Core % / GTT Reserve %)
  2. All-750 Stock 3-Phase Smart Money Scoring + Top-Down Sector Confluence
  3. Portfolio Heat & Sector Concentration Guardrails (via data/trades.json)
  4. Anti-Stop-Hunt Two-Tier Stop Engine (Wide Hard GTT SL + Soft EOD Close SL)
  5. Daily Execution Summary for Tab 4 [F5], On-Demand CLI, and Telegram.
"""

import argparse
import datetime
import json
import math
import os
from typing import Any, Dict, List, Optional

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
TRADE_PLAN_CACHE_PATH = os.path.join(DATA_DIR, "trade_plan.json")

DEFAULT_CAPITAL_INR = 1_000_000.0
DEFAULT_SWING_RISK_PCT = 0.75
MAX_PORTFOLIO_HEAT_PCT = 4.5
MAX_SECTOR_SLOTS = 2

SECTOR_ACCOUNT_ROUTER = {
    "IT": "Kritika",
    "Capital Markets": "Kritika",
    "Telecom": "Kritika",
    "Auto": "Kritika",
    "FMCG & Consumer": "Kritika",
    "Consumer Durables": "Kritika",
    "Media & Entertainment": "Kritika",
    "Textiles": "Kritika",
    "Services & Logistics": "Kritika",
    "Financials": "Vina",
    "PSU Banks": "Vina",
    "Capital Goods": "Vina",
    "Pharmaceuticals": "Vina",
    "Metals & Mining": "Vina",
    "Energy & Power": "Vina",
    "Infrastructure": "Vina",
    "Chemicals": "Vina",
    "Real Estate": "Vina",
}


def _round_cluster_guard(level: float) -> float:
    """
    Shifts stops slightly below psychologically rounded numbers (50 / 100 / 500 / 1000)
    where retail stops and algorithmic liquidity sweeps cluster.
    """
    if level <= 5.0:
        return round(level, 2)
    step = 100.0 if level >= 1500 else (50.0 if level >= 400 else 10.0)
    nearest = round(level / step) * step
    if abs(level - nearest) <= max(1.0, level * 0.0025):
        level = nearest - max(1.5, round(level * 0.0035, 1))
    return round(level, 1)


def compute_market_regime(tape: dict, universe_nodes: list) -> dict:
    """Derives equity risk regime and Swing/Core/GTT allocation from Breadth, VIX, and Cap Phases."""
    adv = int((tape or {}).get("adv", 0) or 0)
    dec = int((tape or {}).get("dec", 0) or 0)
    total = adv + dec
    breadth_pct = round((adv / total) * 100.0, 1) if total > 0 else 55.0
    vix = float(((tape or {}).get("vix") or {}).get("last") or 16.5)

    cap_map = {n.get("id"): n for n in (universe_nodes or []) if n.get("kind") == "cap"}
    mid_tier = (cap_map.get("NIFTY_MID150") or {}).get("preExplodeTier", "NEUTRAL")
    sml_tier = (cap_map.get("NIFTY_SML250") or {}).get("preExplodeTier", "NEUTRAL")

    if breadth_pct >= 55.0 and vix < 18.5 and (mid_tier in ("PHASE_3", "PHASE_2") or sml_tier in ("PHASE_3", "PHASE_2")):
        regime = "RISK_ON_EXPANSION"
        label = "RISK-ON EXPANSION"
        swing_pct, core_pct, gtt_pct, risk_pct = 45, 55, 25, 0.75
    elif breadth_pct < 42.0 or vix >= 21.0:
        regime = "DEFENSIVE_PRESERVATION"
        label = "DEFENSIVE PRESERVATION"
        swing_pct, core_pct, gtt_pct, risk_pct = 15, 85, 55, 0.50
    else:
        regime = "SELECTIVE_ROTATION"
        label = "SELECTIVE ROTATION"
        swing_pct, core_pct, gtt_pct, risk_pct = 30, 70, 40, 0.65

    return {
        "regime": regime,
        "label": label,
        "breadth_pct": breadth_pct,
        "adv": adv,
        "dec": dec,
        "vix": round(vix, 2),
        "midcap_tier": mid_tier,
        "smallcap_tier": sml_tier,
        "swing_budget_pct": swing_pct,
        "core_budget_pct": core_pct,
        "gtt_cash_reserve_pct": gtt_pct,
        "recommended_risk_pct": risk_pct,
        "max_heat_pct": MAX_PORTFOLIO_HEAT_PCT,
    }


def compute_sweep_proof_stops(
    price: float,
    swing_low: float,
    dma20: float,
    ema20: float,
    dma150: float,
    atr14: float,
    entry_ref: Optional[float] = None,
) -> dict:
    """
    Builds Two-Tier Anti-Stop-Hunt Risk Geometry:
      - softEodSl: Closing-basis decision stop at 3:15 PM IST (Swing Low / 20-DMA buffer)
      - hardGttSl: Wide disaster GTT SL anchored min(SwingLow - 1.0*ATR, Entry - 1.5*ATR),
                   clamped between 4.0% and 8.0% risk, nudged off round numbers
      - beTrailSl: Post-T1 trailing stop anchored below 20-EMA / pivot instead of 0.2% chaseable noise
      - coreStructSl: 150-DMA - 1.0*ATR for 8-12M Core compounding
    """
    cmp_val = float(price or 1.0)
    atr = float(atr14) if (atr14 and atr14 > 0) else round(cmp_val * 0.025, 1)
    ref = float(entry_ref) if (entry_ref and entry_ref > 0) else cmp_val
    d20 = float(dma20) if (dma20 and dma20 > 0) else cmp_val * 0.97
    e20 = float(ema20) if (ema20 and ema20 > 0) else d20
    d150 = float(dma150) if (dma150 and dma150 > 0) else cmp_val * 0.88
    sw_low = float(swing_low) if (swing_low and swing_low > 0) else cmp_val * 0.93

    raw_wide = min(sw_low - (1.0 * atr), ref - (1.5 * atr))
    min_sl_cap = ref * 0.92  # Max 8.0% risk
    max_sl_floor = ref * 0.96  # Min 4.0% breathing room
    clamped_sl = max(min_sl_cap, min(max_sl_floor, raw_wide))
    hard_gtt_sl = _round_cluster_guard(clamped_sl)
    if hard_gtt_sl >= ref:
        hard_gtt_sl = round(ref * 0.955, 1)

    wide_risk = max(1.0, round(ref - hard_gtt_sl, 2))
    risk_pct = round((wide_risk / ref) * 100.0, 2) if ref > 0 else 5.0

    soft_raw = max(sw_low * 0.996, d20 - (0.35 * atr))
    soft_eod_sl = round(min(ref * 0.975, max(hard_gtt_sl * 1.008, soft_raw)), 1)

    t1_2r = round(ref + (2.0 * wide_risk), 1)
    t2_35r = round(ref + (3.5 * wide_risk), 1)
    be_trail_sl = _round_cluster_guard(max(e20 - (0.5 * atr), ref - (0.4 * atr)))

    core_struct_sl = _round_cluster_guard(min(ref * 0.90, d150 - (1.0 * atr)))
    return {
        "entryRef": round(ref, 2),
        "entryBand": f"{round(min(ref, d20), 0):.0f}-{round(ref + 0.5 * atr, 0):.0f}",
        "hardGttSl": hard_gtt_sl,
        "softEodSl": soft_eod_sl,
        "beTrailSl": be_trail_sl,
        "riskPerShare": round(wide_risk, 1),
        "riskPct": risk_pct,
        "t1_2r": t1_2r,
        "t2_35r": t2_35r,
        "coreStructSl": core_struct_sl,
    }


def evaluate_open_trades(
    trades: list,
    stock_lookup: dict,
    capital: float = DEFAULT_CAPITAL_INR,
    risk_pct: float = DEFAULT_SWING_RISK_PCT,
) -> dict:
    """
    Audits live open/pending/recent-stop trades from data/trades.json:
      - Computes total open portfolio heat (% & INR)
      - Detects Spring & Reclaim setups on recent intraday stop-outs
      - Emits explicit daily execution instruction per trade.
    """
    open_actions = []
    open_symbols = set()
    sector_counts: Dict[str, int] = {}
    total_open_risk_inr = 0.0

    now_ist = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
    risk_inr_per_slot = capital * (risk_pct / 100.0)

    for tr in (trades or []):
        sym = str(tr.get("symbol", "")).replace(".NS", "")
        status = tr.get("status", "")
        sector = tr.get("sector", "Equities")
        st_live = stock_lookup.get(sym, {})
        cmp_val = float(st_live.get("price") or tr.get("current_price") or tr.get("entry_price") or 0.0)
        entry_p = float(tr.get("entry_price") or cmp_val or 1.0)
        curr_sl = float(tr.get("current_sl") or tr.get("initial_sl") or 0.0)
        t1 = float(tr.get("target_1_2r") or 0.0)
        t2 = float(tr.get("target_2_3r") or 0.0)
        r_mult = float(tr.get("pnl_r") or 0.0)

        if status in ("ACTIVE", "T1_HIT", "PENDING_TRIGGER"):
            open_symbols.add(sym)
            # Map broad sector string cleanly for concentration guard
            sec_key = st_live.get("sector") or sector
            sector_counts[sec_key] = sector_counts.get(sec_key, 0) + 1

            if status == "ACTIVE":
                total_open_risk_inr += risk_inr_per_slot
                if t1 > 0 and cmp_val >= t1 * 0.985:
                    action = "BOOK_T1_40PCT"
                    note = f"Near T1 ₹{t1:.0f} — book 40% & trail SL to Cost/EMA"
                elif r_mult >= 1.0:
                    trail_lvl = round(max(curr_sl, float(st_live.get("ema20") or cmp_val) - 0.5 * float(st_live.get("atr14") or cmp_val * 0.02)), 1)
                    action = "HOLD_TRAIL_SL"
                    note = f"+{r_mult:.2f}R — consider raising SL toward ₹{trail_lvl}"
                else:
                    action = "HOLD_MONITOR_EOD"
                    note = f"Obey Closing SL < ₹{curr_sl:.1f} (avoid premature exit)"
            elif status == "T1_HIT":
                total_open_risk_inr += risk_inr_per_slot * 0.25  # Reduced residual risk
                action = "RIDE_RUNNER"
                note = f"T1 booked; trail remaining 60% toward T2 ₹{t2:.0f} / 20-EMA"
            else:
                # PENDING_TRIGGER
                total_open_risk_inr += risk_inr_per_slot * 0.5
                action = "ARM_BUY_GTT"
                note = f"Buy-Stop GTT @ ₹{entry_p:.1f} | Wide SL ₹{curr_sl:.1f} | After 9:45 AM"

            open_actions.append({
                "symbol": sym,
                "name": tr.get("name", sym),
                "track": tr.get("track", "Track B"),
                "sector": sec_key,
                "status": status,
                "action": action,
                "cmp": round(cmp_val, 2),
                "entry": round(entry_p, 2),
                "sl": round(curr_sl, 1),
                "t1": round(t1, 1),
                "t2": round(t2, 1),
                "pnlPct": tr.get("pnl_pct", 0.0),
                "pnlR": r_mult,
                "sectorTier": st_live.get("sectorTier", "NEUTRAL"),
                "stockTier": st_live.get("preExplodeTier", "NEUTRAL"),
                "note": note,
            })

        elif status in ("STOPPED_OUT", "STOPPED_OUT_BE"):
            exit_dt_str = tr.get("exit_date") or ""
            days_since_exit = 99
            if exit_dt_str:
                try:
                    dt_ex = datetime.datetime.strptime(exit_dt_str, "%Y-%m-%d")
                    days_since_exit = (now_ist.replace(tzinfo=None) - dt_ex).days
                except Exception:
                    pass
            init_sl = float(tr.get("initial_sl") or curr_sl or 0.0)
            dma20 = float(st_live.get("dma20") or cmp_val)
            if days_since_exit <= 7 and cmp_val > init_sl and cmp_val >= dma20 and init_sl > 0:
                open_actions.append({
                    "symbol": sym,
                    "name": tr.get("name", sym),
                    "track": tr.get("track", "Track B"),
                    "sector": st_live.get("sector") or sector,
                    "status": "SPRING_RECLAIM",
                    "action": "REENTRY_WATCH",
                    "cmp": round(cmp_val, 2),
                    "entry": round(cmp_val, 2),
                    "sl": round(init_sl * 0.985, 1),
                    "t1": round(t1, 1),
                    "t2": round(t2, 1),
                    "pnlPct": 0.0,
                    "pnlR": 0.0,
                    "sectorTier": st_live.get("sectorTier", "NEUTRAL"),
                    "stockTier": st_live.get("preExplodeTier", "NEUTRAL"),
                    "note": f"Spring & Reclaim above SL ₹{init_sl:.0f} + 20DMA — 1-shot re-entry eligible",
                })

    open_heat_pct = round((total_open_risk_inr / max(1.0, capital)) * 100.0, 2)
    return {
        "open_actions": open_actions,
        "open_symbols": open_symbols,
        "sector_counts": sector_counts,
        "open_heat_pct": open_heat_pct,
        "open_heat_inr": round(total_open_risk_inr, 0),
    }


def _enrich_candidate_ticket(
    st: dict,
    curated: Optional[dict],
    signal_item: Optional[dict],
    capital: float,
    risk_pct: float,
    swing_slot_inr: float,
    core_slot_inr: float,
    regime: dict,
) -> dict:
    """Computes full Swing + Core ticket fields for any NSE equity."""
    price = float(st.get("price") or (curated or {}).get("price") or 0.0)
    if price <= 0:
        return {}

    entry_ref = float((signal_item or {}).get("entry_trigger") or price)
    stops = compute_sweep_proof_stops(
        price=price,
        swing_low=st.get("swingLow") or (curated or {}).get("swingLow") or price * 0.93,
        dma20=st.get("dma20") or (curated or {}).get("dma20") or price * 0.97,
        ema20=st.get("ema20") or st.get("dma20") or price * 0.97,
        dma150=st.get("dma150") or (curated or {}).get("dma150") or price * 0.88,
        atr14=st.get("atr14") or (curated or {}).get("atr14") or price * 0.025,
        entry_ref=entry_ref,
    )

    max_risk_inr = capital * (risk_pct / 100.0)
    risk_per_share = max(1.0, stops["riskPerShare"])
    qty_by_risk = int(max_risk_inr // risk_per_share)
    qty_by_cap = int(swing_slot_inr // max(1.0, stops["entryRef"]))
    swing_shares = max(0, min(qty_by_risk, qty_by_cap))
    swing_alloc_inr = round(swing_shares * stops["entryRef"], 0)

    t1_sh = swing_shares // 2
    t2_sh = swing_shares - t1_sh

    # Core valuation & 3-tranche scaling (40% Pilot / 35% Confirm / 25% GTT Dip Reserve)
    if curated and curated.get("fairValue"):
        fv = float(curated["fairValue"])
        core_band = f"{round(fv * 0.85):.0f}-{round(fv * 0.95):.0f}"
        core_base = round(float(curated.get("base") or fv), 0)
        core_bull = round(float(curated.get("bull") or fv * 1.15), 0)
        core_upside = round(((core_base - price) / price) * 100.0, 1)
        val_model = curated.get("valMethod", "DCF / Fwd PE")
        kpi_stop = curated.get("kpiStop", "Quarterly Margin / OCF Breach")
        roe_val = curated.get("roe", "--")
    else:
        d150 = float(st.get("dma150") or price * 0.9)
        core_band = f"{round(min(price, d150)):.0f}-{round(price * 0.99):.0f}"
        core_base = round(price * 1.24, 0)
        core_bull = round(price * 1.40, 0)
        core_upside = 24.0
        val_model = "Stage-2 + Sector Alpha"
        kpi_stop = f"Weekly Close < ₹{stops['coreStructSl']:.0f} (150DMA−1×ATR)"
        roe_val = (signal_item or {}).get("roe", "--")

    core_shares = max(0, int(core_slot_inr // price))
    core_t1_sh = int(round(core_shares * 0.40))
    core_t2_sh = int(round(core_shares * 0.35))
    core_t3_sh = max(0, core_shares - core_t1_sh - core_t2_sh)

    sector = st.get("sector") or (curated or {}).get("sector") or "Equities"
    assigned = (curated or {}).get("assigned") or SECTOR_ACCOUNT_ROUTER.get(sector, "Kritika")

    return {
        "ticker": st["ticker"],
        "name": st.get("name") or (curated or {}).get("name") or st["ticker"],
        "sector": sector,
        "bucket": st.get("bucket", "NSE"),
        "price": round(price, 2),
        "chg": st.get("chg", 0.0),
        "w1": st.get("w1", 0.0),
        "m1": st.get("m1", 0.0),
        "m3": st.get("m3", 0.0),
        "y1": st.get("y1", 0.0),
        "sectorTier": st.get("sectorTier") or "NEUTRAL",
        "sectorScore": st.get("sectorScore") or 0,
        "stockTier": st.get("preExplodeTier") or "NEUTRAL",
        "stockScore": st.get("preExplodeScore") or 0,
        "confluence": st.get("confluence") or "STANDARD",
        "signalTag": st.get("signalTag"),
        "bbwPct": st.get("bbwPct", 50.0),
        "atrDecay": st.get("atrDecay", 1.0),
        "volDryRatio": st.get("volDryRatio", 1.0),
        "upDownVol": st.get("upDownVol", 1.0),
        "alphaSec1W": st.get("alphaSec1W", 0.0),
        "alphaSec1M": st.get("alphaSec1M", 0.0),
        "stage2Pass": bool(st.get("stage2Pass", False)),
        "reasons": st.get("preExplodeReasons", []),
        "account": assigned,
        "atr14": st.get("atr14", 0.0),
        "dma20": st.get("dma20", 0.0),
        "dma150": st.get("dma150", 0.0),
        "swingLow": st.get("swingLow", 0.0),
        "swing": {
            "entryRef": stops["entryRef"],
            "entryBand": stops["entryBand"],
            "hardGttSl": stops["hardGttSl"],
            "softEodSl": stops["softEodSl"],
            "beTrailSl": stops["beTrailSl"],
            "riskPerShare": stops["riskPerShare"],
            "riskPct": stops["riskPct"],
            "t1_2r": stops["t1_2r"],
            "t2_35r": stops["t2_35r"],
            "shares": swing_shares,
            "tranche1Shares": t1_sh,
            "tranche2Shares": t2_sh,
            "allocInr": swing_alloc_inr,
            "maxRiskInr": round(swing_shares * wide_risk_val(stops), 0),
        },
        "core": {
            "accumBand": core_band,
            "structSl": stops["coreStructSl"],
            "kpiStop": kpi_stop,
            "baseTarget": core_base,
            "bullTarget": core_bull,
            "upsidePct": core_upside,
            "valModel": val_model,
            "roe": roe_val,
            "shares": core_shares,
            "tranche1Shares": core_t1_sh,
            "tranche2Shares": core_t2_sh,
            "tranche3Shares": core_t3_sh,
            "allocInr": round(core_shares * price, 0),
        },
        "isCurated": bool(curated),
        "isCore": bool((curated or {}).get("isCore")),
        "isSwing": bool((curated or {}).get("isSwing")),
    }


def wide_risk_val(stops: dict) -> float:
    return max(1.0, float(stops.get("riskPerShare") or 1.0))


def build_trade_plan_payload(
    sector_rotation: Optional[dict],
    trades: Optional[list] = None,
    active_breakouts: Optional[list] = None,
    pre_breakout_squeezes: Optional[list] = None,
    capital: float = DEFAULT_CAPITAL_INR,
    risk_pct: float = DEFAULT_SWING_RISK_PCT,
) -> dict:
    """
    Produces the complete Trade Plan payload consumed by Tab 4 F5, Telegram, and CLI.
    """
    sr = sector_rotation or {}
    universe_nodes = sr.get("universe_nodes", [])
    tape = sr.get("tape", {})
    curated_list = sr.get("curated_stocks", [])
    all_scored = sr.get("all_stocks_scored", [])

    curated_map = {s["ticker"]: s for s in curated_list if s.get("ticker")}
    sector_map = {n["group"]: n for n in universe_nodes if n.get("kind") == "sector"}

    sig_map: Dict[str, dict] = {}
    for x in (active_breakouts or []):
        sym = str(x.get("symbol", "")).replace(".NS", "")
        if sym:
            sig_map[sym] = {**x, "signalTag": "TRACK A"}
    for x in (pre_breakout_squeezes or []):
        sym = str(x.get("symbol", "")).replace(".NS", "")
        if sym and sym not in sig_map:
            sig_map[sym] = {**x, "signalTag": "TRACK B"}

    # Merge global evaluated universe + curated stocks
    merged_map: Dict[str, dict] = {}
    for st in all_scored:
        tk = st.get("ticker")
        if not tk:
            continue
        sec = st.get("sector")
        if sec in sector_map and not st.get("sectorTier"):
            st = {
                **st,
                "sectorTier": sector_map[sec].get("preExplodeTier", "NEUTRAL"),
                "sectorScore": sector_map[sec].get("preExplodeScore", 0),
            }
        merged_map[tk] = st

    for tk, cur in curated_map.items():
        if tk not in merged_map and cur.get("ticker") != "NSE":
            merged_map[tk] = cur

    regime = compute_market_regime(tape, universe_nodes)
    audit = evaluate_open_trades(trades or [], merged_map, capital=capital, risk_pct=risk_pct)

    swing_capital = capital * (regime["swing_budget_pct"] / 100.0)
    core_capital = capital * (regime["core_budget_pct"] / 100.0)
    swing_slot_inr = max(50_000.0, swing_capital / 6.0)
    core_slot_inr = max(50_000.0, core_capital / 8.0)

    tickets: List[dict] = []
    for tk, st in merged_map.items():
        tkt = _enrich_candidate_ticket(
            st=st,
            curated=curated_map.get(tk),
            signal_item=sig_map.get(tk),
            capital=capital,
            risk_pct=risk_pct,
            swing_slot_inr=swing_slot_inr,
            core_slot_inr=core_slot_inr,
            regime=regime,
        )
        if tkt:
            tickets.append(tkt)

    # 1. Build 1-2M Swing Queue (Phase 3 stocks or Track A/B, never EXTENDED)
    sim_heat = float(audit["open_heat_pct"])
    sim_sectors = dict(audit["sector_counts"])
    swing_candidates = [
        t for t in tickets
        if t["stockTier"] != "EXTENDED"
        and (
            t.get("signalTag") in ("TRACK A", "TRACK B")
            or t["stockTier"] == "PHASE_3"
            or (t["stockTier"] == "PHASE_2" and t["sectorTier"] in ("PHASE_3", "PHASE_2") and t["stage2Pass"])
        )
    ]
    tier_weight = {"PHASE_3": 3, "PHASE_2": 2, "PHASE_1": 1, "NEUTRAL": 0}
    swing_candidates.sort(
        key=lambda t: (
            1 if t.get("signalTag") else 0,
            1 if t["confluence"] == "DUAL_CONFLUENCE" else 0,
            tier_weight.get(t["stockTier"], 0),
            t["stockScore"] + int(t["sectorScore"] * 0.4),
        ),
        reverse=True,
    )

    swing_queue = []
    for t in swing_candidates[:18]:
        tk = t["ticker"]
        sec = t["sector"]
        size_mult = 1.0 if (t["sectorTier"] in ("PHASE_3", "PHASE_2") or t.get("signalTag")) else 0.5
        if tk in audit["open_symbols"]:
            guard = "ALREADY_OPEN"
        elif sim_sectors.get(sec, 0) >= MAX_SECTOR_SLOTS:
            guard = "SECTOR_CAP"
        elif sim_heat + risk_pct * size_mult > MAX_PORTFOLIO_HEAT_PCT:
            guard = "HEAT_CAP"
        else:
            guard = "EXECUTE_GTT" if t.get("signalTag") == "TRACK B" else ("EXECUTE_ACTIVE" if t.get("signalTag") == "TRACK A" else ("READY_1.0R" if size_mult == 1.0 else "PILOT_0.5R"))
            sim_sectors[sec] = sim_sectors.get(sec, 0) + 1
            sim_heat += risk_pct * size_mult

        row = {**t, "guard": guard, "sizeMult": size_mult}
        if size_mult < 1.0:
            sw = dict(t["swing"])
            sw["shares"] = sw["shares"] // 2
            sw["tranche1Shares"] = sw["shares"] // 2
            sw["tranche2Shares"] = sw["shares"] - sw["tranche1Shares"]
            sw["allocInr"] = round(sw["shares"] * sw["entryRef"], 0)
            sw["maxRiskInr"] = round(sw["shares"] * sw["riskPerShare"], 0)
            row["swing"] = sw
        swing_queue.append(row)

    # 2. Build 8-12M Core Queue (Curated Core + Stage-2 Quality inside P2/P1/early P3 non-extended sectors)
    core_candidates = [
        t for t in tickets
        if t["sectorTier"] != "EXTENDED"
        and t["stockTier"] != "EXTENDED"
        and (
            (t["isCurated"] and t["isCore"])
            or (t["stage2Pass"] and t["sectorTier"] in ("PHASE_2", "PHASE_1", "PHASE_3") and t["stockTier"] in ("PHASE_2", "PHASE_1", "PHASE_3"))
        )
    ]
    core_candidates.sort(
        key=lambda t: (
            1 if (t["isCurated"] and t["isCore"]) else 0,
            1 if t["sectorTier"] in ("PHASE_2", "PHASE_3") else 0,
            t["core"]["upsidePct"] * 0.4 + t["stockScore"] + t["sectorScore"] * 0.5,
        ),
        reverse=True,
    )
    core_queue = []
    for t in core_candidates[:18]:
        st_phase = t["stockTier"]
        sec_phase = t["sectorTier"]
        if sec_phase == "PHASE_3" or st_phase == "PHASE_3":
            action = "CONFIRM_ADD_35%"
        elif sec_phase in ("PHASE_2", "PHASE_1") or st_phase in ("PHASE_2", "PHASE_1"):
            action = "PILOT_ACCUM_40%"
        else:
            action = "GTT_DIP_25%"
        core_queue.append({**t, "coreAction": action})

    # Compact lookup pool covering ALL evaluated universe stocks for single-ticker F5 lookups
    compact_pool = {}
    for t in tickets:
        compact_pool[t["ticker"]] = t

    now_ist = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
    return {
        "generated_at": now_ist.strftime("%b %d, %Y (%I:%M %p IST)"),
        "capital": capital,
        "risk_pct": risk_pct,
        "regime": regime,
        "portfolio_audit": {
            "open_heat_pct": audit["open_heat_pct"],
            "open_heat_inr": audit["open_heat_inr"],
            "sector_counts": audit["sector_counts"],
            "open_actions": audit["open_actions"],
        },
        "swing_queue": swing_queue,
        "core_queue": core_queue,
        "stock_lookup": compact_pool,
    }


def build_daily_trade_plan_telegram(trade_plan: dict) -> str:
    """Renders a crisp, mobile-ready Telegram daily action brief (< 3500 chars)."""
    reg = trade_plan.get("regime", {})
    aud = trade_plan.get("portfolio_audit", {})
    swing = trade_plan.get("swing_queue", [])
    core = trade_plan.get("core_queue", [])
    gen_at = trade_plan.get("generated_at", "Live")
    cap = trade_plan.get("capital", DEFAULT_CAPITAL_INR)

    lines = [
        f"📋 *ANTIGRAVITY TRADE PLAN BRIEF* | _{gen_at}_",
        f"⚖️ *Regime:* `{reg.get('label', 'SELECTIVE')}` (`{reg.get('breadth_pct', 0)}% Adv` | VIX `{reg.get('vix', 0)}`)",
        f"💼 *Budget (₹{cap/100000:.1f}L):* `{reg.get('swing_budget_pct', 30)}%` 1–2M Swing | `{reg.get('core_budget_pct', 70)}%` 8–12M Core (`{reg.get('gtt_cash_reserve_pct', 40)}%` GTT Reserve)",
        f"🔥 *Portfolio Heat:* `{aud.get('open_heat_pct', 0)}%` / `{MAX_PORTFOLIO_HEAT_PCT}%` Cap",
        "",
    ]

    actions = aud.get("open_actions", [])
    if actions:
        lines.append(f"🛡️ *OPEN POSITIONS & LEDGER ACTIONS ({len(actions)}):*")
        for a in actions[:5]:
            lines.append(
                f"• `{a['symbol']}` [{a['status']}]: *{a['action']}* | CMP ₹{a['cmp']} | SL ₹{a['sl']} (`{a['pnlR']:+}R`)"
            )
        lines.append("")

    exec_swings = [s for s in swing if s.get("guard") in ("EXECUTE_GTT", "EXECUTE_ACTIVE", "READY_1.0R", "PILOT_0.5R")]
    lines.append(f"⚡ *1–2M SWING QUEUE (Top Ready — Two-Tier Anti-Hunt SL):*")
    if not exec_swings:
        lines.append("• _No clean Phase 3 swing tickets below heat/extension caps today._")
    else:
        for s in exec_swings[:5]:
            sw = s["swing"]
            tag = f" [{s['signalTag']}]" if s.get("signalTag") else f" [{s['confluence'].replace('_', ' ')}]"
            lines.append(
                f"• `{s['ticker']}` ({s['sectorTier']}->{s['stockTier']} {s['stockScore']}){tag}\n"
                f"  Buy: `₹{sw['entryRef']}` ({sw['shares']} sh = `50%+50%`) | Hard GTT SL: `₹{sw['hardGttSl']}` (`-{sw['riskPct']}%`) | EOD Close SL: `₹{sw['softEodSl']}` | T1/T2: `₹{sw['t1_2r']}`/`₹{sw['t2_35r']}`"
            )
    lines.append("")

    lines.append("🏛 *8–12M CORE ACCUMULATION (40% Pilot / 35% Confirm / 25% GTT Dip):*")
    for c in core[:4]:
        cr = c["core"]
        lines.append(
            f"• `{c['ticker']}` ({c['sectorTier']}/{c['stockTier']}): *{c['coreAction']}* @ `₹{cr['accumBand']}` ({cr['shares']} sh) | 150DMA SL `₹{cr['structSl']}` | 12M Base `₹{cr['baseTarget']:.0f}` (`+{cr['upsidePct']}%`)"
        )
    lines.append("")
    lines.append("⛔ _Anti-Stop-Hunt: Avoid 9:15–9:45 AM market orders; honour Soft SL on 3:15 PM close._")
    lines.append("🌐 [Open Interactive F5 Execution Desk](https://jigarpatel031187.github.io/stock-screener/)")
    return "\n".join(lines)


def save_trade_plan_cache(payload: dict, cache_path: str = TRADE_PLAN_CACHE_PATH) -> str:
    os.makedirs(os.path.dirname(cache_path), exist_ok=True)
    tmp_path = cache_path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    os.replace(tmp_path, cache_path)
    return cache_path


def load_trade_plan_cache(cache_path: str = TRADE_PLAN_CACHE_PATH) -> Optional[dict]:
    if os.path.exists(cache_path):
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AntiGravity Trade Plan Agent")
    parser.add_argument("--capital", type=float, default=DEFAULT_CAPITAL_INR, help="Total capital in INR")
    parser.add_argument("--risk", type=float, default=DEFAULT_SWING_RISK_PCT, help="1R Swing risk pct (e.g. 0.75)")
    parser.add_argument("--ticker", type=str, default=None, help="Inspect single NSE stock ticket")
    args = parser.parse_args()

    from sector_rotation_engine import load_sector_rotation_cache
    from trade_tracker import load_trade_ledger

    sr_cache = load_sector_rotation_cache() or {}
    ledger = load_trade_ledger()
    tp = build_trade_plan_payload(sr_cache, trades=ledger, capital=args.capital, risk_pct=args.risk)
    save_trade_plan_cache(tp)

    if args.ticker:
        sym = args.ticker.strip().upper().replace(".NS", "")
        tkt = tp["stock_lookup"].get(sym)
        print(json.dumps(tkt, indent=2) if tkt else f"Ticker {sym} not found in universe.")
    else:
        print(build_daily_trade_plan_telegram(tp))
