# 🌌 AntiGravity Smart Money Dual Track Radar

Automated daily intelligence bot running on a **Hybrid Data Engine**:
1. **Deep Historical Base (yfinance):** Pulls 2 years of daily data for 200 SMA, 30-week SMA, and 120-day volatility baselines.
2. **Official NSE India Live Feed:** Hits official `nseindia.com` endpoints at 05:00 PM IST to extract the official closing price, high, low, total traded volume, and **official delivery percentage** (filtering out intraday noise).
3. **Dual-Track Segmentation:** Separates **Active Day-1 Breakouts** from **Pre-Breakout Squeezes** (before they explode).

---

## 📋 Dual-Track Screening Engine
Every stock must first pass the **Institutional Quality Base**:
* **Market Cap:** ₹2,000 Cr to ₹35,000 Cr
* **Valuation & Balance Sheet:** P/E < 80.0, Debt to Equity < 1.5
* **Profitability & Quality:** ROE >= 15.0%, ROCE >= 20.0%
* **Cash Flow Reality:** OCF / PAT > 1.0 (> 100% Cash Conversion)

---

### 💣 Track B: HALO Pre-Breakout Squeeze Leaderboard (BEFORE It Explodes)
Spots stocks coiling tightly in a quantitative compression base right beneath resistance:
1. **Rule 1 — ATR Contraction:** Current $\text{ATR}(14) \le 85\%$ of its 20-session baseline, and $\text{ATR}\% \le$ 60-session median.
2. **Rule 2 — Bollinger Band Squeeze:** 20-period 2-SD $\text{BBW} \le$ 25th percentile of preceding 120 completed sessions.
3. **Rule 3 — Volume Dry-Up:** Average volume over last 5 sessions $\le 75\%$ of 20-session average volume.
4. **Rule 4 — Daily Trend Alignment:** $\text{Close} \ge \text{SMA}(50) \ge \text{SMA}(200)$, with $\text{SMA}(50)$ higher than 10 sessions ago.
5. **Rule 5 — Weekly Trend Confirmation:** Completed weekly close $\ge$ 30-week SMA, and 30W SMA rising over 4 weeks.
6. **Rule 6 — Proximity to Resistance:** Current close is **0.0% to 5.5%** below the 20-day breakout pivot (fixed at $t-1$).
7. **Rule 7 — Base Integrity:** Close above 20-day low; 20-day base range $\le 1.8\times$ 60-session median daily range.
* **100-Point HALO Leaderboard:** Candidates are scored across ATR contraction (20), BBW percentile (15), Volume dry-up (10), Daily trend (15), Weekly 30W slope (15), Pivot proximity (10), 3M Relative Strength vs Nifty 500 (10), and Base tightness (5).

---

### 🎯 Systematic Trade Execution Protocol for Track B (Squeeze Candidates)

For every stock flagged on the HALO Squeeze Leaderboard, the bot automatically computes and outputs:
1. **Buy Trigger:** Placed as a **Buy-Stop Limit Order** at `Pivot + 1 tick` ($+0.10\%$).
2. **Initial Stop-Loss ($1R$):** Anchored to the structural **5-Day Base Low** or $1.5\times \text{ATR}(14)$.
3. **Target 1 ($+2R$):** Exit **40% of position**.
4. **The Retest Anchor Rule (No Premature Shakeouts):**
   * Upon $T_1$ fill, stop-loss on remaining shares is **NOT** moved to exact breakeven.
   * It is moved to **1 tick below the Breakout Pivot** (`Pivot - 0.20%`), giving the stock room to execute a standard throwback/retest without knocking you out.
5. **Target 2 ($+3R$):** Exit **30% of position**.
6. **The Multibagger Runner (30%):** Remaining 30% has **no fixed target**; it is trailed systematically with the **20-Day EMA** or weekly close to ride sustained multi-month expansions.
7. **Actionable Rationale:** Every alert synthesizes a direct, single-sentence summary detailing the exact degree of volatility contraction, volume dry-up ratio, macro 30W SMA trend slope, and earnings cash-conversion quality.

---

### 🚀 Track A: Active Breakout & 5-Day Retest State Engine (TODAY'S EXPANSIONS)

Spots confirmed institutional breakouts and manages them through a 5-day state window:
1. **Rule A1 — Breakout Pivot:** Closing price $> P_t$ where $P_t = \max(H_{t-20:t-1})$ (excluding session $t$).
2. **Rule A2 — Volume Expansion:** Volume ratio $\ge 1.5\times$ 20-session baseline (up to 20 pts).
3. **Rule A3 — Closing Range Ratio (CRR):** $\text{CRR} = \frac{\text{Close} - \text{Low}}{\text{High} - \text{Low}} \ge 0.70$ (Closed in top 30% of day's range).
4. **Rule A4 — Range Expansion:** Daily range $\ge 1.2\times \text{ATR}(14)_{t-1}$ (with exhaustion guard if $> 2.2\times$).
5. **Rule A5 — Daily Trend Alignment:** $\text{Close} \ge \text{SMA}(50) \ge \text{SMA}(200)$, with $\text{SMA}(50)$ rising over 10 sessions.
6. **Rule A6 — Weekly Trend Confirmation:** Completed weekly close $\ge$ 30-week SMA, and 30W SMA rising over 4 weeks.
7. **Rule A7 — Anti-Chase Extension Gate:** Planned entry cannot be $> 3.0\%$ above pivot.
* **5-Day Confirmation & Retest State Machine:**
  * `ACTIVE_BREAKOUT`: Fresh Day-1 breakout trigger.
  * `CONFIRMED_RETEST`: Successfully tested pivot within 5 sessions without breaching the 1.0% failure tolerance.
  * `ENTRY_EXTENDED`: Price $>3\%$ above pivot (No chase, wait for retest).
  * `PIVOT_FAILURE`: Daily close fell $>1\%$ below breakout pivot during the window.
* **Two-Target Trade Execution (50% / 50%):**
  * **Structural SL:** $\text{BaseLow} - (0.25\times \text{ATR}_{14})$ or $\text{RetestLow} - (0.25\times \text{ATR}_{14})$.
  * **Target 1 ($+2R$):** Exit 50% and move SL to Cost ($+0.35\%$).
  * **Target 2 ($+3R$):** Exit remaining 50% (Net Payoff: $+2.5R$ on full winners).

---

## ⏰ Schedule

* **Daily Run Time:** Every trading day (Monday to Friday) at **05:00 PM IST** (11:30 AM UTC), 1.5 hours after market close so all EOD BhavCopy prices, volumes, and returns are fully consolidated.
* **Execution Environment:** GitHub Actions Cloud (Free & 100% automated).

---

## 🚀 Activation in 3 Steps

1. Get your Bot Token from `@BotFather` on Telegram for `@Elitestock31187bot`.
2. Push this repo to your private GitHub repository:
   ```bash
   git init
   git add .
   git commit -m "Configure NSE Market Lens 5PM Screener"
   git branch -M main
   git remote add origin https://github.com/<your-username>/nse-marketlens-bot.git
   git push -u origin main
   ```
3. In your GitHub repo:
   * Go to **Settings** $\rightarrow$ **Secrets and variables** $\rightarrow$ **Actions** $\rightarrow$ **New repository secret**.
   * Add:
     * `TELEGRAM_BOT_TOKEN`: *[Your Bot Token]*
     * `TELEGRAM_CHAT_ID`: *[Your Telegram Chat ID or Channel ID]*

You can also run it immediately anytime by opening the **Actions** tab on GitHub and clicking **Run workflow**.
