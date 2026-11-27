"""
Live Sector Rotation, JdK RRG & Constituent Breadth Engine
Computes real daily & weekly JdK RS-Ratio / RS-Momentum trails, multi-timeframe
returns, alpha vs benchmark, market breadth, and live constituent metrics from
official NSE/Yahoo Finance indices and the Nifty 750 universe.
"""

import datetime
import json
import logging
import math
import os
import pandas as pd
import yfinance as yf

logger = logging.getLogger("SectorRotationEngine")

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
CACHE_PATH = os.path.join(DATA_DIR, "sector_rotation.json")

# Official Market Tape tickers
TAPE_TICKERS = {
    "NIFTY_50": "^NSEI",
    "SENSEX": "^BSESN",
    "NIFTY_BANK": "^NSEBANK",
    "INDIA_VIX": "^INDIAVIX",
    "USD_INR": "INR=X",
}

# Official Benchmark & Market-Cap Indices
CAP_INDEX_SPECS = [
    {
        "id": "NIFTY_50",
        "kind": "cap",
        "curated": True,
        "topMover": True,
        "group": "NIFTY 50 (Large Cap)",
        "short": "NIFTY 50",
        "desc": "Large Cap Benchmark",
        "yf": "^NSEI",
        "nse_name": "NIFTY 50",
        "bucket": "Largecap 100",
        "ruler": "Sun / Jupiter",
        "natalNote": "NIFTY Natal (03-Nov-1995): Benchmark large-cap institutional anchor",
    },
    {
        "id": "NIFTY_NEXT50",
        "kind": "cap",
        "curated": True,
        "topMover": False,
        "group": "NIFTY NEXT 50 (Large-Mid)",
        "short": "NEXT 50",
        "desc": "Large-Mid Institutional Leaders",
        "yf": "^NSMIDCP",
        "nse_name": "NIFTY NEXT 50",
        "bucket": "Largecap 100",
        "ruler": "Jupiter / Mercury",
        "natalNote": "Next-rung index heavyweights rotating toward Nifty 50",
    },
    {
        "id": "NIFTY_MID150",
        "kind": "cap",
        "curated": True,
        "topMover": True,
        "group": "NIFTY MIDCAP 150 (Mid Cap)",
        "short": "MIDCAP 150",
        "desc": "Midcap 150 Institutional Growth",
        "yf": "NIFTYMIDCAP150.NS",
        "nse_name": "NIFTY MIDCAP 150",
        "bucket": "Midcap 150",
        "ruler": "Mercury / Mars",
        "natalNote": "High-ROCE midcap momentum leadership tier",
    },
    {
        "id": "NIFTY_SML250",
        "kind": "cap",
        "curated": True,
        "topMover": False,
        "group": "NIFTY SMALLCAP 250 (Small Cap)",
        "short": "SMALLCAP 250",
        "desc": "Smallcap 250 Composite",
        "yf": None,
        "nse_name": "NIFTY SMALLCAP 250",
        "bucket": "Smallcap 250",
        "ruler": "Rahu / Mercury",
        "natalNote": "Selective institutional accumulation in niche smallcaps",
    },
    {
        "id": "NIFTY_MIC250",
        "kind": "cap",
        "curated": True,
        "topMover": False,
        "group": "NIFTY MICROCAP 250",
        "short": "MICROCAP 250",
        "desc": "Microcap 250 Liquidity Composite",
        "yf": None,
        "nse_name": "NIFTY MICROCAP 250",
        "bucket": "Microcap 250",
        "ruler": "Saturn / Ketu",
        "natalNote": "High-beta microcap liquidity & breadth gauge",
    },
]

# NSE Sector Nodes: map official yfinance sector indices + Nifty 750 NSE Industry composites
SECTOR_SPECS = [
    {
        "id": "Financials",
        "curated": True,
        "topMover": True,
        "group": "Financials",
        "short": "FINANCIALS",
        "desc": "Private & PSU Banks, NBFCs & Financial Services",
        "yf": "^NSEBANK",
        "nse_name": "NIFTY FINANCIAL SERVICES",
        "industries": ["Financial Services"],
        "ruler": "Jupiter / Sun",
        "natalNote": "Credit growth & institutional private/PSU banking inflows",
    },
    {
        "id": "PSU Banks",
        "curated": False,
        "topMover": True,
        "group": "PSU Banks",
        "short": "PSU BANKS",
        "desc": "Nifty PSU Bank Index",
        "yf": "^CNXPSUBANK",
        "nse_name": "NIFTY PSU BANK",
        "industries": ["Financial Services"],
        "ruler": "Jupiter / Mars",
        "natalNote": "Public sector bank re-rating & asset quality cycle",
    },
    {
        "id": "Capital Markets",
        "curated": True,
        "topMover": True,
        "group": "Capital Markets",
        "short": "CAP MARKETS",
        "desc": "Exchanges, Depositories, AMCs & Wealth",
        "yf": None,
        "nse_name": "NIFTY CAPITAL MARKETS",
        "industries": ["Financial Services"],
        "tickers_proxy": ["BSE.NS", "CDSL.NS", "MCX.NS", "ANGELONE.NS", "ANANDRATHI.NS", "MOTILALOFS.NS", "CAMS.NS", "KFINTECH.NS", "360ONE.NS", "NUVAMA.NS", "IEX.NS"],
        "ruler": "Mercury / Jupiter",
        "natalNote": "Cash & derivatives ADTO expansion across market venues",
    },
    {
        "id": "IT",
        "curated": True,
        "topMover": True,
        "group": "IT",
        "short": "IT SERVICES",
        "desc": "Large IT, Mid-cap Digital & ER&D Services",
        "yf": "^CNXIT",
        "nse_name": "NIFTY IT",
        "industries": ["Information Technology"],
        "ruler": "Mercury",
        "natalNote": "BFSI & AI deal ramp across Tier-1 and ER&D IT",
    },
    {
        "id": "Auto",
        "curated": True,
        "topMover": True,
        "group": "Auto",
        "short": "AUTO & EV",
        "desc": "2W/EV OEMs, PV/CV & Auto Ancillaries",
        "yf": "^CNXAUTO",
        "nse_name": "NIFTY AUTO",
        "industries": ["Automobile and Auto Components"],
        "ruler": "Venus / Mars",
        "natalNote": "2W/SUV volume leadership & EV ancillary expansion",
    },
    {
        "id": "Telecom",
        "curated": True,
        "topMover": False,
        "group": "Telecom",
        "short": "TELECOM",
        "desc": "Telecom Operators, Towers & CPaaS Platforms",
        "yf": None,
        "nse_name": None,
        "industries": ["Telecommunication"],
        "ruler": "Mercury / Rahu",
        "natalNote": "5G ARPU expansion & enterprise CPaaS platforms",
    },
    {
        "id": "Pharmaceuticals",
        "curated": True,
        "topMover": False,
        "group": "Pharmaceuticals",
        "short": "PHARMA",
        "desc": "Pharma Formulations, CDMO & Healthcare",
        "yf": "^CNXPHARMA",
        "nse_name": "NIFTY PHARMA",
        "industries": ["Healthcare"],
        "ruler": "Sun / Ketu",
        "natalNote": "Specialty pharma, hospitals & CDMO earnings stability",
    },
    {
        "id": "FMCG & Consumer",
        "curated": True,
        "topMover": False,
        "group": "FMCG & Consumer",
        "short": "FMCG & CONS",
        "desc": "Consumer Staples, Retail & Consumption",
        "yf": "^CNXFMCG",
        "nse_name": "NIFTY FMCG",
        "industries": ["Fast Moving Consumer Goods", "Consumer Services"],
        "ruler": "Moon / Venus",
        "natalNote": "Rural staple recovery & organized retail expansion",
    },
    {
        "id": "Consumer Durables",
        "curated": False,
        "topMover": False,
        "group": "Consumer Durables",
        "short": "CONS DURABLES",
        "desc": "EMS, Appliances, Cables & Discretionary",
        "yf": "^CNXCONSUM",
        "nse_name": "NIFTY CONSUMER DURABLES",
        "industries": ["Consumer Durables"],
        "ruler": "Venus / Mercury",
        "natalNote": "EMS manufacturing & discretionary appliance demand",
    },
    {
        "id": "Metals & Mining",
        "curated": True,
        "topMover": True,
        "group": "Metals & Mining",
        "short": "METALS",
        "desc": "Steel, Aluminium, Copper & Mining",
        "yf": "^CNXMETAL",
        "nse_name": "NIFTY METAL",
        "industries": ["Metals & Mining"],
        "ruler": "Saturn / Mars",
        "natalNote": "Global commodity spreads & domestic infra steel demand",
    },
    {
        "id": "Real Estate",
        "curated": False,
        "topMover": False,
        "group": "Real Estate",
        "short": "REAL ESTATE",
        "desc": "Residential Developers & Commercial REITs",
        "yf": "^CNXREALTY",
        "nse_name": "NIFTY REALTY",
        "industries": ["Realty"],
        "ruler": "Mars / Saturn",
        "natalNote": "Premium pre-sales velocity & urban housing cycle",
    },
    {
        "id": "Energy & Power",
        "curated": False,
        "topMover": False,
        "group": "Energy & Power",
        "short": "ENERGY & PWR",
        "desc": "Oil & Gas, Power Generation & Grid Utilities",
        "yf": "^CNXENERGY",
        "nse_name": "NIFTY ENERGY",
        "industries": ["Oil Gas & Consumable Fuels", "Power", "Utilities"],
        "ruler": "Sun / Saturn",
        "natalNote": "Grid transmission capex & energy utilities",
    },
    {
        "id": "Infrastructure",
        "curated": False,
        "topMover": False,
        "group": "Infrastructure",
        "short": "INFRA",
        "desc": "Construction, EPC, Cement & Ports",
        "yf": "^CNXINFRA",
        "nse_name": "NIFTY INFRASTRUCTURE",
        "industries": ["Construction", "Construction Materials"],
        "ruler": "Saturn",
        "natalNote": "Public capex EPC & building material execution",
    },
    {
        "id": "Capital Goods",
        "curated": False,
        "topMover": True,
        "group": "Capital Goods",
        "short": "CAP GOODS",
        "desc": "Electrical Equipment, T&D, Aerospace & Precision Mfg",
        "yf": None,
        "nse_name": None,
        "industries": ["Capital Goods"],
        "ruler": "Saturn / Mars",
        "natalNote": "Industrial electrification, precision forging & defence",
    },
    {
        "id": "Chemicals",
        "curated": False,
        "topMover": False,
        "group": "Chemicals",
        "short": "CHEMICALS",
        "desc": "Specialty & Fluorochemicals",
        "yf": None,
        "nse_name": None,
        "industries": ["Chemicals"],
        "ruler": "Rahu / Venus",
        "natalNote": "Specialty CSM & agrochemical inventory cycle",
    },
    {
        "id": "Services & Logistics",
        "curated": False,
        "topMover": False,
        "group": "Services & Logistics",
        "short": "SERVICES",
        "desc": "Ports, Logistics, Aviation & Commercial Services",
        "yf": None,
        "nse_name": "NIFTY SERVICES SECTOR",
        "industries": ["Services"],
        "ruler": "Mercury / Saturn",
        "natalNote": "Trade logistics, ports & aviation throughput",
    },
    {
        "id": "Textiles",
        "curated": False,
        "topMover": False,
        "group": "Textiles",
        "short": "TEXTILES",
        "desc": "Apparel Exports & Technical Textiles",
        "yf": None,
        "nse_name": None,
        "industries": ["Textiles"],
        "ruler": "Venus",
        "natalNote": "Export garment orderbook & cotton spread recovery",
    },
    {
        "id": "Media & Entertainment",
        "curated": False,
        "topMover": False,
        "group": "Media & Entertainment",
        "short": "MEDIA",
        "desc": "Broadcasting, Music IP & Digital Media",
        "yf": None,
        "nse_name": "NIFTY MEDIA",
        "industries": ["Media Entertainment & Publication"],
        "ruler": "Venus / Mercury",
        "natalNote": "Digital licensing & media monetization cycle",
    },
]

# Default baseline data for the 24 curated equities (prices, technicals & RRG updated live)
CURATED_STOCK_BASE = [
    {"ticker": "ICICIBANK", "name": "ICICI Bank Ltd", "sector": "Financials", "capTier": "NIFTY_50", "desc": "Private Sector Bank L1", "price": 1632.50, "chg": 2.96, "atr14": 28.5, "dma20": 1605.0, "dma150": 1485.0, "swingLow": 1548.0, "fwdPe": 20.06, "secPe": 18.5, "peg": 1.09, "epsCagr": 18.5, "roe": 18.2, "roce": 18.2, "valMethod": "P/B-ROE Gordon Growth", "fairValue": 1860, "verdict": "UNDERVALUED", "stage": "Stage 2A (Breakout)", "fiiQoq": 0.85, "diiQoq": 0.32, "mfNetCr": 1940, "netInstCr": 6270, "smScore": 94, "smRegime": "Accumulating (FII+DII+MF)", "angle": 26, "radius": 111, "ipoNatal": "17-Sep-1997 | Jupiter 5H trine natal Meena Moon; Merc Direct fee income", "assigned": "Vina", "isCore": True, "isSwing": True, "cap": 18, "entry": "1589-1630", "sl": 1505, "t1": 1711, "t2": 1820, "base": 1860, "bull": 1980, "kpiStop": "ROA < 1.8% or GNPA > 2.4%"},
    {"ticker": "HDFCBANK", "name": "HDFC Bank Ltd", "sector": "Financials", "capTier": "NIFTY_50", "desc": "Private Sector Bank L1", "price": 843.10, "chg": 3.09, "atr14": 15.2, "dma20": 794.0, "dma150": 752.0, "swingLow": 738.0, "fwdPe": 16.25, "secPe": 18.5, "peg": 0.98, "epsCagr": 16.5, "roe": 17.5, "roce": 17.5, "valMethod": "P/B-ROE Gordon Growth", "fairValue": 945, "verdict": "UNDERVALUED", "stage": "Stage 2A (Base Turn)", "fiiQoq": 1.15, "diiQoq": -0.40, "mfNetCr": 1120, "netInstCr": 4590, "smScore": 86, "smRegime": "FII + MF Accumulation", "angle": 35, "radius": 106, "ipoNatal": "19-May-1995 | Jupiter 4H Kendra stabilizes CD ratio; FII inflows", "assigned": "Vina", "isCore": True, "isSwing": False, "cap": 10, "entry": "775-798", "sl": 715, "t1": 875, "t2": 925, "base": 945, "bull": 1020, "kpiStop": "NIM < 3.05% for 2 Qtrs"},
    {"ticker": "INDIANB", "name": "Indian Bank", "sector": "PSU Banks", "capTier": "NIFTY_MID150", "desc": "Public Sector Bank L2", "price": 920.50, "chg": -1.34, "atr14": 21.0, "dma20": 938.0, "dma150": 842.0, "swingLow": 900.0, "fwdPe": 9.39, "secPe": 11.0, "peg": 0.44, "epsCagr": 22.0, "roe": 16.8, "roce": 16.8, "valMethod": "P/B-ROE Gordon Growth", "fairValue": 1165, "verdict": "UNDERVALUED", "stage": "Stage 2B (Momentum)", "fiiQoq": 0.52, "diiQoq": 0.48, "mfNetCr": 680, "netInstCr": 1620, "smScore": 91, "smRegime": "Accumulating (FII+DII+MF)", "angle": 20, "radius": 113, "ipoNatal": "01-Mar-2007 | Jupiter + Mars 2H wealth house; pristine asset quality", "assigned": "Vina", "isCore": True, "isSwing": True, "cap": 14, "entry": "925-958", "sl": 868, "t1": 1015, "t2": 1110, "base": 1165, "bull": 1280, "kpiStop": "NNPA > 0.35%"},
    {"ticker": "BSE", "name": "BSE Limited", "sector": "Capital Markets", "capTier": "NIFTY_MID150", "desc": "Asia's Oldest Stock Exchange L1", "price": 3772.00, "chg": 0.40, "atr14": 95.0, "dma20": 3680.0, "dma150": 3190.0, "swingLow": 3632.0, "fwdPe": 50.51, "secPe": 42.0, "peg": 1.06, "epsCagr": 42.0, "roe": 46.0, "roce": 52.4, "valMethod": "Forward P/E + PEG", "fairValue": 4445, "verdict": "GROWTH PREMIUM / GARP", "stage": "Stage 2B (Breakout)", "fiiQoq": 1.48, "diiQoq": 0.76, "mfNetCr": 1180, "netInstCr": 2740, "smScore": 95, "smRegime": "Accumulating (FII+DII+MF)", "angle": 18, "radius": 115, "ipoNatal": "03-Feb-2017 | Jupiter Leo 5H trine natal Mesha Moon; Merc Direct ADTO", "assigned": "Kritika", "isCore": True, "isSwing": True, "cap": 15, "entry": "3712-3780", "sl": 3490, "t1": 4150, "t2": 4445, "base": 4445, "bull": 4800, "kpiStop": "Options ADTO -15% QoQ"},
    {"ticker": "NSE", "name": "NSE India Ltd", "sector": "Capital Markets", "capTier": "NIFTY_NEXT50", "desc": "India's Premier Market Venue L1", "price": 2307.00, "chg": 4.43, "atr14": 48.0, "dma20": 2145.0, "dma150": 1920.0, "swingLow": 1822.0, "fwdPe": 52.09, "secPe": 42.0, "peg": 1.24, "epsCagr": 34.0, "roe": 46.0, "roce": 54.0, "valMethod": "Forward P/E + PEG", "fairValue": 2540, "verdict": "FAIRLY VALUED", "stage": "Stage 2A (Accumulation)", "fiiQoq": 0.92, "diiQoq": 0.38, "mfNetCr": 1540, "netInstCr": 4070, "smScore": 90, "smRegime": "Accumulating (FII+DII+MF)", "angle": 24, "radius": 112, "ipoNatal": "04-Nov-1994 | Mercury Direct transiting natal Tula Sun drives volumes", "assigned": "Kritika", "isCore": True, "isSwing": False, "cap": 10, "entry": "1950-2080", "sl": 1750, "t1": 2380, "t2": 2540, "base": 2540, "bull": 2750, "kpiStop": "Anchor Unlock Supply Dip"},
    {"ticker": "BHARTIARTL", "name": "Bharti Airtel Ltd", "sector": "Telecom", "capTier": "NIFTY_50", "desc": "Telecom Core Operator L1", "price": 2117.80, "chg": -0.50, "atr14": 34.0, "dma20": 2125.0, "dma150": 1940.0, "swingLow": 2061.0, "fwdPe": 41.64, "secPe": 31.0, "peg": 1.18, "epsCagr": 28.5, "roe": 16.8, "roce": 15.4, "valMethod": "EV/EBITDA + DCF", "fairValue": 2490, "verdict": "GROWTH PREMIUM / GARP", "stage": "Stage 2A (Uptrend)", "fiiQoq": 0.64, "diiQoq": 0.29, "mfNetCr": 1410, "netInstCr": 3820, "smScore": 89, "smRegime": "Accumulating (FII+DII+MF)", "angle": 39, "radius": 105, "ipoNatal": "18-Feb-2002 | Rahu Aquarius over natal Sun accelerates 5G ARPU cycle", "assigned": "Kritika", "isCore": True, "isSwing": True, "cap": 14, "entry": "2109-2155", "sl": 2010, "t1": 2320, "t2": 2480, "base": 2490, "bull": 2980, "kpiStop": "India ARPU < ₹265"},
    {"ticker": "TANLA", "name": "Tanla Platforms Ltd", "sector": "Telecom", "capTier": "NIFTY_SML250", "desc": "Enterprise CPaaS Platform L3", "price": 647.35, "chg": -4.87, "atr14": 18.0, "dma20": 655.0, "dma150": 590.0, "swingLow": 645.0, "fwdPe": 15.45, "secPe": 26.0, "peg": 0.75, "epsCagr": 21.8, "roe": 26.3, "roce": 31.2, "valMethod": "Forward P/E + PEG", "fairValue": 860, "verdict": "UNDERVALUED", "stage": "Stage 2A (Re-Rating)", "fiiQoq": 0.44, "diiQoq": 0.35, "mfNetCr": 210, "netInstCr": 480, "smScore": 84, "smRegime": "Accumulating (FII+DII+MF)", "angle": 47, "radius": 103, "ipoNatal": "05-Jan-2007 | Mercury 4H Kendra + Jupiter 2H favors CPaaS margins", "assigned": "Kritika", "isCore": True, "isSwing": True, "cap": 10, "entry": "642-678", "sl": 618, "t1": 760, "t2": 860, "base": 860, "bull": 980, "kpiStop": "Platform OPM < 22%"},
    {"ticker": "INDUSTOWER", "name": "Indus Towers Ltd", "sector": "Telecom", "capTier": "NIFTY_MID150", "desc": "Telecom Tower Infrastructure L1", "price": 378.45, "chg": -0.47, "atr14": 9.5, "dma20": 381.0, "dma150": 348.0, "swingLow": 370.0, "fwdPe": 14.04, "secPe": 18.0, "peg": 0.78, "epsCagr": 18.4, "roe": 31.0, "roce": 24.5, "valMethod": "EV/EBITDA + DCF", "fairValue": 448, "verdict": "UNDERVALUED", "stage": "Stage 2A (Yield Base)", "fiiQoq": 0.31, "diiQoq": -0.18, "mfNetCr": 145, "netInstCr": 290, "smScore": 78, "smRegime": "FII + MF Accumulation", "angle": 56, "radius": 101, "ipoNatal": "28-Dec-2012 | Mercury trine natal Mithuna Moon supports FCF recovery", "assigned": "Kritika", "isCore": True, "isSwing": False, "cap": 8, "entry": "376-386", "sl": 356, "t1": 425, "t2": 448, "base": 448, "bull": 480, "kpiStop": "Tenancy Ratio -5%"},
    {"ticker": "LTTS", "name": "L&T Technology Services", "sector": "IT", "capTier": "NIFTY_MID150", "desc": "Engineering R&D Services L3", "price": 4185.90, "chg": -0.87, "atr14": 88.0, "dma20": 4050.0, "dma150": 3780.0, "swingLow": 3972.0, "fwdPe": 28.87, "secPe": 28.5, "peg": 1.35, "epsCagr": 21.5, "roe": 26.7, "roce": 32.8, "valMethod": "Forward P/E + PEG", "fairValue": 4750, "verdict": "GROWTH PREMIUM / GARP", "stage": "Stage 2B (Breakout)", "fiiQoq": 0.56, "diiQoq": 0.31, "mfNetCr": 410, "netInstCr": 930, "smScore": 88, "smRegime": "Accumulating (FII+DII+MF)", "angle": 106, "radius": 104, "ipoNatal": "23-Sep-2016 | Mercury Direct Swati 2H strengthens ER&D mobility deals", "assigned": "Kritika", "isCore": False, "isSwing": True, "cap": 12, "entry": "4035-4105", "sl": 3840, "t1": 4410, "t2": 4750, "base": 4750, "bull": 5100, "kpiStop": "CC Rev Growth < 10%"},
    {"ticker": "COFORGE", "name": "Coforge Limited", "sector": "IT", "capTier": "NIFTY_MID150", "desc": "Mid-Cap Digital IT Leader L2", "price": 2066.60, "chg": -3.53, "atr14": 54.0, "dma20": 2045.0, "dma150": 1840.0, "swingLow": 2016.0, "fwdPe": 37.61, "secPe": 32.0, "peg": 1.25, "epsCagr": 28.6, "roe": 23.5, "roce": 27.4, "valMethod": "Forward P/E + PEG", "fairValue": 2580, "verdict": "GROWTH PREMIUM / GARP", "stage": "Stage 2B (Leadership)", "fiiQoq": 1.35, "diiQoq": 0.48, "mfNetCr": 890, "netInstCr": 2100, "smScore": 93, "smRegime": "Accumulating (FII+DII+MF)", "angle": 100, "radius": 106, "ipoNatal": "30-Aug-2004 | Jupiter + Mars over natal Simha Sun ignites deal TCV", "assigned": "Kritika", "isCore": True, "isSwing": True, "cap": 15, "entry": "2026-2135", "sl": 1935, "t1": 2350, "t2": 2580, "base": 2580, "bull": 2850, "kpiStop": "Adj. EBIT < 15.0%"},
    {"ticker": "TECHM", "name": "Tech Mahindra Ltd", "sector": "IT", "capTier": "NIFTY_50", "desc": "IT Margin Turnaround L1", "price": 1790.90, "chg": 0.75, "atr14": 32.0, "dma20": 1720.0, "dma150": 1560.0, "swingLow": 1693.0, "fwdPe": 28.84, "secPe": 26.0, "peg": 1.04, "epsCagr": 24.0, "roe": 16.2, "roce": 19.8, "valMethod": "Forward P/E + PEG", "fairValue": 2110, "verdict": "UNDERVALUED", "stage": "Stage 2A (Turnaround)", "fiiQoq": 0.88, "diiQoq": -0.25, "mfNetCr": 390, "netInstCr": 900, "smScore": 83, "smRegime": "FII + MF Accumulation", "angle": 114, "radius": 101, "ipoNatal": "28-Aug-2006 | Mercury Direct over natal Tula Moon accelerates Fortius", "assigned": "Kritika", "isCore": False, "isSwing": True, "cap": 10, "entry": "1693-1765", "sl": 1645, "t1": 1880, "t2": 2110, "base": 2110, "bull": 2350, "kpiStop": "EBIT Trajectory < 14.5%"},
    {"ticker": "HCLTECH", "name": "HCL Technologies Ltd", "sector": "IT", "capTier": "NIFTY_50", "desc": "Large Cap IT Yield L1", "price": 1367.10, "chg": 0.21, "atr14": 26.0, "dma20": 1340.0, "dma150": 1245.0, "swingLow": 1239.0, "fwdPe": 20.27, "secPe": 25.5, "peg": 1.27, "epsCagr": 15.8, "roe": 24.8, "roce": 30.2, "valMethod": "Forward P/E + PEG", "fairValue": 1620, "verdict": "UNDERVALUED", "stage": "Stage 2A (Accumulation)", "fiiQoq": 0.42, "diiQoq": -0.10, "mfNetCr": 510, "netInstCr": 1180, "smScore": 81, "smRegime": "FII + MF Accumulation", "angle": 122, "radius": 100, "ipoNatal": "11-Jan-2000 | Jupiter 7H aspect supports stable Tier-1 software renewals", "assigned": "Kritika", "isCore": True, "isSwing": False, "cap": 8, "entry": "1327-1355", "sl": 1200, "t1": 1500, "t2": 1620, "base": 1620, "bull": 1780, "kpiStop": "EBIT Margin < 17.0%"},
    {"ticker": "BAJAJ-AUTO", "name": "Bajaj Auto Ltd", "sector": "Auto", "capTier": "NIFTY_50", "desc": "2W/EV & Export Cash Cow L3", "price": 10768.00, "chg": 1.17, "atr14": 210.0, "dma20": 10660.0, "dma150": 9680.0, "swingLow": 10335.0, "fwdPe": 23.01, "secPe": 24.5, "peg": 1.06, "epsCagr": 21.5, "roe": 29.2, "roce": 36.5, "valMethod": "EV/EBITDA + DCF", "fairValue": 13200, "verdict": "UNDERVALUED", "stage": "Stage 2B (Leadership)", "fiiQoq": 0.54, "diiQoq": 0.36, "mfNetCr": 940, "netInstCr": 2130, "smScore": 92, "smRegime": "Accumulating (FII+DII+MF)", "angle": 92, "radius": 105, "ipoNatal": "26-May-2008 | Venus/Mars synergy fuels Chetak EV + CNG export margins", "assigned": "Kritika", "isCore": True, "isSwing": True, "cap": 14, "entry": "10649-10880", "sl": 10020, "t1": 11850, "t2": 12850, "base": 13200, "bull": 14600, "kpiStop": "OPM < 19.0%"},
    {"ticker": "TVSMOTOR", "name": "TVS Motor Company", "sector": "Auto", "capTier": "NIFTY_NEXT50", "desc": "2W/EV Growth Compounder L3", "price": 4616.60, "chg": 1.95, "atr14": 92.0, "dma20": 4595.0, "dma150": 4120.0, "swingLow": 4518.0, "fwdPe": 57.28, "secPe": 26.0, "peg": 1.38, "epsCagr": 28.4, "roe": 33.6, "roce": 29.8, "valMethod": "EV/EBITDA + DCF", "fairValue": 5250, "verdict": "GROWTH PREMIUM / GARP", "stage": "Stage 2B (Momentum)", "fiiQoq": 0.41, "diiQoq": 0.22, "mfNetCr": 520, "netInstCr": 1130, "smScore": 87, "smRegime": "Accumulating (FII+DII+MF)", "angle": 98, "radius": 103, "ipoNatal": "12-Aug-1982 | Jupiter 5H trine natal Mesha Moon supports 2W share gains", "assigned": "Kritika", "isCore": False, "isSwing": True, "cap": 9, "entry": "4590-4650", "sl": 4380, "t1": 4950, "t2": 5250, "base": 5250, "bull": 5800, "kpiStop": "ROE < 30%"},
    {"ticker": "M&M", "name": "Mahindra & Mahindra", "sector": "Auto", "capTier": "NIFTY_50", "desc": "SUV, EV & Tractor Leader L2", "price": 3482.10, "chg": -0.15, "atr14": 68.0, "dma20": 3350.0, "dma150": 3010.0, "swingLow": 3152.0, "fwdPe": 20.19, "secPe": 24.5, "peg": 0.87, "epsCagr": 24.8, "roe": 23.5, "roce": 25.1, "valMethod": "EV/EBITDA + DCF", "fairValue": 4250, "verdict": "UNDERVALUED", "stage": "Stage 2A (Accumulation)", "fiiQoq": 0.78, "diiQoq": 0.14, "mfNetCr": 1150, "netInstCr": 2630, "smScore": 91, "smRegime": "Accumulating (FII+DII+MF)", "angle": 88, "radius": 106, "ipoNatal": "03-Jan-1956 | Jupiter + Mars on natal Simha Moon powers SUV dominance", "assigned": "Kritika", "isCore": True, "isSwing": False, "cap": 10, "entry": "3240-3380", "sl": 3050, "t1": 3950, "t2": 4250, "base": 4250, "bull": 4650, "kpiStop": "Auto PBIT < 7.5%"},
    {"ticker": "UNOMINDA", "name": "Uno Minda Limited", "sector": "Auto", "capTier": "NIFTY_MID150", "desc": "EV Sensor & Lighting Ancillary L1", "price": 1375.00, "chg": 1.33, "atr14": 34.0, "dma20": 1330.0, "dma150": 1185.0, "swingLow": 1191.0, "fwdPe": 58.64, "secPe": 30.0, "peg": 1.46, "epsCagr": 25.0, "roe": 19.5, "roce": 21.4, "valMethod": "EV/EBITDA + DCF", "fairValue": 1580, "verdict": "FAIRLY VALUED", "stage": "Stage 2A (Base Breakout)", "fiiQoq": 0.34, "diiQoq": 0.45, "mfNetCr": 340, "netInstCr": 730, "smScore": 82, "smRegime": "Accumulating (FII+DII+MF)", "angle": 105, "radius": 101, "ipoNatal": "12-Aug-1996 | Mercury 5H trine natal Moon boosts EV kit content", "assigned": "Kritika", "isCore": True, "isSwing": False, "cap": 7, "entry": "1295-1345", "sl": 1140, "t1": 1510, "t2": 1580, "base": 1580, "bull": 1750, "kpiStop": "OPM < 10.0%"},
    {"ticker": "HAPPYFORGE", "name": "Happy Forgings Ltd", "sector": "Capital Goods", "capTier": "NIFTY_SML250", "desc": "Heavy Forging & Machining L2", "price": 1766.10, "chg": -0.16, "atr14": 42.0, "dma20": 1795.0, "dma150": 1620.0, "swingLow": 1748.0, "fwdPe": 47.49, "secPe": 36.0, "peg": 1.45, "epsCagr": 26.5, "roe": 20.5, "roce": 24.8, "valMethod": "Forward P/E + PEG", "fairValue": 2150, "verdict": "GROWTH PREMIUM / GARP", "stage": "Stage 2A (Pullback Buy)", "fiiQoq": 0.38, "diiQoq": 0.62, "mfNetCr": 245, "netInstCr": 475, "smScore": 85, "smRegime": "Accumulating (FII+DII+MF)", "angle": 116, "radius": 101, "ipoNatal": "27-Dec-2023 | Saturn 10H Karmic expansion supports export machining", "assigned": "Vina", "isCore": False, "isSwing": True, "cap": 8, "entry": "1770-1815", "sl": 1685, "t1": 2050, "t2": 2180, "base": 2150, "bull": 2450, "kpiStop": "OPM < 27.0%"},
    {"ticker": "UNIMECH", "name": "Unimech Aerospace", "sector": "Capital Goods", "capTier": "NIFTY_SML250", "desc": "Aero-Engine & Nuclear Tooling L3", "price": 1733.00, "chg": -0.98, "atr14": 48.0, "dma20": 1805.0, "dma150": 1590.0, "swingLow": 1747.0, "fwdPe": 100.15, "secPe": 44.0, "peg": 1.18, "epsCagr": 42.0, "roe": 25.8, "roce": 31.5, "valMethod": "Forward P/E + PEG", "fairValue": 2180, "verdict": "GROWTH PREMIUM / GARP", "stage": "Stage 2A (Accumulation)", "fiiQoq": 0.55, "diiQoq": 0.42, "mfNetCr": 195, "netInstCr": 415, "smScore": 86, "smRegime": "Accumulating (FII+DII+MF)", "angle": 122, "radius": 102, "ipoNatal": "31-Dec-2024 | Jupiter 9H fortune trine activates aero tooling exports", "assigned": "Vina", "isCore": True, "isSwing": False, "cap": 7, "entry": "1775-1820", "sl": 1675, "t1": 2025, "t2": 2180, "base": 2180, "bull": 2480, "kpiStop": "OPM < 32.0%"},
    {"ticker": "MTARTECH", "name": "MTAR Technologies", "sector": "Capital Goods", "capTier": "NIFTY_SML250", "desc": "Nuclear & Clean Energy Engg L3", "price": 5517.00, "chg": -2.51, "atr14": 165.0, "dma20": 5420.0, "dma150": 4890.0, "swingLow": 4968.0, "fwdPe": 89.78, "secPe": 45.0, "peg": 1.88, "epsCagr": 34.0, "roe": 18.5, "roce": 21.0, "valMethod": "Forward P/E + PEG", "fairValue": 6450, "verdict": "RICH / STAGGERED BUY", "stage": "Stage 1B (Staggered Base)", "fiiQoq": 0.24, "diiQoq": -0.35, "mfNetCr": 65, "netInstCr": -20, "smScore": 68, "smRegime": "Early Rotation", "angle": 132, "radius": 98, "ipoNatal": "15-Mar-2021 | Saturn Rx over natal Moon; nuclear orderbook underpins base", "assigned": "Vina", "isCore": True, "isSwing": False, "cap": 6, "entry": "5150-5450", "sl": 4720, "t1": 6150, "t2": 6450, "base": 6450, "bull": 7740, "kpiStop": "Operating Cash Flow < 0"},
    {"ticker": "BEL", "name": "Bharat Electronics Ltd", "sector": "Capital Goods", "capTier": "NIFTY_50", "desc": "Defence Radar & Avionics L1", "price": 318.40, "chg": 0.45, "atr14": 7.8, "dma20": 312.0, "dma150": 294.0, "swingLow": 292.0, "fwdPe": 36.2, "secPe": 38.0, "peg": 1.48, "epsCagr": 24.5, "roe": 26.8, "roce": 34.2, "valMethod": "Forward P/E + PEG", "fairValue": 375, "verdict": "FAIRLY VALUED", "stage": "Stage 2A (Base Building)", "fiiQoq": 0.28, "diiQoq": -0.15, "mfNetCr": 420, "netInstCr": 540, "smScore": 79, "smRegime": "FII + MF Accumulation", "angle": 176, "radius": 99, "ipoNatal": "19-Jul-2000 | Mars Leo 10H backs indigenous defence electronics orders", "assigned": "Vina", "isCore": False, "isSwing": False, "cap": 5, "entry": "302-316", "sl": 280, "t1": 352, "t2": 375, "base": 375, "bull": 415, "kpiStop": "Order Inflow < ₹22,000 Cr"},
    {"ticker": "SUNPHARMA", "name": "Sun Pharmaceutical Ind", "sector": "Pharmaceuticals", "capTier": "NIFTY_50", "desc": "Specialty & US Generics L1", "price": 1842.00, "chg": 0.62, "atr14": 29.0, "dma20": 1825.0, "dma150": 1710.0, "swingLow": 1740.0, "fwdPe": 32.4, "secPe": 31.0, "peg": 1.62, "epsCagr": 20.0, "roe": 18.4, "roce": 22.1, "valMethod": "Forward P/E + PEG", "fairValue": 2080, "verdict": "FAIRLY VALUED", "stage": "Stage 2B (Defensive Hold)", "fiiQoq": 0.22, "diiQoq": 0.34, "mfNetCr": 610, "netInstCr": 1290, "smScore": 81, "smRegime": "Accumulating (FII+DII+MF)", "angle": 298, "radius": 103, "ipoNatal": "29-Nov-1994 | Sun Anuradha stabilizes global specialty dermatology franchise", "assigned": "Vina", "isCore": False, "isSwing": False, "cap": 5, "entry": "1790-1835", "sl": 1695, "t1": 1965, "t2": 2080, "base": 2080, "bull": 2260, "kpiStop": "US Specialty Growth < 12%"},
    {"ticker": "NTPC", "name": "NTPC Limited", "sector": "Energy & Power", "capTier": "NIFTY_50", "desc": "Thermal & Green Utility L1", "price": 412.50, "chg": -0.48, "atr14": 8.5, "dma20": 418.0, "dma150": 388.0, "swingLow": 386.0, "fwdPe": 16.8, "secPe": 18.0, "peg": 1.29, "epsCagr": 13.0, "roe": 13.8, "roce": 11.4, "valMethod": "EV/EBITDA + DCF", "fairValue": 468, "verdict": "UNDERVALUED", "stage": "Stage 2A (Utility Base)", "fiiQoq": -0.14, "diiQoq": 0.42, "mfNetCr": 530, "netInstCr": 790, "smScore": 74, "smRegime": "DII + MF Absorption", "angle": 224, "radius": 93, "ipoNatal": "05-Nov-2004 | Saturn-Sun regulated ROE model cushions power digestion", "assigned": "Vina", "isCore": False, "isSwing": False, "cap": 5, "entry": "396-410", "sl": 372, "t1": 445, "t2": 468, "base": 468, "bull": 510, "kpiStop": "Regulated Equity < 15%"},
    {"ticker": "ABB", "name": "ABB India Limited", "sector": "Capital Goods", "capTier": "NIFTY_NEXT50", "desc": "Electrification & Robotics L1", "price": 7840.00, "chg": -0.55, "atr14": 185.0, "dma20": 7960.0, "dma150": 7320.0, "swingLow": 7380.0, "fwdPe": 68.5, "secPe": 55.0, "peg": 2.28, "epsCagr": 30.0, "roe": 24.2, "roce": 32.0, "valMethod": "Forward P/E + PEG", "fairValue": 8450, "verdict": "RICH / STAGGERED BUY", "stage": "Stage 2B (Consolidation)", "fiiQoq": -0.28, "diiQoq": -0.19, "mfNetCr": -180, "netInstCr": -640, "smScore": 62, "smRegime": "Institutional Profit-Booking", "angle": 328, "radius": 98, "ipoNatal": "08-Feb-1995 | Digesting multiple expansion while industrial orders hold", "assigned": "Vina", "isCore": False, "isSwing": False, "cap": 4, "entry": "7420-7680", "sl": 7100, "t1": 8180, "t2": 8450, "base": 8450, "bull": 9200, "kpiStop": "Base Order Growth < 10%"},
    {"ticker": "TRENT", "name": "Trent Limited", "sector": "FMCG & Consumer", "capTier": "NIFTY_50", "desc": "Zudio & Westside Retail L1", "price": 6920.00, "chg": 1.05, "atr14": 160.0, "dma20": 6780.0, "dma150": 6150.0, "swingLow": 6480.0, "fwdPe": 78.0, "secPe": 58.0, "peg": 1.85, "epsCagr": 42.0, "roe": 31.5, "roce": 36.8, "valMethod": "EV/EBITDA + DCF", "fairValue": 7850, "verdict": "GROWTH PREMIUM / GARP", "stage": "Stage 2B (Uptrend)", "fiiQoq": 0.35, "diiQoq": 0.22, "mfNetCr": 490, "netInstCr": 1060, "smScore": 84, "smRegime": "Accumulating (FII+DII+MF)", "angle": 346, "radius": 101, "ipoNatal": "07-Jun-2004 | Venus + Jupiter 5H drives Zudio store rollout velocity", "assigned": "Kritika", "isCore": False, "isSwing": False, "cap": 5, "entry": "6650-6880", "sl": 6240, "t1": 7420, "t2": 7850, "base": 7850, "bull": 8600, "kpiStop": "LFL Same-Store Growth < 8%"},
]


def _normalize_series_index(s: pd.Series) -> pd.Series:
    """Strip timezone and normalize index to date so cross-ticker alignment is exact."""
    s = s.dropna().copy()
    if s.empty:
        return s
    idx = pd.to_datetime(s.index)
    if idx.tz is not None:
        idx = idx.tz_localize(None)
    s.index = idx.normalize()
    s = s[~s.index.duplicated(keep="last")].sort_index()
    return s


def compute_jdk_rrg_trail(price_series: pd.Series, bench_series: pd.Series, is_weekly: bool = False, tail_len: int = 16):
    """
    Computes genuine JdK RS-Ratio and RS-Momentum relative to benchmark.
    Returns (angle, radius, trail_points) where trail_points is a list of {x, y}
    centered around 0 (i.e. RS-Ratio - 100, RS-Momentum - 100).
    """
    p = _normalize_series_index(price_series)
    b = _normalize_series_index(bench_series)
    df = pd.concat([p.rename("p"), b.rename("b")], axis=1).dropna()
    if len(df) < 40:
        return None

    if is_weekly:
        df = df.resample("W-FRI").last().dropna()
        if len(df) < 22:
            return None
        short_span, long_span, z_win, mom_lag = 6, 14, 26, 4
    else:
        short_span, long_span, z_win, mom_lag = 10, 26, 63, 5

    rs = (df["p"] / df["b"]) * 100.0
    rs_fast = rs.ewm(span=short_span, adjust=False).mean()
    rs_slow = rs.ewm(span=long_span, adjust=False).mean()
    rs_trend = ((rs_fast / rs_slow) - 1.0) * 100.0

    roll_mean = rs_trend.rolling(z_win, min_periods=max(12, z_win // 2)).mean()
    roll_std = rs_trend.rolling(z_win, min_periods=max(12, z_win // 2)).std().replace(0, pd.NA)
    z_ratio = ((rs_trend - roll_mean) / roll_std).fillna(0.0).clip(-3.5, 3.5)
    jdk_ratio = 100.0 + z_ratio * 3.8

    mom_raw = jdk_ratio.diff(mom_lag).fillna(0.0)
    mom_smooth = mom_raw.ewm(span=max(3, mom_lag), adjust=False).mean()
    mom_mean = mom_smooth.rolling(z_win, min_periods=max(12, z_win // 2)).mean()
    mom_std = mom_smooth.rolling(z_win, min_periods=max(12, z_win // 2)).std().replace(0, pd.NA)
    z_mom = ((mom_smooth - mom_mean) / mom_std).fillna(0.0).clip(-3.5, 3.5)
    jdk_mom = 100.0 + z_mom * 3.8

    tail_df = pd.DataFrame({"x": jdk_ratio - 100.0, "y": jdk_mom - 100.0}).dropna().tail(tail_len)
    if tail_df.empty:
        return None

    pts = [{"x": round(float(r.x), 2), "y": round(float(r.y), 2)} for r in tail_df.itertuples()]
    hx, hy = pts[-1]["x"], pts[-1]["y"]
    angle = (math.degrees(math.atan2(hy, hx)) + 360.0) % 360.0
    radius = 100.0 + math.hypot(hx, hy)
    return round(angle, 1), round(radius, 2), pts


def _compute_period_returns(series: pd.Series):
    """Computes 1D, 1W, 1M, 3M, 1Y percentage returns from a daily close series."""
    s = _normalize_series_index(series)
    if len(s) < 2:
        return {"d1": 0.0, "w1": 0.0, "m1": 0.0, "m3": 0.0, "y1": 0.0, "last": 0.0}

    last = float(s.iloc[-1])

    def pct_back(bars):
        idx = max(0, len(s) - 1 - bars)
        prev = float(s.iloc[idx])
        return round(((last - prev) / prev) * 100.0, 2) if prev > 0 else 0.0

    return {
        "d1": pct_back(1),
        "w1": pct_back(5),
        "m1": pct_back(21),
        "m3": pct_back(63),
        "y1": pct_back(min(len(s) - 1, 252)),
        "last": round(last, 2),
    }


def _build_equal_weight_series(symbols, all_hist):
    """Builds an equal-weight normalized price composite (base=100) from member tickers."""
    ret_cols = []
    for sym in symbols:
        df = all_hist.get(sym)
        if df is None or len(df) < 30:
            continue
        c = _normalize_series_index(df["Close"])
        r = c.pct_change().dropna()
        if not r.empty:
            ret_cols.append(r.rename(sym))
    if not ret_cols:
        return pd.Series(dtype=float)
    mat = pd.concat(ret_cols, axis=1)
    mean_ret = mat.mean(axis=1, skipna=True).fillna(0.0)
    idx_series = (1.0 + mean_ret).cumprod() * 100.0
    return idx_series


def _fetch_yf_batch(tickers):
    """Downloads 2Y daily history for a list of Yahoo Finance index/stock tickers."""
    out = {}
    unique = sorted(set(t for t in tickers if t))
    if not unique:
        return out
    try:
        data = yf.download(unique, period="2y", group_by="ticker", threads=True, progress=False)
        for t in unique:
            try:
                if isinstance(data.columns, pd.MultiIndex):
                    if t in data.columns.levels[0]:
                        df_t = data[t].dropna(subset=["Close"])
                        if len(df_t) >= 5:
                            out[t] = df_t
                elif not data.empty:
                    df_t = data.dropna(subset=["Close"])
                    if len(df_t) >= 5:
                        out[t] = df_t
            except Exception:
                pass
    except Exception as e:
        logger.warning(f"Sector Rotation yf.download batch warning: {e}")
    return out


def _fetch_nse_live_snapshots(nse_session):
    """Optionally fetches live NSE allIndices and latest daily FII/DII cash stats."""
    indices_map = {}
    fii_dii = None
    if not nse_session:
        return indices_map, fii_dii
    try:
        r = nse_session.get("https://www.nseindia.com/api/allIndices", timeout=8)
        if r.status_code == 200:
            for row in r.json().get("data", []):
                name = row.get("index")
                if name:
                    indices_map[name.upper()] = row
    except Exception as e:
        logger.debug(f"NSE allIndices optional fetch skipped: {e}")

    try:
        r2 = nse_session.get("https://www.nseindia.com/api/fiidiiTradeReact", timeout=8)
        if r2.status_code == 200:
            rows = r2.json()
            parsed = {}
            for row in rows:
                cat = str(row.get("category", "")).upper()
                net = float(str(row.get("netValue", "0")).replace(",", ""))
                dt = row.get("date", "")
                if "FII" in cat or "FPI" in cat:
                    parsed["fii"] = net
                    parsed["date"] = dt
                elif "DII" in cat:
                    parsed["dii"] = net
            if parsed:
                fii_dii = parsed
    except Exception as e:
        logger.debug(f"NSE fiidiiTradeReact optional fetch skipped: {e}")

    return indices_map, fii_dii


def _stock_technicals_from_hist(hist_df):
    """Computes ATR(14), 20-DMA, 150-DMA, 20D Swing Low, and latest Close/Chg."""
    if hist_df is None or len(hist_df) < 22:
        return None
    df = hist_df.dropna(subset=["Close"]).copy()
    close = df["Close"]
    high = df["High"]
    low = df["Low"]
    last = float(close.iloc[-1])
    prev = float(close.iloc[-2]) if len(close) >= 2 else last
    chg = round(((last - prev) / prev) * 100.0, 2) if prev > 0 else 0.0

    tr1 = high - low
    tr2 = (high - close.shift(1)).abs()
    tr3 = (low - close.shift(1)).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr14 = float(tr.rolling(14, min_periods=5).mean().iloc[-1])
    dma20 = float(close.rolling(20, min_periods=10).mean().iloc[-1])
    dma150 = float(close.rolling(min(150, len(close)), min_periods=20).mean().iloc[-1])
    swing_low = float(low.iloc[-21:-1].min()) if len(low) >= 21 else float(low.min())
    return {
        "price": round(last, 2),
        "chg": chg,
        "atr14": round(atr14, 1),
        "dma20": round(dma20, 1),
        "dma150": round(dma150, 1),
        "swingLow": round(swing_low, 1),
    }


def compute_sector_pre_explosion(
    price_series: pd.Series,
    daily_tail: list,
    angle: float,
    d1_alpha: float,
    w1_alpha: float,
    m1_ret: float,
    pct50: int,
    pct200: int,
    sig_a: int,
    sig_b: int,
):
    """
    Computes a 0-100 Smart Money Rotation Probability Score for a sector or market-cap index node by combining:
    1. RRG rotation inflection (0-30 pts)
    2. Index volatility compression - BBW 120D rank & ATR(14) decay (0-20 pts)
    3. 1D/1W relative alpha acceleration vs Nifty 50 / Nifty 500 (0-20 pts)
    4. Constituent breadth building above 50/200-DMA (0-15 pts)
    5. Constituent Track B HALO squeeze / Track A breakout confluence (0-15 pts)
    Returns (score, tier, bbw_pct, atr_decay, reasons), where tier is one of:
      PHASE_3 (Markup Ready >=65), PHASE_2 (Supply Absorption 50-64), PHASE_1 (Early Base 35-49),
      EXTENDED (Late Markup >16% 1M in Leading/Weakening), NEUTRAL (<35).
    """
    # 1. Sector Volatility Compression (BBW 120D percentile + ATR14 20-day decay)
    bbw_pct = 50.0
    atr_decay = 1.0
    s = _normalize_series_index(price_series) if price_series is not None else pd.Series(dtype=float)
    if len(s) < 60:
        return 0, "NEUTRAL", bbw_pct, atr_decay, []

    bb_mid = s.rolling(20).mean()
    bb_std = s.rolling(20).std()
    bbw = (100.0 * (4.0 * bb_std) / bb_mid).dropna()
    if len(bbw) >= 30:
        curr_bbw = float(bbw.iloc[-1])
        hist_bbw = bbw.iloc[-121:-1] if len(bbw) > 30 else bbw.iloc[:-1]
        if len(hist_bbw) >= 15:
            bbw_pct = round(float((hist_bbw < curr_bbw).mean() * 100.0), 1)
    tr_proxy = s.diff().abs()
    atr_proxy = tr_proxy.ewm(alpha=1.0 / 14.0, adjust=False).mean()
    if len(atr_proxy) >= 22 and float(atr_proxy.iloc[-21]) > 0:
        atr_decay = round(float(atr_proxy.iloc[-1]) / float(atr_proxy.iloc[-21]), 2)

    # 2. Quadrant & Heading
    a = angle % 360.0
    quad = "Leading" if a < 90 else ("Improving" if a < 180 else ("Lagging" if a < 270 else "Weakening"))
    heading = "E"
    if daily_tail and len(daily_tail) >= 2:
        p1, p2 = daily_tail[-2], daily_tail[-1]
        deg = (math.degrees(math.atan2(p2["y"] - p1["y"], p2["x"] - p1["x"])) + 360.0) % 360.0
        if deg > 337.5 or deg <= 22.5: heading = "E"
        elif deg <= 67.5: heading = "NE"
        elif deg <= 112.5: heading = "N"
        elif deg <= 157.5: heading = "NW"
        elif deg <= 202.5: heading = "W"
        elif deg <= 247.5: heading = "SW"
        elif deg <= 292.5: heading = "S"
        else: heading = "SE"

    reasons = []
    score = 0

    # Factor A: RRG Inflection (max 30)
    if quad == "Improving" and heading in ("NE", "E", "N"):
        score += 30
        reasons.append(f"Improving ({heading})")
    elif quad == "Lagging" and heading in ("N", "NE", "E"):
        score += 24
        reasons.append(f"Bottom Turn ({heading})")
    elif quad == "Improving":
        score += 22
        reasons.append(f"Improving ({heading})")
    elif quad == "Leading" and a <= 45.0 and heading in ("NE", "E"):
        score += 15
        reasons.append(f"Early Leading ({heading})")

    # Factor B: Sector Compression (max 20)
    if bbw_pct <= 25.0:
        score += 12
        reasons.append(f"BBW {bbw_pct:.0f}% Squeeze")
    elif bbw_pct <= 40.0:
        score += 7
    if atr_decay <= 0.85:
        score += 8
        reasons.append(f"ATR {atr_decay:.2f}x")
    elif atr_decay <= 0.95:
        score += 4

    # Factor C: Relative Alpha Acceleration (max 20)
    if d1_alpha > 0 and w1_alpha > 0:
        score += 20
        reasons.append("+1D/1W Alpha")
    elif d1_alpha > 0 or w1_alpha > 0:
        score += 12
        reasons.append("+Alpha Turn")

    # Factor D: Constituent Breadth (max 15)
    if pct50 >= 50 and pct200 >= 45:
        score += 15
        reasons.append(f"{pct50}% >50D")
    elif pct50 >= 35:
        score += 8

    # Factor E: Track B / Track A Confluence (max 15)
    sig_pts = min(15, sig_b * 10 + sig_a * 8)
    if sig_pts > 0:
        score += sig_pts
        if sig_b:
            reasons.append(f"{sig_b} Squeeze")
        if sig_a:
            reasons.append(f"{sig_a} Breakout")

    # Early-stage guard: avoid flagging late-stage rallies (>16% 1M in Leading/Weakening)
    is_extended = (m1_ret > 16.0 and quad in ("Leading", "Weakening"))
    if is_extended:
        tier = "EXTENDED"
    elif score >= 65:
        tier = "PHASE_3"
    elif score >= 50:
        tier = "PHASE_2"
    elif score >= 35:
        tier = "PHASE_1"
    else:
        tier = "NEUTRAL"

    return score, tier, bbw_pct, atr_decay, reasons


def compute_sector_rotation_payload(
    universe=None,
    all_hist=None,
    nifty500_hist=None,
    nse_session=None,
    active_breakouts=None,
    pre_breakout_squeezes=None,
):
    """
    Builds the complete live payload for Tab 4 (Sector Rotation, RRG & Astro-Quant).
    Always gracefully falls back if any optional endpoint is unavailable.
    """
    universe = universe or []
    all_hist = all_hist or {}
    active_breakouts = active_breakouts or []
    pre_breakout_squeezes = pre_breakout_squeezes or []

    now_ist = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
    date_label = now_ist.strftime("%b %d, %Y (%I:%M %p IST)")

    # 1. Batch download official tape + index tickers + 24 curated stocks
    curated_yf = [f"{s['ticker']}.NS" for s in CURATED_STOCK_BASE if s["ticker"] != "NSE"]
    needed_tickers = (
        list(TAPE_TICKERS.values())
        + ["^CRSLDX"]
        + [s["yf"] for s in CAP_INDEX_SPECS if s.get("yf")]
        + [s["yf"] for s in SECTOR_SPECS if s.get("yf")]
        + [t for t in curated_yf if t not in all_hist]
    )
    yf_cache = _fetch_yf_batch(needed_tickers)

    def get_hist(sym):
        return all_hist.get(sym) if sym in all_hist else yf_cache.get(sym)

    # Benchmark series for JdK RRG (prefer 2Y Nifty 500 ^CRSLDX, else Nifty 50 ^NSEI)
    bench_df = get_hist("^CRSLDX")
    if bench_df is None or len(bench_df) < 120:
        if nifty500_hist is not None and len(nifty500_hist) >= 60:
            bench_df = nifty500_hist
        else:
            bench_df = get_hist("^NSEI")
    bench_close = bench_df["Close"] if (bench_df is not None and not bench_df.empty) else pd.Series(dtype=float)

    nifty50_df = get_hist("^NSEI")
    nifty50_rets = _compute_period_returns(nifty50_df["Close"]) if nifty50_df is not None else {"d1": 0.0, "w1": 0.0, "m1": 0.0, "m3": 0.0, "y1": 0.0, "last": 0.0}
    bench_rets = _compute_period_returns(bench_close) if not bench_close.empty else nifty50_rets

    # Optional NSE live quotes + FII/DII cash flow
    nse_indices, fii_dii_live = _fetch_nse_live_snapshots(nse_session)

    # 2. Universe breadth + lookup maps
    adv_count = 0
    dec_count = 0
    by_bucket = {}
    by_industry = {}
    meta_by_sym = {}

    track_a_syms = {s.get("symbol", "").replace(".NS", "") for s in active_breakouts}
    track_b_syms = {s.get("symbol", "").replace(".NS", "") for s in pre_breakout_squeezes}

    for item in universe:
        sym = item["symbol"]
        meta_by_sym[sym] = item
        by_bucket.setdefault(item.get("bucket", "NSE"), []).append(sym)
        by_industry.setdefault(item.get("sector", "Equities"), []).append(sym)
        hdf = all_hist.get(sym)
        if hdf is not None and len(hdf) >= 2:
            c1 = float(hdf["Close"].iloc[-1])
            c0 = float(hdf["Close"].iloc[-2])
            if c1 > c0:
                adv_count += 1
            elif c1 < c0:
                dec_count += 1

    # 3. Market Tape
    def tape_quote(yf_sym, fallback_val):
        df = get_hist(yf_sym)
        if df is not None and len(df) >= 2:
            r = _compute_period_returns(df["Close"])
            return {"last": r["last"], "chg": r["d1"]}
        return {"last": fallback_val, "chg": 0.0}

    tape = {
        "nifty50": tape_quote("^NSEI", 25704.75),
        "sensex": tape_quote("^BSESN", 83894.22),
        "banknifty": tape_quote("^NSEBANK", 63433.95),
        "vix": tape_quote("^INDIAVIX", 17.99),
        "usdinr": tape_quote("INR=X", 92.26),
        "adv": adv_count,
        "dec": dec_count,
        "fii_day_cr": fii_dii_live.get("fii") if fii_dii_live else None,
        "dii_day_cr": fii_dii_live.get("dii") if fii_dii_live else None,
        "fii_dii_date": fii_dii_live.get("date") if fii_dii_live else None,
        "date_label": date_label,
    }

    # 4. Build Live Sector & Market-Cap Universe Nodes (with real Daily & Weekly JdK RRG trails)
    universe_nodes = []
    sector_constituents = {}

    all_specs = CAP_INDEX_SPECS + SECTOR_SPECS
    for spec in all_specs:
        node_kind = spec.get("kind", "sector")
        # Determine member tickers for breadth & drill-down
        if node_kind == "cap":
            member_syms = list(by_bucket.get(spec.get("bucket", ""), []))
            if spec["id"] == "NIFTY_50" and not member_syms:
                member_syms = by_bucket.get("Largecap 100", [])[:50]
        else:
            if spec.get("tickers_proxy"):
                member_syms = [s for s in spec["tickers_proxy"] if get_hist(s) is not None]
            else:
                member_syms = []
                for ind in spec.get("industries", []):
                    member_syms.extend(by_industry.get(ind, []))

        if not member_syms:
            member_syms = [
                f"{s['ticker']}.NS"
                for s in CURATED_STOCK_BASE
                if s["ticker"] != "NSE" and (
                    (node_kind == "sector" and s["sector"] == spec["group"])
                    or (node_kind == "cap" and s.get("capTier") == spec["id"])
                )
            ]

        # Price series: prefer official Yahoo Finance index with >= 60 bars, else equal-weight composite
        price_series = pd.Series(dtype=float)
        source_tag = "Universe Composite"
        if spec.get("yf"):
            hdf = get_hist(spec["yf"])
            if hdf is not None and len(hdf) >= 60:
                price_series = hdf["Close"]
                source_tag = f"NSE Index ({spec['yf']})"

        if price_series.empty and member_syms:
            merged_hist = {s: get_hist(s) for s in member_syms if get_hist(s) is not None}
            price_series = _build_equal_weight_series(member_syms, merged_hist)
            source_tag = f"Equal-Wt ({len(merged_hist)} stocks)"

        rets = _compute_period_returns(price_series) if not price_series.empty else {"d1": 0.0, "w1": 0.0, "m1": 0.0, "m3": 0.0, "y1": 0.0, "last": 0.0}

        # Overlay official NSE allIndices 1D / 1M / 1Y if available
        nse_row = nse_indices.get((spec.get("nse_name") or "").upper())
        if nse_row:
            if nse_row.get("percentChange") is not None:
                rets["d1"] = round(float(nse_row["percentChange"]), 2)
            if nse_row.get("last") is not None:
                rets["last"] = round(float(nse_row["last"]), 2)

        daily_rrg = compute_jdk_rrg_trail(price_series, bench_close, is_weekly=False, tail_len=16) if not bench_close.empty else None
        weekly_rrg = compute_jdk_rrg_trail(price_series, bench_close, is_weekly=True, tail_len=12) if not bench_close.empty else None

        angle, radius, daily_tail = daily_rrg if daily_rrg else (45.0, 100.0, [{"x": 0.0, "y": 0.0}])
        weekly_tail = weekly_rrg[2] if weekly_rrg else daily_tail

        # Breadth & Scanner Signals inside this node
        above_50 = 0
        above_200 = 0
        valid_breadth = 0
        sig_a = 0
        sig_b = 0
        const_rows = []

        for sym in member_syms:
            hdf = get_hist(sym)
            if hdf is None or len(hdf) < 30:
                continue
            c = hdf["Close"]
            last_c = float(c.iloc[-1])
            sma50 = float(c.rolling(min(50, len(c))).mean().iloc[-1])
            sma200 = float(c.rolling(min(200, len(c))).mean().iloc[-1])
            valid_breadth += 1
            if last_c >= sma50:
                above_50 += 1
            if last_c >= sma200:
                above_200 += 1

            clean = sym.replace(".NS", "")
            if clean in track_a_syms:
                sig_a += 1
            if clean in track_b_syms:
                sig_b += 1

            # Build lightweight constituent RRG metrics (compute top 12 by 3M alpha for fast HTML size)
            s_rets = _compute_period_returns(c)
            const_rows.append((sym, clean, s_rets, hdf))

        const_rows.sort(key=lambda x: x[2]["m3"], reverse=True)
        drill_list = []
        for sym, clean, s_rets, hdf in const_rows[:14]:
            d_rrg = compute_jdk_rrg_trail(hdf["Close"], bench_close, is_weekly=False, tail_len=16) if not bench_close.empty else None
            w_rrg = compute_jdk_rrg_trail(hdf["Close"], bench_close, is_weekly=True, tail_len=12) if not bench_close.empty else None
            tech = _stock_technicals_from_hist(hdf) or {"price": s_rets["last"], "chg": s_rets["d1"], "atr14": 0, "dma20": 0, "dma150": 0, "swingLow": 0}
            s_ang, s_rad, s_dtail = d_rrg if d_rrg else (45.0, 100.0, [{"x": 0.0, "y": 0.0}])
            s_wtail = w_rrg[2] if w_rrg else s_dtail
            m_info = meta_by_sym.get(sym, {})
            signal_tag = "TRACK A" if clean in track_a_syms else ("TRACK B" if clean in track_b_syms else None)
            drill_list.append({
                "ticker": clean,
                "name": m_info.get("name", clean),
                "sector": spec["group"],
                "bucket": m_info.get("bucket", "NSE"),
                "price": tech["price"],
                "chg": s_rets["d1"],
                "w1": s_rets["w1"],
                "m1": s_rets["m1"],
                "m3": s_rets["m3"],
                "y1": s_rets["y1"],
                "alpha3m": round(s_rets["m3"] - nifty50_rets["m3"], 2),
                "atr14": tech["atr14"],
                "dma20": tech["dma20"],
                "dma150": tech["dma150"],
                "swingLow": tech["swingLow"],
                "angle": s_ang,
                "radius": s_rad,
                "dailyTail": s_dtail,
                "weeklyTail": s_wtail,
                "signalTag": signal_tag,
            })

        sector_constituents[spec["id"]] = drill_list

        pct50 = round((above_50 / valid_breadth) * 100) if valid_breadth else 0
        pct200 = round((above_200 / valid_breadth) * 100) if valid_breadth else 0
        alpha_1d = round(rets["d1"] - nifty50_rets["d1"], 2)
        alpha_1w = round(rets["w1"] - nifty50_rets["w1"], 2)

        # For NIFTY 50, score relative alpha against Nifty 500 (same benchmark used by RRG)
        pe_d1_alpha = round(rets["d1"] - bench_rets["d1"], 2) if spec["id"] == "NIFTY_50" else alpha_1d
        pe_w1_alpha = round(rets["w1"] - bench_rets["w1"], 2) if spec["id"] == "NIFTY_50" else alpha_1w

        pe_score, pe_tier, bbw_pct, atr_decay, pe_reasons = compute_sector_pre_explosion(
            price_series=price_series,
            daily_tail=daily_tail,
            angle=angle,
            d1_alpha=pe_d1_alpha,
            w1_alpha=pe_w1_alpha,
            m1_ret=rets["m1"],
            pct50=pct50,
            pct200=pct200,
            sig_a=sig_a,
            sig_b=sig_b,
        )

        desc_str = f"{spec['desc']} ({rets['last']:,.2f})" if rets["last"] > 0 else spec["desc"]
        universe_nodes.append({
            "id": spec["id"],
            "kind": node_kind,
            "curated": spec["curated"],
            "topMover": spec["topMover"] or abs(alpha_1d) >= 1.0 or pe_tier in ("PHASE_3", "PHASE_2"),
            "group": spec["group"],
            "short": spec["short"],
            "desc": desc_str,
            "source": source_tag,
            "memberCount": len(member_syms),
            "pctAbove50": pct50,
            "pctAbove200": pct200,
            "trackACount": sig_a,
            "trackBCount": sig_b,
            "preExplodeScore": pe_score,
            "preExplodeTier": pe_tier,
            "bbwPct": bbw_pct,
            "atrDecay": atr_decay,
            "preExplodeReasons": pe_reasons,
            "angle": angle,
            "radius": radius,
            "dailyTail": daily_tail,
            "weeklyTail": weekly_tail,
            "chg": rets["d1"],
            "alpha": alpha_1d,
            "w1": rets["w1"],
            "m1": rets["m1"],
            "m3": rets["m3"],
            "y1": rets["y1"],
            "ruler": spec["ruler"],
            "natalNote": spec["natalNote"],
        })

    # 5. Update the 24 Curated Fundamental/Astro-Quant Equities with live prices, technicals & JdK RRG
    live_stocks = []
    for base in CURATED_STOCK_BASE:
        st = dict(base)
        yf_sym = f"{st['ticker']}.NS"
        hdf = get_hist(yf_sym)
        if hdf is not None and len(hdf) >= 22:
            tech = _stock_technicals_from_hist(hdf)
            if tech:
                st.update(tech)
            d_rrg = compute_jdk_rrg_trail(hdf["Close"], bench_close, is_weekly=False, tail_len=16) if not bench_close.empty else None
            w_rrg = compute_jdk_rrg_trail(hdf["Close"], bench_close, is_weekly=True, tail_len=12) if not bench_close.empty else None
            if d_rrg:
                st["angle"], st["radius"], st["dailyTail"] = d_rrg
            if w_rrg:
                st["weeklyTail"] = w_rrg[2]
        if st["ticker"] in track_a_syms:
            st["signalTag"] = "TRACK A"
        elif st["ticker"] in track_b_syms:
            st["signalTag"] = "TRACK B"
        live_stocks.append(st)

    payload = {
        "generated_at": date_label,
        "benchmark_name": "NIFTY 500" if (nifty500_hist is not None and not nifty500_hist.empty) else "NIFTY 50",
        "tape": tape,
        "universe_nodes": universe_nodes,
        "curated_stocks": live_stocks,
        "sector_constituents": sector_constituents,
    }
    return payload


def save_sector_rotation_cache(payload, cache_path=CACHE_PATH):
    """Persists the latest live Sector Rotation payload to data/sector_rotation.json."""
    os.makedirs(os.path.dirname(cache_path), exist_ok=True)
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    return cache_path


def load_sector_rotation_cache(cache_path=CACHE_PATH):
    """Loads cached Sector Rotation payload if present."""
    if os.path.exists(cache_path):
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load cached sector rotation JSON: {e}")
    return None


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    from nifty_momentum_bot import fetch_dynamic_universe, download_universe_history, create_nse_session

    nse_sess = create_nse_session()
    try:
        bench = yf.Ticker("^CRSLDX").history(period="2y")
    except Exception:
        bench = yf.Ticker("^NSEI").history(period="2y")
    univ = fetch_dynamic_universe()
    hist_map = download_universe_history(univ, chunk_size=100)
    data = compute_sector_rotation_payload(
        universe=univ,
        all_hist=hist_map,
        nifty500_hist=bench,
        nse_session=nse_sess,
    )
    out = save_sector_rotation_cache(data)
    print(f"Saved live sector rotation payload to {out} ({len(data['universe_nodes'])} nodes)")
