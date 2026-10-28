"""
Dashboard Generator for AntiGravity Smart Money Dual Track Radar
Generates a standalone, responsive, high-performance HTML/JS dashboard
saved to docs/index.html (for GitHub Pages and offline local browsing).
Includes dedicated Tab 3: Strategy Performance Audit Ledger & Trade Tracker.
"""

import os
import json
import datetime

def generate_html_dashboard(active_breakouts, pre_breakout_squeezes, benchmark_indices=None, total_scanned=651, trades=None, strategy_metrics=None):
    """
    Renders a futuristic dark-mode HTML dashboard with embedded JSON data,
    TradingView mini widgets, search/filter controls, and statistics.
    Includes Tab 1 (Track B), Tab 2 (Track A), and Tab 3 (Strategy Performance & Trade Ledger).
    """
    now_ist = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
    formatted_date = now_ist.strftime("%d %b %Y | %I:%M %p IST")
    
    # Load trades from ledger if not explicitly passed
    if trades is None:
        try:
            from trade_tracker import load_trade_ledger, compute_strategy_metrics
            trades = load_trade_ledger()
            if strategy_metrics is None:
                strategy_metrics = compute_strategy_metrics(trades)
        except Exception:
            trades = []

    if strategy_metrics is None:
        try:
            from trade_tracker import compute_strategy_metrics
            strategy_metrics = compute_strategy_metrics(trades)
        except Exception:
            strategy_metrics = {
                "total_signals": len(trades),
                "closed_trades_count": 0,
                "active_trades_count": 0,
                "pending_trades_count": 0,
                "win_count": 0,
                "loss_count": 0,
                "win_rate_pct": 0.0,
                "net_r_multiple": 0.0,
                "gross_gains_r": 0.0,
                "gross_losses_r": 0.0,
                "profit_factor": 0.0,
                "avg_win_pct": 0.0,
                "avg_loss_pct": 0.0,
                "edge_ratio": 1.0,
                "track_a_count": 0,
                "track_b_count": 0
            }

    # Serialize payloads for client-side interactivity
    track_a_json = json.dumps(active_breakouts, indent=2)
    track_b_json = json.dumps(pre_breakout_squeezes, indent=2)
    bench_json = json.dumps(benchmark_indices or [], indent=2)
    trades_json = json.dumps(trades, indent=2)
    metrics_json = json.dumps(strategy_metrics, indent=2)
    
    total_scanned = total_scanned or 651
    track_a_count = len(active_breakouts)
    track_b_count = len(pre_breakout_squeezes)
    total_trades_count = len(trades)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AntiGravity Smart Money Dual Track Radar & Trade Ledger</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-base: #0a0d14;
      --bg-surface: #111622;
      --bg-card: #161c2d;
      --bg-card-hover: #1c2438;
      --border-subtle: rgba(255, 255, 255, 0.08);
      --border-accent: rgba(59, 130, 246, 0.3);
      --text-main: #f1f5f9;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      --accent-blue: #38bdf8;
      --accent-green: #10b981;
      --accent-purple: #a855f7;
      --accent-amber: #f59e0b;
      --accent-rose: #f43f5e;
      --accent-teal: #14b8a6;
      --accent-cyan: #06b6d4;
      --gradient-card: linear-gradient(135deg, rgba(255,255,255,0.03) 0%, rgba(255,255,255,0) 100%);
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      font-family: 'Plus Jakarta Sans', sans-serif;
      background-color: var(--bg-base);
      color: var(--text-main);
      line-height: 1.5;
      padding-bottom: 80px;
      overflow-x: hidden;
    }}

    /* Top glowing bar */
    body::before {{
      content: '';
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      height: 3px;
      background: linear-gradient(90deg, #38bdf8, #a855f7, #10b981);
      z-index: 1000;
    }}

    .container {{
      max-width: 1420px;
      margin: 0 auto;
      padding: 0 24px;
    }}

    /* Header */
    header {{
      padding: 36px 0 24px 0;
      border-bottom: 1px solid var(--border-subtle);
      margin-bottom: 32px;
      background: radial-gradient(circle at 50% -20%, rgba(56, 189, 248, 0.08) 0%, transparent 70%);
    }}

    .header-content {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
    }}

    .brand-title {{
      font-size: 26px;
      font-weight: 800;
      letter-spacing: -0.5px;
      display: flex;
      align-items: center;
      gap: 12px;
      background: linear-gradient(90deg, #ffffff, #94a3b8);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}

    .live-badge {{
      background: rgba(16, 185, 129, 0.15);
      border: 1px solid rgba(16, 185, 129, 0.3);
      color: var(--accent-green);
      font-size: 11px;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: 9999px;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}

    .live-dot {{
      width: 7px;
      height: 7px;
      background-color: var(--accent-green);
      border-radius: 50%;
      box-shadow: 0 0 8px var(--accent-green);
      animation: pulse 2s infinite;
    }}

    @keyframes pulse {{
      0%, 100% {{ opacity: 1; transform: scale(1); }}
      50% {{ opacity: 0.4; transform: scale(0.85); }}
    }}

    .timestamp-box {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 12px;
      color: var(--text-muted);
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      padding: 6px 14px;
      border-radius: 8px;
    }}

    /* Global Summary Stat Cards Banner */
    .stats-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 16px;
      margin-bottom: 32px;
    }}

    .stat-card {{
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 12px;
      padding: 18px 20px;
      position: relative;
      overflow: hidden;
      transition: border-color 0.2s, transform 0.2s;
    }}

    .stat-card:hover {{
      border-color: rgba(255, 255, 255, 0.15);
      transform: translateY(-2px);
    }}

    .stat-label {{
      font-size: 11px;
      font-weight: 700;
      color: var(--text-dim);
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-bottom: 6px;
    }}

    .stat-val {{
      font-size: 24px;
      font-weight: 800;
      color: #fff;
      display: flex;
      align-items: baseline;
      gap: 8px;
    }}

    .stat-sub {{
      font-size: 11px;
      color: var(--text-muted);
      font-weight: 500;
    }}

    /* Navigation Tabs */
    .tab-bar {{
      display: flex;
      gap: 8px;
      background: var(--bg-surface);
      padding: 6px;
      border-radius: 12px;
      border: 1px solid var(--border-subtle);
      margin-bottom: 24px;
      flex-wrap: wrap;
    }}

    .tab-btn {{
      padding: 11px 22px;
      font-size: 14px;
      font-weight: 600;
      color: var(--text-muted);
      background: transparent;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 8px;
      transition: all 0.2s;
    }}

    .tab-btn:hover {{
      color: #fff;
      background: rgba(255, 255, 255, 0.05);
    }}

    .tab-btn.active {{
      background: var(--accent-blue);
      color: #050b14;
      font-weight: 700;
      box-shadow: 0 4px 14px rgba(56, 189, 248, 0.25);
    }}

    .tab-badge {{
      font-size: 11px;
      padding: 2px 8px;
      border-radius: 9999px;
      background: rgba(0,0,0,0.25);
      font-family: 'JetBrains Mono', monospace;
    }}

    .tab-btn.active .tab-badge {{
      background: #050b14;
      color: var(--accent-blue);
    }}

    /* Search & Filter Bar */
    .search-bar {{
      display: flex;
      gap: 12px;
      margin-bottom: 24px;
      flex-wrap: wrap;
    }}

    .search-input {{
      flex: 1;
      min-width: 260px;
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      padding: 12px 18px;
      border-radius: 10px;
      color: #fff;
      font-family: inherit;
      font-size: 14px;
      outline: none;
      transition: border-color 0.2s;
    }}

    .search-input:focus {{
      border-color: var(--accent-blue);
    }}

    /* Stock Cards Grid (Tabs A & B) */
    .stock-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(390px, 1fr));
      gap: 20px;
    }}

    .card {{
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 14px;
      padding: 22px;
      display: flex;
      flex-direction: column;
      gap: 16px;
      transition: transform 0.2s, border-color 0.2s, box-shadow 0.2s;
      position: relative;
    }}

    .card:hover {{
      transform: translateY(-3px);
      border-color: var(--border-accent);
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
    }}

    .card-head {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      border-bottom: 1px solid rgba(255, 255, 255, 0.05);
      padding-bottom: 12px;
    }}

    .stock-sym {{
      font-size: 18px;
      font-weight: 800;
      color: #fff;
      letter-spacing: -0.3px;
    }}

    .stock-name {{
      font-size: 13px;
      color: var(--text-muted);
      font-weight: 500;
      margin-top: 2px;
    }}

    .score-badge {{
      padding: 6px 12px;
      border-radius: 8px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 13px;
      font-weight: 700;
      text-align: right;
    }}

    .score-high {{
      background: rgba(16, 185, 129, 0.15);
      color: var(--accent-green);
      border: 1px solid rgba(16, 185, 129, 0.3);
    }}

    .score-mid {{
      background: rgba(56, 189, 248, 0.15);
      color: var(--accent-blue);
      border: 1px solid rgba(56, 189, 248, 0.3);
    }}

    .bucket-badge {{
      display: inline-block;
      padding: 2px 7px;
      border-radius: 4px;
      font-size: 11px;
      font-weight: 600;
      background: rgba(168, 85, 247, 0.15);
      color: var(--accent-purple);
      border: 1px solid rgba(168, 85, 247, 0.3);
      margin-left: 6px;
      vertical-align: middle;
    }}

    .metrics-row {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 10px;
    }}

    .metric-box {{
      background: var(--bg-surface);
      padding: 8px 10px;
      border-radius: 8px;
      border: 1px solid rgba(255, 255, 255, 0.03);
    }}

    .metric-lbl {{
      font-size: 10px;
      color: var(--text-dim);
      text-transform: uppercase;
      font-weight: 600;
      margin-bottom: 2px;
    }}

    .metric-data {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 13px;
      font-weight: 600;
      color: var(--text-main);
    }}

    .trade-plan {{
      background: rgba(10, 13, 20, 0.7);
      border: 1px dashed rgba(56, 189, 248, 0.3);
      border-radius: 10px;
      padding: 12px 14px;
      display: flex;
      flex-direction: column;
      gap: 6px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 12px;
    }}

    .plan-line {{
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .plan-tag {{
      color: var(--text-dim);
      font-weight: 600;
    }}

    .plan-val {{
      font-weight: 700;
    }}

    .plan-val.buy {{ color: var(--accent-blue); }}
    .plan-val.sl {{ color: var(--accent-rose); }}
    .plan-val.t1 {{ color: var(--accent-green); }}
    .plan-val.t2 {{ color: var(--accent-amber); }}
    .plan-val.runner {{ color: var(--accent-purple); }}

    .rationale-box {{
      font-size: 12px;
      color: #cbd5e1;
      background: rgba(255, 255, 255, 0.02);
      border-left: 3px solid var(--accent-blue);
      padding: 8px 12px;
      border-radius: 0 6px 6px 0;
      font-style: italic;
      line-height: 1.45;
    }}

    .card-footer {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-top: 10px;
      border-top: 1px solid rgba(255, 255, 255, 0.05);
      font-size: 12px;
    }}

    .tv-link {{
      color: var(--accent-blue);
      text-decoration: none;
      font-weight: 600;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      transition: color 0.15s;
    }}

    .tv-link:hover {{
      color: #fff;
    }}

    /* =====================================================================
       TAB 3: TRADE LEDGER & STRATEGY PERFORMANCE STYLES
       ===================================================================== */
    #view-ledger {{
      display: flex;
      flex-direction: column;
      gap: 24px;
    }}

    .ledger-kpis {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
      gap: 16px;
    }}

    .kpi-card {{
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 12px;
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 6px;
      position: relative;
      overflow: hidden;
    }}

    .kpi-title {{
      font-size: 11px;
      font-weight: 700;
      color: var(--text-dim);
      text-transform: uppercase;
      letter-spacing: 0.6px;
    }}

    .kpi-number {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 28px;
      font-weight: 800;
      display: flex;
      align-items: baseline;
      gap: 6px;
    }}

    .kpi-desc {{
      font-size: 12px;
      color: var(--text-muted);
    }}

    .col-green {{ color: var(--accent-green); }}
    .col-blue {{ color: var(--accent-blue); }}
    .col-purple {{ color: var(--accent-purple); }}
    .col-amber {{ color: var(--accent-amber); }}
    .col-cyan {{ color: var(--accent-cyan); }}
    .col-rose {{ color: var(--accent-rose); }}

    /* Lifecycle rule explanation banner */
    .lifecycle-box {{
      background: rgba(17, 22, 34, 0.8);
      border: 1px solid rgba(56, 189, 248, 0.2);
      border-radius: 12px;
      padding: 18px 24px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}

    .lifecycle-title {{
      font-size: 13px;
      font-weight: 700;
      color: var(--accent-blue);
      display: flex;
      align-items: center;
      gap: 8px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}

    .lifecycle-rules {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 14px;
      font-size: 12px;
      color: #cbd5e1;
    }}

    .rule-item {{
      background: rgba(255, 255, 255, 0.02);
      padding: 10px 14px;
      border-radius: 8px;
      border-left: 2px solid var(--accent-blue);
    }}

    .rule-item strong {{
      color: #fff;
    }}

    /* Filter Controls in Ledger */
    .ledger-controls {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
      background: var(--bg-surface);
      padding: 12px 18px;
      border-radius: 12px;
      border: 1px solid var(--border-subtle);
    }}

    .filter-group {{
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
    }}

    .filter-lbl {{
      font-size: 12px;
      font-weight: 700;
      color: var(--text-dim);
      text-transform: uppercase;
      margin-right: 4px;
    }}

    .filter-pill {{
      padding: 6px 14px;
      font-size: 12px;
      font-weight: 600;
      color: var(--text-muted);
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      cursor: pointer;
      transition: all 0.15s;
    }}

    .filter-pill:hover {{
      color: #fff;
      border-color: rgba(255, 255, 255, 0.2);
    }}

    .filter-pill.active {{
      background: var(--accent-blue);
      color: #050b14;
      font-weight: 700;
      border-color: var(--accent-blue);
    }}

    /* Ledger Table Container */
    .ledger-table-wrap {{
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 14px;
      overflow-x: auto;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }}

    .ledger-table {{
      width: 100%;
      border-collapse: collapse;
      text-align: left;
      font-size: 13px;
    }}

    .ledger-table th {{
      background: var(--bg-surface);
      color: var(--text-dim);
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      padding: 14px 16px;
      border-bottom: 1px solid var(--border-subtle);
      white-space: nowrap;
    }}

    .ledger-table td {{
      padding: 14px 16px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.04);
      color: var(--text-main);
      vertical-align: middle;
      white-space: nowrap;
    }}

    .ledger-table tbody tr:hover {{
      background: rgba(255, 255, 255, 0.02);
    }}

    .sym-col {{
      font-weight: 800;
      color: #fff;
      font-size: 14px;
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .mono {{
      font-family: 'JetBrains Mono', monospace;
    }}

    /* Status Badges */
    .status-badge {{
      display: inline-flex;
      align-items: center;
      gap: 5px;
      padding: 4px 10px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 700;
      font-family: 'JetBrains Mono', monospace;
      letter-spacing: 0.3px;
    }}

    .status-active {{
      background: rgba(56, 189, 248, 0.15);
      color: var(--accent-blue);
      border: 1px solid rgba(56, 189, 248, 0.3);
    }}

    .status-pending {{
      background: rgba(245, 158, 11, 0.15);
      color: var(--accent-amber);
      border: 1px solid rgba(245, 158, 11, 0.3);
    }}

    .status-t1 {{
      background: rgba(20, 184, 166, 0.15);
      color: var(--accent-teal);
      border: 1px solid rgba(20, 184, 166, 0.3);
    }}

    .status-t2 {{
      background: rgba(16, 185, 129, 0.15);
      color: var(--accent-green);
      border: 1px solid rgba(16, 185, 129, 0.3);
    }}

    .status-be {{
      background: rgba(6, 182, 212, 0.15);
      color: var(--accent-cyan);
      border: 1px solid rgba(6, 182, 212, 0.3);
    }}

    .status-sl {{
      background: rgba(244, 63, 94, 0.15);
      color: var(--accent-rose);
      border: 1px solid rgba(244, 63, 94, 0.3);
    }}

    .status-expired {{
      background: rgba(148, 163, 184, 0.15);
      color: var(--text-dim);
      border: 1px solid rgba(148, 163, 184, 0.3);
    }}

    .pnl-pill {{
      font-family: 'JetBrains Mono', monospace;
      font-weight: 700;
      font-size: 13px;
      display: inline-block;
    }}

    .pnl-pos {{ color: var(--accent-green); }}
    .pnl-neg {{ color: var(--accent-rose); }}
    .pnl-zero {{ color: var(--text-muted); }}

    /* Empty state */
    .empty-state {{
      grid-column: 1 / -1;
      text-align: center;
      padding: 60px 20px;
      background: var(--bg-surface);
      border: 1px dashed var(--border-subtle);
      border-radius: 16px;
      color: var(--text-muted);
    }}

    .empty-title {{
      font-size: 18px;
      font-weight: 700;
      color: #fff;
      margin-bottom: 8px;
    }}

    /* Footer info */
    footer {{
      margin-top: 60px;
      text-align: center;
      font-size: 12px;
      color: var(--text-dim);
      border-top: 1px solid var(--border-subtle);
      padding-top: 24px;
    }}
  </style>
</head>
<body>

  <div class="container">
    <header>
      <div class="header-content">
        <div>
          <h1 class="brand-title">
            <span>🌌</span> AntiGravity Smart Money Dual Track Radar
          </h1>
          <p style="color: var(--text-muted); font-size: 13px; margin-top: 4px;">
            Institutional High-Quality Quality Compounders (MCap ₹2k–35k Cr | ROE ≥15% | ROCE ≥20% | OCF/PAT ≥0.6)
          </p>
        </div>
        <div style="display: flex; align-items: center; gap: 12px; flex-wrap: wrap;">
          <div class="live-badge">
            <span class="live-dot"></span> Active EOD Feed
          </div>
          <div class="timestamp-box">📅 {formatted_date}</div>
        </div>
      </div>
    </header>

    <!-- Global Stats Banner -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-label">Candidate Universe</div>
        <div class="stat-val">{total_scanned} <span class="stat-sub">Stocks Monitored</span></div>
        <div style="font-size: 11px; color: var(--text-dim); margin-top: 4px;">Nifty Mid 150 + Small 250 + Micro 250</div>
      </div>
      <div class="stat-card" style="border-left: 3px solid var(--accent-purple);">
        <div class="stat-label">Track B: Squeeze Leaderboard</div>
        <div class="stat-val">{track_b_count} <span class="stat-sub">Coiling Beneath Pivot</span></div>
      </div>
      <div class="stat-card" style="border-left: 3px solid var(--accent-green);">
        <div class="stat-label">Track A: Active Breakouts</div>
        <div class="stat-val">{track_a_count} <span class="stat-sub">Volume Blast Confirmations</span></div>
      </div>
      <div class="stat-card" style="border-left: 3px solid var(--accent-blue);">
        <div class="stat-label">Strategy Audit Performance</div>
        <div class="stat-val col-green">{strategy_metrics.get('win_rate_pct', 0)}% <span class="stat-sub">Win Rate ({strategy_metrics.get('net_r_multiple', 0):+}R Net)</span></div>
      </div>
    </div>

    <!-- Navigation Tabs -->
    <div class="tab-bar">
      <button class="tab-btn active" id="tab-btn-b" onclick="switchTab('b')">
        💣 Track B: Pre-Breakout Squeeze Leaderboard
        <span class="tab-badge" id="badge-b">{track_b_count}</span>
      </button>
      <button class="tab-btn" id="tab-btn-a" onclick="switchTab('a')">
        🚀 Track A: Active & Confirmed Breakouts
        <span class="tab-badge" id="badge-a">{track_a_count}</span>
      </button>
      <button class="tab-btn" id="tab-btn-ledger" onclick="switchTab('ledger')">
        📈 Strategy Performance & Trade Ledger
        <span class="tab-badge" id="badge-ledger">{total_trades_count}</span>
      </button>
    </div>

    <!-- Search Input -->
    <div class="search-bar">
      <input type="text" class="search-input" id="search-input" placeholder="Search by Symbol, Company Name, or Sector..." onkeyup="filterCards()">
    </div>

    <!-- TAB 1: Track B Grid -->
    <div class="stock-grid" id="grid-track-b">
      <!-- Injected by JavaScript -->
    </div>

    <!-- TAB 2: Track A Grid -->
    <div class="stock-grid" id="grid-track-a" style="display: none;">
      <!-- Injected by JavaScript -->
    </div>

    <!-- TAB 3: Strategy Performance & Trade Ledger View -->
    <div id="view-ledger" style="display: none;">
      
      <!-- Top Strategy KPI Banner -->
      <div class="ledger-kpis">
        <div class="kpi-card" style="border-left: 3px solid var(--accent-green);">
          <div class="kpi-title">Strategy Win Rate</div>
          <div class="kpi-number col-green" id="kpi-win-rate">{strategy_metrics.get('win_rate_pct', 0)}%</div>
          <div class="kpi-desc" id="kpi-win-sub">
            {strategy_metrics.get('win_count', 0)} Wins · {strategy_metrics.get('loss_count', 0)} Losses ({strategy_metrics.get('closed_trades_count', 0)} Resolved)
          </div>
        </div>

        <div class="kpi-card" style="border-left: 3px solid var(--accent-blue);">
          <div class="kpi-title">Net Strategy R-Return</div>
          <div class="kpi-number col-blue" id="kpi-net-r">{strategy_metrics.get('net_r_multiple', 0):+}R</div>
          <div class="kpi-desc" id="kpi-net-sub">
            Gross Won: +{strategy_metrics.get('gross_gains_r', 0)}R · Gross Lost: -{strategy_metrics.get('gross_losses_r', 0)}R
          </div>
        </div>

        <div class="kpi-card" style="border-left: 3px solid var(--accent-purple);">
          <div class="kpi-title">Profit Factor</div>
          <div class="kpi-number col-purple" id="kpi-profit-factor">{strategy_metrics.get('profit_factor', 0)}x</div>
          <div class="kpi-desc">Gross Win R / Gross Loss R</div>
        </div>

        <div class="kpi-card" style="border-left: 3px solid var(--accent-amber);">
          <div class="kpi-title">Asymmetric Payoff Edge</div>
          <div class="kpi-number col-amber">+{strategy_metrics.get('avg_win_pct', 0)}% / -{strategy_metrics.get('avg_loss_pct', 0)}%</div>
          <div class="kpi-desc">{strategy_metrics.get('edge_ratio', 1.0)}x Advantage over standard stop</div>
        </div>

        <div class="kpi-card" style="border-left: 3px solid var(--accent-cyan);">
          <div class="kpi-title">Lifecycle Distribution</div>
          <div class="kpi-number col-cyan">{strategy_metrics.get('active_trades_count', 0)} Active · {strategy_metrics.get('pending_trades_count', 0)} Pending</div>
          <div class="kpi-desc">{strategy_metrics.get('total_signals', 0)} Total Historical Signals Tracked</div>
        </div>
      </div>

      <!-- Institutional 40/30/30 Profit Lock Architecture -->
      <div class="lifecycle-box">
        <div class="lifecycle-title">
          <span>🛡️</span> Mathematical Edge: AntiGravity 40 / 30 / 30 Capital Protection Engine
        </div>
        <div class="lifecycle-rules">
          <div class="rule-item">
            <strong>Target 1 (+2R):</strong> Book 40% position profit; trailing SL instantly jumps to Breakeven Retest Anchor. The trade is guaranteed profitable at <strong>+0.8R net</strong> even if later stopped out!
          </div>
          <div class="rule-item">
            <strong>Target 2 (+3R):</strong> Book 30% position profit. Total booked profit locks in at <strong>+1.7R to +2.5R</strong>.
          </div>
          <div class="rule-item">
            <strong>Runner (30%):</strong> Trailed with 20-Day EMA to ride multi-month institutional momentum compounders without premature profit capping.
          </div>
          <div class="rule-item">
            <strong>Capital Defense:</strong> If stopped at initial structural stop-loss, loss is strictly defined and capped at exactly <strong>-1.0R</strong>.
          </div>
        </div>
      </div>

      <!-- Ledger Filters -->
      <div class="ledger-controls">
        <div class="filter-group">
          <span class="filter-lbl">Status:</span>
          <button class="filter-pill active" id="pill-status-all" onclick="setLedgerStatusFilter('ALL')">All Trades</button>
          <button class="filter-pill" id="pill-status-active" onclick="setLedgerStatusFilter('ACTIVE')">🔵 Active</button>
          <button class="filter-pill" id="pill-status-pending" onclick="setLedgerStatusFilter('PENDING_TRIGGER')">🟡 Pending</button>
          <button class="filter-pill" id="pill-status-wins" onclick="setLedgerStatusFilter('WINS')">🟢 Targets Hit (Wins)</button>
          <button class="filter-pill" id="pill-status-be" onclick="setLedgerStatusFilter('STOPPED_OUT_BE')">🛡️ Breakeven (+0.8R)</button>
          <button class="filter-pill" id="pill-status-losses" onclick="setLedgerStatusFilter('LOSSES')">🔴 Stopped (-1R)</button>
        </div>
        <div class="filter-group">
          <span class="filter-lbl">Track:</span>
          <button class="filter-pill active" id="pill-track-all" onclick="setLedgerTrackFilter('ALL')">All Tracks</button>
          <button class="filter-pill" id="pill-track-a" onclick="setLedgerTrackFilter('Track A')">🚀 Track A</button>
          <button class="filter-pill" id="pill-track-b" onclick="setLedgerTrackFilter('Track B')">💣 Track B</button>
        </div>
      </div>

      <!-- Trade Audit Ledger Table -->
      <div class="ledger-table-wrap">
        <table class="ledger-table">
          <thead>
            <tr>
              <th>Symbol & Company</th>
              <th>Track & Signal</th>
              <th>Detected</th>
              <th>Trigger / Entry</th>
              <th>Stop Loss (SL)</th>
              <th>Targets (T1 / T2)</th>
              <th>Current / Exit</th>
              <th>Status</th>
              <th>Return (% / R)</th>
              <th>Days</th>
              <th>Chart</th>
            </tr>
          </thead>
          <tbody id="ledger-table-body">
            <!-- Dynamically populated by JS -->
          </tbody>
        </table>
      </div>

    </div>

    <footer>
      ⚡ AntiGravity Smart Money Dual Track Radar · Automated daily at 05:00 PM IST via GitHub Actions · Official NSE India EOD Data & Git Persistent Trade Ledger
    </footer>
  </div>

  <script>
    const trackAData = {track_a_json};
    const trackBData = {track_b_json};
    const tradesData = {trades_json};
    const strategyMetrics = {metrics_json};

    let currentTab = 'b';
    let ledgerStatusFilter = 'ALL';
    let ledgerTrackFilter = 'ALL';

    function renderTrackBCards(data) {{
      const grid = document.getElementById('grid-track-b');
      if (!data || data.length === 0) {{
        grid.innerHTML = `
          <div class="empty-state">
            <div class="empty-title">No Squeeze Candidates Today</div>
            <p>None of the stocks currently meet all 7 HALO quantitative compression rules (ATR contraction, 120D BBW 25th percentile, and volume dry-up). This protects your capital during choppy regimes.</p>
          </div>
        `;
        return;
      }}

      grid.innerHTML = data.map((stock, idx) => `
        <div class="card" data-symbol="${{stock.symbol}}" data-name="${{stock.name}}" data-sector="${{stock.sector}}">
          <div class="card-head">
            <div>
              <div class="stock-sym">${{stock.symbol}} <span style="font-size: 13px; color: var(--text-dim); font-weight: 500;">· ${{stock.sector}}</span> ${{stock.bucket ? `<span class="bucket-badge">${{stock.bucket}}</span>` : ''}}</div>
              <div class="stock-name">${{stock.name}}</div>
            </div>
            <div class="score-badge ${{stock.halo_score >= 80 ? 'score-high' : 'score-mid'}}">
              Score: ${{stock.halo_score}}/100
            </div>
          </div>

          <div class="metrics-row">
            <div class="metric-box">
              <div class="metric-lbl">Current Price</div>
              <div class="metric-data">₹${{stock.price}}</div>
            </div>
            <div class="metric-box">
              <div class="metric-lbl">Pivot (20D High)</div>
              <div class="metric-data">₹${{stock.pivot_ref}}</div>
            </div>
            <div class="metric-box">
              <div class="metric-lbl">Distance</div>
              <div class="metric-data" style="color: var(--accent-amber);">${{stock.dist_to_high}}</div>
            </div>
            <div class="metric-box">
              <div class="metric-lbl">BBW Rank (120D)</div>
              <div class="metric-data">${{stock.bbw_percentile}}</div>
            </div>
            <div class="metric-box">
              <div class="metric-lbl">5D Volume Ratio</div>
              <div class="metric-data">${{stock.vol_dryup_ratio}} (Dry)</div>
            </div>
            <div class="metric-box">
              <div class="metric-lbl">NSE Delivery</div>
              <div class="metric-data">${{stock.delivery_pct}}</div>
            </div>
          </div>

          <!-- Trade Plan Box -->
          <div class="trade-plan">
            <div class="plan-line">
              <span class="plan-tag">🎯 BUY TRIGGER</span>
              <span class="plan-val buy">Buy-Stop Limit @ ₹${{stock.entry_trigger}}</span>
            </div>
            <div class="plan-line">
              <span class="plan-tag">🛑 INITIAL SL (1R)</span>
              <span class="plan-val sl">₹${{stock.initial_sl}} (Risk: ₹${{stock.risk_1r}} · ${{stock.risk_pct}}%)</span>
            </div>
            <div class="plan-line">
              <span class="plan-tag">💰 TARGET 1 (2R)</span>
              <span class="plan-val t1">₹${{stock.target_1_2r}} (Book 40% & Trail SL to ₹${{stock.be_retest_anchor}})</span>
            </div>
            <div class="plan-line">
              <span class="plan-tag">🚀 TARGET 2 (3R)</span>
              <span class="plan-val t2">₹${{stock.target_2_3r}} (Book 30%)</span>
            </div>
            <div class="plan-line">
              <span class="plan-tag">💎 RUNNER (30%)</span>
              <span class="plan-val runner">Trail with 20-Day EMA (Ride Multibagger)</span>
            </div>
          </div>

          <!-- Rationale -->
          <div class="rationale-box">
            💡 ${{stock.rationale}}
          </div>

          <div class="card-footer">
            <span style="color: var(--text-dim); font-size: 11px;">
              ROE: <b>${{stock.roe}}%</b> · ROCE: <b>${{stock.roce}}%</b> · OCF/PAT: <b>${{stock.ocf_to_pat}}x</b>
            </span>
            <a href="https://in.tradingview.com/chart/?symbol=NSE:${{stock.symbol}}" target="_blank" class="tv-link">
              TradingView ↗
            </a>
          </div>
        </div>
      `).join('');
    }}

    function renderTrackACards(data) {{
      const grid = document.getElementById('grid-track-a');
      if (!data || data.length === 0) {{
        grid.innerHTML = `
          <div class="empty-state">
            <div class="empty-title">No Active Breakouts Today</div>
            <p>No stocks completed a fresh 20-Day High breakout on volume ≥ 1.5x with CRR ≥ 0.70 during today's session.</p>
          </div>
        `;
        return;
      }}

      grid.innerHTML = data.map((stock, idx) => `
        <div class="card" data-symbol="${{stock.symbol}}" data-name="${{stock.name}}" data-sector="${{stock.sector}}">
          <div class="card-head">
            <div>
              <div class="stock-sym">${{stock.symbol}} <span style="font-size: 13px; color: var(--text-dim); font-weight: 500;">· ${{stock.sector}}</span> ${{stock.bucket ? `<span class="bucket-badge">${{stock.bucket}}</span>` : ''}}</div>
              <div class="stock-name">${{stock.name}}</div>
            </div>
            <div class="score-badge score-high">
              Score: ${{stock.breakout_score || 85}}/100
            </div>
          </div>

          <div class="metrics-row">
            <div class="metric-box">
              <div class="metric-lbl">State</div>
              <div class="metric-data" style="color: var(--accent-green); font-size: 11px;">[${{stock.state || 'ACTIVE_BREAKOUT'}}]</div>
            </div>
            <div class="metric-box">
              <div class="metric-lbl">Close Price</div>
              <div class="metric-data">₹${{stock.price}}</div>
            </div>
            <div class="metric-box">
              <div class="metric-lbl">Breakout Pivot</div>
              <div class="metric-data">₹${{stock.pivot_ref || stock.breakout_ref}}</div>
            </div>
            <div class="metric-box">
              <div class="metric-lbl">Volume Ratio</div>
              <div class="metric-data" style="color: var(--accent-green);">${{stock.volume_ratio || stock.rvol}}</div>
            </div>
            <div class="metric-box">
              <div class="metric-lbl">CRR (Close Strength)</div>
              <div class="metric-data">${{stock.crr || '0.85'}}</div>
            </div>
            <div class="metric-box">
              <div class="metric-lbl">NSE Delivery</div>
              <div class="metric-data">${{stock.delivery_pct}}</div>
            </div>
          </div>

          <!-- Trade Plan Box -->
          <div class="trade-plan">
            <div class="plan-line">
              <span class="plan-tag">🎯 ENTRY WINDOW</span>
              <span class="plan-val buy">Near Pivot Retest (Max Chase: 3.0%)</span>
            </div>
            <div class="plan-line">
              <span class="plan-tag">🛑 STRUCTURAL SL</span>
              <span class="plan-val sl">₹${{stock.structural_sl || (stock.price * 0.95).toFixed(1)}} (Risk: ${{stock.risk_pct || '4.5'}}%)</span>
            </div>
            <div class="plan-line">
              <span class="plan-tag">💰 TARGET 1 (2R)</span>
              <span class="plan-val t1">₹${{stock.t1_2r || (stock.price * 1.08).toFixed(1)}} (Exit 50% & Move SL to Cost)</span>
            </div>
            <div class="plan-line">
              <span class="plan-tag">🚀 TARGET 2 (3R)</span>
              <span class="plan-val t2">₹${{stock.t2_3r || (stock.price * 1.14).toFixed(1)}} (Exit Remaining 50%)</span>
            </div>
          </div>

          <div class="rationale-box">
            💡 ${{stock.rationale || 'High-volume breakout clearing 20D resistance with strong close and positive relative strength.'}}
          </div>

          <div class="card-footer">
            <span style="color: var(--text-dim); font-size: 11px;">
              1M Return: <b>+${{stock.ret_1m}}%</b> · MCap: <b>${{stock.mcap_cr}}</b>
            </span>
            <a href="https://in.tradingview.com/chart/?symbol=NSE:${{stock.symbol}}" target="_blank" class="tv-link">
              TradingView ↗
            </a>
          </div>
        </div>
      `).join('');
    }}

    /* =====================================================================
       RENDER TRADE AUDIT LEDGER TABLE
       ===================================================================== */
    function renderLedgerTable(data) {{
      const tbody = document.getElementById('ledger-table-body');
      const query = document.getElementById('search-input').value.toLowerCase().trim();

      // Apply Filters
      const filtered = data.filter(trade => {{
        // Status filter
        if (ledgerStatusFilter === 'ACTIVE' && !['ACTIVE', 'T1_HIT'].includes(trade.status)) return false;
        if (ledgerStatusFilter === 'PENDING_TRIGGER' && trade.status !== 'PENDING_TRIGGER') return false;
        if (ledgerStatusFilter === 'WINS' && !['T1_HIT', 'T2_HIT', 'STOPPED_OUT_BE'].includes(trade.status)) return false;
        if (ledgerStatusFilter === 'STOPPED_OUT_BE' && trade.status !== 'STOPPED_OUT_BE') return false;
        if (ledgerStatusFilter === 'LOSSES' && trade.status !== 'STOPPED_OUT') return false;

        // Track filter
        if (ledgerTrackFilter !== 'ALL' && trade.track !== ledgerTrackFilter) return false;

        // Search text
        if (query) {{
          const sym = (trade.symbol || '').toLowerCase();
          const name = (trade.name || '').toLowerCase();
          const sec = (trade.sector || '').toLowerCase();
          const notes = (trade.notes || '').toLowerCase();
          if (!sym.includes(query) && !name.includes(query) && !sec.includes(query) && !notes.includes(query)) {{
            return false;
          }}
        }}

        return true;
      }});

      if (!filtered || filtered.length === 0) {{
        tbody.innerHTML = `
          <tr>
            <td colspan="11" style="text-align: center; padding: 40px; color: var(--text-muted);">
              No trades found matching current filter/search criteria.
            </td>
          </tr>
        `;
        return;
      }}

      tbody.innerHTML = filtered.map(trade => {{
        // Status badge configuration
        let statusBadge = '';
        if (trade.status === 'ACTIVE') {{
          statusBadge = '<span class="status-badge status-active">🔵 ACTIVE</span>';
        }} else if (trade.status === 'PENDING_TRIGGER') {{
          statusBadge = '<span class="status-badge status-pending">🟡 PENDING TRIGGER</span>';
        }} else if (trade.status === 'T1_HIT') {{
          statusBadge = '<span class="status-badge status-t1">🟢 T1 HIT (+2R)</span>';
        }} else if (trade.status === 'T2_HIT') {{
          statusBadge = '<span class="status-badge status-t2">🚀 T2 HIT (+3R)</span>';
        }} else if (trade.status === 'STOPPED_OUT_BE') {{
          statusBadge = '<span class="status-badge status-be">🛡️ STOPPED BE (+0.8R)</span>';
        }} else if (trade.status === 'STOPPED_OUT') {{
          statusBadge = '<span class="status-badge status-sl">🔴 STOPPED OUT (-1R)</span>';
        }} else {{
          statusBadge = `<span class="status-badge status-expired">⚪ ${{trade.status}}</span>`;
        }}

        // PnL Styling
        const pnlPct = trade.pnl_pct || 0.0;
        const pnlR = trade.pnl_r || 0.0;
        let pnlClass = 'pnl-zero';
        let pnlSign = '';
        if (pnlR > 0) {{
          pnlClass = 'pnl-pos';
          pnlSign = '+';
        }} else if (pnlR < 0) {{
          pnlClass = 'pnl-neg';
        }}

        const displayPrice = trade.exit_price ? `₹${{trade.exit_price}}` : `₹${{trade.current_price}}`;
        const cleanSymbol = trade.symbol.replace('.NS', '');

        return `
          <tr>
            <td>
              <div class="sym-col">
                ${{cleanSymbol}}
                ${{trade.bucket ? `<span class="bucket-badge" style="margin: 0; font-size: 10px;">${{trade.bucket}}</span>` : ''}}
              </div>
              <div style="font-size: 11px; color: var(--text-muted);">${{trade.name}} · ${{trade.sector}}</div>
            </td>
            <td>
              <span style="font-weight: 700; color: ${{trade.track === 'Track A' ? 'var(--accent-green)' : 'var(--accent-purple)'}};">
                ${{trade.track === 'Track A' ? '🚀 Track A' : '💣 Track B'}}
              </span>
              <div style="font-size: 10px; color: var(--text-dim);">${{trade.signal_type}}</div>
            </td>
            <td class="mono" style="font-size: 12px; color: var(--text-muted);">
              ${{trade.detected_date}}
            </td>
            <td class="mono">
              <strong style="color: var(--accent-blue);">₹${{trade.entry_price}}</strong>
              <div style="font-size: 10px; color: var(--text-dim);">Trigger: ₹${{trade.entry_trigger || trade.signal_price}}</div>
            </td>
            <td class="mono" style="color: var(--accent-rose);">
              ₹${{trade.current_sl}}
              <div style="font-size: 10px; color: var(--text-dim);">Init: ₹${{trade.initial_sl}} (-${{trade.risk_pct}}%)</div>
            </td>
            <td class="mono">
              <div style="color: var(--accent-green); font-size: 12px;">T1: ₹${{trade.target_1_2r}} (+2R)</div>
              <div style="color: var(--accent-amber); font-size: 12px;">T2: ₹${{trade.target_2_3r}} (+3R)</div>
            </td>
            <td class="mono">
              <strong>${{displayPrice}}</strong>
              <div style="font-size: 10px; color: var(--text-dim);">Peak: ₹${{trade.max_price_seen || trade.current_price}}</div>
            </td>
            <td>
              ${{statusBadge}}
            </td>
            <td>
              <div class="pnl-pill ${{pnlClass}}">
                ${{pnlSign}}${{pnlPct}}%
              </div>
              <div class="mono" style="font-size: 11px; font-weight: 700; color: ${{pnlR > 0 ? 'var(--accent-green)' : (pnlR < 0 ? 'var(--accent-rose)' : 'var(--text-dim)')}};">
                ${{pnlSign}}${{pnlR.toFixed(2)}}R
              </div>
            </td>
            <td class="mono" style="font-size: 12px; color: var(--text-muted);">
              ${{trade.days_held}}d
            </td>
            <td>
              <a href="https://in.tradingview.com/chart/?symbol=NSE:${{cleanSymbol}}" target="_blank" class="tv-link" style="font-size: 12px;">
                Chart ↗
              </a>
            </td>
          </tr>
        `;
      }}).join('');
    }}

    function setLedgerStatusFilter(status) {{
      ledgerStatusFilter = status;
      ['all', 'active', 'pending', 'wins', 'be', 'losses'].forEach(k => {{
        const btn = document.getElementById(`pill-status-${{k}}`);
        if (btn) btn.classList.remove('active');
      }});
      if (status === 'ALL') document.getElementById('pill-status-all')?.classList.add('active');
      if (status === 'ACTIVE') document.getElementById('pill-status-active')?.classList.add('active');
      if (status === 'PENDING_TRIGGER') document.getElementById('pill-status-pending')?.classList.add('active');
      if (status === 'WINS') document.getElementById('pill-status-wins')?.classList.add('active');
      if (status === 'STOPPED_OUT_BE') document.getElementById('pill-status-be')?.classList.add('active');
      if (status === 'LOSSES') document.getElementById('pill-status-losses')?.classList.add('active');
      renderLedgerTable(tradesData);
    }}

    function setLedgerTrackFilter(track) {{
      ledgerTrackFilter = track;
      ['all', 'a', 'b'].forEach(k => {{
        const btn = document.getElementById(`pill-track-${{k}}`);
        if (btn) btn.classList.remove('active');
      }});
      if (track === 'ALL') document.getElementById('pill-track-all')?.classList.add('active');
      if (track === 'Track A') document.getElementById('pill-track-a')?.classList.add('active');
      if (track === 'Track B') document.getElementById('pill-track-b')?.classList.add('active');
      renderLedgerTable(tradesData);
    }}

    function switchTab(tab) {{
      currentTab = tab;
      const btnA = document.getElementById('tab-btn-a');
      const btnB = document.getElementById('tab-btn-b');
      const btnLedger = document.getElementById('tab-btn-ledger');
      const gridA = document.getElementById('grid-track-a');
      const gridB = document.getElementById('grid-track-b');
      const viewLedger = document.getElementById('view-ledger');
      const searchInput = document.getElementById('search-input');

      btnA.classList.remove('active');
      btnB.classList.remove('active');
      btnLedger.classList.remove('active');
      gridA.style.display = 'none';
      gridB.style.display = 'none';
      viewLedger.style.display = 'none';

      if (tab === 'b') {{
        btnB.classList.add('active');
        gridB.style.display = 'grid';
        searchInput.placeholder = "Search Track B by Symbol, Company Name, or Sector...";
        filterCards();
      }} else if (tab === 'a') {{
        btnA.classList.add('active');
        gridA.style.display = 'grid';
        searchInput.placeholder = "Search Track A by Symbol, Company Name, or Sector...";
        filterCards();
      }} else if (tab === 'ledger') {{
        btnLedger.classList.add('active');
        viewLedger.style.display = 'flex';
        searchInput.placeholder = "Search trade ledger by Symbol, Company, Sector, or Notes...";
        renderLedgerTable(tradesData);
      }}
    }}

    function filterCards() {{
      if (currentTab === 'ledger') {{
        renderLedgerTable(tradesData);
        return;
      }}

      const query = document.getElementById('search-input').value.toLowerCase().trim();
      const activeGridId = currentTab === 'b' ? 'grid-track-b' : 'grid-track-a';
      const cards = document.querySelectorAll(`#${{activeGridId}} .card`);

      cards.forEach(card => {{
        const sym = card.getAttribute('data-symbol').toLowerCase();
        const name = card.getAttribute('data-name').toLowerCase();
        const sector = card.getAttribute('data-sector').toLowerCase();
        if (sym.includes(query) || name.includes(query) || sector.includes(query)) {{
          card.style.display = 'flex';
        }} else {{
          card.style.display = 'none';
        }}
      }});
    }}

    // Initial render
    renderTrackBCards(trackBData);
    renderTrackACards(trackAData);
    renderLedgerTable(tradesData);
  </script>
</body>
</html>"""
    return html_content

def save_dashboard(active_breakouts, pre_breakout_squeezes, benchmark_indices=None, output_dir=None, total_scanned=651, trades=None, strategy_metrics=None):
    """Saves generated dashboard to docs/index.html and root dashboard.html."""
    if output_dir is None:
        output_dir = os.path.dirname(os.path.abspath(__file__))
    
    html = generate_html_dashboard(
        active_breakouts, pre_breakout_squeezes, benchmark_indices,
        total_scanned=total_scanned, trades=trades, strategy_metrics=strategy_metrics
    )
    
    # 1. Save to docs/index.html for GitHub Pages
    docs_path = os.path.join(output_dir, "docs", "index.html")
    os.makedirs(os.path.dirname(docs_path), exist_ok=True)
    with open(docs_path, "w", encoding="utf-8") as f:
        f.write(html)
        
    # 2. Also save to root dashboard.html for easy local double-click opening
    local_path = os.path.join(output_dir, "dashboard.html")
    with open(local_path, "w", encoding="utf-8") as f:
        f.write(html)
        
    return docs_path, local_path

if __name__ == "__main__":
    from trade_tracker import load_trade_ledger, compute_strategy_metrics
    t = load_trade_ledger()
    m = compute_strategy_metrics(t)
    p1, p2 = save_dashboard([], [], trades=t, strategy_metrics=m)
    print(f"Dashboard generated successfully at {p1} and {p2}")
