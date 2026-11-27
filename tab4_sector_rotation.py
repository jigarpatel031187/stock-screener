"""
Tab 4 Fragment Generator: Sector Rotation, Interactive JdK RRG & Astro-Quant Terminal.
Produces fully scoped CSS, HTML, and JS embedded inside #view-sector so it merges
cleanly into AntiGravity Dual Track Radar without colliding with Track A/B/Ledger.
"""

import json


def render_tab4_fragments(sector_rotation_data):
    """Returns (sr_css, sr_html, sr_js) ready for embedding into generate_dashboard.py."""
    payload_json = json.dumps(sector_rotation_data or {}, ensure_ascii=False).replace("</", "<\\/")

    sr_css = """
    /* =====================================================================
       TAB 4: SCOPED SECTOR ROTATION, JdK RRG & ASTRO-QUANT STYLES
       ===================================================================== */
    #view-sector {
      background: #070a0f;
      border: 1px solid #1d2738;
      border-radius: 14px;
      overflow: hidden;
      color: #e8eef5;
      font-size: 12.5px;
      box-shadow: 0 12px 35px rgba(0, 0, 0, 0.45);
    }
    #view-sector * { box-sizing: border-box; }
    #view-sector .sr-mono { font-family: 'JetBrains Mono', monospace; font-variant-numeric: tabular-nums; }
    #view-sector .sr-num { text-align: right !important; font-family: 'JetBrains Mono', monospace; font-variant-numeric: tabular-nums; }
    #view-sector .sr-pos { color: #00e676; }
    #view-sector .sr-neg { color: #ff3b5c; }
    #view-sector .sr-warn { color: #ffb300; }
    #view-sector .sr-info { color: #00d4ff; }
    #view-sector .sr-vio { color: #c084fc; }
    #view-sector .sr-muted { color: #8c99ad; }
    #view-sector .sr-bold { font-weight: 700; }

    /* Top Market Tape */
    #view-sector .sr-tape {
      background: #05070a;
      border-bottom: 1px solid #1d2738;
      padding: 8px 14px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      overflow-x: auto;
      white-space: nowrap;
    }
    #view-sector .sr-tape-group { display: flex; align-items: center; gap: 11px; }
    #view-sector .sr-tape-item { display: inline-flex; align-items: baseline; gap: 5px; font-family: 'JetBrains Mono', monospace; font-size: 11px; }
    #view-sector .sr-tape-lbl { color: #8c99ad; font-size: 10px; font-weight: 600; }
    #view-sector .sr-tape-val { color: #e8eef5; font-weight: 700; }
    #view-sector .sr-tape-div { width: 1px; height: 12px; background: #1d2738; }
    #view-sector .sr-live-badge {
      display: inline-flex; align-items: center; gap: 6px;
      padding: 2px 8px; border-radius: 4px;
      background: rgba(0, 230, 118, 0.1); border: 1px solid rgba(0, 230, 118, 0.35);
      color: #00e676; font-family: 'JetBrains Mono', monospace; font-size: 10px; font-weight: 700;
    }
    #view-sector .sr-pulse-dot { width: 6px; height: 6px; border-radius: 50%; background: #00e676; box-shadow: 0 0 6px #00e676; }

    /* Sub-Navigation Ribbon */
    #view-sector .sr-cmd-bar {
      background: #0d121a;
      border-bottom: 1px solid #1d2738;
      padding: 8px 14px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }
    #view-sector .sr-brand {
      font-family: 'JetBrains Mono', monospace; font-weight: 700; font-size: 12.5px; color: #00d4ff;
      display: flex; align-items: center; gap: 8px;
    }
    #view-sector .sr-ver-pill {
      font-size: 10px; padding: 1px 6px; border-radius: 3px;
      background: rgba(0, 212, 255, 0.12); border: 1px solid rgba(0, 212, 255, 0.35); color: #00d4ff;
    }
    #view-sector .sr-nav-tabs { display: flex; align-items: center; gap: 4px; flex-wrap: wrap; }
    #view-sector .sr-nav-tab {
      background: transparent; border: 1px solid transparent; color: #8c99ad;
      padding: 5px 9px; border-radius: 5px; cursor: pointer; font-size: 11.5px; font-weight: 500;
      display: inline-flex; align-items: center; gap: 5px; transition: all 0.15s; font-family: inherit;
    }
    #view-sector .sr-nav-tab:hover { background: #131a26; color: #e8eef5; border-color: #1d2738; }
    #view-sector .sr-nav-tab.active {
      background: rgba(0, 212, 255, 0.12); border-color: rgba(0, 212, 255, 0.45);
      color: #00d4ff; font-weight: 600;
    }
    #view-sector .sr-fkey {
      font-family: 'JetBrains Mono', monospace; font-size: 9.5px; padding: 1px 4px; border-radius: 3px;
      background: #070a0f; border: 1px solid #1d2738; color: #5c6a7e;
    }
    #view-sector .sr-nav-tab.active .sr-fkey { color: #00d4ff; border-color: rgba(0, 212, 255, 0.4); }

    #view-sector .sr-action-cluster { display: flex; align-items: center; gap: 6px; flex-wrap: wrap; }
    #view-sector .sr-btn {
      background: #131a26; border: 1px solid #1d2738; color: #e8eef5;
      padding: 5px 10px; border-radius: 5px; font-size: 11.5px; font-weight: 500; cursor: pointer;
      display: inline-flex; align-items: center; gap: 5px; transition: all 0.15s; font-family: inherit;
    }
    #view-sector .sr-btn:hover { border-color: #33435c; background: #1a2434; }
    #view-sector .sr-btn.active { background: rgba(0, 212, 255, 0.14); border-color: #00d4ff; color: #00d4ff; font-weight: 600; }
    #view-sector .sr-btn.cyan { background: #00d4ff; border-color: #00d4ff; color: #05090e; font-weight: 700; }
    #view-sector .sr-btn.cyan:hover { filter: brightness(1.08); }
    #view-sector .sr-btn.violet { background: rgba(168, 85, 247, 0.18); border-color: #a855f7; color: #e9d5ff; font-weight: 600; }
    #view-sector .sr-btn.amber { background: rgba(255, 179, 0, 0.14); border-color: #ffb300; color: #ffb300; font-weight: 600; }

    #view-sector .sr-input, #view-sector .sr-select {
      background: #090d14; border: 1px solid #1d2738; color: #e8eef5;
      padding: 5px 8px; border-radius: 5px; font-size: 11.5px; outline: none; font-family: inherit;
    }
    #view-sector .sr-input:focus, #view-sector .sr-select:focus { border-color: #00d4ff; }

    #view-sector .sr-workspace { padding: 12px 14px; }
    #view-sector .sr-tab-view { display: none; }
    #view-sector .sr-tab-view.active { display: block; }

    #view-sector .sr-panel {
      background: #0d121a; border: 1px solid #1d2738;
      border-radius: 6px; overflow: hidden; margin-bottom: 12px;
    }
    #view-sector .sr-panel-hdr {
      background: #131a26; border-bottom: 1px solid #1d2738;
      padding: 8px 12px; display: flex; justify-content: space-between; align-items: center; gap: 10px; flex-wrap: wrap;
    }
    #view-sector .sr-panel-title {
      font-family: 'JetBrains Mono', monospace; font-size: 11px; font-weight: 700; letter-spacing: 0.4px;
      text-transform: uppercase; color: #e8eef5; display: flex; align-items: center; gap: 7px;
    }
    #view-sector .sr-panel-body { padding: 12px; }

    #view-sector .sr-pill {
      display: inline-flex; align-items: center; gap: 4px; padding: 2px 6px; border-radius: 4px;
      font-family: 'JetBrains Mono', monospace; font-size: 10px; font-weight: 700; white-space: nowrap;
      border: 1px solid transparent;
    }
    #view-sector .pill-emerald { background: rgba(0, 230, 118, 0.12); color: #00e676; border-color: rgba(0, 230, 118, 0.35); }
    #view-sector .pill-cyan { background: rgba(0, 212, 255, 0.12); color: #00d4ff; border-color: rgba(0, 212, 255, 0.35); }
    #view-sector .pill-blue { background: rgba(59, 130, 246, 0.14); color: #60a5fa; border-color: rgba(59, 130, 246, 0.35); }
    #view-sector .pill-amber { background: rgba(255, 179, 0, 0.12); color: #ffb300; border-color: rgba(255, 179, 0, 0.35); }
    #view-sector .pill-crimson { background: rgba(255, 59, 92, 0.12); color: #ff3b5c; border-color: rgba(255, 59, 92, 0.35); }
    #view-sector .pill-violet { background: rgba(168, 85, 247, 0.15); color: #d8b4fe; border-color: rgba(168, 85, 247, 0.38); }
    #view-sector .pill-p3 {
      background: rgba(232, 121, 249, 0.16); color: #f5d0fe; border-color: rgba(232, 121, 249, 0.78);
      box-shadow: 0 0 8px rgba(232, 121, 249, 0.28);
    }
    #view-sector .pill-p2 {
      background: rgba(168, 85, 247, 0.16); color: #e9d5ff; border-color: rgba(168, 85, 247, 0.62);
    }
    #view-sector .pill-p1 {
      background: rgba(56, 189, 248, 0.12); color: #bae6fd; border-color: rgba(56, 189, 248, 0.52);
    }
    #view-sector .pill-neutral { background: #121822; color: #8c99ad; border-color: #1d2738; }

    #view-sector .sr-sm-radar-bar {
      background: linear-gradient(90deg, rgba(232, 121, 249, 0.11), rgba(168, 85, 247, 0.08), rgba(56, 189, 248, 0.06), rgba(13, 18, 26, 0.96));
      border: 1px solid rgba(232, 121, 249, 0.52); border-radius: 6px;
      padding: 9px 12px; margin-bottom: 12px; display: flex; flex-direction: column; gap: 7px;
      box-shadow: 0 0 14px rgba(232, 121, 249, 0.10);
    }

    #view-sector .sr-gann-pill {
      display: inline-flex; align-items: center; gap: 4px; padding: 2px 6px; border-radius: 4px;
      background: rgba(255, 179, 0, 0.08); border: 1px dashed rgba(255, 179, 0, 0.5);
      color: #ffb300; font-family: 'JetBrains Mono', monospace; font-size: 10px; font-weight: 600;
    }

    #view-sector .sr-kpi-strip { display: grid; grid-template-columns: repeat(auto-fit, minmax(195px, 1fr)); gap: 10px; margin-bottom: 12px; }
    #view-sector .sr-kpi-card {
      background: #0d121a; border: 1px solid #1d2738; border-radius: 6px;
      padding: 10px 12px; display: flex; flex-direction: column; gap: 3px;
    }
    #view-sector .sr-kpi-lbl { font-family: 'JetBrains Mono', monospace; font-size: 10px; color: #8c99ad; text-transform: uppercase; }
    #view-sector .sr-kpi-val { font-family: 'JetBrains Mono', monospace; font-size: 15px; font-weight: 700; }
    #view-sector .sr-kpi-sub { font-family: 'JetBrains Mono', monospace; font-size: 10.5px; color: #8c99ad; }

    #view-sector .sr-grid-rrg { display: grid; grid-template-columns: 1.48fr 1fr; gap: 12px; align-items: start; }
    #view-sector .sr-grid-main { display: grid; grid-template-columns: 1.35fr 1fr; gap: 12px; align-items: start; }
    #view-sector .sr-grid-equal { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; align-items: start; }
    @media (max-width: 1180px) {
      #view-sector .sr-grid-rrg,
      #view-sector .sr-grid-main,
      #view-sector .sr-grid-equal { grid-template-columns: 1fr; }
    }

    #view-sector .sr-cap-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(195px, 1fr)); gap: 8px; }
    #view-sector .sr-cap-card {
      background: #070a0f; border: 1px solid #1d2738; border-radius: 5px;
      padding: 8px 10px; cursor: pointer; transition: border-color 0.15s, transform 0.12s;
    }
    #view-sector .sr-cap-card:hover { border-color: #00d4ff; transform: translateY(-1px); }
    #view-sector .sr-cap-card.sr-cap-p3 {
      border-color: rgba(232, 121, 249, 0.78); background: rgba(232, 121, 249, 0.08);
      box-shadow: 0 0 12px rgba(232, 121, 249, 0.18), inset 3px 0 0 #e879f9;
    }
    #view-sector .sr-cap-card.sr-cap-p2 {
      border-color: rgba(168, 85, 247, 0.62); background: rgba(168, 85, 247, 0.07);
      box-shadow: inset 3px 0 0 #a855f7;
    }
    #view-sector .sr-cap-card.sr-cap-p1 {
      border-color: rgba(56, 189, 248, 0.50); background: rgba(56, 189, 248, 0.05);
      box-shadow: inset 3px 0 0 #38bdf8;
    }

    #view-sector .sr-breadcrumb {
      background: linear-gradient(90deg, rgba(0, 212, 255, 0.14), rgba(168, 85, 247, 0.1));
      border: 1px solid rgba(0, 212, 255, 0.48);
      border-radius: 6px; padding: 8px 12px; margin-bottom: 12px;
      display: flex; justify-content: space-between; align-items: center; gap: 10px; flex-wrap: wrap;
    }

    #view-sector .sr-canvas-wrap {
      background: #05080c; position: relative; display: flex; justify-content: center; align-items: center; overflow: hidden;
    }
    #view-sector canvas { display: block; width: 100%; height: auto; cursor: grab; }
    #view-sector canvas:active { cursor: grabbing; }

    #view-sector .sr-zoom-hud {
      position: absolute; bottom: 10px; left: 10px; display: flex; align-items: center; gap: 5px;
      background: rgba(13, 18, 26, 0.9); border: 1px solid #1d2738;
      padding: 4px 8px; border-radius: 5px; font-family: 'JetBrains Mono', monospace; font-size: 10px;
    }

    #view-sector .sr-dock-list {
      max-height: 545px; overflow-y: auto; padding: 8px; display: flex; flex-direction: column; gap: 6px;
    }
    #view-sector .sr-dock-hdr {
      font-family: 'JetBrains Mono', monospace; font-size: 10px; font-weight: 700; color: #00d4ff;
      padding: 4px 4px 3px 4px; border-bottom: 1px solid #1d2738; text-transform: uppercase;
      display: flex; justify-content: space-between;
    }
    #view-sector .sr-dock-card {
      background: #070a0f; border: 1px solid #1d2738; border-radius: 5px;
      padding: 7px 9px; cursor: pointer; transition: all 0.14s;
    }
    #view-sector .sr-dock-card:hover { border-color: #00d4ff; background: #131a26; }
    #view-sector .sr-dock-card.highlighted { border-color: #00d4ff; background: rgba(0, 212, 255, 0.1); box-shadow: inset 3px 0 0 #00d4ff; }
    #view-sector .sr-dock-card.sr-dock-p3 { border-color: rgba(232, 121, 249, 0.72); background: rgba(232, 121, 249, 0.07); box-shadow: inset 3px 0 0 #e879f9; }
    #view-sector .sr-dock-card.sr-dock-p2 { border-color: rgba(168, 85, 247, 0.58); background: rgba(168, 85, 247, 0.06); box-shadow: inset 3px 0 0 #a855f7; }
    #view-sector .sr-dock-card.sr-dock-p1 { border-color: rgba(56, 189, 248, 0.48); background: rgba(56, 189, 248, 0.045); box-shadow: inset 3px 0 0 #38bdf8; }

    #view-sector .sr-flow-track { height: 5px; background: #162030; border-radius: 3px; overflow: hidden; margin-top: 4px; }
    #view-sector .sr-flow-pos { height: 100%; background: #00e676; }
    #view-sector .sr-flow-neg { height: 100%; background: #ff3b5c; }

    #view-sector .sr-table-wrap { width: 100%; overflow-x: auto; }
    #view-sector table.sr-table { width: 100%; border-collapse: collapse; font-size: 11.5px; }
    #view-sector table.sr-table th {
      text-align: left; padding: 8px 9px; background: #090d14;
      border-bottom: 1px solid #33435c; color: #8c99ad;
      font-family: 'JetBrains Mono', monospace; font-size: 10px; font-weight: 700; text-transform: uppercase;
      white-space: nowrap; cursor: pointer; user-select: none;
    }
    #view-sector table.sr-table th:hover { color: #00d4ff; }
    #view-sector table.sr-table td {
      padding: 7px 9px; border-bottom: 1px solid #141c28; white-space: nowrap; vertical-align: middle;
    }
    #view-sector table.sr-table tr:hover td { background: rgba(0, 212, 255, 0.045); }
    #view-sector table.sr-table tr.sr-row-p3 td { background: rgba(232, 121, 249, 0.075); }
    #view-sector table.sr-table tr.sr-row-p3 td:first-child { border-left: 3px solid #e879f9; }
    #view-sector table.sr-table tr.sr-row-p2 td { background: rgba(168, 85, 247, 0.055); }
    #view-sector table.sr-table tr.sr-row-p2 td:first-child { border-left: 3px solid #a855f7; }
    #view-sector table.sr-table tr.sr-row-p1 td { background: rgba(56, 189, 248, 0.04); }
    #view-sector table.sr-table tr.sr-row-p1 td:first-child { border-left: 3px solid #38bdf8; }
    #view-sector .sr-row-click { cursor: pointer; }
    #view-sector .sr-ticker-btn { font-family: 'JetBrains Mono', monospace; font-weight: 700; color: #e8eef5; cursor: pointer; }
    #view-sector .sr-ticker-btn:hover { color: #00d4ff; text-decoration: underline; }

    #view-sector .sr-meth-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 10px; }
    #view-sector .sr-meth-card {
      background: #070a0f; border: 1px solid #1d2738; border-radius: 5px;
      padding: 10px 12px; font-size: 11.5px; line-height: 1.52;
    }
    #view-sector .sr-meth-card h4 { font-family: 'JetBrains Mono', monospace; font-size: 10.5px; color: #00d4ff; margin-bottom: 5px; text-transform: uppercase; }
    #view-sector .sr-formula-box {
      background: #06090e; border: 1px solid #1c2636; border-radius: 4px;
      padding: 5px 8px; margin: 4px 0; font-family: 'JetBrains Mono', monospace; font-size: 10.5px; color: #e2e8f0;
    }

    #view-sector .sr-editable { border-bottom: 1px dashed #475569; padding: 1px 4px; cursor: text; }
    #view-sector .sr-editable:hover { background: #182232; border-bottom-color: #00d4ff; }
    #view-sector .sr-editable:focus { outline: 1px solid #00d4ff; background: #070a0f; }

    #view-sector .sr-eph-strip { display: grid; grid-template-columns: repeat(auto-fit, minmax(145px, 1fr)); gap: 7px; }
    #view-sector .sr-eph-box {
      background: #070a0f; border: 1px solid #1d2738; border-radius: 5px;
      padding: 7px 9px; font-family: 'JetBrains Mono', monospace; font-size: 10.5px;
    }
    #view-sector .sr-syn-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 8px; }
    #view-sector .sr-syn-card { background: #070a0f; border: 1px solid #1d2738; border-radius: 5px; padding: 9px 11px; font-size: 11.5px; line-height: 1.45; }
    #view-sector .sr-tg-box {
      background: #06090d; border: 1px solid #1d2738; border-radius: 5px; padding: 12px;
      font-family: 'JetBrains Mono', monospace; font-size: 11.5px; line-height: 1.55; white-space: pre-wrap;
      max-height: 410px; overflow-y: auto; color: #d1d9e0;
    }

    #view-sector .sr-switch { position: relative; display: inline-block; width: 34px; height: 18px; }
    #view-sector .sr-switch input { opacity: 0; width: 0; height: 0; }
    #view-sector .sr-slider { position: absolute; cursor: pointer; inset: 0; background: #263244; border-radius: 18px; transition: 0.2s; }
    #view-sector .sr-slider:before { position: absolute; content: ""; height: 12px; width: 12px; left: 3px; bottom: 3px; background: #fff; border-radius: 50%; transition: 0.2s; }
    #view-sector input:checked + .sr-slider { background: #a855f7; }
    #view-sector input:checked + .sr-slider:before { transform: translateX(16px); }

    #view-sector .sr-modal-bg {
      display: none; position: fixed; inset: 0; background: rgba(4, 7, 11, 0.84);
      backdrop-filter: blur(4px); z-index: 4000; justify-content: center; align-items: center; padding: 16px;
    }
    #view-sector .sr-modal-box {
      background: #0d121a; border: 1px solid #00d4ff; border-radius: 8px;
      width: 920px; max-width: 100%; max-height: 92vh; display: flex; flex-direction: column; overflow: hidden;
      box-shadow: 0 24px 60px rgba(0, 0, 0, 0.88);
    }
    #view-sector .sr-modal-body { padding: 14px; overflow-y: auto; }

    #view-sector .sr-hud-tip {
      position: fixed; background: rgba(9, 13, 20, 0.97); border: 1px solid #00d4ff;
      border-radius: 6px; padding: 9px 12px; font-family: 'JetBrains Mono', monospace; font-size: 11px;
      pointer-events: none; z-index: 5000; display: none; min-width: 260px;
      box-shadow: 0 10px 28px rgba(0, 0, 0, 0.88); color: #e8eef5;
    }

    #view-sector .sr-toast {
      position: fixed; bottom: 24px; right: 16px; background: #131a26;
      border: 1px solid #00d4ff; color: #e8eef5; font-family: 'JetBrains Mono', monospace;
      font-size: 11.5px; padding: 8px 14px; border-radius: 6px; z-index: 6000;
      opacity: 0; transform: translateY(10px); pointer-events: none; transition: all 0.2s;
    }
    #view-sector .sr-toast.show { opacity: 1; transform: translateY(0); }

    #view-sector .sr-footer-bar {
      background: #05070a; border-top: 1px solid #1d2738; padding: 6px 14px;
      display: flex; justify-content: space-between; align-items: center; font-family: 'JetBrains Mono', monospace;
      font-size: 10px; color: #8c99ad; overflow-x: auto; white-space: nowrap; gap: 12px;
    }
    """

    sr_html = """
    <div id="view-sector" style="display: none;">
      <!-- Top Institutional Market Tape -->
      <div class="sr-tape">
        <div class="sr-tape-group">
          <div class="sr-tape-item"><span class="sr-tape-lbl">NIFTY 50</span><span class="sr-tape-val" id="sr-tape-nifty">--</span><span id="sr-tape-nifty-chg">--</span></div>
          <div class="sr-tape-div"></div>
          <div class="sr-tape-item"><span class="sr-tape-lbl">SENSEX</span><span class="sr-tape-val" id="sr-tape-sensex">--</span><span id="sr-tape-sensex-chg">--</span></div>
          <div class="sr-tape-div"></div>
          <div class="sr-tape-item"><span class="sr-tape-lbl">NIFTY BANK</span><span class="sr-tape-val" id="sr-tape-bank">--</span><span id="sr-tape-bank-chg">--</span></div>
          <div class="sr-tape-div"></div>
          <div class="sr-tape-item"><span class="sr-tape-lbl">INDIA VIX</span><span class="sr-tape-val" id="sr-tape-vix">--</span><span id="sr-tape-vix-chg">--</span></div>
          <div class="sr-tape-div"></div>
          <div class="sr-tape-item"><span class="sr-tape-lbl">USD/INR</span><span class="sr-tape-val" id="sr-tape-usdinr">--</span><span id="sr-tape-usdinr-chg">--</span></div>
          <div class="sr-tape-div"></div>
          <div class="sr-tape-item"><span class="sr-tape-lbl">UNIVERSE BREADTH</span><span class="sr-pos" id="sr-tape-adv">-- Adv</span><span class="sr-muted">/</span><span class="sr-neg" id="sr-tape-dec">-- Dec</span></div>
        </div>
        <div class="sr-tape-group">
          <div class="sr-tape-item"><span class="sr-tape-lbl">FII CASH</span><span class="sr-bold" id="sr-hdr-fii">Live / EOD</span></div>
          <div class="sr-tape-div"></div>
          <div class="sr-tape-item"><span class="sr-tape-lbl">DII CASH</span><span class="sr-bold" id="sr-hdr-dii">Live / EOD</span></div>
          <div class="sr-tape-div"></div>
          <div class="sr-live-badge"><span class="sr-pulse-dot"></span><span id="sr-hdr-date">Live EOD</span></div>
        </div>
      </div>

      <!-- Command Ribbon & F1-F6 Sub-Tabs -->
      <div class="sr-cmd-bar">
        <div style="display:flex; align-items:center; gap:12px; flex-wrap:wrap;">
          <div class="sr-brand">◈ NSE SECTOR ROTATION, JdK RRG &amp; ASTRO-QUANT <span class="sr-ver-pill">v5.0 LIVE</span></div>
          <div class="sr-nav-tabs">
            <button class="sr-nav-tab active" data-srtab="f1" onclick="SR.app.switchTab('f1')"><span class="sr-fkey">F1</span> Overview</button>
            <button class="sr-nav-tab" data-srtab="f2" onclick="SR.app.switchTab('f2')"><span class="sr-fkey">F2</span> Interactive RRG &amp; Drill-Down</button>
            <button class="sr-nav-tab" data-srtab="f3" onclick="SR.app.switchTab('f3')"><span class="sr-fkey">F3</span> Alpha &amp; Breadth Heatmap</button>
            <button class="sr-nav-tab" data-srtab="f4" onclick="SR.app.switchTab('f4')"><span class="sr-fkey">F4</span> Fair Value Screener</button>
            <button class="sr-nav-tab" data-srtab="f5" onclick="SR.app.switchTab('f5')"><span class="sr-fkey">F5</span> 1-2M &amp; 8-12M Trade Plan</button>
            <button class="sr-nav-tab" data-srtab="f6" onclick="SR.app.switchTab('f6')"><span class="sr-fkey">F6</span> Astro-Quant &amp; Broadcast</button>
          </div>
        </div>

        <div class="sr-action-cluster">
          <input type="text" id="sr-quick-search" class="sr-input sr-mono" style="width:185px;" placeholder="Jump Ticker / Sector..." onkeydown="if(event.key==='Enter') SR.app.quickJump(this.value)">
          <button class="sr-btn amber" onclick="SR.methodologyModal.open()">📐 Buy/SL/Target Logic</button>
          <button class="sr-btn cyan" onclick="SR.csvModal.open()">⬆ EOD CSV</button>
        </div>
      </div>

      <!-- Main Tab 4 Workspace -->
      <div class="sr-workspace">

        <!-- [F1] COMMAND OVERVIEW -->
        <section id="sr-view-f1" class="sr-tab-view active">
          <div class="sr-kpi-strip">
            <div class="sr-kpi-card">
              <span class="sr-kpi-lbl">Market Breadth &amp; VIX</span>
              <span class="sr-kpi-val sr-pos" id="sr-f1-regime">LIVE BREADTH</span>
              <span class="sr-kpi-sub" id="sr-f1-regime-sub">--</span>
            </div>
            <div class="sr-kpi-card">
              <span class="sr-kpi-lbl">Cap-Tier Rotation Leader</span>
              <span class="sr-kpi-val sr-info" id="sr-f1-cap-leader">--</span>
              <span class="sr-kpi-sub" id="sr-f1-cap-sub">--</span>
            </div>
            <div class="sr-kpi-card">
              <span class="sr-kpi-lbl">Leading / Improving Sectors</span>
              <span class="sr-kpi-val sr-pos" id="sr-f1-quad-count">--</span>
              <span class="sr-kpi-sub" id="sr-f1-quad-sub">--</span>
            </div>
            <div class="sr-kpi-card">
              <span class="sr-kpi-lbl">24-Stock Intrinsic Fair Value</span>
              <span class="sr-kpi-val sr-pos" id="sr-f1-fv-kpi">--</span>
              <span class="sr-kpi-sub">P/B-ROE, EV/EBITDA+DCF &amp; Fwd P/E+PEG</span>
            </div>
            <div class="sr-kpi-card">
              <span class="sr-kpi-lbl">Astro-Quant Seg-3 Routing</span>
              <span class="sr-kpi-val sr-vio">KRITIKA &amp; VINA ACTIVE</span>
              <span class="sr-kpi-sub">Jigar &amp; Dipak VETOED till Dec 5</span>
            </div>
          </div>

          <div id="sr-f1-sm-bar" class="sr-sm-radar-bar" style="display:none;"></div>

          <div class="sr-panel">
            <div class="sr-panel-hdr">
              <span class="sr-panel-title">◆ MARKET-CAP &amp; BENCHMARK ROTATION (CLICK ANY CAP INDEX TO LAUNCH CONSTITUENT STOCK RRG)</span>
              <button class="sr-btn" onclick="SR.app.openCapInRRG()">Open Cap Indices in RRG [F2] →</button>
            </div>
            <div class="sr-panel-body">
              <div id="sr-f1-cap-grid" class="sr-cap-grid"></div>
            </div>
          </div>

          <div class="sr-grid-main">
            <div class="sr-panel">
              <div class="sr-panel-hdr">
                <span class="sr-panel-title">◎ CURATED JdK RRG OVERVIEW (CLICK ANY NODE TO DRILL INTO STOCK RRG)</span>
                <button class="sr-btn cyan" onclick="SR.app.switchTab('f2')">Full Interactive RRG [F2] →</button>
              </div>
              <div class="sr-canvas-wrap">
                <canvas id="sr-f1-rrg-canvas" width="660" height="400"></canvas>
              </div>
            </div>

            <div class="sr-panel">
              <div class="sr-panel-hdr">
                <span class="sr-panel-title">⚡ 7 DUAL-HORIZON GEMS — 1-2M SWING &amp; 8-12M FAIR VALUE</span>
                <button class="sr-btn" onclick="SR.app.switchTab('f5')">Trade Plan &amp; Formulas [F5] →</button>
              </div>
              <div class="sr-table-wrap">
                <table class="sr-table">
                  <thead>
                    <tr>
                      <th>Ticker</th>
                      <th class="sr-num">Live CMP</th>
                      <th>Entry Zone</th>
                      <th class="sr-num">Hard SL</th>
                      <th class="sr-num">1-2M T1</th>
                      <th class="sr-num">12M FV</th>
                      <th>Seg-3</th>
                    </tr>
                  </thead>
                  <tbody id="sr-f1-gems-tbody"></tbody>
                </table>
              </div>
            </div>
          </div>
        </section>

        <!-- [F2] INTERACTIVE SECTOR & STOCK RRG -->
        <section id="sr-view-f2" class="sr-tab-view">
          <div class="sr-breadcrumb">
            <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;" class="sr-mono">
              <span class="sr-pill pill-cyan" id="sr-rrg-mode-badge">MACRO SECTOR &amp; CAP RRG</span>
              <span id="sr-rrg-crumb-trail" style="font-size:11.5px; font-weight:700;">All Sectors &amp; Cap Indices</span>
            </div>
            <div style="display:flex; align-items:center; gap:8px;" id="sr-rrg-crumb-actions">
              <span class="sr-muted sr-mono" style="font-size:10.5px;">Click any sector/index node or row to drill into live Constituent Stock RRG</span>
            </div>
          </div>

          <div class="sr-panel">
            <div class="sr-panel-hdr">
              <div style="display:flex; align-items:center; gap:6px; flex-wrap:wrap;" id="sr-rrg-macro-filters">
                <span class="sr-panel-title">UNIVERSE:</span>
                <select id="sr-rrg-universe-select" class="sr-select" onchange="SR.rrgEngine.setUniverse(this.value)">
                  <option value="curated_10">Curated Leaders &amp; Market Cap Indices</option>
                  <option value="all_23" selected>All NSE Sectors + Market Cap Indices</option>
                  <option value="sm_active">🏦 Smart Money Active (All 3 Phases)</option>
                  <option value="sm_p3">★ Phase 3: Markup Ready Only</option>
                  <option value="sm_p2">◈ Phase 2: Supply Absorption Only</option>
                  <option value="sm_p1">◎ Phase 1: Early Base Only</option>
                  <option value="cap_5">Market Cap Indices Only (5 Nodes)</option>
                  <option value="sectors_18">All NSE Sectors Only</option>
                  <option value="leading_only">Leading Quadrant Only</option>
                  <option value="improving_only">Improving Quadrant Only</option>
                </select>
                <button class="sr-btn active" id="sr-rrg-tf-daily" onclick="SR.rrgEngine.setTimeframe('daily')">Daily</button>
                <button class="sr-btn" id="sr-rrg-tf-weekly" onclick="SR.rrgEngine.setTimeframe('weekly')">Weekly</button>
              </div>

              <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
                <div style="display:flex; align-items:center; gap:4px;">
                  <span class="sr-mono sr-muted" style="font-size:10px;">LABELS:</span>
                  <select id="sr-rrg-label-mode" class="sr-select" onchange="SR.rrgEngine.setLabelMode(this.value)">
                    <option value="all">All (De-Overlapped)</option>
                    <option value="top">Top Movers + Active</option>
                    <option value="hover">Hover / Active Only</option>
                  </select>
                </div>
                <div style="display:flex; align-items:center; gap:5px;" class="sr-mono">
                  <span class="sr-muted" style="font-size:10px;">TRAIL:</span>
                  <input type="range" id="sr-rrg-trail-slider" min="3" max="16" value="8" style="width:82px;" oninput="SR.rrgEngine.setTrail(this.value)">
                  <span id="sr-rrg-trail-val" class="sr-info sr-bold" style="font-size:11px;">8</span>
                </div>
                <button class="sr-btn" id="sr-rrg-play-btn" onclick="SR.rrgEngine.togglePlay()">▶ Play</button>
                <button class="sr-btn" onclick="SR.rrgEngine.resetZoom()">⌖ Reset Zoom</button>
              </div>
            </div>
          </div>

          <div class="sr-grid-rrg">
            <div class="sr-panel">
              <div class="sr-panel-hdr">
                <span class="sr-panel-title" id="sr-rrg-canvas-title">JdK RELATIVE ROTATION GRAPH — SCROLL TO ZOOM • DRAG TO PAN • CLICK NODE FOR STOCK RRG</span>
                <span class="sr-mono sr-muted" style="font-size:10px;">◆ Cap | ● Sector | <span style="color:#e879f9;">★ P3 Markup</span> · <span style="color:#c084fc;">◈ P2 Absorp</span> · <span style="color:#38bdf8;">◎ P1 Base</span></span>
              </div>
              <div class="sr-canvas-wrap">
                <canvas id="sr-main-rrg-canvas" width="840" height="550"></canvas>
                <div class="sr-zoom-hud">
                  <span class="sr-muted">ZOOM:</span>
                  <span id="sr-rrg-zoom-lbl" class="sr-info sr-bold">100%</span>
                  <button class="sr-btn" style="padding:1px 6px; font-size:10px;" onclick="SR.rrgEngine.zoomBy(1.2)">+</button>
                  <button class="sr-btn" style="padding:1px 6px; font-size:10px;" onclick="SR.rrgEngine.zoomBy(0.83)">−</button>
                  <button class="sr-btn" style="padding:1px 6px; font-size:10px;" onclick="SR.rrgEngine.resetZoom()">Reset</button>
                </div>
              </div>
            </div>

            <div class="sr-panel">
              <div class="sr-panel-hdr">
                <span class="sr-panel-title sr-info" id="sr-dock-title">SECTOR &amp; CAP ROTATION DIRECTORY</span>
                <span class="sr-mono sr-muted" id="sr-dock-subtitle" style="font-size:10px;">Hover to isolate • Click to drill</span>
              </div>
              <div id="sr-dock-context-bar" style="padding:7px 10px; background:#090d14; border-bottom:1px solid #1d2738; font-size:11px; display:none;"></div>
              <div id="sr-rrg-right-list" class="sr-dock-list"></div>
            </div>
          </div>
        </section>

        <!-- [F3] ALPHA & BREADTH HEATMAP -->
        <section id="sr-view-f3" class="sr-tab-view">
          <div class="sr-panel">
            <div class="sr-panel-hdr">
              <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
                <span class="sr-panel-title">▤ LIVE ALPHA, BREADTH &amp; BREAKOUT DENSITY HEATMAP</span>
                <button class="sr-btn active" id="sr-hm-btn-abs" onclick="SR.heatmapEngine.setMetric('abs')">Absolute % Return</button>
                <button class="sr-btn" id="sr-hm-btn-alpha" onclick="SR.heatmapEngine.setMetric('alpha')">Alpha vs NIFTY 50</button>
                <select id="sr-hm-filter-type" class="sr-select" onchange="SR.heatmapEngine.render()">
                  <option value="all">All Sectors &amp; Cap Indices</option>
                  <option value="sm_active">🏦 Smart Money Active (Phase 1–3)</option>
                  <option value="sm_p3">★ Phase 3: Markup Ready Only</option>
                  <option value="cap">Market Cap &amp; Benchmark Indices</option>
                  <option value="sector">NSE Sectors Only</option>
                </select>
              </div>
              <span class="sr-mono sr-muted" style="font-size:10.5px;">Click column headers to sort • Click any row to launch Constituent Stock RRG</span>
            </div>
            <div class="sr-table-wrap" id="sr-heatmap-table-wrap"></div>
          </div>
        </section>

        <!-- [F4] INTRINSIC FAIR VALUE SCREENER -->
        <section id="sr-view-f4" class="sr-tab-view">
          <div class="sr-panel">
            <div class="sr-panel-hdr">
              <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
                <span class="sr-panel-title">⚖ INTRINSIC VALUATION &amp; GROWTH FAIR VALUE SCREENER (24 EQUITIES, LIVE CMP)</span>
                <span class="sr-gann-pill">Gann Sq9 Shown Strictly as Non-Execution Reference</span>
              </div>
              <span id="sr-f4-count" class="sr-mono sr-info" style="font-size:11px;">24 Stocks</span>
            </div>
            <div class="sr-panel-body" style="border-bottom:1px solid #1d2738; display:flex; gap:8px; flex-wrap:wrap; align-items:center;">
              <select id="sr-f4-sec-flt" class="sr-select" onchange="SR.screenerEngine.render()"></select>
              <select id="sr-f4-verdict-flt" class="sr-select" onchange="SR.screenerEngine.render()">
                <option value="ALL">All Fair Value Verdicts</option>
                <option value="UNDERVALUED">UNDERVALUED</option>
                <option value="FAIRLY VALUED">FAIRLY VALUED</option>
                <option value="GROWTH PREMIUM / GARP">GROWTH PREMIUM / GARP</option>
                <option value="RICH / STAGGERED BUY">RICH / STAGGERED BUY</option>
              </select>
              <select id="sr-f4-sort" class="sr-select" onchange="SR.screenerEngine.render()">
                <option value="mos">Sort: Fair Value Upside % (High-Low)</option>
                <option value="sm">Sort: Smart Money Score (High-Low)</option>
                <option value="peg">Sort: PEG Ratio (Low-High)</option>
                <option value="cagr">Sort: 3Y EPS CAGR % (High-Low)</option>
                <option value="ticker">Sort: Ticker (A-Z)</option>
              </select>
              <input type="text" id="sr-f4-search" class="sr-input" style="flex:1; min-width:180px;" placeholder="Search ticker, sector, valuation model..." oninput="SR.screenerEngine.render()">
            </div>
            <div class="sr-table-wrap">
              <table class="sr-table">
                <thead>
                  <tr>
                    <th>Ticker / Sector</th>
                    <th>Valuation Model</th>
                    <th class="sr-num">Live CMP (₹)</th>
                    <th class="sr-num">Fwd FY28E</th>
                    <th class="sr-num">Sec Med</th>
                    <th class="sr-num">PEG</th>
                    <th class="sr-num">3Y CAGR</th>
                    <th class="sr-num">ROE / ROCE</th>
                    <th class="sr-num">Intrinsic FV</th>
                    <th class="sr-num">Upside %</th>
                    <th>Fair Value Verdict</th>
                    <th class="sr-num">Net FII+DII</th>
                    <th>Gann Ref (Non-Exec)</th>
                  </tr>
                </thead>
                <tbody id="sr-f4-tbody"></tbody>
              </table>
            </div>
          </div>
        </section>

        <!-- [F5] 1-2M & 8-12M TRADE PLAN -->
        <section id="sr-view-f5" class="sr-tab-view">
          <div class="sr-panel" style="border-color: rgba(0, 212, 255, 0.42);">
            <div class="sr-panel-hdr" style="background: linear-gradient(90deg, rgba(0,212,255,0.12), #131a26);">
              <span class="sr-panel-title sr-info">📐 TRANSPARENT BUY, HARD SL &amp; TARGET FORMULA ENGINE (1–2M SWING vs. 8–12M CORE)</span>
              <div style="display:flex; gap:6px;">
                <button class="sr-btn active" id="sr-btn-toggle-formulas" onclick="SR.execEngine.toggleFormulaDrawer()">Hide Formula Cards</button>
                <button class="sr-btn amber" onclick="SR.methodologyModal.open()">Full Audit Modal</button>
              </div>
            </div>
            <div class="sr-panel-body" id="sr-f5-formula-drawer">
              <div class="sr-meth-grid">
                <div class="sr-meth-card">
                  <h4>⚡ 1–2 Month Swing Logic (Momentum &amp; ATR)</h4>
                  <div class="sr-formula-box">Entry = [20-DMA / Breakout Retest, CMP + 0.5×ATR(14)]</div>
                  <div class="sr-formula-box">Hard SL = Swing Low − 1.5×ATR(14) (Capped 5%–8%)</div>
                  <div class="sr-formula-box">T1 = Entry Mid + 2.0×Risk | T2 = Entry Mid + 3.5×Risk</div>
                  <div class="sr-muted" style="font-size:10.5px;">Never chases &gt;1.5×ATR above 20-DMA. T1 locks 2:1 R:R partial gain; T2 captures Fibonacci 1.618 extension.</div>
                </div>
                <div class="sr-meth-card">
                  <h4>🏛 8–12 Month Core Logic (Intrinsic Fair Value)</h4>
                  <div class="sr-formula-box">Entry = [Intrinsic FV × 0.85, Intrinsic FV × 0.95] / 150-DMA</div>
                  <div class="sr-formula-box">Dual Stop = 150-DMA − 1×ATR OR Fundamental KPI Breach</div>
                  <div class="sr-formula-box">Base = FY28E EPS × Justified P/E | Bull = +15% Rerating</div>
                  <div class="sr-muted" style="font-size:10.5px;">Banks use FY28E BVPS × Justified P/B; Telecom/Auto use EV/EBITDA + DCF; IT/Exchanges use Fwd P/E + PEG.</div>
                </div>
                <div class="sr-meth-card" style="border-color:rgba(168,85,247,0.4);">
                  <h4 style="color:#c084fc;">🪐 Astro-Quant &amp; Gann Guardrails</h4>
                  <div class="sr-formula-box">Astro Seg 1–3 = Timing &amp; Account Router Only</div>
                  <div class="sr-formula-box">Gann Sq9 (90°/180°) = Non-Execution Reference Only</div>
                  <div class="sr-muted" style="font-size:10.5px;">Kritika &amp; Vina Patel active; Jigar &amp; Dipak Patel vetoed till Dec 5. Gann geometry NEVER enters Buy/SL/Target math.</div>
                </div>
              </div>
            </div>
          </div>

          <div class="sr-panel">
            <div class="sr-panel-hdr">
              <div style="display:flex; align-items:center; gap:6px; flex-wrap:wrap;">
                <span class="sr-panel-title">EXECUTION BUCKET:</span>
                <button class="sr-btn active" id="sr-bkt-dual" onclick="SR.execEngine.setBucket('dual')">7 Overlapping Dual-Horizon Gems</button>
                <button class="sr-btn" id="sr-bkt-swing" onclick="SR.execEngine.setBucket('swing')">1-2M Swing Trades (11)</button>
                <button class="sr-btn" id="sr-bkt-core" onclick="SR.execEngine.setBucket('core')">8-12M Core Investments (15)</button>
                <button class="sr-btn" id="sr-bkt-all" onclick="SR.execEngine.setBucket('all')">All 24 Stocks</button>
              </div>
              <span class="sr-mono sr-muted" style="font-size:10.5px;">Click Math → for exact stock-by-stock Buy/SL/Target derivation audit</span>
            </div>
            <div class="sr-panel-body" style="display:flex; gap:22px; align-items:center; flex-wrap:wrap;">
              <div>
                <div class="sr-kpi-lbl">Total Capital (₹)</div>
                <input type="number" id="sr-exec-cap-input" class="sr-input sr-mono sr-bold" style="width:145px; margin-top:3px;" value="1000000" step="100000" oninput="SR.execEngine.updateCap(this.value)">
              </div>
              <div style="min-width:210px;">
                <div class="sr-kpi-lbl">Phase 2 GTT Cash Reserve: <span id="sr-exec-gtt-lbl" class="sr-info">42%</span></div>
                <input type="range" id="sr-exec-gtt-slider" min="0" max="70" value="42" style="width:100%; margin-top:6px;" oninput="SR.execEngine.updateGtt(this.value)">
              </div>
              <div>
                <div class="sr-kpi-lbl">Phase 1 Active Capital</div>
                <div id="sr-exec-p1-val" class="sr-mono sr-pos sr-bold" style="font-size:14px; margin-top:3px;">₹5,80,000</div>
              </div>
              <div>
                <div class="sr-kpi-lbl">Phase 2 GTT Reserve</div>
                <div id="sr-exec-p2-val" class="sr-mono sr-info sr-bold" style="font-size:14px; margin-top:3px;">₹4,20,000</div>
              </div>
              <div>
                <div class="sr-kpi-lbl">Bucket Weight Sum</div>
                <div id="sr-exec-sum-val" class="sr-mono sr-bold" style="font-size:14px; margin-top:3px;">100%</div>
              </div>
            </div>
          </div>

          <div class="sr-panel">
            <div class="sr-table-wrap">
              <table class="sr-table">
                <thead id="sr-exec-thead"></thead>
                <tbody id="sr-exec-tbody"></tbody>
              </table>
            </div>
          </div>
        </section>

        <!-- [F6] ASTRO-QUANT & TELEGRAM BROADCAST -->
        <section id="sr-view-f6" class="sr-tab-view">
          <div class="sr-grid-equal">
            <div>
              <div class="sr-panel">
                <div class="sr-panel-hdr">
                  <span class="sr-panel-title">🪐 SEGMENT 1: SIDEREAL LAHIRI EPHEMERIS (NOV 20, 2026)</span>
                  <span class="sr-pill pill-violet">Timing &amp; Gatekeeper Only</span>
                </div>
                <div class="sr-panel-body">
                  <div class="sr-eph-strip" id="sr-f6-eph-strip"></div>
                  <div style="margin-top:9px; padding:8px 10px; background:rgba(168,85,247,0.08); border:1px solid rgba(168,85,247,0.3); border-radius:5px; font-size:11.5px; line-height:1.5;">
                    <strong class="sr-vio">Seg-1 Regime Gate:</strong> Jupiter (1°55' Leo) &amp; Mars (3°11' Leo) trine BSE (01-Apr-1875) natal fiery expansion points while Mercury Direct (13°47' Lib, Swati) energizes NIFTY (03-Nov-1995) natal Libra exchange axis. Saturn Rx (14°05' Pis) filters weak microcaps while favoring quality Stage 2 leaders.
                  </div>
                </div>
              </div>

              <div class="sr-panel">
                <div class="sr-panel-hdr">
                  <span class="sr-panel-title">🧬 SEGMENT 3: FAMILY ACCOUNT SYNASTRY GATEKEEPERS</span>
                  <span class="sr-pill pill-crimson">2 Circuit Breakers Active Till Dec 5</span>
                </div>
                <div class="sr-panel-body">
                  <div class="sr-syn-grid">
                    <div class="sr-syn-card" style="border-color:rgba(0,230,118,0.4);">
                      <div style="display:flex; justify-content:space-between; margin-bottom:3px;"><strong>Kritika Patel</strong><span class="sr-pill pill-emerald">SEG-3 PASS</span></div>
                      <div class="sr-mono sr-muted" style="font-size:10px;">Lagna: Kumbha | Moon: Mithuna (Ardra)</div>
                      <div style="margin-top:4px;">Active: <span class="sr-info">Mercury (5H) &amp; Venus (6H)</span> → Capital Markets, IT, Telecom, Auto.</div>
                    </div>
                    <div class="sr-syn-card" style="border-color:rgba(0,230,118,0.4);">
                      <div style="display:flex; justify-content:space-between; margin-bottom:3px;"><strong>Vina Patel</strong><span class="sr-pill pill-emerald">SEG-3 PASS</span></div>
                      <div class="sr-mono sr-muted" style="font-size:10px;">Lagna: Mesha | Moon: Vrishabha (Rohini)</div>
                      <div style="margin-top:4px;">Active: <span class="sr-info">Jupiter (5H Trine) &amp; Saturn (11H)</span> → Financials, Banks, Precision Mfg.</div>
                    </div>
                    <div class="sr-syn-card" style="border-color:rgba(255,59,92,0.45);">
                      <div style="display:flex; justify-content:space-between; margin-bottom:3px;"><strong>Jigar Patel</strong><span class="sr-pill pill-crimson">VETOED &lt; DEC 5</span></div>
                      <div class="sr-mono sr-muted" style="font-size:10px;">Lagna: Meena | Moon: Meena (Revati)</div>
                      <div class="sr-neg" style="margin-top:4px;">Hard Circuit Breaker: Saturn Rx over natal Moon + Rahu axis till Dec 5.</div>
                    </div>
                    <div class="sr-syn-card" style="border-color:rgba(255,59,92,0.45);">
                      <div style="display:flex; justify-content:space-between; margin-bottom:3px;"><strong>Dipak Patel</strong><span class="sr-pill pill-crimson">VETOED &lt; DEC 5</span></div>
                      <div class="sr-mono sr-muted" style="font-size:10px;">Lagna: Dhanu | Moon: Karka (Pushya)</div>
                      <div class="sr-neg" style="margin-top:4px;">Hard Circuit Breaker: Ashtama Rahu / Saturn transit block till Dec 5.</div>
                    </div>
                  </div>
                </div>
              </div>

              <div class="sr-panel">
                <div class="sr-panel-hdr">
                  <span class="sr-panel-title">🏛 SEGMENT 2: COMPANY IPO NATAL &amp; SECTOR PLANET GATE MATRIX (24)</span>
                </div>
                <div class="sr-table-wrap" style="max-height:285px; overflow-y:auto;">
                  <table class="sr-table">
                    <thead>
                      <tr>
                        <th>Ticker</th>
                        <th>Sector Ruler</th>
                        <th>Company IPO Natal Alignment</th>
                        <th>Seg-3 Account</th>
                      </tr>
                    </thead>
                    <tbody id="sr-f6-seg2-tbody"></tbody>
                  </table>
                </div>
              </div>
            </div>

            <div class="sr-panel">
              <div class="sr-panel-hdr">
                <span class="sr-panel-title">📱 TELEGRAM CHANNEL BROADCAST STUDIO</span>
                <label style="display:flex; align-items:center; gap:7px; cursor:pointer; font-size:11px;">
                  <span class="sr-muted">Public Mode (Masks Names + SEBI Disclaimer)</span>
                  <label class="sr-switch">
                    <input type="checkbox" id="sr-tg-public-mode" checked onchange="SR.tgModule.render()">
                    <span class="sr-slider"></span>
                  </label>
                </label>
              </div>
              <div class="sr-panel-body" style="display:flex; flex-direction:column; gap:10px;">
                <div style="display:flex; gap:6px; flex-wrap:wrap;">
                  <button class="sr-btn active" id="sr-tg-tpl-rrg" onclick="SR.tgModule.setTpl('rrg')">1. Sector &amp; Cap RRG</button>
                  <button class="sr-btn" id="sr-tg-tpl-heatmap" onclick="SR.tgModule.setTpl('heatmap')">2. Alpha &amp; Breadth Heatmap</button>
                  <button class="sr-btn" id="sr-tg-tpl-valuation" onclick="SR.tgModule.setTpl('valuation')">3. Fair Value Picks</button>
                  <button class="sr-btn" id="sr-tg-tpl-plan" onclick="SR.tgModule.setTpl('plan')">4. 1-12M Trade Plan</button>
                </div>

                <div id="sr-tg-preview-box" class="sr-tg-box"></div>

                <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px;">
                  <input type="text" id="sr-tg-bot-token" class="sr-input sr-mono" placeholder="Bot Token (Optional: 123456:ABC...)">
                  <input type="text" id="sr-tg-channel-id" class="sr-input sr-mono" placeholder="Channel ID (Optional: -100...)">
                </div>

                <div style="display:flex; gap:8px; flex-wrap:wrap;">
                  <button class="sr-btn cyan" onclick="SR.tgModule.copyText()">📋 Copy Text</button>
                  <button class="sr-btn" onclick="SR.tgModule.copyHtml()">🌐 Copy HTML</button>
                  <button class="sr-btn violet" style="margin-left:auto;" onclick="SR.tgModule.autoPublish()">🚀 Auto-Publish</button>
                </div>
              </div>
            </div>
          </div>
        </section>
      </div>

      <div class="sr-footer-bar">
        <div><span class="sr-pos">●</span> JdK RELATIVE ROTATION &amp; SECTOR BREADTH ENGINE • LIVE COMPUTED FROM NSE INDICES &amp; 750-STOCK UNIVERSE</div>
        <div>CONTROLS: <span class="sr-info">CLICK NODE</span> FOR CONSTITUENT STOCK RRG • <span class="sr-info">WHEEL</span> ZOOM • <span class="sr-info">DRAG</span> PAN</div>
      </div>

      <!-- Tab 4 Scoped Modals & Overlays -->
      <div id="sr-inspector-modal" class="sr-modal-bg" onclick="if(event.target===this) SR.inspectorModal.close()">
        <div class="sr-modal-box">
          <div class="sr-panel-hdr" style="background:#101722;">
            <span class="sr-panel-title sr-info" id="sr-insp-hdr-title" style="font-size:13px;">EQUITY BUY / SL / TARGET DERIVATION &amp; LIVE TECHNICAL AUDIT</span>
            <button class="sr-btn" onclick="SR.inspectorModal.close()">✕ Close [ESC]</button>
          </div>
          <div id="sr-insp-modal-body" class="sr-modal-body"></div>
        </div>
      </div>

      <div id="sr-methodology-modal" class="sr-modal-bg" onclick="if(event.target===this) SR.methodologyModal.close()">
        <div class="sr-modal-box" style="width:860px;">
          <div class="sr-panel-hdr" style="background:#101722;">
            <span class="sr-panel-title sr-info">📐 COMPLETE BUY, STOP-LOSS &amp; TARGET FORMULA SPECIFICATION</span>
            <button class="sr-btn" onclick="SR.methodologyModal.close()">✕ Close [ESC]</button>
          </div>
          <div class="sr-modal-body">
            <div class="sr-meth-grid">
              <div class="sr-meth-card">
                <h4>1. 1–2 Month Swing Trade Formulas</h4>
                <div class="sr-formula-box">Entry Zone = [20-DMA / Retest, CMP + 0.5×ATR(14)]</div>
                <div class="sr-formula-box">Hard SL = Swing Low − 1.5×ATR(14) (5%–8% Max Risk)</div>
                <div class="sr-formula-box">T1 = Entry Mid + 2.0×Risk | T2 = Entry Mid + 3.5×Risk</div>
                <p>Anchored strictly to Stage 2 volatility structure. Entries are rejected if extended &gt;1.5×ATR(14) above the 20-DMA.</p>
              </div>
              <div class="sr-meth-card">
                <h4>2. 8–12 Month Core Investment Formulas</h4>
                <div class="sr-formula-box">Accumulation = [Intrinsic FV × 0.85, FV × 0.95] / 150-DMA</div>
                <div class="sr-formula-box">Dual Stop = 150-DMA − 1×ATR OR KPI Thesis Stop</div>
                <div class="sr-formula-box">Base = FY28E EPS × Justified P/E | Bull = +15% Rerating</div>
                <p>Uses sector-matched intrinsic valuation: <em>P/B-ROE Gordon Growth</em> (Banks), <em>EV/EBITDA + DCF</em> (Telecom/Auto/Power), and <em>Forward P/E + PEG</em> (IT/Exchanges/Precision/Defence/Pharma).</p>
              </div>
              <div class="sr-meth-card" style="border-color:rgba(168,85,247,0.45);">
                <h4 style="color:#c084fc;">3. Astro-Quant Gatekeeper (Timing &amp; Account Only)</h4>
                <p>Evaluates Seg-1 (BSE 1875 &amp; NIFTY 1995 natal transits), Seg-2 (Sector planet &amp; Company IPO natal chart), and Seg-3 (Kritika &amp; Vina Patel PASS; Jigar &amp; Dipak Patel VETOED till Dec 5). Never modifies price levels.</p>
              </div>
              <div class="sr-meth-card" style="border-color:rgba(255,179,0,0.45);">
                <h4 style="color:#ffb300;">4. Gann Square of 9 (Strictly Non-Execution Reference)</h4>
                <p>Gann Sq9 <code>90°</code> and <code>180°</code> levels (<code>(√CMP + deg/180)²</code>) are displayed in a separate reference column only and <strong>never</strong> enter Buy, SL, or Target math.</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div id="sr-csv-modal" class="sr-modal-bg" onclick="if(event.target===this) SR.csvModal.close()">
        <div class="sr-modal-box" style="width:580px;">
          <div class="sr-panel-hdr" style="background:#101722;">
            <span class="sr-panel-title sr-info">⬆ EOD OVERRIDE / CSV IMPORT</span>
            <button class="sr-btn" onclick="SR.csvModal.close()">✕ Close</button>
          </div>
          <div class="sr-modal-body" style="display:flex; flex-direction:column; gap:10px;">
            <p class="sr-muted" style="font-size:11.5px;">Paste CSV rows (<code>Ticker_or_Sector, RRG_Angle, RRG_Radius, Chg%, Alpha%, Price, FII_Flow_Cr</code>) to override live RRG coordinates or prices in-session.</p>
            <textarea id="sr-csv-textarea" class="sr-input sr-mono" style="height:130px; resize:vertical;" placeholder="Financials, 28.0, 107.0, 2.20, 0.80, 28771.75, 51200"></textarea>
            <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:8px;">
              <div><div class="sr-kpi-lbl">EOD Date</div><input type="text" id="sr-csv-date" class="sr-input sr-mono" style="width:100%; margin-top:3px;" value="Live EOD"></div>
              <div><div class="sr-kpi-lbl">FII Cash</div><input type="text" id="sr-csv-fii" class="sr-input sr-mono" style="width:100%; margin-top:3px;" value="Live / EOD"></div>
              <div><div class="sr-kpi-lbl">DII Cash</div><input type="text" id="sr-csv-dii" class="sr-input sr-mono" style="width:100%; margin-top:3px;" value="Live / EOD"></div>
            </div>
            <div style="display:flex; justify-content:flex-end; gap:8px; margin-top:6px;">
              <button class="sr-btn" onclick="SR.csvModal.close()">Cancel</button>
              <button class="sr-btn cyan" onclick="SR.csvModal.process()">Process &amp; Re-Render</button>
            </div>
          </div>
        </div>
      </div>

      <div id="sr-hud-tip" class="sr-hud-tip"></div>
      <div id="sr-toast" class="sr-toast"></div>
    </div>
    """

    sr_js = """
    const SR_LIVE_DATA = __SECTOR_ROTATION_JSON__;

    window.SR = (function () {
      const UNIVERSE_DB = (SR_LIVE_DATA.universe_nodes || []).map(n => ({ ...n }));
      const STOCK_DB = (SR_LIVE_DATA.curated_stocks || []).map(s => ({ ...s }));
      const SECTOR_CONSTITUENTS = SR_LIVE_DATA.sector_constituents || {};
      const LIVE_TAPE = SR_LIVE_DATA.tape || {};
      const BENCH_NAME = SR_LIVE_DATA.benchmark_name || 'NIFTY 500';

      const EPHEMERIS_NOV20 = [
        { body: 'Sun', pos: "3°12' Sco", nak: 'Anuradha', motion: 'Direct' },
        { body: 'Mars', pos: "3°11' Leo", nak: 'Magha', motion: 'Direct' },
        { body: 'Jupiter', pos: "1°55' Leo", nak: 'Magha', motion: 'Direct' },
        { body: 'Mercury', pos: "13°47' Lib", nak: 'Swati', motion: 'Direct' },
        { body: 'Saturn', pos: "14°05' Pis", nak: 'U.Bhadra', motion: 'Retrograde' },
        { body: 'Rahu', pos: "0°50' Aqu", nak: 'Dhanishta', motion: 'Mean' },
        { body: 'Ketu', pos: "0°50' Leo", nak: 'Magha', motion: 'Mean' }
      ];

      function deriveQuadrant(angle) {
        const a = ((angle % 360) + 360) % 360;
        if (a < 90) return 'Leading';
        if (a < 180) return 'Improving';
        if (a < 270) return 'Lagging';
        return 'Weakening';
      }

      function quadColor(q) {
        if (q === 'Leading') return '#00e676';
        if (q === 'Improving') return '#3b82f6';
        if (q === 'Weakening') return '#ffb300';
        return '#ff3b5c';
      }

      function quadPill(q) {
        if (q === 'Leading') return 'pill-emerald';
        if (q === 'Improving') return 'pill-blue';
        if (q === 'Weakening') return 'pill-amber';
        return 'pill-crimson';
      }

      function verdictPill(v) {
        if (v === 'UNDERVALUED') return 'pill-emerald';
        if (v === 'FAIRLY VALUED') return 'pill-cyan';
        if (v === 'GROWTH PREMIUM / GARP') return 'pill-violet';
        return 'pill-amber';
      }

      function smPill(regime) {
        if (!regime) return 'pill-neutral';
        if (regime.startsWith('Accumulating')) return 'pill-emerald';
        if (regime.startsWith('FII')) return 'pill-cyan';
        if (regime.startsWith('DII') || regime.startsWith('Early')) return 'pill-blue';
        return 'pill-crimson';
      }

      function computeHeading(tail) {
        if (!tail || tail.length < 2) return 'E';
        const p1 = tail[tail.length - 2];
        const p2 = tail[tail.length - 1];
        const deg = (Math.atan2(p2.y - p1.y, p2.x - p1.x) * 180) / Math.PI;
        const n = deg < 0 ? deg + 360 : deg;
        if (n > 337.5 || n <= 22.5) return 'E';
        if (n <= 67.5) return 'NE';
        if (n <= 112.5) return 'N';
        if (n <= 157.5) return 'NW';
        if (n <= 202.5) return 'W';
        if (n <= 247.5) return 'SW';
        if (n <= 292.5) return 'S';
        return 'SE';
      }

      function generateSmoothTail(item, periods, stepDeg) {
        const label = item.group || item.ticker || 'NODE';
        const seed = label.split('').reduce((s, c) => s + c.charCodeAt(0), 0);
        const dist = Math.max(0.5, ((item.radius || 100) - 100.0) * 1.15);
        const pts = [];
        for (let i = 0; i < periods; i++) {
          const rad = (((item.angle || 45) + i * stepDeg) * Math.PI) / 180;
          const wave = Math.sin((i * 0.65) + seed * 0.1) * 0.42;
          const r = Math.max(0.3, dist - i * 0.14 + wave);
          pts.push({ x: r * Math.cos(rad), y: r * Math.sin(rad) });
        }
        return pts.reverse();
      }

      function gannSq9Ref(price) {
        const root = Math.sqrt(Math.max(1, price));
        return { r90: Math.pow(root + 0.5, 2), r180: Math.pow(root + 1.0, 2) };
      }

      function evaluateSeg3(stock) {
        const p = (stock && stock.assigned) || 'Kritika';
        if (p === 'Jigar' || p === 'Dipak') {
          return { person: `${p} Patel`, status: 'fail', pill: 'pill-crimson', badge: 'VETO < DEC 5' };
        }
        if (p === 'Kritika') {
          return { person: 'Kritika Patel', status: 'pass', pill: 'pill-emerald', badge: 'PASS (Merc/Ven)' };
        }
        return { person: 'Vina Patel', status: 'pass', pill: 'pill-emerald', badge: 'PASS (Jup/Sat)' };
      }

      function getConstituentsForNode(node) {
        if (!node) return [];
        const liveList = SECTOR_CONSTITUENTS[node.id] || [];
        const curatedMatches = STOCK_DB.filter(s =>
          (node.kind === 'sector' && s.sector === node.group) ||
          (node.kind === 'cap' && s.capTier === node.id)
        );
        const mergedMap = new Map();
        liveList.forEach(item => {
          const curated = STOCK_DB.find(s => s.ticker === item.ticker);
          mergedMap.set(item.ticker, curated ? { ...item, ...curated, dailyTail: item.dailyTail || curated.dailyTail, weeklyTail: item.weeklyTail || curated.weeklyTail } : { ...item });
        });
        curatedMatches.forEach(s => {
          if (!mergedMap.has(s.ticker)) mergedMap.set(s.ticker, { ...s });
        });
        return Array.from(mergedMap.values());
      }

      const ui = {
        timer: null,
        escAttr: (s) => String(s).replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/'/g, '&#39;'),
        copyFallback: (text) => {
          const ta = document.createElement('textarea');
          ta.value = text;
          document.body.appendChild(ta);
          ta.select();
          document.execCommand('copy');
          document.body.removeChild(ta);
        },
        toast: (msg) => {
          const el = document.getElementById('sr-toast');
          if (!el) return;
          el.textContent = msg;
          el.classList.add('show');
          clearTimeout(ui.timer);
          ui.timer = setTimeout(() => el.classList.remove('show'), 2500);
        },
        fmtCr: (v) => {
          if (v === null || v === undefined || isNaN(v)) return 'N/A';
          const sign = v > 0 ? '+' : '';
          if (Math.abs(v) >= 100000) return `${sign}₹${(v / 100000).toFixed(2)}L Cr`;
          return `${sign}₹${Math.round(v).toLocaleString('en-IN')} Cr`;
        },
        fmtInr: (v) => {
          if (Math.abs(v) >= 100000) return `₹${(v / 100000).toFixed(2)}L`;
          return `₹${Math.round(v).toLocaleString('en-IN')}`;
        }
      };

      const app = {
        currentTab: 'f1',
        initialized: false,
        init: () => {
          if (app.initialized) return;
          app.initialized = true;
          app.renderTape();
          rrgEngine.build();
          overviewEngine.render();
          rrgEngine.init();
          heatmapEngine.render();
          screenerEngine.init();
          execEngine.render();
          astroEngine.render();
          tgModule.render();

          window.addEventListener('keydown', (e) => {
            if (typeof currentTab !== 'undefined' && currentTab !== 'sector') return;
            if (e.key === 'Escape') {
              inspectorModal.close();
              methodologyModal.close();
              csvModal.close();
            }
            if (['F1', 'F2', 'F3', 'F4', 'F5', 'F6'].includes(e.key)) {
              e.preventDefault();
              app.switchTab(e.key.toLowerCase());
            }
          });
        },

        renderTape: () => {
          const setItem = (idVal, idChg, obj, invColor) => {
            const vEl = document.getElementById(idVal);
            const cEl = document.getElementById(idChg);
            if (!vEl || !cEl || !obj) return;
            vEl.textContent = Number(obj.last || 0).toLocaleString('en-IN', { maximumFractionDigits: 2 });
            const c = Number(obj.chg || 0);
            cEl.textContent = `${c > 0 ? '+' : ''}${c.toFixed(2)}%`;
            cEl.className = invColor ? (c > 0 ? 'sr-warn' : 'sr-pos') : (c >= 0 ? 'sr-pos' : 'sr-neg');
          };
          setItem('sr-tape-nifty', 'sr-tape-nifty-chg', LIVE_TAPE.nifty50, false);
          setItem('sr-tape-sensex', 'sr-tape-sensex-chg', LIVE_TAPE.sensex, false);
          setItem('sr-tape-bank', 'sr-tape-bank-chg', LIVE_TAPE.banknifty, false);
          setItem('sr-tape-vix', 'sr-tape-vix-chg', LIVE_TAPE.vix, true);
          setItem('sr-tape-usdinr', 'sr-tape-usdinr-chg', LIVE_TAPE.usdinr, true);

          document.getElementById('sr-tape-adv').textContent = `${LIVE_TAPE.adv || 0} Adv`;
          document.getElementById('sr-tape-dec').textContent = `${LIVE_TAPE.dec || 0} Dec`;
          const dtLbl = LIVE_TAPE.date_label || SR_LIVE_DATA.generated_at || 'Live EOD';
          document.getElementById('sr-hdr-date').textContent = dtLbl;
          document.getElementById('sr-csv-date').value = dtLbl;

          const fiiEl = document.getElementById('sr-hdr-fii');
          const diiEl = document.getElementById('sr-hdr-dii');
          if (LIVE_TAPE.fii_day_cr !== null && LIVE_TAPE.fii_day_cr !== undefined) {
            fiiEl.textContent = ui.fmtCr(LIVE_TAPE.fii_day_cr);
            fiiEl.className = `sr-bold ${LIVE_TAPE.fii_day_cr >= 0 ? 'sr-pos' : 'sr-neg'}`;
            document.getElementById('sr-csv-fii').value = fiiEl.textContent;
          }
          if (LIVE_TAPE.dii_day_cr !== null && LIVE_TAPE.dii_day_cr !== undefined) {
            diiEl.textContent = ui.fmtCr(LIVE_TAPE.dii_day_cr);
            diiEl.className = `sr-bold ${LIVE_TAPE.dii_day_cr >= 0 ? 'sr-pos' : 'sr-neg'}`;
            document.getElementById('sr-csv-dii').value = diiEl.textContent;
          }
        },

        switchTab: (tab) => {
          app.currentTab = tab;
          document.querySelectorAll('#view-sector .sr-nav-tab').forEach(b => b.classList.toggle('active', b.dataset.srtab === tab));
          document.querySelectorAll('#view-sector .sr-tab-view').forEach(v => v.classList.toggle('active', v.id === `sr-view-${tab}`));
          if (tab === 'f1') overviewEngine.render();
          if (tab === 'f2') rrgEngine.renderAll();
          if (tab === 'f3') heatmapEngine.render();
          if (tab === 'f4') screenerEngine.render();
          if (tab === 'f5') execEngine.render();
          if (tab === 'f6') { astroEngine.render(); tgModule.render(); }
        },

        openPreExplodeInRRG: () => {
          app.switchTab('f2');
          rrgEngine.mode = 'macro';
          rrgEngine.universe = 'all_23';
          const uSel = document.getElementById('sr-rrg-universe-select');
          if (uSel) uSel.value = 'all_23';
          rrgEngine.renderAll();
          ui.toast('Highlighted ★ P3 Markup, ◈ P2 Absorption & ◎ P1 Early Base on RRG');
        },

        openCapInRRG: () => {
          app.switchTab('f2');
          rrgEngine.exitDrilldown();
          document.getElementById('sr-rrg-universe-select').value = 'cap_5';
          rrgEngine.setUniverse('cap_5');
        },

        drillSectorFromAnywhere: (id) => {
          app.switchTab('f2');
          rrgEngine.drillIntoNode(id);
        },

        quickJump: (q) => {
          const term = q.trim().toUpperCase();
          if (!term) return;
          const stock = STOCK_DB.find(s => s.ticker === term || s.ticker.includes(term) || s.name.toUpperCase().includes(term));
          if (stock) { inspectorModal.open(stock.ticker); return; }
          for (const secId of Object.keys(SECTOR_CONSTITUENTS)) {
            const hit = (SECTOR_CONSTITUENTS[secId] || []).find(s => s.ticker === term || s.ticker.includes(term));
            if (hit) { inspectorModal.open(hit.ticker, secId); return; }
          }
          const node = rrgEngine.macroNodes.find(n => n.group.toUpperCase().includes(term) || n.short.includes(term));
          if (node) { app.drillSectorFromAnywhere(node.id); return; }
          ui.toast(`No match for "${q}"`);
        }
      };

      const overviewEngine = {
        render: () => {
          const adv = LIVE_TAPE.adv || 0;
          const dec = LIVE_TAPE.dec || 0;
          const vixVal = LIVE_TAPE.vix ? LIVE_TAPE.vix.last : '--';
          const breadthPct = (adv + dec) > 0 ? Math.round((adv / (adv + dec)) * 100) : 50;
          const regEl = document.getElementById('sr-f1-regime');
          regEl.textContent = breadthPct >= 50 ? 'WEINSTEIN STAGE 2' : 'SELECTIVE ROTATION';
          regEl.className = `sr-kpi-val ${breadthPct >= 50 ? 'sr-pos' : 'sr-warn'}`;
          document.getElementById('sr-f1-regime-sub').textContent = `${adv} Adv / ${dec} Dec (${breadthPct}% Adv) • VIX ${vixVal}`;

          const caps = rrgEngine.macroNodes.filter(n => n.kind === 'cap');
          const capSorted = [...caps].sort((a, b) => (b.m1 + b.chg) - (a.m1 + a.chg));
          if (capSorted.length) {
            const topCap = capSorted[0];
            document.getElementById('sr-f1-cap-leader').textContent = `${topCap.short} (${topCap.chg > 0 ? '+' : ''}${topCap.chg.toFixed(2)}%)`;
            document.getElementById('sr-f1-cap-sub').textContent = `${topCap.quadrant} (${topCap.heading}) • 1M ${topCap.m1 > 0 ? '+' : ''}${topCap.m1.toFixed(1)}%`;
          }

          const sectors = rrgEngine.macroNodes.filter(n => n.kind === 'sector');
          const leadCount = sectors.filter(n => n.quadrant === 'Leading').length;
          const impCount = sectors.filter(n => n.quadrant === 'Improving').length;
          const sortScore = (a, b) => (b.preExplodeScore || 0) - (a.preExplodeScore || 0);
          const p3Nodes = rrgEngine.macroNodes.filter(n => n.preExplodeTier === 'PHASE_3').sort(sortScore);
          const p2Nodes = rrgEngine.macroNodes.filter(n => n.preExplodeTier === 'PHASE_2').sort(sortScore);
          const p1Nodes = rrgEngine.macroNodes.filter(n => n.preExplodeTier === 'PHASE_1').sort(sortScore);
          document.getElementById('sr-f1-quad-count').textContent = `${leadCount} Lead • ${impCount} Imp • P3:${p3Nodes.length} / P2:${p2Nodes.length}`;
          document.getElementById('sr-f1-quad-sub').textContent = `Out of ${sectors.length} NSE Sectors (JdK vs ${BENCH_NAME})`;

          const smBar = document.getElementById('sr-f1-sm-bar');
          if (smBar) {
            const totalActive = p3Nodes.length + p2Nodes.length + p1Nodes.length;
            if (!totalActive) {
              smBar.style.display = 'none';
            } else {
              smBar.style.display = 'flex';
              const makeChip = (n, cls, icon, tag) => {
                const safeId = ui.escAttr(n.id);
                const reasons = (n.preExplodeReasons || []).join(' • ');
                const kp = n.kind === 'cap' ? '◆ ' : '';
                return `<button class="sr-pill ${cls}" style="cursor:pointer;" onclick="SR.app.drillSectorFromAnywhere('${safeId}')" title="${ui.escAttr(reasons)}">${icon} ${kp}${n.short} ${n.preExplodeScore} (${tag})</button>`;
              };
              const primaryChips = [
                ...p3Nodes.map(n => makeChip(n, 'pill-p3', '★', 'P3 MARKUP')),
                ...p2Nodes.map(n => makeChip(n, 'pill-p2', '◈', 'P2 ABSORP'))
              ].join('');
              const p1Chips = p1Nodes.map(n => makeChip(n, 'pill-p1', '◎', 'P1 BASE')).join('');
              smBar.innerHTML = `
                <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap; width:100%; justify-content:space-between;">
                  <div style="display:flex; align-items:center; gap:7px; flex-wrap:wrap;">
                    <span class="sr-mono" style="color:#f5d0fe; font-weight:800; font-size:11px; letter-spacing:0.4px;">🏦 SMART MONEY ROTATION RADAR:</span>
                    ${primaryChips || '<span class="sr-muted sr-mono" style="font-size:10.5px;">No Phase 2/3 triggers yet</span>'}
                  </div>
                  <button class="sr-btn" style="border-color:#e879f9; color:#f5d0fe; padding:3px 9px; font-size:10.5px;" onclick="SR.app.openPreExplodeInRRG()">Highlight on RRG [F2] →</button>
                </div>
                ${p1Nodes.length ? `
                <div style="display:flex; align-items:center; gap:6px; flex-wrap:wrap; padding-top:5px; border-top:1px solid rgba(56, 189, 248, 0.16);">
                  <span class="sr-mono" style="color:#bae6fd; font-weight:700; font-size:10px;">P1 · EARLY BASE (${p1Nodes.length}):</span>
                  ${p1Chips}
                </div>` : ''}
              `;
            }
          }

          const badgeEl = document.getElementById('badge-sector');
          if (badgeEl) badgeEl.textContent = p3Nodes.length > 0 ? `${leadCount} Lead • P3:${p3Nodes.length}` : `${leadCount} Lead`;

          const avgUp = STOCK_DB.length
            ? STOCK_DB.reduce((a, s) => a + ((s.fairValue - s.price) / s.price) * 100, 0) / STOCK_DB.length
            : 0;
          document.getElementById('sr-f1-fv-kpi').textContent = `${avgUp >= 0 ? '+' : ''}${avgUp.toFixed(1)}% Avg Upside`;

          document.getElementById('sr-f1-cap-grid').innerHTML = caps.map(c => {
            const peTier = c.preExplodeTier || 'NEUTRAL';
            const isP3 = peTier === 'PHASE_3';
            const isP2 = peTier === 'PHASE_2';
            const isP1 = peTier === 'PHASE_1';
            const cardCls = isP3 ? 'sr-cap-p3' : (isP2 ? 'sr-cap-p2' : (isP1 ? 'sr-cap-p1' : ''));
            const peBadge = isP3
              ? `<span class="sr-pill pill-p3" style="font-size:8.5px; padding:1px 4px;">★ P3 ${c.preExplodeScore}</span>`
              : (isP2 ? `<span class="sr-pill pill-p2" style="font-size:8.5px; padding:1px 4px;">◈ P2 ${c.preExplodeScore}</span>`
              : (isP1 ? `<span class="sr-pill pill-p1" style="font-size:8.5px; padding:1px 4px;">◎ P1 ${c.preExplodeScore}</span>` : ''));
            return `
            <div class="sr-cap-card ${cardCls}" onclick="SR.app.drillSectorFromAnywhere('${ui.escAttr(c.id)}')" title="${ui.escAttr((c.preExplodeReasons || []).join(' • '))}">
              <div style="display:flex; justify-content:space-between; align-items:center; gap:4px; margin-bottom:4px;">
                <span class="sr-mono sr-bold ${isP3 ? '' : 'sr-info'}" style="font-size:10.5px; ${isP3 ? 'color:#f5d0fe;' : ''}">◆ ${c.short} ${peBadge}</span>
                <span class="sr-pill ${quadPill(c.quadrant)}" style="font-size:9px; padding:1px 5px;">${c.quadrant}</span>
              </div>
              <div class="sr-mono sr-bold ${c.chg >= 0 ? 'sr-pos' : 'sr-neg'}" style="font-size:13.5px;">
                ${c.chg > 0 ? '+' : ''}${c.chg.toFixed(2)}%
                <span class="sr-muted" style="font-size:10px;">(α ${c.alpha > 0 ? '+' : ''}${c.alpha.toFixed(2)}%)</span>
              </div>
              <div class="sr-mono sr-muted" style="font-size:10px; margin-top:3px;">1M: ${c.m1 > 0 ? '+' : ''}${c.m1.toFixed(1)}% • &gt;50D: ${c.pctAbove50 ?? '--'}% • BBW ${c.bbwPct ?? '--'}% →</div>
            </div>
          `;
          }).join('');

          const curated = rrgEngine.macroNodes.filter(n => n.curated);
          rrgEngine.renderCanvas(document.getElementById('sr-f1-rrg-canvas'), curated, {
            trailLen: 8, isMini: true, zoom: 1, panX: 0, panY: 0, labelMode: 'all', hoveredId: null, highlightedId: null
          });

          const gems = STOCK_DB.filter(s => s.isCore && s.isSwing);
          document.getElementById('sr-f1-gems-tbody').innerHTML = gems.map(s => {
            const seg = evaluateSeg3(s);
            return `
              <tr class="sr-row-click" onclick="SR.inspectorModal.open('${ui.escAttr(s.ticker)}')">
                <td><span class="sr-ticker-btn">${s.ticker}</span> <span class="sr-muted sr-mono" style="font-size:10px;">${s.sector}</span></td>
                <td class="sr-num sr-bold">₹${s.price.toFixed(1)}</td>
                <td class="sr-mono sr-vio">${s.entry}</td>
                <td class="sr-num sr-neg">${s.sl}</td>
                <td class="sr-num sr-pos">${s.t1}</td>
                <td class="sr-num sr-info sr-bold">₹${s.fairValue}</td>
                <td><span class="sr-pill ${seg.pill}">${seg.person.split(' ')[0]}</span></td>
              </tr>
            `;
          }).join('');
        }
      };

      const rrgEngine = {
        macroNodes: [],
        stockNodes: [],
        mode: 'macro',
        drilledParent: null,
        universe: 'all_23',
        timeframe: 'daily',
        trailLen: 8,
        labelMode: 'all',
        hoveredId: null,
        highlightedId: null,
        playing: false,
        animStep: 3,
        zoom: 1.0,
        panX: 0,
        panY: 0,
        dragging: false,
        dragStart: { x: 0, y: 0 },
        didDrag: false,
        screenNodes: [],
        miniScreenNodes: [],

        pickTail: (item, isW, periods, step) => {
          if (!item._csvOverridden) {
            const raw = isW ? item.weeklyTail : item.dailyTail;
            if (Array.isArray(raw) && raw.length >= 2) return raw;
          }
          return generateSmoothTail(item, periods, step);
        },

        build: () => {
          const isW = rrgEngine.timeframe === 'weekly';
          const periods = isW ? 12 : 16;
          const step = isW ? 6.0 : 3.8;
          rrgEngine.macroNodes = UNIVERSE_DB.map(item => {
            const tail = rrgEngine.pickTail(item, isW, periods, step);
            const head = tail[tail.length - 1] || { x: 0, y: 0 };
            const ang = (Math.atan2(head.y, head.x) * 180 / Math.PI + 360) % 360;
            return { ...item, angle: ang, quadrant: deriveQuadrant(ang), tail, heading: computeHeading(tail) };
          });
          if (rrgEngine.mode === 'stock' && rrgEngine.drilledParent) {
            rrgEngine.buildStockNodes(rrgEngine.drilledParent);
          }
        },

        buildStockNodes: (parent) => {
          const isW = rrgEngine.timeframe === 'weekly';
          const periods = isW ? 12 : 16;
          const step = isW ? 6.2 : 4.0;
          const rawStocks = getConstituentsForNode(parent);
          rrgEngine.stockNodes = rawStocks.map(s => {
            const tail = rrgEngine.pickTail(s, isW, periods, step);
            const head = tail[tail.length - 1] || { x: 0, y: 0 };
            const ang = (Math.atan2(head.y, head.x) * 180 / Math.PI + 360) % 360;
            return {
              ...s,
              id: s.ticker,
              kind: 'stock',
              group: `${s.ticker} — ${s.name}`,
              short: s.ticker,
              topMover: Math.abs(s.chg || 0) >= 1.2 || (s.smScore || 0) >= 90 || !!s.signalTag,
              angle: ang,
              quadrant: deriveQuadrant(ang),
              tail,
              heading: computeHeading(tail)
            };
          });
        },

        init: () => {
          const canvas = document.getElementById('sr-main-rrg-canvas');
          const f1Canvas = document.getElementById('sr-f1-rrg-canvas');

          canvas.addEventListener('wheel', (e) => {
            e.preventDefault();
            rrgEngine.zoomBy(e.deltaY < 0 ? 1.15 : 0.87);
          }, { passive: false });

          canvas.addEventListener('mousedown', (e) => {
            rrgEngine.dragging = true;
            rrgEngine.didDrag = false;
            rrgEngine.dragStart = { x: e.clientX - rrgEngine.panX, y: e.clientY - rrgEngine.panY };
          });
          window.addEventListener('mousemove', (e) => {
            if (!rrgEngine.dragging) return;
            const nx = e.clientX - rrgEngine.dragStart.x;
            const ny = e.clientY - rrgEngine.dragStart.y;
            if (Math.hypot(nx - rrgEngine.panX, ny - rrgEngine.panY) > 3) rrgEngine.didDrag = true;
            rrgEngine.panX = nx;
            rrgEngine.panY = ny;
            rrgEngine.drawCanvasOnly();
          });
          window.addEventListener('mouseup', () => { rrgEngine.dragging = false; });

          canvas.addEventListener('mousemove', (e) => {
            if (rrgEngine.dragging) return;
            const hit = rrgEngine.hitTest(canvas, e);
            const newHover = hit ? hit.id : null;
            if (newHover !== rrgEngine.hoveredId) {
              rrgEngine.hoveredId = newHover;
              rrgEngine.drawCanvasOnly();
              rrgEngine.syncDockHighlight();
            }
            rrgEngine.updateTooltip(hit, e);
          });
          canvas.addEventListener('mouseleave', () => {
            rrgEngine.hoveredId = null;
            document.getElementById('sr-hud-tip').style.display = 'none';
            rrgEngine.drawCanvasOnly();
            rrgEngine.syncDockHighlight();
          });

          canvas.addEventListener('click', (e) => {
            if (rrgEngine.didDrag) return;
            const hit = rrgEngine.hitTest(canvas, e);
            if (!hit) return;
            if (rrgEngine.mode === 'macro') rrgEngine.drillIntoNode(hit.id);
            else inspectorModal.open(hit.id, rrgEngine.drilledParent ? rrgEngine.drilledParent.id : null);
          });

          f1Canvas.addEventListener('click', (e) => {
            const hit = rrgEngine.hitTest(f1Canvas, e);
            if (hit) app.drillSectorFromAnywhere(hit.id);
          });

          rrgEngine.renderAll();
        },

        zoomBy: (factor) => {
          rrgEngine.zoom = Math.max(0.65, Math.min(3.5, rrgEngine.zoom * factor));
          document.getElementById('sr-rrg-zoom-lbl').textContent = `${Math.round(rrgEngine.zoom * 100)}%`;
          rrgEngine.drawCanvasOnly();
        },

        resetZoom: () => {
          rrgEngine.zoom = 1.0;
          rrgEngine.panX = 0;
          rrgEngine.panY = 0;
          document.getElementById('sr-rrg-zoom-lbl').textContent = '100%';
          rrgEngine.drawCanvasOnly();
        },

        setUniverse: (u) => {
          rrgEngine.universe = u;
          rrgEngine.resetZoom();
          rrgEngine.renderAll();
        },

        setTimeframe: (tf) => {
          rrgEngine.timeframe = tf;
          document.getElementById('sr-rrg-tf-daily').classList.toggle('active', tf === 'daily');
          document.getElementById('sr-rrg-tf-weekly').classList.toggle('active', tf === 'weekly');
          const max = tf === 'weekly' ? 12 : 16;
          const slider = document.getElementById('sr-rrg-trail-slider');
          slider.max = max;
          if (rrgEngine.trailLen > max) {
            rrgEngine.trailLen = max;
            slider.value = max;
            document.getElementById('sr-rrg-trail-val').textContent = max;
          }
          rrgEngine.build();
          rrgEngine.renderAll();
        },

        setLabelMode: (m) => {
          rrgEngine.labelMode = m;
          rrgEngine.drawCanvasOnly();
        },

        setTrail: (v) => {
          rrgEngine.trailLen = parseInt(v, 10);
          document.getElementById('sr-rrg-trail-val').textContent = v;
          rrgEngine.drawCanvasOnly();
        },

        togglePlay: () => {
          rrgEngine.playing = !rrgEngine.playing;
          const btn = document.getElementById('sr-rrg-play-btn');
          btn.textContent = rrgEngine.playing ? '❚❚ Pause' : '▶ Play';
          btn.classList.toggle('active', rrgEngine.playing);
          if (rrgEngine.playing) {
            rrgEngine.animStep = 3;
            requestAnimationFrame(rrgEngine.animate);
          } else {
            rrgEngine.drawCanvasOnly();
          }
        },

        animate: () => {
          if (!rrgEngine.playing) return;
          const max = rrgEngine.timeframe === 'weekly' ? 12 : 16;
          rrgEngine.animStep += 0.12;
          if (rrgEngine.animStep > max) rrgEngine.animStep = 3;
          const step = Math.floor(rrgEngine.animStep);
          document.getElementById('sr-rrg-trail-slider').value = step;
          document.getElementById('sr-rrg-trail-val').textContent = step;
          rrgEngine.drawCanvasOnly(step);
          requestAnimationFrame(rrgEngine.animate);
        },

        drillIntoNode: (id) => {
          const parent = rrgEngine.macroNodes.find(n => n.id === id);
          if (!parent) return;
          rrgEngine.mode = 'stock';
          rrgEngine.drilledParent = parent;
          rrgEngine.hoveredId = null;
          rrgEngine.highlightedId = null;
          rrgEngine.buildStockNodes(parent);
          rrgEngine.resetZoom();
          document.getElementById('sr-hud-tip').style.display = 'none';
          rrgEngine.renderAll();
          ui.toast(`Drilled into ${parent.group}: ${rrgEngine.stockNodes.length} Constituent Stocks`);
        },

        exitDrilldown: () => {
          rrgEngine.mode = 'macro';
          rrgEngine.drilledParent = null;
          rrgEngine.hoveredId = null;
          rrgEngine.highlightedId = null;
          rrgEngine.resetZoom();
          document.getElementById('sr-hud-tip').style.display = 'none';
          rrgEngine.renderAll();
        },

        getActiveList: () => {
          if (rrgEngine.mode === 'stock') return rrgEngine.stockNodes;
          const u = rrgEngine.universe;
          if (u === 'curated_10') return rrgEngine.macroNodes.filter(n => n.curated);
          if (u === 'sm_active') return rrgEngine.macroNodes.filter(n => n.preExplodeTier === 'PHASE_3' || n.preExplodeTier === 'PHASE_2' || n.preExplodeTier === 'PHASE_1');
          if (u === 'sm_p3') return rrgEngine.macroNodes.filter(n => n.preExplodeTier === 'PHASE_3');
          if (u === 'sm_p2') return rrgEngine.macroNodes.filter(n => n.preExplodeTier === 'PHASE_2');
          if (u === 'sm_p1') return rrgEngine.macroNodes.filter(n => n.preExplodeTier === 'PHASE_1');
          if (u === 'cap_5') return rrgEngine.macroNodes.filter(n => n.kind === 'cap');
          if (u === 'sectors_18') return rrgEngine.macroNodes.filter(n => n.kind === 'sector');
          if (u === 'leading_only') return rrgEngine.macroNodes.filter(n => n.quadrant === 'Leading');
          if (u === 'improving_only') return rrgEngine.macroNodes.filter(n => n.quadrant === 'Improving');
          return rrgEngine.macroNodes;
        },

        renderAll: () => {
          rrgEngine.updateChrome();
          rrgEngine.drawCanvasOnly();
          rrgEngine.renderRightDock();
        },

        updateChrome: () => {
          const badge = document.getElementById('sr-rrg-mode-badge');
          const trail = document.getElementById('sr-rrg-crumb-trail');
          const actions = document.getElementById('sr-rrg-crumb-actions');
          const macroFlt = document.getElementById('sr-rrg-macro-filters');
          const canvasTitle = document.getElementById('sr-rrg-canvas-title');

          if (rrgEngine.mode === 'macro') {
            badge.className = 'sr-pill pill-cyan';
            badge.textContent = 'MACRO SECTOR & CAP RRG';
            const uSel = document.getElementById('sr-rrg-universe-select');
            trail.textContent = `All Sectors & Cap Indices > ${uSel.options[uSel.selectedIndex].text}`;
            actions.innerHTML = `<span class="sr-muted sr-mono" style="font-size:10.5px;">Click any sector or market-cap node to launch Constituent Stock RRG</span>`;
            macroFlt.style.visibility = 'visible';
            canvasTitle.textContent = `JdK SECTOR & CAP RRG (VS ${BENCH_NAME}) — CLICK NODE FOR CONSTITUENT STOCKS`;
          } else {
            const p = rrgEngine.drilledParent;
            badge.className = 'sr-pill pill-violet';
            badge.textContent = 'CONSTITUENT STOCK RRG';
            trail.innerHTML = `<span class="sr-info" style="cursor:pointer; text-decoration:underline;" onclick="SR.rrgEngine.exitDrilldown()">All Sectors &amp; Indices</span> &nbsp;&gt;&nbsp; <span class="sr-pos">${p.group} (${rrgEngine.stockNodes.length} Constituent Stocks)</span>`;
            actions.innerHTML = `<button class="sr-btn cyan" onclick="SR.rrgEngine.exitDrilldown()">← Back to Macro Sector RRG</button>`;
            macroFlt.style.visibility = 'hidden';
            canvasTitle.textContent = `${p.group.toUpperCase()} — LIVE CONSTITUENT STOCK RRG (CLICK STOCK FOR AUDIT &amp; LEVELS)`;
          }
        },

        drawCanvasOnly: (overrideTrail = null) => {
          const canvas = document.getElementById('sr-main-rrg-canvas');
          const list = rrgEngine.getActiveList();
          rrgEngine.renderCanvas(canvas, list, {
            trailLen: overrideTrail || rrgEngine.trailLen,
            isMini: false,
            zoom: rrgEngine.zoom,
            panX: rrgEngine.panX,
            panY: rrgEngine.panY,
            labelMode: rrgEngine.labelMode,
            hoveredId: rrgEngine.hoveredId,
            highlightedId: rrgEngine.highlightedId
          });
        },

        renderCanvas: (canvas, list, opts) => {
          if (!canvas) return;
          const ctx = canvas.getContext('2d');
          const w = canvas.width, h = canvas.height;
          const trailLen = opts.trailLen;

          let minX = -4.5, maxX = 4.5, minY = -4.5, maxY = 4.5;
          list.forEach(node => {
            const sub = node.tail.slice(Math.max(0, node.tail.length - trailLen));
            sub.forEach(p => {
              if (p.x < minX) minX = p.x;
              if (p.x > maxX) maxX = p.x;
              if (p.y < minY) minY = p.y;
              if (p.y > maxY) maxY = p.y;
            });
          });
          const maxSpan = Math.max(Math.abs(minX), Math.abs(maxX), Math.abs(minY), Math.abs(maxY), 5.0);
          const padFactor = opts.isMini ? 0.72 : 0.76;
          const baseScale = (Math.min(w, h) * 0.5 * padFactor) / maxSpan;
          const scale = baseScale * (opts.zoom || 1);

          const cx = w / 2 + (opts.panX || 0);
          const cy = h / 2 + (opts.panY || 0);

          ctx.clearRect(0, 0, w, h);

          ctx.fillStyle = 'rgba(0, 230, 118, 0.045)'; ctx.fillRect(cx, 0, w - cx, cy);
          ctx.fillStyle = 'rgba(59, 130, 246, 0.045)'; ctx.fillRect(0, 0, cx, cy);
          ctx.fillStyle = 'rgba(255, 59, 92, 0.045)';  ctx.fillRect(0, cy, cx, h - cy);
          ctx.fillStyle = 'rgba(255, 179, 0, 0.045)';  ctx.fillRect(cx, cy, w - cx, h - cy);

          ctx.strokeStyle = 'rgba(29, 39, 56, 0.9)';
          ctx.lineWidth = 1;
          [4, 8, 12, 16].forEach(r => {
            ctx.beginPath();
            ctx.arc(cx, cy, r * scale, 0, Math.PI * 2);
            ctx.stroke();
          });

          ctx.strokeStyle = '#33435c';
          ctx.lineWidth = 1.3;
          ctx.beginPath();
          ctx.moveTo(cx, 0); ctx.lineTo(cx, h);
          ctx.moveTo(0, cy); ctx.lineTo(w, cy);
          ctx.stroke();

          ctx.font = opts.isMini ? '700 9.5px JetBrains Mono, monospace' : '700 11px JetBrains Mono, monospace';
          ctx.fillStyle = 'rgba(0, 230, 118, 0.78)'; ctx.textAlign = 'right'; ctx.fillText('LEADING', w - 12, 18);
          ctx.fillStyle = 'rgba(59, 130, 246, 0.78)'; ctx.textAlign = 'left';  ctx.fillText('IMPROVING', 12, 18);
          ctx.fillStyle = 'rgba(255, 59, 92, 0.78)';  ctx.textAlign = 'left';  ctx.fillText('LAGGING', 12, h - 10);
          ctx.fillStyle = 'rgba(255, 179, 0, 0.78)';  ctx.textAlign = 'right'; ctx.fillText('WEAKENING', w - 12, h - 10);

          if (!opts.isMini) {
            ctx.fillStyle = '#5c6a7e';
            ctx.font = '10px JetBrains Mono, monospace';
            ctx.textAlign = 'left'; ctx.fillText('↑ JdK RS-MOMENTUM (100.0)', Math.max(10, cx + 8), 16);
            ctx.textAlign = 'right'; ctx.fillText('JdK RS-RATIO (100.0) →', w - 12, Math.max(30, Math.min(h - 24, cy - 7)));
          }

          const focusId = opts.hoveredId || opts.highlightedId;
          const placedLabels = [];
          const hitList = [];

          const ordered = [...list].sort((a, b) => (a.id === focusId ? 1 : b.id === focusId ? -1 : 0));

          ordered.forEach(node => {
            const color = quadColor(node.quadrant);
            const sub = node.tail.slice(Math.max(0, node.tail.length - trailLen));
            if (!sub.length) return;

            const isFocus = node.id === focusId;
            const peTier = node.preExplodeTier || 'NEUTRAL';
            const isP3 = (rrgEngine.mode === 'macro' && peTier === 'PHASE_3');
            const isP2 = (rrgEngine.mode === 'macro' && peTier === 'PHASE_2');
            const isP1 = (rrgEngine.mode === 'macro' && peTier === 'PHASE_1');
            const isSM = (isP3 || isP2 || isP1);
            const alpha = focusId && !isFocus ? 0.13 : 1.0;

            ctx.save();
            ctx.globalAlpha = alpha;

            const pts = sub.map(p => ({ x: cx + p.x * scale, y: cy - p.y * scale }));
            ctx.strokeStyle = isFocus ? '#00d4ff' : (isP3 ? '#e879f9' : color);
            ctx.lineWidth = isFocus ? 2.8 : (isP3 ? 2.4 : (node.kind === 'cap' ? 2.1 : 1.6));
            if (node.kind === 'cap') ctx.setLineDash([4, 2]);
            else ctx.setLineDash([]);

            ctx.beginPath();
            ctx.moveTo(pts[0].x, pts[0].y);
            for (let i = 1; i < pts.length - 1; i++) {
              const xc = (pts[i].x + pts[i + 1].x) / 2;
              const yc = (pts[i].y + pts[i + 1].y) / 2;
              ctx.quadraticCurveTo(pts[i].x, pts[i].y, xc, yc);
            }
            ctx.lineTo(pts[pts.length - 1].x, pts[pts.length - 1].y);
            ctx.stroke();
            ctx.setLineDash([]);

            for (let i = 0; i < pts.length - 1; i++) {
              const r = 1.6 + (i / pts.length) * 1.6;
              ctx.fillStyle = color;
              ctx.beginPath();
              ctx.arc(pts[i].x, pts[i].y, r, 0, Math.PI * 2);
              ctx.fill();
            }

            const head = pts[pts.length - 1];
            const rawHead = sub[sub.length - 1];
            hitList.push({ id: node.id, hx: head.x, hy: head.y, node, rawHead });

            if (pts.length >= 2) {
              const prev = pts[pts.length - 2];
              const ang = Math.atan2(head.y - prev.y, head.x - prev.x);
              const aLen = opts.isMini ? 7 : 9;
              ctx.fillStyle = isFocus ? '#00d4ff' : color;
              ctx.beginPath();
              ctx.moveTo(head.x + Math.cos(ang) * 4, head.y + Math.sin(ang) * 4);
              ctx.lineTo(head.x - aLen * Math.cos(ang - 0.42), head.y - aLen * Math.sin(ang - 0.42));
              ctx.lineTo(head.x - aLen * Math.cos(ang + 0.42), head.y - aLen * Math.sin(ang + 0.42));
              ctx.closePath();
              ctx.fill();
            }

            if (isSM && !isFocus) {
              ctx.save();
              ctx.strokeStyle = isP3 ? '#e879f9' : (isP2 ? '#a855f7' : '#38bdf8');
              ctx.lineWidth = isP3 ? (opts.isMini ? 1.8 : 2.5) : (isP2 ? (opts.isMini ? 1.3 : 1.8) : (opts.isMini ? 1.0 : 1.3));
              if (isP2) ctx.setLineDash([3, 2]);
              else if (isP1) ctx.setLineDash([2, 2]);
              ctx.beginPath();
              const haloR = isP3 ? (opts.isMini ? 9.2 : 13.0) : (isP2 ? (opts.isMini ? 8.0 : 10.8) : (opts.isMini ? 7.0 : 9.4));
              ctx.arc(head.x, head.y, haloR, 0, Math.PI * 2);
              ctx.stroke();
              ctx.restore();
            }

            if (isFocus) {
              ctx.strokeStyle = '#00d4ff';
              ctx.lineWidth = 2;
              ctx.beginPath();
              ctx.arc(head.x, head.y, 12, 0, Math.PI * 2);
              ctx.stroke();
            }

            if (node.kind === 'cap') {
              const d = opts.isMini ? 6 : 8;
              ctx.fillStyle = color;
              ctx.strokeStyle = isFocus ? '#00d4ff' : (isP3 ? '#e879f9' : (isP2 ? '#a855f7' : (isP1 ? '#38bdf8' : '#ffb300')));
              ctx.lineWidth = 2;
              ctx.beginPath();
              ctx.moveTo(head.x, head.y - d);
              ctx.lineTo(head.x + d, head.y);
              ctx.lineTo(head.x, head.y + d);
              ctx.lineTo(head.x - d, head.y);
              ctx.closePath();
              ctx.fill();
              ctx.stroke();
            } else {
              ctx.fillStyle = color;
              ctx.strokeStyle = isFocus ? '#00d4ff' : (isP3 ? '#e879f9' : (isP2 ? '#a855f7' : (isP1 ? '#38bdf8' : '#070a0f')));
              ctx.lineWidth = isSM ? 2.0 : 1.6;
              ctx.beginPath();
              ctx.arc(head.x, head.y, opts.isMini ? (isP3 ? 4.8 : 4.3) : (isP3 ? 6.5 : 5.8), 0, Math.PI * 2);
              ctx.fill();
              ctx.stroke();
            }

            const showLabel =
              isFocus ||
              isP3 ||
              isP2 ||
              (isP1 && (rrgEngine.universe === 'sm_active' || rrgEngine.universe === 'sm_p1')) ||
              opts.labelMode === 'all' ||
              (opts.labelMode === 'top' && (node.topMover || node.kind === 'cap'));

            if (showLabel) {
              ctx.font = node.kind === 'cap'
                ? (opts.isMini ? '700 8.5px JetBrains Mono, monospace' : '700 10px JetBrains Mono, monospace')
                : (opts.isMini ? '600 8.5px Plus Jakarta Sans, sans-serif' : '600 10px JetBrains Mono, monospace');
              const text = (isP3 ? '★ ' : (isP2 ? '◈ ' : (isP1 ? '◎ ' : ''))) + node.short;
              const tw = ctx.measureText(text).width + 8;
              const th = 15;

              const offsets = [
                { dx: 11, dy: -7 }, { dx: 11, dy: 9 },
                { dx: -tw - 11, dy: -7 }, { dx: -tw - 11, dy: 9 },
                { dx: -tw / 2, dy: -22 }, { dx: -tw / 2, dy: 14 },
                { dx: 15, dy: -22 }, { dx: -tw - 15, dy: 22 }
              ];

              let bestBox = null;
              for (const off of offsets) {
                const bx = Math.max(6, Math.min(w - tw - 6, head.x + off.dx));
                const by = Math.max(22, Math.min(h - th - 18, head.y + off.dy));
                const box = { x: bx, y: by, w: tw, h: th };
                const overlaps = placedLabels.some(p =>
                  box.x < p.x + p.w + 3 && box.x + box.w + 3 > p.x &&
                  box.y < p.y + p.h + 2 && box.y + box.h + 2 > p.y
                );
                if (!overlaps) { bestBox = box; break; }
              }
              if (!bestBox) {
                const bx = Math.max(6, Math.min(w - tw - 6, head.x + 11));
                let by = Math.max(22, Math.min(h - th - 18, head.y - 7));
                while (placedLabels.some(p => Math.abs(p.x - bx) < tw && Math.abs(p.y - by) < th + 2) && by < h - 22) {
                  by += th + 2;
                }
                bestBox = { x: bx, y: by, w: tw, h: th };
              }
              placedLabels.push(bestBox);

              const anchorX = bestBox.x > head.x ? bestBox.x : bestBox.x + bestBox.w;
              const anchorY = bestBox.y + bestBox.h / 2;
              if (Math.hypot(anchorX - head.x, anchorY - head.y) > 13) {
                ctx.strokeStyle = isFocus ? 'rgba(0,212,255,0.75)' : 'rgba(140,153,173,0.45)';
                ctx.lineWidth = 0.9;
                ctx.beginPath();
                ctx.moveTo(head.x, head.y);
                ctx.lineTo(anchorX, anchorY);
                ctx.stroke();
              }

              ctx.fillStyle = isFocus
                ? 'rgba(0, 212, 255, 0.22)'
                : (isP3 ? 'rgba(232, 121, 249, 0.22)' : (isP2 ? 'rgba(168, 85, 247, 0.18)' : (isP1 ? 'rgba(56, 189, 248, 0.14)' : 'rgba(9, 13, 20, 0.86)')));
              ctx.strokeStyle = isFocus
                ? '#00d4ff'
                : (isP3 ? '#e879f9' : (isP2 ? '#a855f7' : (isP1 ? '#38bdf8' : 'rgba(30, 41, 59, 0.95)')));
              ctx.lineWidth = isP3 ? 1.6 : (isP2 ? 1.3 : (isP1 ? 1.15 : 1));
              ctx.beginPath();
              if (typeof ctx.roundRect === 'function') ctx.roundRect(bestBox.x, bestBox.y, bestBox.w, bestBox.h, 3);
              else ctx.rect(bestBox.x, bestBox.y, bestBox.w, bestBox.h);
              ctx.fill();
              ctx.stroke();

              ctx.fillStyle = node.kind === 'cap' ? '#00d4ff' : (isP3 ? '#fdf4ff' : (isP2 ? '#f3e8ff' : (isP1 ? '#bae6fd' : '#f1f5f9')));
              ctx.textAlign = 'left';
              ctx.fillText(text, bestBox.x + 4, bestBox.y + 11);
            }

            ctx.restore();
          });

          if (!opts.isMini) rrgEngine.screenNodes = hitList;
          else rrgEngine.miniScreenNodes = hitList;
        },

        hitTest: (canvas, e) => {
          const rect = canvas.getBoundingClientRect();
          const mx = (e.clientX - rect.left) * (canvas.width / rect.width);
          const my = (e.clientY - rect.top) * (canvas.height / rect.height);
          const pool = canvas.id === 'sr-f1-rrg-canvas' ? (rrgEngine.miniScreenNodes || []) : (rrgEngine.screenNodes || []);
          for (let i = pool.length - 1; i >= 0; i--) {
            const item = pool[i];
            if (Math.hypot(mx - item.hx, my - item.hy) < 14) return item;
          }
          return null;
        },

        updateTooltip: (hit, e) => {
          const tip = document.getElementById('sr-hud-tip');
          if (!hit) { tip.style.display = 'none'; return; }
          const { node, rawHead } = hit;
          tip.style.display = 'block';
          tip.style.left = Math.min(window.innerWidth - 280, e.clientX + 14) + 'px';
          tip.style.top = Math.min(window.innerHeight - 210, e.clientY + 14) + 'px';

          if (rrgEngine.mode === 'macro') {
            const peTier = node.preExplodeTier || 'NEUTRAL';
            const peCol = peTier === 'PHASE_3' ? '#e879f9' : (peTier === 'PHASE_2' ? '#a855f7' : (peTier === 'PHASE_1' ? '#38bdf8' : (peTier === 'EXTENDED' ? '#ffb300' : '#8c99ad')));
            const peBadge = peTier === 'PHASE_3'
              ? `★ P3: Markup Ready (${node.preExplodeScore}/100)`
              : (peTier === 'PHASE_2' ? `◈ P2: Supply Absorption (${node.preExplodeScore}/100)`
              : (peTier === 'PHASE_1' ? `◎ P1: Early Base (${node.preExplodeScore}/100)`
              : (peTier === 'EXTENDED' ? `Late Markup / Extended (${node.preExplodeScore || 0}/100)` : `Low Sponsorship (${node.preExplodeScore || 0}/100)`)));
            const reasonsStr = (node.preExplodeReasons || []).join(' • ');
            tip.innerHTML = `
              <div style="color:${node.kind === 'cap' ? '#ffb300' : '#00d4ff'}; font-weight:700; border-bottom:1px solid #1d2738; padding-bottom:4px; margin-bottom:5px;">
                ${node.kind === 'cap' ? '◆ CAP BENCHMARK: ' : '● NSE SECTOR: '}${node.group}
              </div>
              <div style="display:flex; justify-content:space-between;"><span class="sr-muted">JdK RS-RATIO / MOM:</span><span>${(100 + rawHead.x).toFixed(2)} / ${(100 + rawHead.y).toFixed(2)}</span></div>
              <div style="display:flex; justify-content:space-between;"><span class="sr-muted">QUADRANT / HEADING:</span><span style="color:${quadColor(node.quadrant)}; font-weight:700;">${node.quadrant} (${node.heading})</span></div>
              <div style="display:flex; justify-content:space-between; gap:8px;"><span class="sr-muted">SMART MONEY PHASE:</span><span style="color:${peCol}; font-weight:700;">${peBadge}</span></div>
              ${reasonsStr ? `<div class="sr-muted" style="font-size:9.5px; margin-top:2px;">BBW ${node.bbwPct ?? '--'}% • ATR ${node.atrDecay ?? '--'}x • ${reasonsStr}</div>` : ''}
              <div style="display:flex; justify-content:space-between;"><span class="sr-muted">1D / 1M RETURN:</span><span class="${node.chg >= 0 ? 'sr-pos' : 'sr-neg'}">${node.chg > 0 ? '+' : ''}${node.chg.toFixed(2)}% / ${node.m1 > 0 ? '+' : ''}${node.m1.toFixed(1)}%</span></div>
              <div style="display:flex; justify-content:space-between; margin-top:4px; padding-top:4px; border-top:1px solid #1d2738;"><span class="sr-muted">&gt;50DMA / &gt;200DMA:</span><span>${node.pctAbove50 ?? '--'}% / ${node.pctAbove200 ?? '--'}%</span></div>
              <div style="display:flex; justify-content:space-between;"><span class="sr-muted">SCANNER SIGNALS:</span><span>Track A: ${node.trackACount || 0} | Track B: ${node.trackBCount || 0}</span></div>
              <div style="margin-top:5px; color:#00d4ff; font-size:10px;">▶ Click node to drill into Constituent Stock RRG</div>
            `;
          } else {
            const fvLine = node.fairValue
              ? `<div style="display:flex; justify-content:space-between;"><span class="sr-muted">CMP → FAIR VALUE:</span><span>₹${node.price.toFixed(1)} → <strong class="sr-pos">₹${node.fairValue}</strong></span></div>`
              : `<div style="display:flex; justify-content:space-between;"><span class="sr-muted">1M / 3M RETURN:</span><span class="${(node.m3 || 0) >= 0 ? 'sr-pos' : 'sr-neg'}">${(node.m1 || 0) > 0 ? '+' : ''}${(node.m1 || 0).toFixed(1)}% / ${(node.m3 || 0) > 0 ? '+' : ''}${(node.m3 || 0).toFixed(1)}%</span></div>`;
            tip.innerHTML = `
              <div style="color:#00d4ff; font-weight:700; border-bottom:1px solid #1d2738; padding-bottom:4px; margin-bottom:5px;">
                ${node.ticker} — ${node.name} ${node.signalTag ? `[${node.signalTag}]` : ''}
              </div>
              <div style="display:flex; justify-content:space-between;"><span class="sr-muted">JdK RS-RATIO / MOM:</span><span>${(100 + rawHead.x).toFixed(2)} / ${(100 + rawHead.y).toFixed(2)}</span></div>
              <div style="display:flex; justify-content:space-between;"><span class="sr-muted">RRG QUADRANT:</span><span style="color:${quadColor(node.quadrant)}; font-weight:700;">${node.quadrant} (${node.heading})</span></div>
              ${fvLine}
              <div style="display:flex; justify-content:space-between;"><span class="sr-muted">20-DMA / ATR(14):</span><span>₹${node.dma20 || '--'} / ₹${node.atr14 || '--'}</span></div>
              <div style="margin-top:5px; color:#00d4ff; font-size:10px;">▶ Click stock for Swing/Core Audit &amp; TradingView Link</div>
            `;
          }
        },

        highlightFromDock: (id) => {
          rrgEngine.highlightedId = id;
          rrgEngine.drawCanvasOnly();
        },

        syncDockHighlight: () => {
          const active = rrgEngine.hoveredId || rrgEngine.highlightedId;
          document.querySelectorAll('#view-sector .sr-dock-card').forEach(el => {
            el.classList.toggle('highlighted', el.dataset.id === active);
          });
        },

        renderRightDock: () => {
          const title = document.getElementById('sr-dock-title');
          const sub = document.getElementById('sr-dock-subtitle');
          const ctxBar = document.getElementById('sr-dock-context-bar');
          const listEl = document.getElementById('sr-rrg-right-list');

          if (rrgEngine.mode === 'macro') {
            title.textContent = 'SECTOR & CAP ROTATION DIRECTORY';
            sub.textContent = 'Hover to isolate • Click to drill';
            ctxBar.style.display = 'none';

            const vis = rrgEngine.getActiveList();
            const caps = vis.filter(n => n.kind === 'cap');
            const secs = vis.filter(n => n.kind === 'sector');

            let html = '';
            if (caps.length) {
              html += `<div class="sr-dock-hdr"><span>◆ Market Cap Indices (${caps.length})</span><span>1D / Breadth</span></div>`;
              html += caps.map(n => rrgEngine.macroDockCard(n)).join('');
            }
            if (secs.length) {
              html += `<div class="sr-dock-hdr"><span>● NSE Sectors (${secs.length})</span><span>1D / Breadth</span></div>`;
              html += secs.map(n => rrgEngine.macroDockCard(n)).join('');
            }
            listEl.innerHTML = html;
          } else {
            const p = rrgEngine.drilledParent;
            title.textContent = `CONSTITUENTS & ROTATION — ${p.short}`;
            sub.textContent = 'Sorted by 3M Strength / Smart Money';
            ctxBar.style.display = 'block';
            ctxBar.innerHTML = `
              <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:6px;">
                <span>Source: <strong class="sr-info">${p.source || 'NSE'}</strong> | &gt;50DMA: <strong>${p.pctAbove50 ?? '--'}%</strong> | Track A: <strong class="sr-pos">${p.trackACount || 0}</strong> | Track B: <strong class="sr-vio">${p.trackBCount || 0}</strong></span>
                <span class="sr-pill pill-violet">Ruler: ${p.ruler}</span>
              </div>
            `;

            const sorted = [...rrgEngine.stockNodes].sort((a, b) => ((b.smScore || 0) - (a.smScore || 0)) || ((b.m3 || 0) - (a.m3 || 0)));
            const maxMetric = Math.max(...sorted.map(s => Math.abs(s.m3 || s.chg || 1)), 1);

            listEl.innerHTML = sorted.map(s => {
              const m3 = s.m3 ?? 0;
              const barW = Math.min(100, Math.round((Math.abs(m3) / maxMetric) * 100));
              const safeTk = ui.escAttr(s.ticker);
              const sigBadge = s.signalTag ? `<span class="sr-pill ${s.signalTag === 'TRACK A' ? 'pill-emerald' : 'pill-violet'}" style="font-size:9px;">${s.signalTag}</span>` : '';
              const extraLine = s.fairValue
                ? `<span>FV: <strong class="sr-pos">₹${s.fairValue}</strong> | Net Inst: <strong class="${(s.netInstCr || 0) >= 0 ? 'sr-pos' : 'sr-neg'}">${ui.fmtCr(s.netInstCr)}</strong></span>`
                : `<span>20DMA: ₹${s.dma20 || '--'} | ATR: ₹${s.atr14 || '--'}</span>`;
              return `
                <div class="sr-dock-card" data-id="${safeTk}"
                     onmouseenter="SR.rrgEngine.highlightFromDock('${safeTk}')"
                     onmouseleave="SR.rrgEngine.highlightFromDock(null)"
                     onclick="SR.inspectorModal.open('${safeTk}', '${ui.escAttr(p.id)}')">
                  <div style="display:flex; justify-content:space-between; align-items:center; gap:6px;">
                    <div>
                      <span class="sr-mono sr-bold sr-info" style="font-size:12px;">${s.ticker}</span>
                      <span class="sr-muted" style="font-size:10.5px;"> • ₹${Number(s.price || 0).toFixed(1)}</span>
                      ${sigBadge}
                    </div>
                    <span class="sr-pill ${quadPill(s.quadrant)}">${s.quadrant} (${s.heading})</span>
                  </div>
                  <div class="sr-flow-track">
                    <div class="${m3 >= 0 ? 'sr-flow-pos' : 'sr-flow-neg'}" style="width:${barW}%"></div>
                  </div>
                  <div class="sr-mono sr-muted" style="display:flex; justify-content:space-between; font-size:10px; margin-top:5px;">
                    <span>1D <strong class="${s.chg >= 0 ? 'sr-pos' : 'sr-neg'}">${s.chg > 0 ? '+' : ''}${Number(s.chg || 0).toFixed(2)}%</strong> | 1M <strong class="${(s.m1 || 0) >= 0 ? 'sr-pos' : 'sr-neg'}">${(s.m1 || 0) > 0 ? '+' : ''}${Number(s.m1 || 0).toFixed(1)}%</strong> | 3M <strong class="${m3 >= 0 ? 'sr-pos' : 'sr-neg'}">${m3 > 0 ? '+' : ''}${Number(m3).toFixed(1)}%</strong></span>
                  </div>
                  <div class="sr-mono" style="display:flex; justify-content:space-between; font-size:10px; margin-top:4px; padding-top:4px; border-top:1px solid #182130;">
                    ${extraLine}
                    <span class="sr-info">Audit →</span>
                  </div>
                </div>
              `;
            }).join('');
          }
        },

        macroDockCard: (n) => {
          const safeId = ui.escAttr(n.id);
          const peTier = n.preExplodeTier || 'NEUTRAL';
          const isP3 = peTier === 'PHASE_3';
          const isP2 = peTier === 'PHASE_2';
          const isP1 = peTier === 'PHASE_1';
          const dockCls = isP3 ? 'sr-dock-p3' : (isP2 ? 'sr-dock-p2' : (isP1 ? 'sr-dock-p1' : ''));
          const pePill = isP3
            ? `<span class="sr-pill pill-p3" style="font-size:9px;">★ P3 · ${n.preExplodeScore}</span>`
            : (isP2 ? `<span class="sr-pill pill-p2" style="font-size:9px;">◈ P2 · ${n.preExplodeScore}</span>`
            : (isP1 ? `<span class="sr-pill pill-p1" style="font-size:9px;">◎ P1 · ${n.preExplodeScore}</span>` : ''));
          const sigTxt = (n.trackACount || n.trackBCount)
            ? ` • <span class="sr-pos">A:${n.trackACount || 0}</span>/<span class="sr-vio">B:${n.trackBCount || 0}</span>`
            : '';
          const bbwTxt = (n.bbwPct !== undefined) ? ` • BBW ${Math.round(n.bbwPct)}%` : '';
          return `
            <div class="sr-dock-card ${dockCls}" data-id="${safeId}"
                 onmouseenter="SR.rrgEngine.highlightFromDock('${safeId}')"
                 onmouseleave="SR.rrgEngine.highlightFromDock(null)"
                 onclick="SR.rrgEngine.drillIntoNode('${safeId}')">
              <div style="display:flex; justify-content:space-between; align-items:center; gap:5px;">
                <span class="sr-bold" style="font-size:11.5px; color:${n.kind === 'cap' ? '#00d4ff' : (isP3 ? '#f5d0fe' : '#e8eef5')};">
                  ${n.kind === 'cap' ? '◆' : '●'} ${n.group} ${pePill}
                </span>
                <span class="sr-pill ${quadPill(n.quadrant)}" style="font-size:9.5px;">${n.quadrant} (${n.heading})</span>
              </div>
              <div class="sr-mono sr-muted" style="display:flex; justify-content:space-between; font-size:10px; margin-top:4px;">
                <span>1D <strong class="${n.chg >= 0 ? 'sr-pos' : 'sr-neg'}">${n.chg > 0 ? '+' : ''}${n.chg.toFixed(2)}%</strong> | 1M <strong class="${n.m1 >= 0 ? 'sr-pos' : 'sr-neg'}">${n.m1 > 0 ? '+' : ''}${n.m1.toFixed(1)}%</strong></span>
                <span>&gt;50D <strong>${n.pctAbove50 ?? '--'}%</strong>${bbwTxt}${sigTxt}</span>
              </div>
            </div>
          `;
        }
      };

      const heatmapEngine = {
        metric: 'abs',
        sortCol: 'chg',
        sortDir: -1,

        setMetric: (m) => {
          heatmapEngine.metric = m;
          document.getElementById('sr-hm-btn-abs').classList.toggle('active', m === 'abs');
          document.getElementById('sr-hm-btn-alpha').classList.toggle('active', m === 'alpha');
          heatmapEngine.render();
        },

        sortBy: (col) => {
          if (heatmapEngine.sortCol === col) heatmapEngine.sortDir *= -1;
          else { heatmapEngine.sortCol = col; heatmapEngine.sortDir = col === 'group' ? 1 : -1; }
          heatmapEngine.render();
        },

        tint: (v) => {
          if (v > 0) return `background:rgba(0,230,118,${Math.min(0.28, 0.04 + Math.abs(v) * 0.012).toFixed(2)});`;
          if (v < 0) return `background:rgba(255,59,92,${Math.min(0.28, 0.04 + Math.abs(v) * 0.012).toFixed(2)});`;
          return '';
        },

        render: () => {
          const flt = document.getElementById('sr-hm-filter-type').value;
          const isAlp = heatmapEngine.metric === 'alpha';
          const nifty50 = rrgEngine.macroNodes.find(n => n.id === 'NIFTY_50');
          const b = nifty50
            ? { d1: nifty50.chg, w1: nifty50.w1, m1: nifty50.m1, m3: nifty50.m3, y1: nifty50.y1 }
            : { d1: 0, w1: 0, m1: 0, m3: 0, y1: 0 };

          const alphaBtn = document.getElementById('sr-hm-btn-alpha');
          if (alphaBtn) alphaBtn.textContent = `Alpha vs NIFTY 50 (${b.d1 > 0 ? '+' : ''}${b.d1.toFixed(2)}%)`;

          let rows = rrgEngine.macroNodes.filter(n => {
            if (flt === 'all') return true;
            if (flt === 'sm_active') return n.preExplodeTier === 'PHASE_3' || n.preExplodeTier === 'PHASE_2' || n.preExplodeTier === 'PHASE_1';
            if (flt === 'sm_p3') return n.preExplodeTier === 'PHASE_3';
            return n.kind === flt;
          }).map(n => ({
            ...n,
            v1d: isAlp ? +(n.chg - b.d1).toFixed(2) : n.chg,
            v1w: isAlp ? +(n.w1 - b.w1).toFixed(2) : n.w1,
            v1m: isAlp ? +(n.m1 - b.m1).toFixed(2) : n.m1,
            v3m: isAlp ? +(n.m3 - b.m3).toFixed(2) : n.m3,
            v1y: isAlp ? +(n.y1 - b.y1).toFixed(2) : n.y1
          }));

          rows.sort((a, b2) => {
            const c = heatmapEngine.sortCol;
            if (c === 'group') return a.group.localeCompare(b2.group) * heatmapEngine.sortDir;
            return ((a[c] || 0) - (b2[c] || 0)) * heatmapEngine.sortDir;
          });

          const renderSMPhaseCell = (r) => {
            const tier = r.preExplodeTier || 'NEUTRAL';
            const sc = r.preExplodeScore || 0;
            const reasons = ui.escAttr((r.preExplodeReasons || []).join(' • ') || `BBW ${r.bbwPct ?? '--'}%`);
            if (tier === 'PHASE_3') return `<span class="sr-pill pill-p3" title="${reasons}">★ P3 · MARKUP (${sc})</span>`;
            if (tier === 'PHASE_2') return `<span class="sr-pill pill-p2" title="${reasons}">◈ P2 · ABSORP (${sc})</span>`;
            if (tier === 'PHASE_1') return `<span class="sr-pill pill-p1" title="${reasons}">◎ P1 · EARLY BASE (${sc})</span>`;
            if (tier === 'EXTENDED') return `<span class="sr-pill pill-amber" title="${reasons}">EXTENDED (${sc})</span>`;
            return `<span class="sr-muted sr-mono" style="font-size:10px;" title="${reasons}">${sc}</span>`;
          };

          document.getElementById('sr-heatmap-table-wrap').innerHTML = `
            <table class="sr-table">
              <thead>
                <tr>
                  <th onclick="SR.heatmapEngine.sortBy('group')">Sector / Market Cap Index ⇅</th>
                  <th>Category</th>
                  <th>RRG Quadrant</th>
                  <th class="sr-num" onclick="SR.heatmapEngine.sortBy('preExplodeScore')">SM Phase ⇅</th>
                  <th>Astro Ruler</th>
                  <th class="sr-num" onclick="SR.heatmapEngine.sortBy('v1d')">1D ⇅</th>
                  <th class="sr-num" onclick="SR.heatmapEngine.sortBy('v1w')">1W ⇅</th>
                  <th class="sr-num" onclick="SR.heatmapEngine.sortBy('v1m')">1M ⇅</th>
                  <th class="sr-num" onclick="SR.heatmapEngine.sortBy('v3m')">3M ⇅</th>
                  <th class="sr-num" onclick="SR.heatmapEngine.sortBy('v1y')">1Y ⇅</th>
                  <th class="sr-num" onclick="SR.heatmapEngine.sortBy('pctAbove50')">&gt;50DMA ⇅</th>
                  <th class="sr-num" onclick="SR.heatmapEngine.sortBy('pctAbove200')">&gt;200DMA ⇅</th>
                  <th class="sr-num">Track A / B</th>
                </tr>
              </thead>
              <tbody>
                ${rows.map(r => {
                  const rowCls = r.preExplodeTier === 'PHASE_3' ? 'sr-row-p3' : (r.preExplodeTier === 'PHASE_2' ? 'sr-row-p2' : (r.preExplodeTier === 'PHASE_1' ? 'sr-row-p1' : ''));
                  return `
                  <tr class="sr-row-click ${rowCls}" onclick="SR.app.drillSectorFromAnywhere('${ui.escAttr(r.id)}')">
                    <td>
                      <span class="sr-bold" style="color:${r.kind === 'cap' ? '#00d4ff' : (r.preExplodeTier === 'PHASE_3' ? '#f5d0fe' : '#e8eef5')};">${r.kind === 'cap' ? '◆ ' : '● '}${r.group}</span>
                      <div class="sr-muted" style="font-size:10px;">${r.desc} • ${r.source || ''}</div>
                    </td>
                    <td><span class="sr-pill ${r.kind === 'cap' ? 'pill-amber' : 'pill-neutral'}">${r.kind === 'cap' ? 'CAP INDEX' : 'SECTOR'}</span></td>
                    <td><span class="sr-pill ${quadPill(r.quadrant)}">${r.quadrant} (${r.heading})</span></td>
                    <td class="sr-num">${renderSMPhaseCell(r)}</td>
                    <td class="sr-mono sr-vio" style="font-size:10.5px;">${r.ruler}</td>
                    ${[r.v1d, r.v1w, r.v1m, r.v3m, r.v1y].map(v =>
                      `<td class="sr-num ${v >= 0 ? 'sr-pos' : 'sr-neg'}" style="${heatmapEngine.tint(v)}">${v > 0 ? '+' : ''}${v.toFixed(2)}%</td>`
                    ).join('')}
                    <td class="sr-num sr-mono">${r.pctAbove50 ?? '--'}%</td>
                    <td class="sr-num sr-mono">${r.pctAbove200 ?? '--'}%</td>
                    <td class="sr-num sr-mono"><span class="sr-pos">${r.trackACount || 0}A</span> / <span class="sr-vio">${r.trackBCount || 0}B</span></td>
                  </tr>
                `;
                }).join('')}
              </tbody>
            </table>
          `;
        }
      };

      const screenerEngine = {
        init: () => {
          const secs = [...new Set(STOCK_DB.map(s => s.sector))].sort();
          document.getElementById('sr-f4-sec-flt').innerHTML = `<option value="ALL">All Sectors (${secs.length})</option>` +
            secs.map(s => `<option value="${ui.escAttr(s)}">${s}</option>`).join('');
          screenerEngine.render();
        },

        render: () => {
          const sec = document.getElementById('sr-f4-sec-flt').value;
          const verd = document.getElementById('sr-f4-verdict-flt').value;
          const sort = document.getElementById('sr-f4-sort').value;
          const q = document.getElementById('sr-f4-search').value.trim().toUpperCase();

          let list = [...STOCK_DB];
          if (sec !== 'ALL') list = list.filter(s => s.sector === sec);
          if (verd !== 'ALL') list = list.filter(s => s.verdict === verd);
          if (q) list = list.filter(s => s.ticker.includes(q) || s.sector.toUpperCase().includes(q) || s.valMethod.toUpperCase().includes(q));

          list.sort((a, b) => {
            if (sort === 'mos') return ((b.fairValue - b.price) / b.price) - ((a.fairValue - a.price) / a.price);
            if (sort === 'sm') return b.smScore - a.smScore;
            if (sort === 'peg') return a.peg - b.peg;
            if (sort === 'cagr') return b.epsCagr - a.epsCagr;
            return a.ticker.localeCompare(b.ticker);
          });

          document.getElementById('sr-f4-count').textContent = `${list.length} of ${STOCK_DB.length} Equities`;
          document.getElementById('sr-f4-tbody').innerHTML = list.map(s => {
            const up = ((s.fairValue - s.price) / s.price) * 100;
            const gann = gannSq9Ref(s.price);
            const safeTk = ui.escAttr(s.ticker);
            return `
              <tr class="sr-row-click" onclick="SR.inspectorModal.open('${safeTk}')">
                <td>
                  <span class="sr-ticker-btn">${s.ticker}</span>
                  <div class="sr-muted" style="font-size:10px;">${s.sector} • ${s.stage}</div>
                </td>
                <td><span class="sr-pill pill-neutral">${s.valMethod}</span></td>
                <td class="sr-num sr-bold">₹${s.price.toFixed(2)}</td>
                <td class="sr-num sr-bold sr-info">${s.fwdPe.toFixed(1)}x</td>
                <td class="sr-num sr-muted">${s.secPe.toFixed(1)}x</td>
                <td class="sr-num ${s.peg <= 1.25 ? 'sr-pos' : s.peg > 1.75 ? 'sr-warn' : ''}">${s.peg.toFixed(2)}x</td>
                <td class="sr-num sr-pos">+${s.epsCagr.toFixed(1)}%</td>
                <td class="sr-num sr-mono">${s.roe.toFixed(1)}% / ${s.roce.toFixed(1)}%</td>
                <td class="sr-num sr-pos sr-bold">₹${s.fairValue.toLocaleString('en-IN')}</td>
                <td class="sr-num sr-bold ${up >= 0 ? 'sr-pos' : 'sr-neg'}">${up > 0 ? '+' : ''}${up.toFixed(1)}%</td>
                <td><span class="sr-pill ${verdictPill(s.verdict)}">${s.verdict}</span></td>
                <td class="sr-num sr-bold ${s.netInstCr >= 0 ? 'sr-pos' : 'sr-neg'}">${ui.fmtCr(s.netInstCr)}</td>
                <td><span class="sr-gann-pill">90°: ₹${Math.round(gann.r90)} | 180°: ₹${Math.round(gann.r180)}</span></td>
              </tr>
            `;
          }).join('');
        }
      };

      const execEngine = {
        bucket: 'dual',
        capital: 1000000,
        gttPct: 0.42,
        showFormulas: true,

        toggleFormulaDrawer: () => {
          execEngine.showFormulas = !execEngine.showFormulas;
          document.getElementById('sr-f5-formula-drawer').style.display = execEngine.showFormulas ? 'block' : 'none';
          document.getElementById('sr-btn-toggle-formulas').textContent = execEngine.showFormulas ? 'Hide Formula Cards' : 'Show Formula Cards';
        },

        setBucket: (b) => {
          execEngine.bucket = b;
          ['dual', 'swing', 'core', 'all'].forEach(k => document.getElementById(`sr-bkt-${k}`).classList.toggle('active', k === b));
          execEngine.render();
        },

        updateCap: (v) => {
          execEngine.capital = Math.max(50000, parseFloat(v) || 1000000);
          execEngine.render();
        },

        updateGtt: (pct) => {
          execEngine.gttPct = parseInt(pct, 10) / 100;
          document.getElementById('sr-exec-gtt-lbl').textContent = `${pct}%`;
          execEngine.updateSummary(execEngine.getStocks());
        },

        getStocks: () => {
          if (execEngine.bucket === 'dual') return STOCK_DB.filter(s => s.isCore && s.isSwing);
          if (execEngine.bucket === 'swing') return STOCK_DB.filter(s => s.isSwing);
          if (execEngine.bucket === 'core') return STOCK_DB.filter(s => s.isCore);
          return [...STOCK_DB];
        },

        setAccount: (ticker, person) => {
          const st = STOCK_DB.find(s => s.ticker === ticker);
          if (!st) return;
          st.assigned = person;
          const seg = evaluateSeg3(st);
          ui.toast(`${ticker} routed to ${seg.person} (${seg.badge})`);
          execEngine.render();
          overviewEngine.render();
          astroEngine.render();
        },

        editCell: (ticker, field, raw) => {
          const st = STOCK_DB.find(s => s.ticker === ticker);
          if (!st) return;
          const val = raw.trim();
          if (field === 'price') st.price = Math.max(1, parseFloat(val) || st.price);
          if (field === 'entry') st.entry = val;
          if (field === 'sl') st.sl = parseFloat(val) || st.sl;
          if (field === 'cap') {
            const parsed = parseFloat(val.replace('%', ''));
            st.cap = isNaN(parsed) ? (st.cap ?? 8) : Math.max(0, Math.min(100, parsed));
          }
          execEngine.render();
        },

        render: () => {
          const list = execEngine.getStocks().sort((a, b) => a.ticker.localeCompare(b.ticker));
          const thead = document.getElementById('sr-exec-thead');
          const tbody = document.getElementById('sr-exec-tbody');

          if (execEngine.bucket === 'dual' || execEngine.bucket === 'all') {
            thead.innerHTML = `<tr>
              <th>Ticker / Sector</th><th class="sr-num">Live CMP (₹)</th><th>Seg-3 Account</th><th>Stage 2 Entry Zone</th>
              <th class="sr-num">ATR Hard SL</th><th class="sr-num">1-2M T1 / T2</th><th class="sr-num">8-12M Base / Bull</th>
              <th class="sr-num">R:R (T1)</th><th class="sr-num">Alloc %</th><th class="sr-num">Alloc ₹</th><th class="sr-num">Shares</th>
              <th>Audit</th><th>Gann Ref (Non-Exec)</th>
            </tr>`;
          } else if (execEngine.bucket === 'swing') {
            thead.innerHTML = `<tr>
              <th>Ticker / Sector</th><th class="sr-num">Live CMP (₹)</th><th>Seg-3 Account</th><th>20-DMA / Retest Entry</th>
              <th class="sr-num">SwingLow−1.5×ATR</th><th class="sr-num">Target 1 (2R)</th><th class="sr-num">Target 2 (3.5R)</th>
              <th class="sr-num">R:R (T1/T2)</th><th class="sr-num">Alloc %</th><th class="sr-num">Alloc ₹</th><th class="sr-num">Shares</th>
              <th>Audit</th><th>Gann Ref (Non-Exec)</th>
            </tr>`;
          } else {
            thead.innerHTML = `<tr>
              <th>Ticker / Sector</th><th class="sr-num">Live CMP (₹)</th><th>Seg-3 Account</th><th>0.85–0.95×FV Entry</th>
              <th>Fundamental KPI Stop</th><th class="sr-num">Base FV (12M)</th><th class="sr-num">Bull (+15% Rerating)</th>
              <th>Valuation Model</th><th class="sr-num">Alloc %</th><th class="sr-num">Alloc ₹</th><th class="sr-num">Shares</th>
              <th>Audit</th><th>Gann Ref (Non-Exec)</th>
            </tr>`;
          }

          tbody.innerHTML = list.map(s => {
            const seg = evaluateSeg3(s);
            const gann = gannSq9Ref(s.price);
            const capPct = s.cap ?? 8;
            const allocAmt = execEngine.capital * (capPct / 100);
            const shares = Math.floor(allocAmt / s.price);
            const risk = Math.max(1, s.price - s.sl);
            const rr1 = ((s.t1 - s.price) / risk).toFixed(1);
            const rr2 = ((s.t2 - s.price) / risk).toFixed(1);
            const safeTk = ui.escAttr(s.ticker);

            const acctDropdown = `
              <select class="sr-select" style="padding:2px 5px; font-size:10.5px; color:${seg.status === 'pass' ? '#00e676' : '#ff3b5c'};" onchange="SR.execEngine.setAccount('${safeTk}', this.value)">
                <option value="Kritika" ${s.assigned === 'Kritika' ? 'selected' : ''}>Kritika Patel (PASS)</option>
                <option value="Vina" ${s.assigned === 'Vina' ? 'selected' : ''}>Vina Patel (PASS)</option>
                <option value="Jigar" ${s.assigned === 'Jigar' ? 'selected' : ''}>Jigar Patel (VETO)</option>
                <option value="Dipak" ${s.assigned === 'Dipak' ? 'selected' : ''}>Dipak Patel (VETO)</option>
              </select>
            `;

            let midCells = '';
            if (execEngine.bucket === 'dual' || execEngine.bucket === 'all') {
              midCells = `
                <td class="sr-mono sr-vio"><span class="sr-editable" contenteditable="true" onblur="SR.execEngine.editCell('${safeTk}','entry',this.innerText)">${s.entry}</span></td>
                <td class="sr-num sr-neg"><span class="sr-editable" contenteditable="true" onblur="SR.execEngine.editCell('${safeTk}','sl',this.innerText)">${s.sl}</span></td>
                <td class="sr-num sr-pos">${s.t1} / ${s.t2}</td>
                <td class="sr-num sr-info sr-bold">₹${s.base} / ₹${s.bull}</td>
                <td class="sr-num sr-bold">${rr1}:1</td>
              `;
            } else if (execEngine.bucket === 'swing') {
              midCells = `
                <td class="sr-mono sr-vio"><span class="sr-editable" contenteditable="true" onblur="SR.execEngine.editCell('${safeTk}','entry',this.innerText)">${s.entry}</span></td>
                <td class="sr-num sr-neg"><span class="sr-editable" contenteditable="true" onblur="SR.execEngine.editCell('${safeTk}','sl',this.innerText)">${s.sl}</span></td>
                <td class="sr-num sr-pos">${s.t1}</td>
                <td class="sr-num sr-pos sr-bold">${s.t2}</td>
                <td class="sr-num sr-bold">${rr1}:1 / ${rr2}:1</td>
              `;
            } else {
              midCells = `
                <td class="sr-mono sr-vio"><span class="sr-editable" contenteditable="true" onblur="SR.execEngine.editCell('${safeTk}','entry',this.innerText)">${s.entry}</span></td>
                <td class="sr-neg" style="font-size:11px;">${s.kpiStop}</td>
                <td class="sr-num sr-pos sr-bold">₹${s.base}</td>
                <td class="sr-num sr-info sr-bold">₹${s.bull}</td>
                <td><span class="sr-pill pill-neutral">${s.valMethod}</span></td>
              `;
            }

            return `
              <tr>
                <td>
                  <span class="sr-ticker-btn" onclick="SR.inspectorModal.open('${safeTk}')">${s.ticker}</span>
                  <div class="sr-muted" style="font-size:10px;">${s.sector}</div>
                </td>
                <td class="sr-num sr-bold"><span class="sr-editable" contenteditable="true" onblur="SR.execEngine.editCell('${safeTk}','price',this.innerText)">${s.price.toFixed(2)}</span></td>
                <td>${acctDropdown}</td>
                ${midCells}
                <td class="sr-num"><span class="sr-editable" contenteditable="true" onblur="SR.execEngine.editCell('${safeTk}','cap',this.innerText)">${capPct}%</span></td>
                <td class="sr-num">${ui.fmtInr(allocAmt)}</td>
                <td class="sr-num sr-bold sr-info">${shares}</td>
                <td><button class="sr-btn" style="padding:2px 7px; font-size:10px;" onclick="SR.inspectorModal.open('${safeTk}')">Math →</button></td>
                <td><span class="sr-gann-pill">90°: ₹${Math.round(gann.r90)} | 180°: ₹${Math.round(gann.r180)}</span></td>
              </tr>
            `;
          }).join('');

          execEngine.updateSummary(list);
        },

        updateSummary: (list) => {
          const sumPct = list.reduce((a, s) => a + (s.cap ?? 8), 0);
          const gttAmt = execEngine.capital * execEngine.gttPct;
          const p1Amt = execEngine.capital - gttAmt;
          document.getElementById('sr-exec-p1-val').textContent = ui.fmtInr(p1Amt);
          document.getElementById('sr-exec-p2-val').textContent = ui.fmtInr(gttAmt);
          document.getElementById('sr-exec-sum-val').textContent = `${sumPct}%`;
        }
      };

      const astroEngine = {
        render: () => {
          document.getElementById('sr-f6-eph-strip').innerHTML = EPHEMERIS_NOV20.map(e => `
            <div class="sr-eph-box">
              <div style="display:flex; justify-content:space-between; margin-bottom:2px;">
                <strong class="sr-info">${e.body}</strong>
                <span class="${e.motion === 'Retrograde' ? 'sr-neg' : 'sr-pos'}" style="font-size:9.5px;">${e.motion}</span>
              </div>
              <div class="sr-bold">${e.pos}</div>
              <div class="sr-muted" style="font-size:10px;">${e.nak}</div>
            </div>
          `).join('');

          document.getElementById('sr-f6-seg2-tbody').innerHTML = STOCK_DB.map(s => {
            const secNode = UNIVERSE_DB.find(n => n.group === s.sector);
            const seg = evaluateSeg3(s);
            const safeTk = ui.escAttr(s.ticker);
            return `
              <tr class="sr-row-click" onclick="SR.inspectorModal.open('${safeTk}')">
                <td><span class="sr-ticker-btn">${s.ticker}</span></td>
                <td class="sr-mono sr-vio" style="font-size:10.5px;">${secNode ? secNode.ruler : 'Jupiter'}</td>
                <td style="font-size:11px; white-space:normal; max-width:270px;">${s.ipoNatal}</td>
                <td><span class="sr-pill ${seg.pill}">${seg.person} (${seg.badge})</span></td>
              </tr>
            `;
          }).join('');
        }
      };

      const tgModule = {
        tpl: 'rrg',
        setTpl: (t) => {
          tgModule.tpl = t;
          ['rrg', 'heatmap', 'valuation', 'plan'].forEach(k => document.getElementById(`sr-tg-tpl-${k}`).classList.toggle('active', k === t));
          tgModule.render();
        },

        render: () => {
          const pub = document.getElementById('sr-tg-public-mode').checked;
          const dt = document.getElementById('sr-hdr-date').textContent;
          const n50 = LIVE_TAPE.nifty50 || { last: 0, chg: 0 };

          let txt = '';
          if (tgModule.tpl === 'rrg') {
            const caps = rrgEngine.macroNodes.filter(n => n.kind === 'cap');
            const leads = rrgEngine.macroNodes.filter(n => n.kind === 'sector' && n.quadrant === 'Leading').slice(0, 5);
            const imps = rrgEngine.macroNodes.filter(n => n.kind === 'sector' && n.quadrant === 'Improving').slice(0, 4);
            txt = `📊 *NSE SECTOR & CAP-TIER JdK RRG ROTATION | ${dt}*\\n`;
            txt += `NIFTY 50: ${n50.last} (${n50.chg > 0 ? '+' : ''}${n50.chg.toFixed(2)}%) | Breadth: ${LIVE_TAPE.adv || 0} Adv / ${LIVE_TAPE.dec || 0} Dec\\n\\n`;
            txt += `*◆ Market-Cap Rotation:*\\n`;
            caps.forEach(c => { txt += `• ${c.short}: ${c.quadrant} (${c.heading}) | 1D ${c.chg > 0 ? '+' : ''}${c.chg.toFixed(2)}% | 1M ${c.m1 > 0 ? '+' : ''}${c.m1.toFixed(1)}%\\n`; });
            txt += `\\n*● Leading Sectors:*\\n`;
            leads.forEach(l => { txt += `• ${l.group} (${l.heading}) — 1M ${l.m1 > 0 ? '+' : ''}${l.m1.toFixed(1)}% | >50DMA ${l.pctAbove50 ?? '--'}%\\n`; });
            txt += `\\n*● Improving Rotation:*\\n`;
            imps.forEach(i => { txt += `• ${i.group} (${i.heading}) — 1M ${i.m1 > 0 ? '+' : ''}${i.m1.toFixed(1)}% | >50DMA ${i.pctAbove50 ?? '--'}%\\n`; });
          } else if (tgModule.tpl === 'heatmap') {
            const sorted = [...rrgEngine.macroNodes].sort((a, b) => b.chg - a.chg);
            txt = `🔥 *NSE ALPHA & BREADTH HEATMAP | ${dt}*\\nNIFTY 50: ${n50.last} (${n50.chg > 0 ? '+' : ''}${n50.chg.toFixed(2)}%)\\n\\n`;
            txt += `*Top 5 Outperformers:*\\n`;
            sorted.slice(0, 5).forEach(r => { txt += `• ${r.group}: ${r.chg > 0 ? '+' : ''}${r.chg.toFixed(2)}% (α ${r.alpha > 0 ? '+' : ''}${r.alpha.toFixed(2)}%) | >50DMA ${r.pctAbove50 ?? '--'}%\\n`; });
            txt += `\\n*Bottom 3 Laggards:*\\n`;
            sorted.slice(-3).reverse().forEach(r => { txt += `• ${r.group}: ${r.chg.toFixed(2)}% (α ${r.alpha.toFixed(2)}%)\\n`; });
          } else if (tgModule.tpl === 'valuation') {
            const picks = STOCK_DB.filter(s => s.verdict === 'UNDERVALUED').slice(0, 5);
            txt = `⚖ *INTRINSIC VALUATION & SMART MONEY PICKS | ${dt}*\\n\\n`;
            picks.forEach(s => {
              const up = (((s.fairValue - s.price) / s.price) * 100).toFixed(1);
              txt += `\\`${s.ticker}\\` (${s.valMethod})\\nCMP: ₹${s.price} → Intrinsic FV: ₹${s.fairValue} (${up > 0 ? '+' : ''}${up}% Upside) | Net Inst: ${ui.fmtCr(s.netInstCr)}\\n\\n`;
            });
          } else {
            const gems = STOCK_DB.filter(s => s.isCore && s.isSwing);
            txt = `📋 *7 DUAL-HORIZON GEMS TRADE PLAN | ${dt}*\\n\\n`;
            gems.forEach(s => {
              const seg = evaluateSeg3(s);
              const acctTag = pub ? ' [Seg-3 Verified]' : ` [${seg.person}]`;
              txt += `\\`${s.ticker}\\`${acctTag} | CMP: ₹${s.price} | Entry: ${s.entry} | SL: ${s.sl} | 1-2M T1: ${s.t1} | 12M FV: ₹${s.base}\\n`;
            });
          }

          if (pub) {
            txt = txt.replace(/Kritika Patel|Vina Patel|Jigar Patel|Dipak Patel/g, 'Verified Account');
            txt += `\\n---\\n*DISCLAIMER: Educational & institutional research only. Not SEBI RIA investment advice. Gann levels are reference-only geometry.*`;
          }
          document.getElementById('sr-tg-preview-box').textContent = txt;
        },

        copyText: () => {
          const txt = document.getElementById('sr-tg-preview-box').textContent;
          if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(txt).then(() => ui.toast('Formatted Telegram post copied!')).catch(() => { ui.copyFallback(txt); ui.toast('Formatted Telegram post copied!'); });
          } else {
            ui.copyFallback(txt);
            ui.toast('Formatted Telegram post copied!');
          }
        },

        copyHtml: () => {
          const html = `<pre>${document.getElementById('sr-tg-preview-box').textContent}</pre>`;
          ui.copyFallback(html);
          ui.toast('HTML snippet copied to clipboard!');
        },

        autoPublish: () => {
          const token = document.getElementById('sr-tg-bot-token').value.trim();
          const chatId = document.getElementById('sr-tg-channel-id').value.trim();
          const text = document.getElementById('sr-tg-preview-box').textContent;
          if (!token || !chatId) { ui.toast('Enter Bot Token and Channel ID first'); return; }
          fetch(`https://api.telegram.org/bot${token}/sendMessage`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ chat_id: chatId, text, parse_mode: 'Markdown' })
          }).then(r => r.json()).then(d => {
            ui.toast(d.ok ? 'Published to Telegram!' : `Telegram Error: ${d.description}`);
          }).catch(() => ui.toast('Network error sending to Telegram API'));
        }
      };

      const inspectorModal = {
        open: (ticker, sectorId = null) => {
          const s = STOCK_DB.find(x => x.ticker === ticker);
          if (s) {
            const up = (((s.fairValue - s.price) / s.price) * 100).toFixed(1);
            const gann = gannSq9Ref(s.price);
            const seg = evaluateSeg3(s);
            const secNode = UNIVERSE_DB.find(n => n.group === s.sector);
            const risk = Math.max(1, s.price - s.sl);
            const rr1 = ((s.t1 - s.price) / risk).toFixed(1);
            const rr2 = ((s.t2 - s.price) / risk).toFixed(1);
            const coreBandLow = Math.round(s.fairValue * 0.85);
            const coreBandHigh = Math.round(s.fairValue * 0.95);
            const struct150Stop = Math.round((s.dma150 || s.price * 0.9) - (s.atr14 || s.price * 0.02));

            document.getElementById('sr-insp-hdr-title').textContent = `${s.ticker} — ${s.name} (${s.sector}) | COMPLETE BUY / SL / TARGET AUDIT`;
            document.getElementById('sr-insp-modal-body').innerHTML = `
              <div class="sr-meth-grid">
                <div class="sr-meth-card">
                  <h4>⚡ 1–2 Month Swing Derivation (Technical + ATR)</h4>
                  <div class="sr-formula-box">Live CMP: ₹${s.price.toFixed(2)} | 20-DMA: ₹${s.dma20} | Swing Low: ₹${s.swingLow} | ATR(14): ₹${s.atr14}</div>
                  <div><strong>Entry Zone:</strong> <span class="sr-vio sr-bold">${s.entry}</span> <span class="sr-muted">(20-DMA retest to CMP+0.5×ATR)</span></div>
                  <div><strong>Hard Stop-Loss:</strong> <span class="sr-neg sr-bold">₹${s.sl}</span> <span class="sr-muted">(Swing Low − 1.5×ATR = ₹${(s.swingLow - 1.5 * s.atr14).toFixed(0)})</span></div>
                  <div><strong>Target 1 (T1):</strong> <span class="sr-pos sr-bold">₹${s.t1}</span> <span class="sr-muted">(${rr1}:1 R:R partial exit)</span></div>
                  <div><strong>Target 2 (T2):</strong> <span class="sr-pos sr-bold">₹${s.t2}</span> <span class="sr-muted">(${rr2}:1 R:R Fib 1.618 extension)</span></div>
                </div>
                <div class="sr-meth-card">
                  <h4>🏛 8–12 Month Core Derivation (Intrinsic Valuation)</h4>
                  <div class="sr-formula-box">Model: ${s.valMethod} | Fwd FY28E P/E: ${s.fwdPe}x vs Sec ${s.secPe}x | PEG: ${s.peg}x</div>
                  <div><strong>Accumulation Band:</strong> <span class="sr-info sr-bold">₹${coreBandLow} – ₹${coreBandHigh}</span> <span class="sr-muted">(0.85–0.95×FV / 150-DMA ₹${s.dma150})</span></div>
                  <div><strong>Dual Guardrail Stop:</strong> <span class="sr-neg sr-bold">150-DMA−1×ATR (₹${struct150Stop})</span> OR <span class="sr-neg">${s.kpiStop}</span></div>
                  <div><strong>12M Base Target:</strong> <span class="sr-pos sr-bold">₹${s.base} (${up > 0 ? '+' : ''}${up}%)</span> <span class="sr-muted">(3Y EPS CAGR +${s.epsCagr}%, ROE ${s.roe}%)</span></div>
                  <div><strong>12M Bull Target:</strong> <span class="sr-info sr-bold">₹${s.bull}</span> <span class="sr-muted">(+15% valuation multiple rerating)</span></div>
                </div>
                <div class="sr-meth-card">
                  <h4>💰 Smart Money (FII + DII + MF) Rotation</h4>
                  <div><strong>Institutional Regime:</strong> <span class="sr-pill ${smPill(s.smRegime)}">${s.smRegime}</span></div>
                  <div><strong>Quarterly Delta:</strong> FII <span class="${s.fiiQoq >= 0 ? 'sr-pos' : 'sr-neg'}">${s.fiiQoq > 0 ? '+' : ''}${s.fiiQoq}%</span> | DII <span class="${s.diiQoq >= 0 ? 'sr-pos' : 'sr-neg'}">${s.diiQoq > 0 ? '+' : ''}${s.diiQoq}%</span></div>
                  <div><strong>MF Net Flow:</strong> <span class="${s.mfNetCr >= 0 ? 'sr-pos' : 'sr-neg'}">${ui.fmtCr(s.mfNetCr)}</span> | <strong>Combined Net:</strong> <span class="${s.netInstCr >= 0 ? 'sr-pos' : 'sr-neg'} sr-bold">${ui.fmtCr(s.netInstCr)}</span></div>
                  <div><strong>Smart Money Score:</strong> <span class="sr-info sr-bold">${s.smScore}/100</span> • <span class="sr-muted">${s.stage}</span></div>
                </div>
                <div class="sr-meth-card" style="border-color:rgba(168,85,247,0.4);">
                  <h4 style="color:#c084fc;">🪐 Astro-Quant Gatekeeper &amp; Gann Ref</h4>
                  <div><strong>Sector Ruler:</strong> ${secNode ? secNode.ruler : 'Jupiter'}</div>
                  <div><strong>Company IPO Natal:</strong> ${s.ipoNatal}</div>
                  <div><strong>Seg-3 Account:</strong> <span class="sr-pill ${seg.pill}">${seg.person} — ${seg.badge}</span></div>
                  <div style="margin-top:6px; display:flex; gap:8px; flex-wrap:wrap; align-items:center;">
                    <span class="sr-gann-pill">Gann Sq9 (Ref Only): 90° ₹${Math.round(gann.r90)} | 180° ₹${Math.round(gann.r180)}</span>
                    <a href="https://in.tradingview.com/chart/?symbol=NSE:${encodeURIComponent(s.ticker)}" target="_blank" class="sr-btn cyan" style="text-decoration:none; padding:2px 8px; font-size:10px;">TradingView ↗</a>
                  </div>
                </div>
              </div>
            `;
            document.getElementById('sr-inspector-modal').style.display = 'flex';
            return;
          }

          // Fallback for any constituent stock in the 750-stock universe
          let c = null;
          if (sectorId && SECTOR_CONSTITUENTS[sectorId]) {
            c = SECTOR_CONSTITUENTS[sectorId].find(x => x.ticker === ticker);
          }
          if (!c) {
            for (const sid of Object.keys(SECTOR_CONSTITUENTS)) {
              const found = (SECTOR_CONSTITUENTS[sid] || []).find(x => x.ticker === ticker);
              if (found) { c = found; break; }
            }
          }
          if (!c) return;

          const atr = c.atr14 || +(c.price * 0.025).toFixed(1);
          const dma20 = c.dma20 || c.price;
          const swLow = c.swingLow || +(c.price * 0.94).toFixed(1);
          const sl = Math.max(1, Math.round(swLow - 1.5 * atr));
          const entryLow = Math.round(dma20);
          const entryHigh = Math.round(c.price + 0.5 * atr);
          const entryMid = (entryLow + entryHigh) / 2;
          const risk = Math.max(1, entryMid - sl);
          const t1 = Math.round(entryMid + 2.0 * risk);
          const t2 = Math.round(entryMid + 3.5 * risk);
          const gann = gannSq9Ref(c.price);
          const quad = deriveQuadrant(c.angle || 45);

          document.getElementById('sr-insp-hdr-title').textContent = `${c.ticker} — ${c.name} (${c.sector}) | LIVE UNIVERSE TECHNICAL & RRG AUDIT`;
          document.getElementById('sr-insp-modal-body').innerHTML = `
            <div class="sr-meth-grid">
              <div class="sr-meth-card">
                <h4>⚡ Dynamic 1–2M ATR Swing Levels</h4>
                <div class="sr-formula-box">Live CMP: ₹${c.price.toFixed(2)} | 20-DMA: ₹${dma20} | 150-DMA: ₹${c.dma150 || '--'} | ATR(14): ₹${atr}</div>
                <div><strong>Swing Entry Band:</strong> <span class="sr-vio sr-bold">₹${entryLow} – ₹${entryHigh}</span> <span class="sr-muted">(20-DMA to CMP+0.5×ATR)</span></div>
                <div><strong>Hard Stop-Loss:</strong> <span class="sr-neg sr-bold">₹${sl}</span> <span class="sr-muted">(20D Swing Low ₹${swLow} − 1.5×ATR)</span></div>
                <div><strong>Target 1 (2R):</strong> <span class="sr-pos sr-bold">₹${t1}</span> | <strong>Target 2 (3.5R):</strong> <span class="sr-pos sr-bold">₹${t2}</span></div>
              </div>
              <div class="sr-meth-card">
                <h4>◎ Relative Strength &amp; Scanner Status</h4>
                <div class="sr-formula-box">RRG Quadrant: ${quad} (Angle ${c.angle}°, Radius ${c.radius})</div>
                <div><strong>1D / 1W / 1M:</strong> <span class="${c.chg >= 0 ? 'sr-pos' : 'sr-neg'}">${c.chg}%</span> / ${c.w1}% / ${c.m1}%</div>
                <div><strong>3M / 1Y / α vs Nifty 50:</strong> ${c.m3}% / ${c.y1}% / <span class="${(c.alpha3m || 0) >= 0 ? 'sr-pos' : 'sr-neg'}">${(c.alpha3m || 0) > 0 ? '+' : ''}${c.alpha3m}%</span></div>
                <div style="margin-top:6px; display:flex; gap:8px; flex-wrap:wrap; align-items:center;">
                  ${c.signalTag ? `<span class="sr-pill ${c.signalTag === 'TRACK A' ? 'pill-emerald' : 'pill-violet'}">${c.signalTag} SIGNAL ACTIVE</span>` : '<span class="sr-pill pill-neutral">UNIVERSE CONSTITUENT</span>'}
                  <span class="sr-gann-pill">Gann Sq9 (Ref Only): 90° ₹${Math.round(gann.r90)} | 180° ₹${Math.round(gann.r180)}</span>
                  <a href="https://in.tradingview.com/chart/?symbol=NSE:${encodeURIComponent(c.ticker)}" target="_blank" class="sr-btn cyan" style="text-decoration:none; padding:2px 8px; font-size:10px;">TradingView ↗</a>
                </div>
              </div>
            </div>
          `;
          document.getElementById('sr-inspector-modal').style.display = 'flex';
        },
        close: () => { document.getElementById('sr-inspector-modal').style.display = 'none'; }
      };

      const methodologyModal = {
        open: () => { document.getElementById('sr-methodology-modal').style.display = 'flex'; },
        close: () => { document.getElementById('sr-methodology-modal').style.display = 'none'; }
      };

      const csvModal = {
        open: () => { document.getElementById('sr-csv-modal').style.display = 'flex'; },
        close: () => { document.getElementById('sr-csv-modal').style.display = 'none'; },
        process: () => {
          const raw = document.getElementById('sr-csv-textarea').value.trim();
          const nl = String.fromCharCode(10);
          if (raw) {
            raw.split(nl).forEach(line => {
              const c = line.split(',').map(x => x.trim());
              if (c.length < 3) return;
              const key = c[0];
              const ang = parseFloat(c[1]);
              const rad = parseFloat(c[2]);
              const chg = parseFloat(c[3]);
              const alp = parseFloat(c[4]);
              const prc = parseFloat(c[5]);
              const flw = parseFloat(c[6]);

              const node = UNIVERSE_DB.find(n => n.id.toLowerCase() === key.toLowerCase() || n.group.toLowerCase() === key.toLowerCase());
              if (node) {
                node._csvOverridden = true;
                if (!isNaN(ang)) node.angle = ang;
                if (!isNaN(rad)) node.radius = rad;
                if (!isNaN(chg)) node.chg = chg;
                if (!isNaN(alp)) node.alpha = alp;
                if (!isNaN(flw)) node.fii = flw;
              }
              const st = STOCK_DB.find(s => s.ticker.toLowerCase() === key.toLowerCase());
              if (st) {
                st._csvOverridden = true;
                if (!isNaN(ang)) st.angle = ang;
                if (!isNaN(rad)) st.radius = rad;
                if (!isNaN(chg)) st.chg = chg;
                if (!isNaN(prc) && prc > 0) st.price = prc;
              }
            });
          }
          document.getElementById('sr-hdr-date').textContent = document.getElementById('sr-csv-date').value;
          document.getElementById('sr-hdr-fii').textContent = document.getElementById('sr-csv-fii').value;
          document.getElementById('sr-hdr-dii').textContent = document.getElementById('sr-csv-dii').value;

          rrgEngine.build();
          overviewEngine.render();
          rrgEngine.renderAll();
          heatmapEngine.render();
          screenerEngine.render();
          execEngine.render();
          tgModule.render();
          csvModal.close();
          ui.toast('EOD override applied & Sector Rotation views updated');
        }
      };

      return { app, overviewEngine, rrgEngine, heatmapEngine, screenerEngine, execEngine, astroEngine, tgModule, inspectorModal, methodologyModal, csvModal };
    })();
    """

    sr_js = sr_js.replace("__SECTOR_ROTATION_JSON__", payload_json)
    return sr_css, sr_html, sr_js
