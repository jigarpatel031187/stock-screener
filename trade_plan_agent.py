"""
Trade Plan Agent Engine for AntiGravity Smart Money Dual Track Radar.

Combines:
  1. Market Regime & Cap-Tier Budget Allocator (Swing % / Core % / GTT Reserve %)
  2. Exclusive Confirm 1-2M Gate (Stock P3 + Sector P2/P3, <=2/sector, max 10 active swings)
     plus Track A/B in P1 sectors flagged explicitly as 0.5R PILOT WATCH
  3. Confirm 8-12M Gate with Live Yahoo Finance Fundamentals (ROE >= 12%, Sector D/E, Valuation)
     cached with 7-day TTL (data/fundamentals_cache.json) across Stage-2 candidates (~40-65 stocks)
  4. Common in Both (Confirm 1-2M ∩ Confirm 8-12M) & Watchlist (24 Curated + Top Tight P1/P2 Coils)
  5. Asymmetric Sizing (1.25R Common+Dual+Track in Risk-On / 1.0R Confirm / 0.5R Watch)
     & Profit Pyramiding Schedule (40% Pilot / 45% +1R EMA-Retest / 15% Sector RS>100)
  6. Exit & Free-Roll Architecture: 40% T1 (+2R -> 0% Heat) / 35% T2 (+3.5R) / 25% Uncapped 20-EMA Runner
     + 18-Session Stale Time-Stop Rotation + Anti-Stop-Hunt Two-Tier SL
  7. Smart Telegram Cadence: Mon-Thu Change Diff + Rationale; Every Friday Evening Full Weekly Review
"""

import argparse
import datetime
import json
import logging
import math
import os
import re
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
TRADE_PLAN_CACHE_PATH = os.path.join(DATA_DIR, "trade_plan.json")
PREV_TRADE_PLAN_PATH = os.path.join(DATA_DIR, "trade_plan_prev.json")
FUNDAMENTALS_CACHE_PATH = os.path.join(DATA_DIR, "fundamentals_cache.json")

DEFAULT_CAPITAL_INR = 1_000_000.0
DEFAULT_SWING_RISK_PCT = 0.75
MAX_PORTFOLIO_HEAT_PCT = 4.5
MAX_SECTOR_SLOTS = 2
MAX_ACTIVE_SWINGS = 10
TIME_STOP_SESSIONS = 18
MIN_CORE_ROE = 12.0
MAX_CORE_PE = 90.0
FUND_TTL_DAYS = 7

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


def _sector_de_cap(sector_name: str, yf_sector_ind: str = "") -> Tuple[Optional[float], str]:
    """Maps sector/industry to prudent Debt-to-Equity limit (BFSI exempt)."""
    s = f"{sector_name} {yf_sector_ind}".lower()
    if any(k in s for k in ["bank", "nbfc", "financial", "insurance", "housing finance", "broking", "lending"]):
        return None, "BFSI"
    if re.search(r"\b(it|software|tech|technology|digital|internet)\b", s):
        return 0.35, "IT & Tech"
    if any(k in s for k in ["fmcg", "consumer", "food", "beverage", "retail", "media", "durable"]):
        return 0.60, "Consumer"
    if any(k in s for k in ["pharma", "health", "hospital", "biotech", "life science"]):
        return 0.60, "Healthcare"
    if any(k in s for k in ["metal", "mining", "cement", "steel", "mineral"]):
        return 1.20, "Metals & Materials"
    if any(k in s for k in ["real estate", "realty", "power", "telecom", "utility", "infra", "energy", "oil", "gas"]):
        return 1.80, "Capital Intensive"
    return 0.90, "Industrial / General"


def _round_cluster_guard(level: float) -> float:
    """Shifts stops slightly below round numbers (50 / 100 / 500 / 1000) to dodge liquidity sweeps."""
    if level <= 5.0:
        return round(level, 2)
    step = 100.0 if level >= 1500 else (50.0 if level >= 400 else 10.0)
    nearest = round(level / step) * step
    if abs(level - nearest) <= max(1.0, level * 0.0025):
        level = nearest - max(1.5, round(level * 0.0035, 1))
    return round(level, 1)


def load_fundamentals_cache(cache_path: str = FUNDAMENTALS_CACHE_PATH) -> dict:
    if os.path.exists(cache_path):
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_fundamentals_cache(cache: dict, cache_path: str = FUNDAMENTALS_CACHE_PATH) -> str:
    os.makedirs(os.path.dirname(cache_path), exist_ok=True)
    tmp_path = cache_path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2)
    os.replace(tmp_path, cache_path)
    return cache_path


def _evaluate_fundamental_quality(
    ticker: str,
    sector: str,
    info: dict,
) -> dict:
    """Evaluates ROE >= 12%, Sector D/E cap, and P/E / P/B valuation sanity from yfinance .info."""
    mcap = info.get("marketCap")
    mcap_cr = round(mcap / 10_000_000.0, 1) if mcap else None

    tr_pe = info.get("trailingPE")
    fw_pe = info.get("forwardPE")
    pe_raw = fw_pe if (fw_pe and fw_pe > 0) else tr_pe
    pe_val = round(float(pe_raw), 2) if (pe_raw and pe_raw > 0) else None
    pb_raw = info.get("priceToBook")
    pb_val = round(float(pb_raw), 2) if (pb_raw and pb_raw > 0) else None

    de_raw = info.get("debtToEquity")
    de_ratio = round(float(de_raw) / 100.0, 2) if de_raw is not None else None

    roe_raw = info.get("returnOnEquity")
    book_val = info.get("bookValue")
    shares = info.get("sharesOutstanding")
    net_inc = info.get("netIncomeToCommon")
    equity = (float(book_val) * float(shares)) if (book_val and shares) else None
    if roe_raw is not None:
        roe_pct = round(float(roe_raw) * 100.0, 1)
    elif net_inc and equity and equity > 0:
        roe_pct = round((float(net_inc) / equity) * 100.0, 1)
    else:
        roe_pct = None

    max_de, sec_cat = _sector_de_cap(sector, f"{info.get('sector', '')} {info.get('industry', '')}")
    is_bfsi = (max_de is None)

    c_roe = (roe_pct is not None and roe_pct >= MIN_CORE_ROE)
    c_de = True if is_bfsi else (de_ratio is None or de_ratio <= max_de)
    if pe_val is not None:
        c_val = (0 < pe_val <= MAX_CORE_PE)
    elif is_bfsi and pb_val is not None:
        c_val = (0 < pb_val <= 6.0)
    else:
        c_val = False

    fails = []
    if not c_roe:
        fails.append(f"ROE {roe_pct if roe_pct is not None else 'N/A'}% < {MIN_CORE_ROE}%")
    if not c_de:
        fails.append(f"D/E {de_ratio} > {max_de} ({sec_cat})")
    if not c_val:
        fails.append(f"Val P/E {pe_val} P/B {pb_val} out of bounds")

    qualifies = bool(c_roe and c_de and c_val)
    summary = (
        f"ROE {roe_pct}% | D/E {de_ratio if de_ratio is not None else 'BFSI'} | P/E {pe_val or pb_val or '--'}"
        if qualifies
        else "; ".join(fails)
    )
    return {
        "ticker": ticker,
        "roePct": roe_pct,
        "deRatio": de_ratio,
        "peRatio": pe_val,
        "pbRatio": pb_val,
        "mcapCr": mcap_cr,
        "qualifiesCore": qualifies,
        "fundReason": summary,
    }


def fetch_stage2_fundamentals(
    candidates: List[dict],
    cache_path: str = FUNDAMENTALS_CACHE_PATH,
    ttl_days: int = FUND_TTL_DAYS,
    max_live_fetches: int = 65,
    allow_network: bool = True,
) -> Dict[str, dict]:
    """
    Fetches & caches live Yahoo Finance fundamentals ONLY for non-extended Stage-2 P1/P2/P3
    and Curated candidates (<= 65 tickers per run) with a 7-day cache TTL.
    """
    cache = load_fundamentals_cache(cache_path)
    today = (datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)).date()
    today_str = today.strftime("%Y-%m-%d")

    to_fetch = []
    for st in candidates[:max_live_fetches]:
        tk = st.get("ticker", "")
        if not tk or tk == "NSE":
            continue
        entry = cache.get(tk)
        stale = True
        if entry and entry.get("fetched_at"):
            try:
                f_dt = datetime.datetime.strptime(entry["fetched_at"], "%Y-%m-%d").date()
                stale = (today - f_dt).days >= ttl_days
            except Exception:
                stale = True
        if stale:
            to_fetch.append((tk, st.get("sector", "Equities")))

    if allow_network and to_fetch:
        try:
            import yfinance as yf
        except Exception:
            yf = None

        if yf is not None:
            changed = False
            for tk, sec in to_fetch:
                try:
                    info = yf.Ticker(f"{tk}.NS").info or {}
                    if info:
                        ev = _evaluate_fundamental_quality(tk, sec, info)
                        ev["fetched_at"] = today_str
                        cache[tk] = ev
                        changed = True
                except Exception as e:
                    logger.debug(f"Yahoo fundamental fetch skipped for {tk}: {e}")
            if changed:
                save_fundamentals_cache(cache, cache_path)

    return cache


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
    shelf_low_5d: Optional[float] = None,
) -> dict:
    """
    Two-Tier Anti-Stop-Hunt Risk Geometry (Unified with Track A/B Bot):
      - softEodSl: Closing-basis 1R anchor from min(5D Shelf Low - 0.75*ATR, Entry - 1.5*ATR),
                   nudged off round clusters BEFORE clamping strictly within 4.0% - 8.0%
      - hardGttSl: Wide disaster GTT circuit breaker 0.5*ATR deeper than softEodSl
      - beTrailSl: Post-T1 Free-Roll trailing SL guaranteed >= entry_ref
      - coreStructSl: 150-DMA - 1.0*ATR for 8-12M Core compounding
    """
    cmp_val = float(price or 1.0)
    atr = float(atr14) if (atr14 and atr14 > 0) else round(cmp_val * 0.025, 1)
    ref = float(entry_ref) if (entry_ref and entry_ref > 0) else cmp_val
    d20 = float(dma20) if (dma20 and dma20 > 0) else cmp_val * 0.97
    e20 = float(ema20) if (ema20 and ema20 > 0) else d20
    d150 = float(dma150) if (dma150 and dma150 > 0) else cmp_val * 0.88
    sw_low = float(swing_low) if (swing_low and swing_low > 0) else cmp_val * 0.93
    shelf5d = float(shelf_low_5d) if (shelf_low_5d and shelf_low_5d > 0) else max(sw_low, d20 - 0.5 * atr)

    # Precision-safe rounding (2 decimals below Rs.100 so penny/low-price stocks keep exact 4%-8% band)
    nd = 2 if ref < 100.0 else 1
    scale = 10 ** nd
    min_sl_strict = math.ceil((ref * 0.92) * scale) / scale
    max_sl_strict = math.floor((ref * 0.96) * scale) / scale
    if max_sl_strict <= min_sl_strict:
        max_sl_strict = min_sl_strict

    # Apply round-cluster guard BEFORE 4%-8% clamp so Risk% NEVER overflows 8.0%
    raw_struct = min(shelf5d - (0.75 * atr), ref - (1.5 * atr))
    guarded_eod = _round_cluster_guard(raw_struct)
    soft_eod_sl = round(max(min_sl_strict, min(max_sl_strict, guarded_eod)), nd)
    if soft_eod_sl >= ref:
        soft_eod_sl = round(ref * 0.955, nd)

    unit_risk = max(0.05 if ref < 50.0 else 0.1, round(ref - soft_eod_sl, nd))
    risk_pct = round((unit_risk / ref) * 100.0, 2) if ref > 0 else 5.0

    # Disaster Intraday GTT Floor sits ~0.5*ATR deeper than Soft EOD Stop (capped at max 10%)
    hard_gtt_raw = _round_cluster_guard(soft_eod_sl - (0.5 * atr))
    hard_gtt_sl = round(max(ref * 0.90, min(soft_eod_sl * 0.992, hard_gtt_raw)), nd)

    t1_2r = round(ref + (2.0 * unit_risk), nd)
    t2_35r = round(ref + (3.5 * unit_risk), nd)
    be_trail_sl = round(max(ref * 1.002, _round_cluster_guard(max(e20 - (0.4 * atr), ref + 0.1 * atr))), nd)

    core_struct_sl = round(_round_cluster_guard(min(ref * 0.90, d150 - (1.0 * atr))), nd)
    return {
        "entryRef": round(ref, 2),
        "entryBand": f"{round(min(ref, d20), nd if ref < 100 else 0):.{nd if ref < 100 else 0}f}-{round(ref + 0.5 * atr, nd if ref < 100 else 0):.{nd if ref < 100 else 0}f}",
        "hardGttSl": hard_gtt_sl,
        "softEodSl": soft_eod_sl,
        "beTrailSl": be_trail_sl,
        "riskPerShare": unit_risk,
        "riskPct": risk_pct,
        "t1_2r": t1_2r,
        "t2_35r": t2_35r,
        "coreStructSl": core_struct_sl,
    }


def evaluate_open_trades(
    trades: list,
    stock_lookup: dict,
    sector_map: dict,
    capital: float = DEFAULT_CAPITAL_INR,
    risk_pct: float = DEFAULT_SWING_RISK_PCT,
) -> dict:
    """
    Audits live ledger positions:
      - T1_HIT / RUNNER_ACTIVE with SL >= Entry count as Free-Roll (0% heat & frees sector/swing slot!)
      - ACTIVE held >= 18 sessions & < +0.5R while Home Sector rose -> TIME_STOP_ROTATE
      - RUNNER_ACTIVE -> trails remaining 25% uncapped on Daily/Weekly Close < 20-EMA / 50-DMA
      - Recent <= 7D stops -> Spring & Reclaim watch
    """
    open_actions = []
    open_symbols = set()
    active_non_freeroll_count = 0
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
        days_held = int(tr.get("days_held") or 0)
        sec_key = st_live.get("sector") or sector
        sec_node = sector_map.get(sec_key) or {}
        sec_moved_up = (float(sec_node.get("w1", 0.0)) > 0.0) or (float(sec_node.get("m1", 0.0)) > 0.0)

        if status in ("ACTIVE", "T1_HIT", "RUNNER_ACTIVE", "PENDING_TRIGGER"):
            open_symbols.add(sym)
            is_free_roll = (
                status in ("T1_HIT", "RUNNER_ACTIVE")
                and (curr_sl >= entry_p * 0.999 or bool(tr.get("free_roll")))
            )
            time_stop = False

            if not is_free_roll:
                sector_counts[sec_key] = sector_counts.get(sec_key, 0) + 1
                if status != "PENDING_TRIGGER":
                    active_non_freeroll_count += 1

            if status == "RUNNER_ACTIVE":
                ema20_val = float(tr.get("latest_ema20") or st_live.get("ema20") or cmp_val)
                dma50_val = float(tr.get("latest_dma50") or st_live.get("dma50") or 0.0)
                trail_ref = max(curr_sl, round(ema20_val, 1))
                action = "TRAIL_RUNNER_25%"
                note = f"25% Uncapped Runner (0% Heat) — hold until Close < 20-EMA ₹{ema20_val:.0f}" + (
                    f" or 50-DMA ₹{dma50_val:.0f}" if dma50_val > 0 else ""
                )
            elif status == "T1_HIT":
                if not is_free_roll:
                    total_open_risk_inr += risk_inr_per_slot * 0.25
                action = "FREE_ROLL_HOLD" if is_free_roll else "TRAIL_TO_T2"
                note = (
                    f"Free-Roll (0% Heat, Slot Freed): 40% booked @ T1; hold 35% to T2 ₹{t2:.0f}, keep 25% uncapped runner"
                    if is_free_roll
                    else f"40% booked @ T1; move SL >= ₹{entry_p:.0f} to lock Free-Roll & target T2 ₹{t2:.0f}"
                )
            elif status == "ACTIVE":
                total_open_risk_inr += risk_inr_per_slot
                if days_held >= TIME_STOP_SESSIONS and r_mult < 0.5 and sec_moved_up:
                    time_stop = True
                    action = "TIME_STOP_ROTATE"
                    note = f"Stale {days_held}d (< +0.5R while {sec_key} rose) — exit at market & rotate slot to Confirm 1-2M"
                elif t1 > 0 and cmp_val >= t1 * 0.985:
                    action = "BOOK_T1_40%"
                    note = f"Near T1 ₹{t1:.0f} — book 40% & move SL >= ₹{entry_p:.0f} (frees slot & 0% heat)"
                elif r_mult >= 1.0:
                    ema20_v = float(st_live.get("ema20") or cmp_val)
                    atr_v = float(st_live.get("atr14") or cmp_val * 0.02)
                    trail_lvl = round(max(curr_sl, ema20_v - 0.5 * atr_v), 1)
                    action = "PYRAMID_+45%_EMA"
                    note = f"+{r_mult:.2f}R — eligible for +45% add-on holding 10/20-EMA; raise SL toward ₹{trail_lvl}"
                else:
                    action = "HOLD_MONITOR_EOD"
                    note = f"Day {days_held}/{TIME_STOP_SESSIONS} | Obey 3:15 PM Closing SL < ₹{curr_sl:.1f}"
            else:
                total_open_risk_inr += risk_inr_per_slot * 0.5
                action = "ARM_BUY_GTT"
                note = f"40% Pilot Buy-Stop GTT @ ₹{entry_p:.1f} | Wide SL ₹{curr_sl:.1f} | After 9:45 AM"

            open_actions.append({
                "symbol": sym,
                "name": tr.get("name", sym),
                "track": tr.get("track", "Track B"),
                "sector": sec_key,
                "status": status,
                "action": action,
                "freeRoll": is_free_roll,
                "timeStop": time_stop,
                "daysHeld": days_held,
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
                    "sector": sec_key,
                    "status": "SPRING_RECLAIM",
                    "action": "REENTRY_WATCH",
                    "freeRoll": False,
                    "timeStop": False,
                    "daysHeld": days_held,
                    "cmp": round(cmp_val, 2),
                    "entry": round(cmp_val, 2),
                    "sl": round(init_sl * 0.985, 1),
                    "t1": round(t1, 1),
                    "t2": round(t2, 1),
                    "pnlPct": 0.0,
                    "pnlR": 0.0,
                    "sectorTier": st_live.get("sectorTier", "NEUTRAL"),
                    "stockTier": st_live.get("preExplodeTier", "NEUTRAL"),
                    "note": f"Spring & Reclaim above SL ₹{init_sl:.0f} + 20DMA — 1-shot re-entry watch",
                })

    open_heat_pct = round((total_open_risk_inr / max(1.0, capital)) * 100.0, 2)
    return {
        "open_actions": open_actions,
        "open_symbols": open_symbols,
        "active_swing_count": active_non_freeroll_count,
        "sector_counts": sector_counts,
        "open_heat_pct": open_heat_pct,
        "open_heat_inr": round(total_open_risk_inr, 0),
    }


def _enrich_candidate_ticket(
    st: dict,
    curated: Optional[dict],
    signal_item: Optional[dict],
    fund_info: Optional[dict],
    capital: float,
    risk_pct: float,
    swing_slot_inr: float,
    core_slot_inr: float,
) -> dict:
    """Computes complete live ticket with 40/45/15 Swing pyramiding and Yahoo-checked Core sizing."""
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
        shelf_low_5d=st.get("shelfLow5d"),
    )

    max_risk_inr = capital * (risk_pct / 100.0)
    risk_per_share = max(1.0, stops["riskPerShare"])
    qty_by_risk = int(max_risk_inr // risk_per_share)
    qty_by_cap = int(swing_slot_inr // max(1.0, stops["entryRef"]))
    swing_shares = max(0, min(qty_by_risk, qty_by_cap))
    swing_alloc_inr = round(swing_shares * stops["entryRef"], 0)

    # User-defined 40 / 45 / 15 Pyramiding Split
    sw_t1_sh = int(round(swing_shares * 0.40))
    sw_t2_sh = int(round(swing_shares * 0.45))
    sw_t3_sh = max(0, swing_shares - sw_t1_sh - sw_t2_sh)

    # Fundamental quality (Yahoo live .info cache or Curated fallback)
    f_qualifies = bool((fund_info or {}).get("qualifiesCore", False))
    roe_val = (fund_info or {}).get("roePct")
    if roe_val is None and curated:
        roe_val = curated.get("roe")
    de_val = (fund_info or {}).get("deRatio")
    pe_val = (fund_info or {}).get("peRatio")
    if pe_val is None and curated:
        pe_val = curated.get("fwdPe")
    fund_reason = (fund_info or {}).get("fundReason") or ("Curated Core Baseline" if (curated and curated.get("isCore")) else "Pending Fund Check")

    # Core valuation (auto-refresh stale curated FV if price deviated >25%, e.g. splits/reratings)
    if curated and curated.get("fairValue") and abs(float(curated["fairValue"]) - price) / price <= 0.45:
        fv = float(curated["fairValue"])
        core_band = f"{round(fv * 0.85):.0f}-{round(fv * 0.95):.0f}"
        core_base = round(float(curated.get("base") or fv), 0)
        core_bull = round(float(curated.get("bull") or fv * 1.15), 0)
        core_upside = round(((core_base - price) / price) * 100.0, 1)
        val_model = curated.get("valMethod", "DCF / Fwd PE")
        kpi_stop = curated.get("kpiStop", f"Weekly Close < ₹{stops['coreStructSl']:.0f}")
    else:
        d150 = float(st.get("dma150") or price * 0.9)
        core_band = f"{round(min(price, d150)):.0f}-{round(price * 0.99):.0f}"
        core_base = round(price * 1.24, 0)
        core_bull = round(price * 1.42, 0)
        core_upside = 24.0
        val_model = f"Yahoo Q-Check (P/E {pe_val or '--'} | ROE {roe_val or '--'}%)" if f_qualifies else "Stage-2 + Sector Alpha"
        kpi_stop = f"Weekly Close < ₹{stops['coreStructSl']:.0f} (150DMA−1×ATR)"

    core_shares = max(0, int(core_slot_inr // price))
    cr_t1_sh = int(round(core_shares * 0.40))
    cr_t2_sh = int(round(core_shares * 0.35))
    cr_t3_sh = max(0, core_shares - cr_t1_sh - cr_t2_sh)

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
        "sectorRsRatio": st.get("sectorRsRatio") or 100.0,
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
        "ema20": st.get("ema20", st.get("dma20", 0.0)),
        "dma150": st.get("dma150", 0.0),
        "swingLow": st.get("swingLow", 0.0),
        "qualifiesCore": f_qualifies,
        "roePct": roe_val,
        "deRatio": de_val,
        "peRatio": pe_val,
        "fundReason": fund_reason,
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
            "tranche1Shares": sw_t1_sh,
            "tranche2Shares": sw_t2_sh,
            "tranche3Shares": sw_t3_sh,
            "allocInr": swing_alloc_inr,
            "maxRiskInr": round(swing_shares * stops["riskPerShare"], 0),
        },
        "core": {
            "accumBand": core_band,
            "structSl": stops["coreStructSl"],
            "kpiStop": kpi_stop,
            "baseTarget": core_base,
            "bullTarget": core_bull,
            "upsidePct": core_upside,
            "valModel": val_model,
            "roe": roe_val if roe_val is not None else "--",
            "pe": pe_val if pe_val is not None else "--",
            "de": de_val if de_val is not None else "--",
            "shares": core_shares,
            "tranche1Shares": cr_t1_sh,
            "tranche2Shares": cr_t2_sh,
            "tranche3Shares": cr_t3_sh,
            "allocInr": round(core_shares * price, 0),
        },
        "isCurated": bool(curated),
        "isCore": bool((curated or {}).get("isCore")),
        "isSwing": bool((curated or {}).get("isSwing")),
        "isCommonDual": False,
        "watchRemark": "",
    }


def _apply_size_multiplier(ticket: dict, size_mult: float) -> dict:
    """Scales shares/risk/40-45-15 pyramiding tranches proportionally to size_mult (1.25 / 1.0 / 0.5)."""
    sw = dict(ticket["swing"])
    if size_mult != 1.0:
        scaled = max(1, int(round(sw["shares"] * size_mult))) if sw["shares"] > 0 else 0
        sw["shares"] = scaled
        sw["tranche1Shares"] = int(round(scaled * 0.40))
        sw["tranche2Shares"] = int(round(scaled * 0.45))
        sw["tranche3Shares"] = max(0, scaled - sw["tranche1Shares"] - sw["tranche2Shares"])
        sw["allocInr"] = round(scaled * sw["entryRef"], 0)
        sw["maxRiskInr"] = round(scaled * sw["riskPerShare"], 0)
    return {**ticket, "swing": sw, "sizeMult": size_mult}


def compute_trade_plan_diff(curr_tp: dict, prev_tp: Optional[dict]) -> dict:
    """
    Computes daily delta + rationale across ALL 5 buckets:
      confirm_swing (Confirm 1-2M), confirm_core (Confirm 8-12M),
      common_dual (Common in Both), open_positions (Open Ledger & Runners), watchlist.
    """
    if not prev_tp or not isinstance(prev_tp, dict):
        return {
            "has_prev": False,
            "total_changes": 0,
            "confirm_swing": {"added": [], "removed": []},
            "confirm_core": {"added": [], "removed": []},
            "common_dual": {"added": [], "removed": []},
            "open_positions": {"added": [], "removed": [], "status_changed": []},
            "watchlist": {"added": [], "removed": []},
        }

    curr_lookup = curr_tp.get("stock_lookup", {})

    def _get_list(tp_obj, new_key, old_key=None):
        lst = tp_obj.get(new_key)
        if lst is None and old_key:
            lst = tp_obj.get(old_key, [])
        return lst or []

    def _diff_queue(new_key, old_key=None):
        c_rows = {x.get("ticker"): x for x in _get_list(curr_tp, new_key, old_key) if x.get("ticker")}
        p_rows = {x.get("ticker"): x for x in _get_list(prev_tp, new_key, old_key) if x.get("ticker")}
        added = []
        for tk in sorted(set(c_rows.keys()) - set(p_rows.keys())):
            r = c_rows[tk]
            added.append({
                "ticker": tk,
                "reason": (
                    f"{r.get('sector')} {r.get('sectorTier')} | Stock {r.get('stockTier')} ({r.get('stockScore')})"
                    + (f" [{r.get('signalTag')}]" if r.get("signalTag") else "")
                    + (f" | ROE {r.get('roePct')}%" if r.get("roePct") is not None else "")
                ),
            })
        removed = []
        for tk in sorted(set(p_rows.keys()) - set(c_rows.keys())):
            now_st = curr_lookup.get(tk) or p_rows[tk]
            tier = now_st.get("stockTier", "N/A")
            sec_tier = now_st.get("sectorTier", "N/A")
            if tier == "EXTENDED":
                why = "Turned EXTENDED (>20% 1M or >2.5xATR — blocked by anti-chase)"
            elif new_key == "confirm_swing" and sec_tier not in ("PHASE_3", "PHASE_2") and not now_st.get("signalTag"):
                why = f"Sector {now_st.get('sector', '')} cooled to {sec_tier}"
            elif new_key == "confirm_core" and not now_st.get("qualifiesCore", True):
                why = f"Failed fundamental gate ({now_st.get('fundReason', 'ROE/Val')})"
            else:
                why = f"Rotated out (Stock {tier} {now_st.get('stockScore', 0)} / Sector {sec_tier})"
            removed.append({"ticker": tk, "reason": why})
        return {"added": added, "removed": removed}

    d_swing = _diff_queue("confirm_swing", "swing_queue")
    d_core = _diff_queue("confirm_core", "core_queue")
    d_common = _diff_queue("common_dual")
    d_watch = _diff_queue("watchlist")

    c_open = {x.get("symbol"): x for x in ((curr_tp.get("portfolio_audit") or {}).get("open_actions") or []) if x.get("symbol")}
    p_open = {x.get("symbol"): x for x in ((prev_tp.get("portfolio_audit") or {}).get("open_actions") or []) if x.get("symbol")}
    o_added = [{"ticker": s, "reason": f"{c_open[s].get('status')} -> {c_open[s].get('action')}"} for s in sorted(set(c_open) - set(p_open))]
    o_removed = [{"ticker": s, "reason": f"Closed / Exited ledger watch (was {p_open[s].get('status')})"} for s in sorted(set(p_open) - set(c_open))]
    o_changed = []
    for s in sorted(set(c_open) & set(p_open)):
        cs, ps = c_open[s], p_open[s]
        if cs.get("status") != ps.get("status") or cs.get("action") != ps.get("action"):
            o_changed.append({
                "ticker": s,
                "reason": f"{ps.get('status')}/{ps.get('action')} -> {cs.get('status')}/{cs.get('action')} ({cs.get('note', '')[:70]})",
            })

    total_changes = sum(
        len(d["added"]) + len(d["removed"])
        for d in (d_swing, d_core, d_common, d_watch)
    ) + len(o_added) + len(o_removed) + len(o_changed)

    return {
        "has_prev": True,
        "total_changes": total_changes,
        "confirm_swing": d_swing,
        "confirm_core": d_core,
        "common_dual": d_common,
        "open_positions": {"added": o_added, "removed": o_removed, "status_changed": o_changed},
        "watchlist": d_watch,
    }


def build_trade_plan_payload(
    sector_rotation: Optional[dict],
    trades: Optional[list] = None,
    active_breakouts: Optional[list] = None,
    pre_breakout_squeezes: Optional[list] = None,
    capital: float = DEFAULT_CAPITAL_INR,
    risk_pct: float = DEFAULT_SWING_RISK_PCT,
    fetch_live_fundamentals: bool = True,
    prev_trade_plan: Optional[dict] = None,
) -> dict:
    """
    Produces complete Trade Plan payload consumed by Tab 4 [F5], Mon-Thu Delta / Friday Brief Telegram, and CLI.
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

    merged_map: Dict[str, dict] = {}
    for st in all_scored:
        tk = st.get("ticker")
        if not tk:
            continue
        sec = st.get("sector")
        sec_node = sector_map.get(sec)
        sec_rs = 100.0
        if sec_node and sec_node.get("dailyTail"):
            sec_rs = round(100.0 + float(sec_node["dailyTail"][-1].get("x", 0.0)), 2)
        enriched_st = dict(st)
        enriched_st["sectorRsRatio"] = sec_rs
        if sec_node and not enriched_st.get("sectorTier"):
            enriched_st["sectorTier"] = sec_node.get("preExplodeTier", "NEUTRAL")
            enriched_st["sectorScore"] = sec_node.get("preExplodeScore", 0)
        if tk in sig_map and not enriched_st.get("signalTag"):
            enriched_st["signalTag"] = sig_map[tk].get("signalTag")
        merged_map[tk] = enriched_st

    for tk, cur in curated_map.items():
        if tk not in merged_map and cur.get("ticker") != "NSE":
            sec_node = sector_map.get(cur.get("sector"))
            c_copy = dict(cur)
            if sec_node and sec_node.get("dailyTail"):
                c_copy["sectorRsRatio"] = round(100.0 + float(sec_node["dailyTail"][-1].get("x", 0.0)), 2)
            merged_map[tk] = c_copy

    # Fetch live Yahoo fundamentals ONLY for Stage-2 non-extended P1/P2/P3 & Curated candidates (<= 65 stocks, 7D TTL)
    fund_candidates = [
        st for st in merged_map.values()
        if st.get("preExplodeTier") != "EXTENDED"
        and (
            st.get("ticker") in curated_map
            or st.get("signalTag") in ("TRACK A", "TRACK B")
            or (st.get("stage2Pass") and st.get("preExplodeTier") in ("PHASE_3", "PHASE_2", "PHASE_1"))
        )
    ]
    fund_candidates.sort(
        key=lambda x: (
            1 if x.get("ticker") in curated_map else 0,
            1 if x.get("signalTag") else 0,
            x.get("preExplodeScore", 0),
        ),
        reverse=True,
    )
    fund_cache = fetch_stage2_fundamentals(
        fund_candidates,
        allow_network=fetch_live_fundamentals,
    )

    regime = compute_market_regime(tape, universe_nodes)
    audit = evaluate_open_trades(trades or [], merged_map, sector_map, capital=capital, risk_pct=risk_pct)

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
            fund_info=fund_cache.get(tk),
            capital=capital,
            risk_pct=risk_pct,
            swing_slot_inr=swing_slot_inr,
            core_slot_inr=core_slot_inr,
        )
        if tkt:
            tickets.append(tkt)

    # 1. Determine Confirm 8-12M FIRST (Curated Core OR Stage-2 P1/P2/P3 with Yahoo ROE >= 12% & clean D/E & Valuation)
    core_candidates = [
        t for t in tickets
        if t["sectorTier"] != "EXTENDED"
        and t["stockTier"] != "EXTENDED"
        and (t.get("roePct") is None or float(t["roePct"]) >= MIN_CORE_ROE)
        and (
            (t["isCurated"] and t["isCore"])
            or (
                t["stage2Pass"]
                and t["qualifiesCore"]
                and t["sectorTier"] in ("PHASE_2", "PHASE_1", "PHASE_3")
                and t["stockTier"] in ("PHASE_2", "PHASE_1", "PHASE_3")
            )
        )
    ]
    core_candidates.sort(
        key=lambda t: (
            1 if (t["isCurated"] and t["isCore"]) else 0,
            1 if t["qualifiesCore"] else 0,
            1 if t["sectorTier"] in ("PHASE_2", "PHASE_3") else 0,
            t["core"]["upsidePct"] * 0.4 + t["stockScore"] + t["sectorScore"] * 0.5,
        ),
        reverse=True,
    )
    confirm_core = []
    core_ticker_set = set()
    for t in core_candidates[:20]:
        st_phase = t["stockTier"]
        sec_phase = t["sectorTier"]
        if sec_phase == "PHASE_3" or st_phase == "PHASE_3":
            action = "CONFIRM_ADD_35%"
        elif sec_phase in ("PHASE_2", "PHASE_1") or st_phase in ("PHASE_2", "PHASE_1"):
            action = "PILOT_ACCUM_40%"
        else:
            action = "GTT_DIP_25%"
        confirm_core.append({**t, "coreAction": action})
        core_ticker_set.add(t["ticker"])

    # 2. Confirm 1-2M (Exclusively Stock PHASE_3 + Sector PHASE_2/3, plus Track A/B in P1 Sector as 0.5R WATCH)
    swing_candidates = []
    for t in tickets:
        if t["stockTier"] == "EXTENDED":
            continue
        is_confirmed = (t["stockTier"] == "PHASE_3" and t["sectorTier"] in ("PHASE_3", "PHASE_2"))
        is_p1_exception = (
            not is_confirmed
            and t.get("signalTag") in ("TRACK A", "TRACK B")
            and t["sectorTier"] == "PHASE_1"
        )
        if not (is_confirmed or is_p1_exception):
            continue
        if t["ticker"] in core_ticker_set:
            t["isCommonDual"] = True
        swing_candidates.append((t, is_p1_exception))

    swing_candidates.sort(
        key=lambda pair: (
            0 if pair[1] else 1,  # Confirmed Sector P2/P3 first, P1 Track A/B Watch after
            1 if pair[0]["isCommonDual"] else 0,
            1 if pair[0].get("signalTag") else 0,
            1 if pair[0]["confluence"] == "DUAL_CONFLUENCE" else 0,
            pair[0]["stockScore"] + int(pair[0]["sectorScore"] * 0.4),
        ),
        reverse=True,
    )

    sim_heat = float(audit["open_heat_pct"])
    sim_sectors = dict(audit["sector_counts"])
    sim_active_swings = int(audit["active_swing_count"])

    confirm_swing = []
    confirm_swing_tickers = set()
    for t, is_p1_watch in swing_candidates[:18]:
        tk = t["ticker"]
        sec = t["sector"]

        if is_p1_watch:
            size_mult = 0.5
            remark = f"⚠️ 0.5R WATCH: Home Sector ({sec}) in Early Base P1 — Wait for P2 or Half-Size Pilot Only"
        elif regime["regime"] == "RISK_ON_EXPANSION" and t["isCommonDual"] and t["confluence"] == "DUAL_CONFLUENCE" and t.get("signalTag"):
            size_mult = 1.25
            remark = f"🔥 1.25R MAX EDGE: Common Dual + {t['signalTag']} in {t['sectorTier']} Sector"
        elif regime["regime"] == "DEFENSIVE_PRESERVATION":
            size_mult = 0.5
            remark = "Defensive Regime — 0.5R Half Size Only"
        else:
            size_mult = 1.0
            remark = f"Sector {t['sectorTier']} ({t['sectorScore']}) -> Stock P3 ({t['stockScore']}) | RS {t['sectorRsRatio']}"

        if tk in audit["open_symbols"]:
            guard = "ALREADY_OPEN"
        elif sim_active_swings >= MAX_ACTIVE_SWINGS:
            guard = "MAX_10_CAP"
        elif sim_sectors.get(sec, 0) >= MAX_SECTOR_SLOTS:
            guard = "SECTOR_CAP"
        elif sim_heat + (risk_pct * size_mult) > MAX_PORTFOLIO_HEAT_PCT:
            guard = "HEAT_CAP"
        elif is_p1_watch:
            guard = "0.5R_WATCH"
            sim_sectors[sec] = sim_sectors.get(sec, 0) + 1
            sim_active_swings += 1
            sim_heat += risk_pct * size_mult
        else:
            guard = "EXECUTE_GTT" if t.get("signalTag") == "TRACK B" else ("EXECUTE_ACTIVE" if t.get("signalTag") == "TRACK A" else ("READY_1.25R" if size_mult == 1.25 else "READY_1.0R"))
            sim_sectors[sec] = sim_sectors.get(sec, 0) + 1
            sim_active_swings += 1
            sim_heat += risk_pct * size_mult

        row = _apply_size_multiplier({**t, "guard": guard, "watchRemark": remark, "isP1Watch": is_p1_watch}, size_mult)
        confirm_swing.append(row)
        confirm_swing_tickers.add(tk)

    # 3. Common in Both (Confirm 1-2M ∩ Confirm 8-12M)
    core_by_tk = {c["ticker"]: c for c in confirm_core}
    common_dual = []
    for sw_row in confirm_swing:
        tk = sw_row["ticker"]
        if tk in core_by_tk:
            cr_row = core_by_tk[tk]
            common_dual.append({**sw_row, "coreAction": cr_row["coreAction"], "isCommonDual": True})

    # 4. Watchlist (All 24 Curated Focus Stocks w/ live prices/stops + Top 30 Tightest Non-Confirmed P1/P2 Coils)
    watchlist_candidates = []
    seen_watch = set()
    for t in tickets:
        tk = t["ticker"]
        if t["isCurated"]:
            seen_watch.add(tk)
            watchlist_candidates.append({**t, "watchTag": "FOCUS_LIST"})
        elif tk not in confirm_swing_tickers and t["stockTier"] in ("PHASE_2", "PHASE_1") and t["sectorTier"] != "EXTENDED":
            watchlist_candidates.append({**t, "watchTag": "COILING_RADAR"})

    # Keep NSE unlisted focus row visible in Watchlist with live placeholder tag
    nse_cur = curated_map.get("NSE")
    if nse_cur and "NSE" not in seen_watch:
        watchlist_candidates.append({
            "ticker": "NSE",
            "name": nse_cur.get("name", "NSE India Ltd"),
            "sector": "Capital Markets",
            "bucket": "Unlisted Focus",
            "price": float(nse_cur.get("price", 2307.0)),
            "chg": 0.0, "w1": 0.0, "m1": 0.0, "m3": 0.0, "y1": 0.0,
            "sectorTier": "PHASE_1", "sectorScore": 45, "sectorRsRatio": 100.0,
            "stockTier": "NEUTRAL", "stockScore": 0, "confluence": "PRE_IPO",
            "signalTag": "PRE-IPO", "bbwPct": 50.0, "atrDecay": 1.0,
            "volDryRatio": 1.0, "upDownVol": 1.0, "alphaSec1W": 0.0, "alphaSec1M": 0.0,
            "stage2Pass": False, "reasons": ["Pre-IPO Focus"], "account": "Kritika",
            "atr14": 48.0, "dma20": 2145.0, "ema20": 2145.0, "dma150": 1920.0, "swingLow": 1822.0,
            "qualifiesCore": True, "roePct": nse_cur.get("roe", 46.0), "deRatio": 0.0, "peRatio": nse_cur.get("fwdPe", 52.1),
            "fundReason": "Unlisted Pre-IPO Curated",
            "swing": {
                "entryRef": 2080.0, "entryBand": "1950-2080", "hardGttSl": 1750.0,
                "softEodSl": 1820.0, "beTrailSl": 2100.0, "riskPerShare": 330.0,
                "riskPct": 15.8, "t1_2r": 2380.0, "t2_35r": 2540.0,
                "shares": 0, "tranche1Shares": 0, "tranche2Shares": 0, "tranche3Shares": 0,
                "allocInr": 0, "maxRiskInr": 0,
            },
            "core": {
                "accumBand": "1950-2080", "structSl": 1750.0, "kpiStop": nse_cur.get("kpiStop", "Pre-IPO"),
                "baseTarget": 2540.0, "bullTarget": 2750.0, "upsidePct": 10.1,
                "valModel": nse_cur.get("valMethod", "Forward P/E"),
                "roe": nse_cur.get("roe", 46.0), "pe": nse_cur.get("fwdPe", 52.1), "de": "--",
                "shares": 0, "tranche1Shares": 0, "tranche2Shares": 0, "tranche3Shares": 0, "allocInr": 0,
            },
            "isCurated": True, "isCore": True, "isSwing": False, "isCommonDual": False,
            "watchRemark": "Pre-IPO Unlisted Equity", "watchTag": "PRE_IPO_FOCUS",
        })

    # Prioritize all 24 Curated + Top 30 tightest Phase 2/1 coils
    curated_watch = [w for w in watchlist_candidates if w.get("isCurated")]
    radar_coils = [w for w in watchlist_candidates if not w.get("isCurated")]
    radar_coils.sort(
        key=lambda x: (
            1 if x["stockTier"] == "PHASE_2" else 0,
            1 if x["sectorTier"] in ("PHASE_3", "PHASE_2") else 0,
            x["stockScore"],
            -x["bbwPct"],
        ),
        reverse=True,
    )
    watchlist = curated_watch + radar_coils[:30]

    # Single-ticker universal lookup (preserve isCommonDual & sizeMult on confirm rows)
    compact_pool = {t["ticker"]: t for t in tickets}
    for s in confirm_swing:
        compact_pool[s["ticker"]] = s

    now_ist = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
    today_prefix = now_ist.strftime("%b %d, %Y")

    # Resolve yesterday's baseline for daily delta computation
    baseline_prev = prev_trade_plan
    if baseline_prev is None:
        cached_curr = load_trade_plan_cache(TRADE_PLAN_CACHE_PATH)
        if cached_curr and not str(cached_curr.get("generated_at", "")).startswith(today_prefix):
            baseline_prev = cached_curr
            try:
                save_trade_plan_cache(cached_curr, PREV_TRADE_PLAN_PATH)
            except Exception:
                pass
        else:
            baseline_prev = load_trade_plan_cache(PREV_TRADE_PLAN_PATH)

    payload = {
        "generated_at": now_ist.strftime("%b %d, %Y (%I:%M %p IST)"),
        "capital": capital,
        "risk_pct": risk_pct,
        "regime": regime,
        "portfolio_audit": {
            "open_heat_pct": audit["open_heat_pct"],
            "open_heat_inr": audit["open_heat_inr"],
            "active_swing_count": audit["active_swing_count"],
            "max_active_swings": MAX_ACTIVE_SWINGS,
            "sector_counts": audit["sector_counts"],
            "open_actions": audit["open_actions"],
        },
        "confirm_swing": confirm_swing,
        "confirm_core": confirm_core,
        "common_dual": common_dual,
        "watchlist": watchlist,
        # Keep backward-compatible aliases
        "swing_queue": confirm_swing,
        "core_queue": confirm_core,
        "stock_lookup": compact_pool,
    }
    payload["diff_summary"] = compute_trade_plan_diff(payload, baseline_prev)
    return payload


def build_daily_trade_plan_telegram(
    trade_plan: dict,
    prev_trade_plan: Optional[dict] = None,
    force_friday_mode: Optional[bool] = None,
) -> str:
    """
    Smart Telegram Cadence:
      - Mon-Thu (5 PM): Sends ONLY daily changes + rationale across Confirm 1-2M,
        Confirm 8-12M, Common in Both, Open Positions, and Watchlist.
      - Every Friday Evening: Sends Daily Changes + Full Complete Existing Roster of
        Common in Both, Confirm 1-2M, Confirm 8-12M, and Open Ledger / 25% Runners.
    """
    now_ist = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
    is_friday = (now_ist.weekday() == 4) if force_friday_mode is None else bool(force_friday_mode)

    reg = trade_plan.get("regime", {})
    aud = trade_plan.get("portfolio_audit", {})
    swings = trade_plan.get("confirm_swing", trade_plan.get("swing_queue", []))
    cores = trade_plan.get("confirm_core", trade_plan.get("core_queue", []))
    commons = trade_plan.get("common_dual", [])
    watch = trade_plan.get("watchlist", [])
    diff = compute_trade_plan_diff(trade_plan, prev_trade_plan) if prev_trade_plan is not None else trade_plan.get("diff_summary", {})
    gen_at = trade_plan.get("generated_at", "Live")
    cap = trade_plan.get("capital", DEFAULT_CAPITAL_INR)

    header_title = (
        f"📅 *FRIDAY FULL WEEKLY TRADE PLAN SUMMARY* | _{gen_at}_"
        if is_friday
        else f"⚡ *DAILY TRADE PLAN CHANGE BRIEF (5 PM)* | _{gen_at}_"
    )
    lines = [
        header_title,
        f"⚖️ *Regime:* `{reg.get('label', 'SELECTIVE')}` (`{reg.get('breadth_pct', 0)}% Adv` | VIX `{reg.get('vix', 0)}`) | Capital `₹{cap/100000:.1f}L`",
        f"🔥 *Open Heat:* `{aud.get('open_heat_pct', 0)}%` / `{MAX_PORTFOLIO_HEAT_PCT}%` Cap | Active Non-FreeRoll Swings: `{aud.get('active_swing_count', 0)}/{MAX_ACTIVE_SWINGS}`",
        "",
    ]

    # Section A: Daily Changes & Rationale (Sent EVERY Day Mon-Fri)
    lines.append("🔔 *DAILY CHANGES & RATIONALE (vs Prior Run):*")
    if not diff.get("has_prev"):
        lines.append("• _Baseline snapshot initialized today; daily change alerts active from next 5 PM run._")
    elif diff.get("total_changes", 0) == 0:
        lines.append("• _No additions, removals, or status triggers today — stay anchored to current levels._")
    else:
        bucket_titles = [
            ("common_dual", "🔥 Common in Both"),
            ("confirm_swing", "⚡ Confirm 1–2M"),
            ("confirm_core", "🏛 Confirm 8–12M"),
            ("watchlist", "📋 Watchlist"),
        ]
        for key, label in bucket_titles:
            b = diff.get(key, {})
            for item in b.get("added", [])[:5]:
                lines.append(f"• *+ ADDED [{label}] `{item['ticker']}`:* {item['reason']}")
            for item in b.get("removed", [])[:5]:
                lines.append(f"• *- REMOVED [{label}] `{item['ticker']}`:* {item['reason']}")
        op = diff.get("open_positions", {})
        for item in op.get("added", [])[:5]:
            lines.append(f"• *+ NEW POSITION `{item['ticker']}`:* {item['reason']}")
        for item in op.get("status_changed", [])[:5]:
            lines.append(f"• *↻ STATUS SHIFT `{item['ticker']}`:* {item['reason']}")
        for item in op.get("removed", [])[:5]:
            lines.append(f"• *✓ EXITED `{item['ticker']}`:* {item['reason']}")
    lines.append("")

    # Always flag urgent Open Action triggers (18D Time-Stops, T1 Free-Roll, 25% Runners, Spring Reclaim)
    urgent_actions = [
        a for a in aud.get("open_actions", [])
        if a.get("timeStop") or a.get("status") in ("T1_HIT", "RUNNER_ACTIVE", "SPRING_RECLAIM") or "BOOK_T1" in str(a.get("action")) or "PYRAMID" in str(a.get("action"))
    ]
    if urgent_actions:
        lines.append(f"🛡️ *IMMEDIATE POSITION ACTIONS ({len(urgent_actions)}):*")
        for a in urgent_actions[:6]:
            fr = " [0% Heat]" if a.get("freeRoll") else ""
            lines.append(f"• `{a['symbol']}` ({a['status']}{fr}): *{a['action']}* @ ₹{a['cmp']} — {a['note']}")
        lines.append("")

    # Section B: Friday Full Review of All Existing Rosters
    if is_friday or not diff.get("has_prev"):
        lines.append(f"🔥 *COMMON IN BOTH (Dual Confirm — {len(commons)}):*")
        if not commons:
            lines.append("• _None currently passing both gates simultaneously._")
        else:
            for s in commons[:8]:
                sw = s["swing"]
                lines.append(
                    f"• `{s['ticker']}` (`{s['sizeMult']}R` | SM `{s['stockScore']}` | ROE `{s.get('roePct', '--')}%`): "
                    f"Buy `₹{sw['entryRef']}` ({sw['shares']} sh = `40%/45%/15%`) | Hard SL `₹{sw['hardGttSl']}` | EOD SL `₹{sw['softEodSl']}` | T1 `₹{sw['t1_2r']}`"
                )
        lines.append("")

        lines.append(f"⚡ *CONFIRM 1–2M ROSTER ({len(swings)} | Top Sector P2/P3 + Stock P3):*")
        for s in swings[:10]:
            sw = s["swing"]
            w_tag = " `[0.5R WATCH: P1 Sector]`" if s.get("isP1Watch") else f" `[{s['guard']}]`"
            lines.append(
                f"• `{s['ticker']}` ({s['sectorTier']}->{s['stockTier']} {s['stockScore']}){w_tag}: "
                f"₹{sw['entryRef']} ({sw['shares']}sh) | GTT SL ₹{sw['hardGttSl']} | EOD SL ₹{sw['softEodSl']}"
            )
        lines.append("")

        lines.append(f"🏛 *CONFIRM 8–12M CORE ROSTER ({len(cores)} | ROE >=12% Verified):*")
        for c in cores[:10]:
            cr = c["core"]
            lines.append(
                f"• `{c['ticker']}` (ROE `{cr.get('roe', '--')}%` | P/E `{cr.get('pe', '--')}`): *{c['coreAction']}* "
                f"@ `₹{cr['accumBand']}` ({cr['shares']}sh) | 150DMA SL `₹{cr['structSl']}` | Base `₹{cr['baseTarget']:.0f}`"
            )
        lines.append("")

        p2_watch = [w for w in watch if not w.get("isCurated")][:5]
        if p2_watch:
            lines.append(f"📋 *WATCHLIST TOP COILS ({len(watch)} Total — Focus + Early Coils):*")
            lines.append("• " + ", ".join(f"`{w['ticker']}` ({w['stockTier']} {w['stockScore']})" for w in p2_watch))
            lines.append("")
    else:
        lines.append(f"📊 *Roster Snapshot:* Common Dual `{len(commons)}` · Confirm 1–2M `{len(swings)}` · Confirm 8–12M `{len(cores)}` · Watchlist `{len(watch)}` _(Full roster sent every Friday 5 PM)_")

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
    parser.add_argument("--friday", action="store_true", help="Preview full Friday weekly Telegram report")
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
        print(build_daily_trade_plan_telegram(tp, force_friday_mode=(True if args.friday else None)))
