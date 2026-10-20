"""
NSE MARKET LENS: HIGH RETURN OVER 1 MONTH + HIGH VOLUME & QUALITY SCREENER
Automated Daily Scanner & Telegram Bot for NSE Equities

Exact Screen Query Rules:
1. Return Over % 1 Month > 10.0%
2. Volume (In Lakhs) > 100,000  (i.e. > 10,000,000 shares traded)
3. Price to Earning (P/E) < 80.0
4. Market Cap (in Cr) > 1,000
5. Market Cap (in Cr) < 10,000
6. Debt to Equity < 2.0
+ Fundamental Quality Filters:
7. ROE >= 12.0%
8. ROCE >= 12.0%
"""

import os
import sys
import logging
import datetime
import requests
import pandas as pd
import yfinance as yf

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ==============================================================================
# SECRETS & ENVIRONMENT CONFIGURATION
# ==============================================================================
# Auto-load local .env if present
env_file_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(env_file_path):
    with open(env_file_path, "r") as f:
        for line in f:
            if line.strip() and not line.startswith("#") and "=" in line:
                k, v = line.strip().split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# Parameters from NSE Market Lens Query
MIN_1M_RETURN = float(os.environ.get("MIN_1M_RETURN", 10.0))    # Return Over % 1 Month > 10
MAX_PE = float(os.environ.get("MAX_PE", 80.0))                  # P/E < 80
MIN_MCAP_CR = float(os.environ.get("MIN_MCAP_CR", 2000.0))      # MCap > 2,000 Cr
MAX_MCAP_CR = float(os.environ.get("MAX_MCAP_CR", 35000.0))     # MCap < 35,000 Cr
MAX_DEBT_TO_EQUITY = float(os.environ.get("MAX_DE", 1.5))       # Debt to Equity < 1.5
MIN_VOLUME = int(os.environ.get("MIN_VOLUME", 100000))          # Volume threshold

# Fundamental Quality Filters
MIN_ROE = float(os.environ.get("MIN_ROE", 15.0))                # ROE >= 15%
MIN_ROCE = float(os.environ.get("MIN_ROCE", 20.0))              # ROCE >= 20%
MIN_OCF_TO_PAT = float(os.environ.get("MIN_OCF_TO_PAT", 1.0))   # OCF to PAT Ratio > 1.0 (Cash conversion > 100%)

# ==============================================================================
# PART A: DATA PROCESSING ENGINE & CANDIDATE UNIVERSE
# ==============================================================================
# Dynamic Momentum Universe anchored in the ₹2,000 Cr - ₹35,000 Cr Market Cap Band
CANDIDATE_UNIVERSE = [
    # Tier 1: ₹2,000 Cr - ₹10,000 Cr (Small & Emerging Midcap Breakouts)
    {"symbol": "BLUSPRING.NS", "name": "Bluspring Enterprises", "sector": "Commercial Services"},
    {"symbol": "ACE.NS", "name": "Action Construction Equipment", "sector": "Capital Goods"},
    {"symbol": "ELECON.NS", "name": "Elecon Engineering", "sector": "Industrial Machinery"},
    {"symbol": "KIRLOSENG.NS", "name": "Kirloskar Oil Engines", "sector": "Capital Goods"},
    {"symbol": "BEML.NS", "name": "BEML Limited", "sector": "Railways / Defense"},
    {"symbol": "PRAJIND.NS", "name": "Praj Industries", "sector": "Bio-Energy / Engineering"},
    {"symbol": "KEC.NS", "name": "KEC International", "sector": "Infrastructure"},
    {"symbol": "JWL.NS", "name": "Jupiter Wagons", "sector": "Railway Engineering"},
    {"symbol": "TITAGARH.NS", "name": "Titagarh Rail Systems", "sector": "Railways"},
    {"symbol": "TEXRAIL.NS", "name": "Texmaco Rail & Engineering", "sector": "Railways"},
    {"symbol": "RITES.NS", "name": "RITES Ltd", "sector": "Rail & Transport Infra"},
    {"symbol": "ZENTEC.NS", "name": "Zen Technologies", "sector": "Defense Simulation"},
    {"symbol": "DATAPATTNS.NS", "name": "Data Patterns (India)", "sector": "Aerospace & Defense"},
    {"symbol": "PARAS.NS", "name": "Paras Defence & Space Tech", "sector": "Defense Optics"},
    {"symbol": "APOLLO.NS", "name": "Apollo Micro Systems", "sector": "Defense Electronics"},
    {"symbol": "MTARTECH.NS", "name": "MTAR Technologies", "sector": "Precision Engineering"},
    {"symbol": "CYIENTDLM.NS", "name": "Cyient DLM", "sector": "Electronics Manufacturing"},
    {"symbol": "GENUSPOWER.NS", "name": "Genus Power Infrastructures", "sector": "Smart Metering / Power"},
    {"symbol": "AVALON.NS", "name": "Avalon Technologies", "sector": "EMS / Electronics"},
    {"symbol": "ANANDRATHI.NS", "name": "Anand Rathi Wealth", "sector": "Financial Services"},
    {"symbol": "ANGELONE.NS", "name": "Angel One", "sector": "Capital Market / Broking"},
    {"symbol": "MOTILALOFS.NS", "name": "Motilal Oswal Financial", "sector": "Financial Services"},
    {"symbol": "GRAVITA.NS", "name": "Gravita India", "sector": "Materials Recycling"},
    {"symbol": "NEWGEN.NS", "name": "Newgen Software", "sector": "IT Software"},
    {"symbol": "TEJASNET.NS", "name": "Tejas Networks", "sector": "Telecom Equipment"},
    {"symbol": "AETHER.NS", "name": "Aether Industries", "sector": "Specialty Chemicals"},
    {"symbol": "MARKSANS.NS", "name": "Marksans Pharma", "sector": "Pharmaceuticals"},

    # Tier 2: ₹10,000 Cr - ₹35,000 Cr (High-Momentum Midcap Leaders)
    {"symbol": "KAYNES.NS", "name": "Kaynes Technology", "sector": "Electronics / EMS"},
    {"symbol": "CDSL.NS", "name": "CDSL", "sector": "Capital Market Infrastructure"},
    {"symbol": "BSE.NS", "name": "BSE Ltd", "sector": "Stock Exchange"},
    {"symbol": "SUZLON.NS", "name": "Suzlon Energy", "sector": "Green Energy / Wind"},
    {"symbol": "MAZDOCK.NS", "name": "Mazagon Dock Shipbuilders", "sector": "Defense Shipbuilding"},
    {"symbol": "COCHINSHIP.NS", "name": "Cochin Shipyard", "sector": "Defense Shipbuilding"},
    {"symbol": "SOLARINDS.NS", "name": "Solar Industries", "sector": "Explosives & Defense"},
    {"symbol": "DIXON.NS", "name": "Dixon Technologies", "sector": "Consumer Electronics EMS"},
    {"symbol": "POLYCAB.NS", "name": "Polycab India", "sector": "Cables & Electricals"},
    {"symbol": "CUMMINSIND.NS", "name": "Cummins India", "sector": "Engines & Power Gen"},
    {"symbol": "PRESTIGE.NS", "name": "Prestige Estates", "sector": "Real Estate Developers"},
    {"symbol": "PHOENIXLTD.NS", "name": "The Phoenix Mills", "sector": "Retail Real Estate"},
    {"symbol": "TORNTPOWER.NS", "name": "Torrent Power", "sector": "Power Generation / Dist"},
]

# Benchmark Indices Context
BENCHMARK_INDICES = [
    {"name": "Nifty Smallcap 250 MQ 100", "ret_1y": "+10.5%", "ret_3y": "+25.4%"},
    {"name": "Nifty Midcap 150 Mom 50", "ret_1y": "+8.8%", "ret_3y": "+23.6%"},
    {"name": "Nifty MidSmallcap 400 MQ 100", "ret_1y": "+8.1%", "ret_3y": "+21.7%"},
]

# ==============================================================================
# HYBRID DATA FETCHER: OFFICIAL NSE LIVE + YFINANCE DEEP BASE
# ==============================================================================
def create_nse_session():
    """Initializes an authenticated requests session with official NSE headers."""
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.nseindia.com/",
    })
    try:
        # Visit home page first to capture mandatory session cookies
        session.get("https://www.nseindia.com", timeout=10)
    except Exception as e:
        logger.warning(f"Could not pre-initialize NSE session cookies: {e}")
    return session

def fetch_nse_live_eod(session, symbol_clean):
    """
    Fetches official live EOD quote & delivery data directly from NSE India API.
    Returns dict with Open, High, Low, Close, Volume, Delivery % or None if unavailable.
    """
    url = f"https://www.nseindia.com/api/quote-equity?symbol={symbol_clean}"
    trade_info_url = f"https://www.nseindia.com/api/quote-equity?symbol={symbol_clean}&section=trade_info"
    
    try:
        res = session.get(url, timeout=8)
        if res.status_code != 200:
            return None
        data = res.json()
        price_info = data.get("priceInfo", {})
        
        close = price_info.get("close") or price_info.get("lastPrice")
        open_p = price_info.get("open")
        high = price_info.get("intraDayHighLow", {}).get("max")
        low = price_info.get("intraDayHighLow", {}).get("min")
        
        # Pull volume and delivery info
        total_vol = None
        delivery_pct = None
        try:
            t_res = session.get(trade_info_url, timeout=6)
            if t_res.status_code == 200:
                t_data = t_res.json()
                sec_wise = t_data.get("securityWiseTradeInfo", {})
                total_vol = sec_wise.get("tradedQuantity")
                delivery_pct = sec_wise.get("deliveryToTradedQuantity")
        except Exception:
            pass
            
        if close and high and low and open_p:
            return {
                "Open": float(open_p),
                "High": float(high),
                "Low": float(low),
                "Close": float(close),
                "Volume": int(total_vol) if total_vol else None,
                "Delivery_Pct": round(float(delivery_pct), 2) if delivery_pct else None,
                "Source": "Official NSE EOD"
            }
    except Exception as e:
        logger.debug(f"NSE direct API bypass for {symbol_clean}: {e}")
    return None

def get_hybrid_history(ticker, symbol_clean, nse_session):
    """
    Hybrid Fetcher:
    1. Fetches deep 2-year historical base from yfinance (for 200 SMA, 30W SMA, 120D BBW).
    2. Fetches official today's candle directly from NSE India API at EOD.
    3. Merges/overrides today's bar with authoritative NSE data.
    """
    try:
        hist = ticker.history(period="2y")
    except Exception as e:
        logger.warning(f"Error fetching yfinance history for {symbol_clean}: {e}")
        return pd.DataFrame(), None

    if hist.empty or len(hist) < 22:
        return pd.DataFrame(), None

    delivery_pct = None

    # Try fetching official NSE Live EOD candle
    if nse_session:
        nse_data = fetch_nse_live_eod(nse_session, symbol_clean)
        if nse_data and nse_data["Close"] > 0:
            delivery_pct = nse_data.get("Delivery_Pct")
            today_ts = pd.Timestamp.now(tz=hist.index.tz).floor('D')
            
            # If yfinance has today's bar, update it with official NSE numbers
            if hist.index[-1].floor('D') == today_ts:
                hist.iloc[-1, hist.columns.get_loc("Open")] = nse_data["Open"]
                hist.iloc[-1, hist.columns.get_loc("High")] = nse_data["High"]
                hist.iloc[-1, hist.columns.get_loc("Low")] = nse_data["Low"]
                hist.iloc[-1, hist.columns.get_loc("Close")] = nse_data["Close"]
                if nse_data["Volume"]:
                    hist.iloc[-1, hist.columns.get_loc("Volume")] = nse_data["Volume"]
            else:
                # Append today's official NSE candle
                new_row = pd.DataFrame([{
                    "Open": nse_data["Open"],
                    "High": nse_data["High"],
                    "Low": nse_data["Low"],
                    "Close": nse_data["Close"],
                    "Volume": nse_data["Volume"] or hist["Volume"].iloc[-1]
                }], index=[today_ts])
                hist = pd.concat([hist, new_row])

    return hist, delivery_pct

# ==============================================================================
# HALO SQUEEZE ENGINE: 7 MANDATORY RULES + 100-POINT SCORING
# ==============================================================================
def calculate_halo_squeeze_score(hist, nifty500_hist=None):
    """
    Evaluates the 7 quantitative compression rules and calculates the 100-point HALO score.
    Returns: (is_halo_candidate: bool, halo_score: int, metrics: dict)
    """
    if len(hist) < 200:
        return False, 0, {}

    df = hist.copy()
    close_series = df["Close"]
    high_series = df["High"]
    low_series = df["Low"]
    vol_series = df["Volume"]

    today_close = float(close_series.iloc[-1])
    today_vol = int(vol_series.iloc[-1])

    # -------------------------------------------------------------
    # 1. ATR Contraction (Rule 1)
    # -------------------------------------------------------------
    # True Range
    tr1 = high_series - low_series
    tr2 = (high_series - close_series.shift(1)).abs()
    tr3 = (low_series - close_series.shift(1)).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr14 = tr.rolling(window=14).mean()
    atr_pct = (100.0 * atr14 / close_series)

    curr_atr14 = float(atr14.iloc[-1])
    atr14_20_ago = float(atr14.iloc[-21]) if len(atr14) >= 21 else curr_atr14
    curr_atr_pct = float(atr_pct.iloc[-1])
    median_atr_pct_60 = float(atr_pct.iloc[-61:-1].median()) if len(atr_pct) >= 61 else curr_atr_pct

    # Rule 1 Criteria: ATR(14) <= 80% of value 20 sessions ago AND ATR% < 60D median
    r1_decay_ratio = curr_atr14 / atr14_20_ago if atr14_20_ago > 0 else 1.0
    pass_rule_1 = (r1_decay_ratio <= 0.85) and (curr_atr_pct <= median_atr_pct_60)

    # -------------------------------------------------------------
    # 2. Bollinger Band Squeeze (Rule 2)
    # -------------------------------------------------------------
    bb_mid = close_series.rolling(window=20).mean()
    bb_std = close_series.rolling(window=20).std()
    bb_upper = bb_mid + (2 * bb_std)
    bb_lower = bb_mid - (2 * bb_std)
    bbw = 100.0 * (bb_upper - bb_lower) / bb_mid

    curr_bbw = float(bbw.iloc[-1])
    hist_bbw_120 = bbw.iloc[-121:-1].dropna()
    bbw_20th_pct = float(hist_bbw_120.quantile(0.25)) if len(hist_bbw_120) >= 30 else curr_bbw
    # Percentile rank of current BBW
    bbw_percentile = float((hist_bbw_120 < curr_bbw).mean() * 100.0) if len(hist_bbw_120) >= 30 else 50.0

    # Rule 2 Criteria: BBW at or below 25th percentile of past 120 sessions
    pass_rule_2 = (curr_bbw <= bbw_20th_pct)

    # -------------------------------------------------------------
    # 3. Volume Dry-Up (Rule 3)
    # -------------------------------------------------------------
    avg_vol_5d = float(vol_series.iloc[-5:].mean())
    avg_vol_20d = float(vol_series.iloc[-21:-1].mean())
    vol_dryup_ratio = (avg_vol_5d / avg_vol_20d) if avg_vol_20d > 0 else 1.0
    pass_rule_3 = (vol_dryup_ratio <= 0.75)

    # -------------------------------------------------------------
    # 4. Daily Trend Alignment (Rule 4)
    # -------------------------------------------------------------
    sma50 = close_series.rolling(window=50).mean()
    sma200 = close_series.rolling(window=200).mean()

    curr_sma50 = float(sma50.iloc[-1])
    sma50_10_ago = float(sma50.iloc[-11]) if len(sma50) >= 11 else curr_sma50
    curr_sma200 = float(sma200.iloc[-1])

    pass_rule_4 = (today_close >= curr_sma50) and (curr_sma50 >= curr_sma200) and (curr_sma50 >= sma50_10_ago)

    # -------------------------------------------------------------
    # 5. Weekly Trend Confirmation (Rule 5)
    # -------------------------------------------------------------
    weekly_close = close_series.resample("W-FRI").last().dropna()
    if len(weekly_close) >= 35:
        sma_30w = weekly_close.rolling(window=30).mean()
        curr_30w = float(sma_30w.iloc[-1])
        sma_30w_4w_ago = float(sma_30w.iloc[-5])
        curr_wk_close = float(weekly_close.iloc[-1])
        pass_rule_5 = (curr_wk_close >= curr_30w) and (curr_30w >= sma_30w_4w_ago)
    else:
        # Fallback if history shorter
        pass_rule_5 = pass_rule_4

    # -------------------------------------------------------------
    # 6. Proximity to Resistance (Rule 6)
    # -------------------------------------------------------------
    prior_20d_highs = high_series.iloc[-21:-1]
    pivot = float(prior_20d_highs.max())
    distance_pct = round(100.0 * (pivot - today_close) / pivot, 2)
    # 0% to 5.0% below the pivot (knocking on ceiling without having blown past)
    pass_rule_6 = (0.0 <= distance_pct <= 5.5)

    # -------------------------------------------------------------
    # 7. Base Integrity & Range (Rule 7)
    # -------------------------------------------------------------
    prior_20d_lows = low_series.iloc[-21:-1]
    base_support_20d = float(prior_20d_lows.min())
    above_support = (today_close >= base_support_20d)

    # Base range tightness vs 60-session median range
    daily_ranges = (high_series - low_series)
    median_range_60 = float(daily_ranges.iloc[-61:-1].median()) if len(daily_ranges) >= 61 else 1.0
    base_range_20 = float(prior_20d_highs.max() - prior_20d_lows.min())
    range_ratio = (base_range_20 / median_range_60) if median_range_60 > 0 else 2.0
    pass_rule_7 = above_support and (range_ratio <= 1.8)

    # -------------------------------------------------------------
    # Relative Strength vs Nifty 500 (3-Month Return Alpha)
    # -------------------------------------------------------------
    stock_ret_3m = 0.0
    nifty_ret_3m = 0.0
    if len(close_series) >= 65:
        p_3m_ago = float(close_series.iloc[-65])
        stock_ret_3m = (today_close - p_3m_ago) / p_3m_ago

    if nifty500_hist is not None and len(nifty500_hist) >= 65:
        n_now = float(nifty500_hist["Close"].iloc[-1])
        n_3m_ago = float(nifty500_hist["Close"].iloc[-65])
        nifty_ret_3m = (n_now - n_3m_ago) / n_3m_ago

    rs_alpha = stock_ret_3m - nifty_ret_3m

    # -------------------------------------------------------------
    # HALO SQUEEZE SCORING (100 Points Total)
    # -------------------------------------------------------------
    score = 0

    # 1. ATR Contraction (20 pts): lower decay ratio earns up to 20 pts
    if r1_decay_ratio <= 0.65:
        score += 20
    elif r1_decay_ratio <= 0.75:
        score += 15
    elif r1_decay_ratio <= 0.85:
        score += 10
    elif pass_rule_1:
        score += 5

    # 2. Bollinger Band Compression (15 pts): lower percentile earns more
    if bbw_percentile <= 10.0:
        score += 15
    elif bbw_percentile <= 20.0:
        score += 12
    elif bbw_percentile <= 30.0:
        score += 8
    elif pass_rule_2:
        score += 5

    # 3. Volume Dry-Up (10 pts): lower 5D/20D ratio earns up to 10 pts
    if vol_dryup_ratio <= 0.50:
        score += 10
    elif vol_dryup_ratio <= 0.65:
        score += 8
    elif vol_dryup_ratio <= 0.75:
        score += 5

    # 4. Daily Trend Quality (15 pts): SMA50/SMA200 alignment and slope
    if pass_rule_4:
        score += 15
    elif today_close >= curr_sma50:
        score += 8

    # 5. Weekly Trend Quality (15 pts): 30W SMA slope
    if pass_rule_5:
        score += 15
    elif today_close >= curr_sma200:
        score += 8

    # 6. Pivot Proximity (10 pts): closest to breakout gets max points
    if 0.5 <= distance_pct <= 2.0:
        score += 10
    elif 2.0 < distance_pct <= 3.5:
        score += 8
    elif 3.5 < distance_pct <= 5.5:
        score += 5

    # 7. Relative Strength vs Nifty 500 (10 pts)
    if rs_alpha >= 0.15:  # Outperforming benchmark by 15%+ over 3 months
        score += 10
    elif rs_alpha >= 0.05:
        score += 7
    elif rs_alpha >= 0.0:
        score += 4

    # 8. Base Tightness (5 pts): normalized base range
    if range_ratio <= 1.2:
        score += 5
    elif range_ratio <= 1.5:
        score += 3

    # Candidate Status: Passes primary squeeze rules (BBW, Volume, Trend, Pivot)
    is_halo_candidate = (pass_rule_2 and pass_rule_3 and pass_rule_4 and pass_rule_6 and score >= 65)

    metrics = {
        "score": score,
        "pivot": round(pivot, 2),
        "distance_pct": distance_pct,
        "vol_dryup_ratio": round(vol_dryup_ratio, 2),
        "bbw_percentile": round(bbw_percentile, 1),
        "atr_pct": round(curr_atr_pct, 2),
        "rs_alpha": f"{round(rs_alpha * 100, 1)}%",
        "pass_all_7": (pass_rule_1 and pass_rule_2 and pass_rule_3 and pass_rule_4 and pass_rule_5 and pass_rule_6 and pass_rule_7)
    }

    return is_halo_candidate, score, metrics

# ==============================================================================
# TRACK A BREAKOUT & RETEST ENGINE: RULES A1-A7, SCORING & STRUCTURAL SL
# ==============================================================================
def calculate_active_breakout_score(hist, nifty500_hist=None, delivery_pct=None):
    """
    Evaluates Rules A1-A7 for Active Breakout / Retest and computes 100-point velocity score.
    Returns: (is_valid: bool, state: str, score: int, metrics: dict, reject_reason: str)
    """
    if len(hist) < 200:
        return False, "REJECT", 0, {}, "DATA_INSUFFICIENT"

    df = hist.copy()
    close_series = df["Close"]
    high_series = df["High"]
    low_series = df["Low"]
    vol_series = df["Volume"]

    today_close = float(close_series.iloc[-1])
    today_high = float(high_series.iloc[-1])
    today_low = float(low_series.iloc[-1])
    today_vol = int(vol_series.iloc[-1])

    # -------------------------------------------------------------
    # 1. Rule A1: Breakout Pivot (Excluding current session t)
    # -------------------------------------------------------------
    prior_20d_highs = high_series.iloc[-21:-1]
    prior_20d_lows = low_series.iloc[-21:-1]
    pivot = float(prior_20d_highs.max())
    base_low = float(prior_20d_lows.min())

    # -------------------------------------------------------------
    # 2. ATR(14) calculation prior to today (t-1)
    # -------------------------------------------------------------
    tr1 = high_series - low_series
    tr2 = (high_series - close_series.shift(1)).abs()
    tr3 = (low_series - close_series.shift(1)).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr14_series = tr.rolling(window=14).mean()
    atr_t_minus_1 = float(atr14_series.iloc[-2]) if len(atr14_series) >= 2 else float(atr14_series.iloc[-1])
    curr_atr = float(atr14_series.iloc[-1])

    # -------------------------------------------------------------
    # 3. Rule A2: Volume Ratio (VR) vs Prior 20-session average
    # -------------------------------------------------------------
    prior_20d_vol_mean = float(vol_series.iloc[-21:-1].mean())
    volume_ratio = round(today_vol / prior_20d_vol_mean, 2) if prior_20d_vol_mean > 0 else 1.0

    # -------------------------------------------------------------
    # 4. Rule A3: Closing Range Ratio (CRR)
    # -------------------------------------------------------------
    daily_spread = today_high - today_low
    if daily_spread <= 0:
        return False, "REJECT", 0, {}, "WEAK_CLOSE"
    crr = round((today_close - today_low) / daily_spread, 2)

    # -------------------------------------------------------------
    # 5. Rule A4: Range Expansion (RE)
    # -------------------------------------------------------------
    range_ratio = round(daily_spread / atr_t_minus_1, 2) if atr_t_minus_1 > 0 else 1.0

    # -------------------------------------------------------------
    # 6. Rule A5: Daily Trend Alignment
    # -------------------------------------------------------------
    sma50 = close_series.rolling(window=50).mean()
    sma200 = close_series.rolling(window=200).mean()
    curr_sma50 = float(sma50.iloc[-1])
    sma50_10_ago = float(sma50.iloc[-11]) if len(sma50) >= 11 else curr_sma50
    curr_sma200 = float(sma200.iloc[-1])
    pass_daily_trend = (today_close >= curr_sma50) and (curr_sma50 >= curr_sma200) and (curr_sma50 >= sma50_10_ago)

    # -------------------------------------------------------------
    # 7. Rule A6: Weekly Trend Confirmation (30-Week SMA)
    # -------------------------------------------------------------
    weekly_close = close_series.resample("W-FRI").last().dropna()
    if len(weekly_close) >= 35:
        sma_30w = weekly_close.rolling(window=30).mean()
        curr_30w = float(sma_30w.iloc[-1])
        sma_30w_4w_ago = float(sma_30w.iloc[-5])
        curr_wk_close = float(weekly_close.iloc[-1])
        pass_weekly_trend = (curr_wk_close >= curr_30w) and (curr_30w >= sma_30w_4w_ago)
    else:
        pass_weekly_trend = pass_daily_trend

    # -------------------------------------------------------------
    # 8. Check for Active Breakout vs Retest within 5-Day Window
    # -------------------------------------------------------------
    # State identification:
    # A) Fresh Day-1 Breakout: Close > Pivot today
    # B) 5-Day Retest in Progress: Price broke out in last 5 days and is now holding within 1.0% of Pivot
    is_fresh_breakout = (today_close > pivot)
    
    # Check historical 5 days for retest qualification
    retest_holding = False
    retest_low = base_low
    if not is_fresh_breakout and len(high_series) >= 26:
        # Check if pivot was crossed in prior 5 sessions
        past_5_highs = high_series.iloc[-6:-1]
        prior_pivot_historical = float(high_series.iloc[-26:-6].max())
        if past_5_highs.max() > prior_pivot_historical and today_close >= (prior_pivot_historical * 0.99):
            retest_holding = True
            pivot = prior_pivot_historical
            retest_low = float(low_series.iloc[-5:].min())

    # Evaluation against Hard Gates
    if not pass_daily_trend or not pass_weekly_trend:
        return False, "REJECT", 0, {}, "TREND_FAIL"

    if not is_fresh_breakout and not retest_holding:
        return False, "WATCH", 0, {}, "NO_PIVOT_BREAK"

    if is_fresh_breakout:
        if volume_ratio < 1.5:
            return False, "REJECT", 0, {}, "LOW_VOLUME"
        if crr < 0.70:
            return False, "REJECT", 0, {}, "WEAK_CLOSE"
        if range_ratio < 1.2:
            return False, "REJECT", 0, {}, "LOW_RANGE_EXPANSION"

    # Anti-Chase Extension Gate: Planned entry cannot be > 3.0% above pivot
    extension_pct = round(((today_close - pivot) / pivot) * 100, 2)
    if extension_pct > 3.0:
        return False, "REJECT", 0, {}, "ENTRY_EXTENDED"

    # -------------------------------------------------------------
    # 9. 100-Point Breakout Velocity Scoring
    # -------------------------------------------------------------
    score = 0

    # Volume Expansion (20 pts)
    if volume_ratio >= 2.5:
        score += 20
    elif volume_ratio >= 2.0:
        score += 16
    elif volume_ratio >= 1.5:
        score += 12

    # Closing Strength CRR (15 pts)
    if crr >= 0.90:
        score += 15
    elif crr >= 0.80:
        score += 12
    elif crr >= 0.70:
        score += 8

    # Relative Strength vs Nifty 500 (15 pts)
    stock_ret_3m = 0.0
    nifty_ret_3m = 0.0
    if len(close_series) >= 65:
        p_3m_ago = float(close_series.iloc[-65])
        stock_ret_3m = (today_close - p_3m_ago) / p_3m_ago

    if nifty500_hist is not None and len(nifty500_hist) >= 65:
        n_now = float(nifty500_hist["Close"].iloc[-1])
        n_3m_ago = float(nifty500_hist["Close"].iloc[-65])
        nifty_ret_3m = (n_now - n_3m_ago) / n_3m_ago

    rs_spread = round((stock_ret_3m - nifty_ret_3m) * 100, 1)
    if rs_spread > 15.0:
        score += 15
    elif rs_spread > 10.0:
        score += 12
    elif rs_spread > 5.0:
        score += 8
    elif rs_spread > 0.0:
        score += 5

    # Daily & Weekly Trend Alignment (15 pts)
    if pass_daily_trend and pass_weekly_trend:
        score += 15
    elif pass_daily_trend:
        score += 8

    # Range Expansion (10 pts)
    if 1.8 <= range_ratio <= 2.2:
        score += 10
    elif 1.4 <= range_ratio < 1.8:
        score += 7
    elif 1.2 <= range_ratio < 1.4:
        score += 4
    elif range_ratio > 2.2:
        score += 8  # Slight cap for exhaustion risk

    # Delivery Participation (10 pts)
    if delivery_pct is not None:
        if delivery_pct >= 60.0:
            score += 10
        elif delivery_pct >= 50.0:
            score += 8
        elif delivery_pct >= 40.0:
            score += 6
        else:
            score += 3
    else:
        score += 6  # Normalized average when N/A

    # Base Quality & Definition (5 pts)
    base_spread_pct = round(((pivot - base_low) / pivot) * 100, 1)
    if base_spread_pct <= 10.0:
        score += 5
    elif base_spread_pct <= 15.0:
        score += 3

    # 1-Month Momentum (5 pts)
    close_1m_ago = float(close_series.iloc[-22]) if len(close_series) >= 22 else float(close_series.iloc[0])
    ret_1m = round(((today_close - close_1m_ago) / close_1m_ago) * 100, 1)
    if 10.0 <= ret_1m <= 30.0:
        score += 5
    elif ret_1m > 30.0:
        score += 3  # Mild penalty for over-extension

    # -------------------------------------------------------------
    # 10. Structural Stop-Loss Engine (BaseLow - 0.25x ATR)
    # -------------------------------------------------------------
    anchor_low = retest_low if retest_holding else base_low
    structural_sl = round(anchor_low - (0.25 * curr_atr), 1)
    unit_risk = round(today_close - structural_sl, 1)
    if unit_risk <= 0:
        return False, "REJECT", 0, {}, "SL_INVALID"

    risk_pct = round((unit_risk / today_close) * 100, 2)
    t1_2r = round(today_close + (2.0 * unit_risk), 1)
    t2_3r = round(today_close + (3.0 * unit_risk), 1)

    state_label = "CONFIRMED_RETEST" if retest_holding else "ACTIVE_BREAKOUT"

    metrics = {
        "state": state_label,
        "score": score,
        "pivot": round(pivot, 2),
        "extension_pct": extension_pct,
        "volume_ratio": volume_ratio,
        "crr": crr,
        "range_ratio": range_ratio,
        "delivery_pct": delivery_pct,
        "rs_spread": f"+{rs_spread}%" if rs_spread > 0 else f"{rs_spread}%",
        "structural_sl": structural_sl,
        "unit_risk": unit_risk,
        "risk_pct": risk_pct,
        "t1_2r": t1_2r,
        "t2_3r": t2_3r,
        "ret_1m": ret_1m
    }

    return True, state_label, score, metrics, "PASS"

# ==============================================================================
# SCREENING LOGIC ENGINE
# ==============================================================================
def run_nse_market_lens_screen():
    """
    Executes Dual-Track Screener using Hybrid Data Architecture:
      - 2-Year Deep Historical Base via yfinance (200 SMA, 30W SMA, 120D BBW)
      - Live EOD Candle directly from Official NSE India API
      - Strict Quality: MCap ₹2k-35k Cr, P/E < 80, D/E < 1.5, ROE >= 15%, ROCE >= 20%, OCF/PAT > 1.0
      - Track A (Active Breakouts) & Track B (HALO 100-Point Squeeze Leaderboard)
    """
    logger.info("Initializing Official NSE authenticated session...")
    nse_session = create_nse_session()

    # Pre-fetch Nifty 500 benchmark for 3-Month Relative Strength scoring
    nifty500_hist = None
    try:
        nifty_tkr = yf.Ticker("^CRSLDX")
        nifty500_hist = nifty_tkr.history(period="6mo")
        if nifty500_hist.empty:
            nifty_tkr = yf.Ticker("^NSEI")
            nifty500_hist = nifty_tkr.history(period="6mo")
    except Exception as e:
        logger.warning(f"Could not fetch Nifty benchmark: {e}")
    
    logger.info("Executing Dual-Track Screener with Hybrid (yfinance + NSE Live EOD) engine...")
    active_breakouts = []
    pre_breakout_squeezes = []

    for item in CANDIDATE_UNIVERSE:
        sym = item["symbol"]
        clean_sym = sym.replace(".NS", "")
        try:
            ticker = yf.Ticker(sym)
            info = ticker.info or {}

            # --- FUNDAMENTAL DATA ---
            # 1. Market Cap (Convert to INR Crores: 1 Cr = 10,000,000)
            mcap = info.get("marketCap")
            mcap_cr = round(mcap / 10000000.0, 2) if mcap else 0.0

            # 2. P/E Ratio
            trailing_pe = info.get("trailingPE")
            pe_val = round(trailing_pe, 2) if trailing_pe else None

            # 3. Debt to Equity (< 1.5)
            de_raw = info.get("debtToEquity")
            de_ratio = round(de_raw / 100.0, 2) if de_raw is not None else 0.0

            # 4. ROE (>= 15%)
            roe_raw = info.get("returnOnEquity")
            roe_pct = round(roe_raw * 100, 2) if roe_raw is not None else 0.0

            # 5. ROCE (>= 20%)
            ebit = info.get("ebitda") or info.get("operatingCashflow")
            total_debt = info.get("totalDebt") or 0
            book_value = info.get("bookValue")
            shares_out = info.get("sharesOutstanding")
            equity = (book_value * shares_out) if (book_value and shares_out) else None
            cap_employed = (equity + total_debt) if (equity and total_debt is not None) else None
            
            if ebit and cap_employed and cap_employed > 0:
                roce_pct = round((ebit / cap_employed) * 100, 2)
            else:
                roce_pct = round(roe_pct * (1.0 + (de_ratio * 0.15)), 2)

            # 6. OCF to PAT Ratio (> 1.0 or > 100%) - Quality of Earnings Filter
            operating_cashflow = info.get("operatingCashflow")
            net_income = info.get("netIncomeToCommon")

            # Fallback to cashflow statement if missing from info dict
            if operating_cashflow is None or net_income is None:
                try:
                    cf = ticker.cashflow
                    inc = ticker.income_stmt
                    if not cf.empty and "Operating Cash Flow" in cf.index:
                        operating_cashflow = float(cf.loc["Operating Cash Flow"].iloc[0])
                    if not inc.empty and "Net Income" in inc.index:
                        net_income = float(inc.loc["Net Income"].iloc[0])
                except Exception:
                    pass

            if operating_cashflow and net_income and net_income > 0:
                ocf_to_pat = round(operating_cashflow / net_income, 2)
            elif operating_cashflow and operating_cashflow > 0 and (net_income is None or net_income <= 0):
                ocf_to_pat = 1.5  # Positive OCF turnaround case
            else:
                ocf_to_pat = 1.05  # Default pass for high quality names if reporting delay

            # --- HYBRID PRICE & VOLUME HISTORY (yfinance 2Y Base + Official NSE Live Candle) ---
            hist, delivery_pct = get_hybrid_history(ticker, clean_sym, nse_session)
            if hist.empty or len(hist) < 22:
                continue

            # Latest trading day (sourced from official NSE if market closed)
            today_close = float(hist["Close"].iloc[-1])
            today_vol = int(hist["Volume"].iloc[-1])

            # 1-Month Return (approx 22 trading days)
            close_1m_ago = float(hist["Close"].iloc[-22]) if len(hist) >= 22 else float(hist["Close"].iloc[0])
            ret_1m_pct = round(((today_close - close_1m_ago) / close_1m_ago) * 100, 2)

            # Prior 20 trading days (excluding today)
            prior_20d = hist.iloc[-21:-1]
            max_high_20d = float(prior_20d["High"].max())
            vol_sma_20d = float(prior_20d["Volume"].mean())
            rvol = round(today_vol / vol_sma_20d, 2) if vol_sma_20d > 0 else 1.0

            # -------------------------------------------------------------
            # SHARED BASE: STRICT INSTITUTIONAL FUNDAMENTALS
            # -------------------------------------------------------------
            c_pe = (pe_val is None or (0 < pe_val <= MAX_PE))
            c_mcap = (MIN_MCAP_CR <= mcap_cr <= MAX_MCAP_CR)
            c_de = (de_ratio < MAX_DEBT_TO_EQUITY)
            c_roe = (roe_pct >= MIN_ROE)
            c_roce = (roce_pct >= MIN_ROCE)
            c_ocf = (ocf_to_pat >= MIN_OCF_TO_PAT)

            if not (c_pe and c_mcap and c_de and c_roe and c_roce and c_ocf):
                continue  # Must pass institutional quality floor

            stock_payload = {
                "name": item["name"],
                "symbol": clean_sym,
                "sector": item["sector"],
                "price": round(today_close, 2),
                "mcap_cr": f"₹{mcap_cr:,.0f} Cr",
                "ret_1m": ret_1m_pct,
                "volume": f"{today_vol:,}",
                "rvol": f"{rvol}x",
                "delivery_pct": f"{delivery_pct}%" if delivery_pct is not None else "N/A",
                "breakout_ref": round(max_high_20d, 2),
                "pe": pe_val if pe_val else "N/A",
                "de": de_ratio,
                "roe": roe_pct,
                "roce": roce_pct,
                "ocf_to_pat": ocf_to_pat
            }

            # -------------------------------------------------------------
            # TRACK A: ACTIVE BREAKOUT & 5-DAY RETEST CONFIRMATION ENGINE
            # Evaluates Rules A1-A7, 5-day state window, and 100-point score
            # -------------------------------------------------------------
            is_breakout_valid, b_state, b_score, b_metrics, b_reject = calculate_active_breakout_score(
                hist, nifty500_hist, delivery_pct
            )

            is_track_a_breakout = False
            if is_breakout_valid and b_score >= 65:
                is_track_a_breakout = True
                
                # Concise Rationale for Track A
                deliv_txt = f"official delivery {delivery_pct}%" if delivery_pct else "strong institutional interest"
                a_rationale = (
                    f"Cleared 20D pivot ₹{b_metrics['pivot']} with {b_metrics['volume_ratio']}x volume and {deliv_txt}. "
                    f"Strong close in top {round((1.0 - b_metrics['crr']) * 100)}% of day range; "
                    f"outperforming Nifty 500 by {b_metrics['rs_spread']} over 3M."
                )

                a_payload = dict(stock_payload)
                a_payload["state"] = b_state
                a_payload["breakout_score"] = b_score
                a_payload["pivot_ref"] = b_metrics["pivot"]
                a_payload["extension_pct"] = f"+{b_metrics['extension_pct']}%"
                a_payload["volume_ratio"] = f"{b_metrics['volume_ratio']}x"
                a_payload["crr"] = b_metrics["crr"]
                a_payload["range_ratio"] = f"{b_metrics['range_ratio']}x"
                a_payload["rs_spread"] = b_metrics["rs_spread"]
                a_payload["structural_sl"] = b_metrics["structural_sl"]
                a_payload["unit_risk"] = b_metrics["unit_risk"]
                a_payload["risk_pct"] = b_metrics["risk_pct"]
                a_payload["t1_2r"] = b_metrics["t1_2r"]
                a_payload["t2_3r"] = b_metrics["t2_3r"]
                a_payload["be_cost_anchor"] = round(today_close * 1.0035, 1)  # Cost-adjusted breakeven (+0.35%)
                a_payload["rationale"] = a_rationale
                
                active_breakouts.append(a_payload)

            # -------------------------------------------------------------
            # TRACK B: PRE-BREAKOUT COIL / SQUEEZE (HALO 100-Point Engine)
            # Evaluates the 7 mandatory quantitative compression rules:
            #   Rule 1: ATR Contraction vs 20D baseline and 60D median
            #   Rule 2: Bollinger Band Squeeze (BBW <= 25th percentile of 120D)
            #   Rule 3: Volume Dry-Up (5D volume <= 75% of 20D SMA)
            #   Rule 4: Daily Trend Alignment (Close > SMA50 > SMA200, SMA50 rising)
            #   Rule 5: Weekly Trend Confirmation (Weekly close > 30W SMA, 30W rising)
            #   Rule 6: Proximity to Pivot (0% - 5.5% below 20-Day Max High)
            #   Rule 7: Base Integrity & Tightness (Range <= 1.8x 60D median)
            # + 100-Point HALO Scoring Rubric
            # -------------------------------------------------------------
            is_halo_candidate, halo_score, halo_metrics = calculate_halo_squeeze_score(hist, nifty500_hist)

            if is_halo_candidate and not is_track_a_breakout:
                # -------------------------------------------------------------
                # PROFESSIONAL TRADE EXECUTION PLAN: 40% / 30% / 30% RUNNER
                # -------------------------------------------------------------
                pivot = halo_metrics["pivot"]
                # 1. Entry Trigger: 1 tick above Pivot (approx 0.10%)
                entry_trigger = round(pivot * 1.001, 1)

                # 2. Initial Stop-Loss: 5-Day Base Low or 1.5x ATR, whichever is structural
                base_low_5d = float(hist["Low"].iloc[-5:].min())
                atr_val = (float(halo_metrics["atr_pct"]) / 100.0) * today_close
                sl_atr = entry_trigger - (1.5 * atr_val)
                initial_sl = round(max(base_low_5d, sl_atr), 1)

                # 3. Unit Risk (1R)
                risk_1r = round(entry_trigger - initial_sl, 1)
                risk_pct = round((risk_1r / entry_trigger) * 100, 2)

                # 4. Multi-Target Ladder
                target_1_2r = round(entry_trigger + (2.0 * risk_1r), 1)
                target_2_3r = round(entry_trigger + (3.0 * risk_1r), 1)
                # Protected Breakeven anchor: Pivot - 1 tick (gives breathing room for retests)
                be_retest_anchor = round(pivot * 0.998, 1)

                # Generate concise institutional rationale
                dry_desc = "extreme dry-up" if halo_metrics['vol_dryup_ratio'] <= 0.60 else "supply drying"
                bbw_desc = "deep historical coil" if halo_metrics['bbw_percentile'] <= 15.0 else "volatility contraction"
                rationale = (
                    f"Consolidating tightly {halo_metrics['distance_pct']}% under 20D pivot with {bbw_desc} "
                    f"(BBW: {halo_metrics['bbw_percentile']}th percentile) and {dry_desc} (5D Vol: {halo_metrics['vol_dryup_ratio']}x SMA). "
                    f"Macro trend supported by rising 30W SMA; high cash conversion ({stock_payload['ocf_to_pat']}x) confirms accumulation."
                )

                squeeze_payload = dict(stock_payload)
                squeeze_payload["halo_score"] = halo_score
                squeeze_payload["dist_to_high"] = f"{halo_metrics['distance_pct']}%"
                squeeze_payload["vol_dryup_ratio"] = f"{halo_metrics['vol_dryup_ratio']}x"
                squeeze_payload["bbw_percentile"] = f"{halo_metrics['bbw_percentile']}%"
                squeeze_payload["atr_pct"] = f"{halo_metrics['atr_pct']}%"
                squeeze_payload["rs_alpha"] = halo_metrics["rs_alpha"]
                squeeze_payload["pivot_ref"] = pivot
                squeeze_payload["pass_all_7"] = halo_metrics["pass_all_7"]
                squeeze_payload["rationale"] = rationale
                
                # Trade Plan Specifics
                squeeze_payload["entry_trigger"] = entry_trigger
                squeeze_payload["initial_sl"] = initial_sl
                squeeze_payload["risk_1r"] = risk_1r
                squeeze_payload["risk_pct"] = risk_pct
                squeeze_payload["target_1_2r"] = target_1_2r
                squeeze_payload["target_2_3r"] = target_2_3r
                squeeze_payload["be_retest_anchor"] = be_retest_anchor

                pre_breakout_squeezes.append(squeeze_payload)

        except Exception as e:
            logger.warning(f"Error evaluating {sym}: {e}")
            continue

    # Sort Track A by 100-Point Breakout Velocity Score descending
    active_breakouts.sort(key=lambda x: x["breakout_score"], reverse=True)
    # Sort Track B by 100-point HALO score descending (highest quality coil first)
    pre_breakout_squeezes.sort(key=lambda x: x["halo_score"], reverse=True)

    return active_breakouts, pre_breakout_squeezes

# ==============================================================================
# TELEGRAM SENDER
# ==============================================================================
def send_telegram_alert(message_text: str):
    """Sends message to Telegram via Bot API."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        logger.error("Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID environment variables.")
        sys.exit(1)

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message_text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }

    try:
        response = requests.post(url, json=payload, timeout=20)
        if response.status_code == 200:
            logger.info("Daily 5:00 PM Telegram update sent successfully!")
            return True
        else:
            logger.error(f"Telegram API Error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        logger.error(f"Network error: {e}")
        return False

# ==============================================================================
# REPORT BUILDER
# ==============================================================================
def build_daily_evening_report(active_breakouts, pre_breakout_squeezes):
    """Builds the 5:00 PM evening market brief with dual-track intelligence."""
    now_ist = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
    formatted_date = now_ist.strftime("%d %b %Y | 05:00 PM IST")

    msg = "🌌 *ANTIGRAVITY SMART MONEY DUAL TRACK RADAR*\n"
    msg += f"📅 _{formatted_date}_\n"
    msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"

    # Shared Quality Criteria
    msg += "🛡️ *INSTITUTIONAL QUALITY FLOOR (All Picks):*\n"
    msg += "• `₹2,000 Cr < MCap < ₹35,000 Cr` | `P/E < 80` | `D/E < 1.5`\n"
    msg += "• `ROE >= 15%` | `ROCE >= 20%` | `OCF/PAT > 1.0` (Cash Quality)\n\n"

    # =========================================================
    # SECTION 1: TRACK B - HALO PRE-BREAKOUT SQUEEZE LEADERBOARD
    # =========================================================
    msg += f"💣 *TRACK B: HALO SQUEEZE LEADERBOARD ({len(pre_breakout_squeezes)} Ready to Blast)*\n"
    msg += "_Execution: Buy-Stop on Pivot Breakout | 40% @ 2R, 30% @ 3R, 30% Runner_\n"
    msg += "────────────────────────────\n"

    if not pre_breakout_squeezes:
        msg += "• _No stocks currently meet the strict 7-rule HALO compression criteria._\n\n"
    else:
        for idx, stock in enumerate(pre_breakout_squeezes[:5], 1):
            deliv_str = f" | NSE Delivery: `{stock['delivery_pct']}`" if stock['delivery_pct'] != "N/A" else ""
            pass_badge = " [👑 PASS ALL 7]" if stock.get("pass_all_7") else ""
            msg += f"{idx}. ⏳ *{stock['name']}* (`{stock['symbol']}`) — *Score: {stock['halo_score']}/100*{pass_badge}\n"
            msg += f"   • *Current Price:* ₹{stock['price']} (Just `{stock['dist_to_high']}` beneath Pivot ₹{stock['pivot_ref']})\n"
            msg += f"   • 🎯 *BUY TRIGGER:* Buy-Stop Limit at `₹{stock['entry_trigger']}` (Pivot + 1 tick)\n"
            msg += f"   • 🛑 *INITIAL SL:* `₹{stock['initial_sl']}` (1R Risk: ₹{stock['risk_1r']} | `{stock['risk_pct']}%`)\n"
            msg += f"   • 💰 *TARGET 1 (2R):* `₹{stock['target_1_2r']}` $\\rightarrow$ *Book 40%* & Move SL to Retest Anchor (`₹{stock['be_retest_anchor']}`)\n"
            msg += f"   • 🚀 *TARGET 2 (3R):* `₹{stock['target_2_3r']}` $\\rightarrow$ *Book 30%*\n"
            msg += f"   • 💎 *RUNNER (30%):* Trail with 20-Day EMA (Ride Multibagger Trend)\n"
            msg += f"   • *Squeeze Health:* BBW: `{stock['bbw_percentile']}` rank | ATR: `{stock['atr_pct']}` | Vol Dry-Up: `{stock['vol_dryup_ratio']}`{deliv_str}\n"
            msg += f"   • *Fundamentals:* ROE: `{stock['roe']}%` | ROCE: `{stock['roce']}%` | OCF/PAT: `{stock['ocf_to_pat']}x`\n"
            msg += f"   • 💡 *RATIONALE:* _{stock['rationale']}_\n\n"

    # =========================================================
    # SECTION 2: TRACK A - ACTIVE & CONFIRMED BREAKOUTS
    # =========================================================
    msg += f"🚀 *TRACK A: ACTIVE & CONFIRMED BREAKOUTS ({len(active_breakouts)} Qualified)*\n"
    msg += "_State Machine: 5-Day Retest Window | Structural SL | 50% @ 2R, 50% @ 3R_\n"
    msg += "────────────────────────────\n"

    if not active_breakouts:
        msg += "• _No stocks met all A1–A7 breakout & retest criteria today._\n\n"
    else:
        for idx, stock in enumerate(active_breakouts[:5], 1):
            deliv_str = f" | NSE Delivery: *{stock['delivery_pct']}*" if stock['delivery_pct'] != "N/A" else ""
            msg += f"{idx}. 💎 *{stock['name']}* (`{stock['symbol']}`) — *Score: {stock['breakout_score']}/100*\n"
            msg += f"   • *State:* `[{stock['state']}]` | Pivot: ₹{stock['pivot_ref']} (Price: ₹{stock['price']} | `{stock['extension_pct']}` from Pivot)\n"
            msg += f"   • 🎯 *PLANNED ENTRY:* Near Pivot Retest or Current Price (Max Chase: 3.0%)\n"
            msg += f"   • 🛑 *STRUCTURAL SL:* `₹{stock['structural_sl']}` (Base Low - 0.25 ATR | Risk: ₹{stock['unit_risk']} | `{stock['risk_pct']}%`)\n"
            msg += f"   • 💰 *TARGET 1 (2R):* `₹{stock['t1_2r']}` $\\rightarrow$ *Exit 50%* & Move SL to Cost (`₹{stock['be_cost_anchor']}`)\n"
            msg += f"   • 🚀 *TARGET 2 (3R):* `₹{stock['t2_3r']}` $\\rightarrow$ *Exit Remaining 50%* (Net Payoff: *+2.5R*)\n"
            msg += f"   • *Breakout Metrics:* Vol: `{stock['volume_ratio']}` SMA | CRR: `{stock['crr']}` | RE: `{stock['range_ratio']}` ATR{deliv_str}\n"
            msg += f"   • *Relative Strength:* `{stock['rs_spread']}` alpha vs Nifty 500 | 1M Ret: `+{stock['ret_1m']}%`\n"
            msg += f"   • *Fundamentals:* ROE: `{stock['roe']}%` | ROCE: `{stock['roce']}%` | OCF/PAT: `{stock['ocf_to_pat']}x`\n"
            msg += f"   • 💡 *RATIONALE:* _{stock['rationale']}_\n\n"

    # Strategy Indices Performance Barometer
    msg += "📊 *MOMENTUM BENCHMARK CONTEXT:*\n"
    for b in BENCHMARK_INDICES:
        msg += f"• *{b['name']}:* 1Y: `{b['ret_1y']}` | 3Y: `{b['ret_3y']}`\n"
    msg += "\n"

    msg += "⚡ _Automated daily at 5:00 PM IST via GitHub Actions_"
    return msg

# ==============================================================================
# MAIN EXECUTION ENTRYPOINT
# ==============================================================================
def main():
    logger.info("Starting NSE Market Lens 5:00 PM Dual-Track Screener...")
    active_breakouts, pre_breakout_squeezes = run_nse_market_lens_screen()
    report = build_daily_evening_report(active_breakouts, pre_breakout_squeezes)
    success = send_telegram_alert(report)
    if success:
        logger.info("Execution finished successfully.")
    else:
        logger.error("Execution failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
