# FX Trading Strategy — Detail

## Strategy: CAD Mean-Reversion
- When CAD is historically strong vs a foreign currency → convert to that currency
- When CAD weakens back toward mean → convert back to CAD at a profit
- No carry income (IBKR doesn't pay interest on Warren's position sizes)
- CADJPY exception: JPY charges negative interest — small drag

## CAD/USD 20-year range (as of 2026-04-08)
- p5: 0.719, median: 0.792, p95: 1.007
- Entry zone: CAD/USD crosses above ~0.80–0.82 (60th–65th percentile)

## Thresholds
- Entry: p99 (CAD extremely strong)
- Exit: p75 (mean reversion target)

## Cross Selection
Sequential / first-to-trigger preferred (correlations too high during broad CAD-strength events).
Priority: USD first (liquidity), then EUR, GBP.

## Infrastructure
- IB Gateway 1037 at ~/Jts/ibgateway/1037/ — paper trading port 4002, live port 7497
- ib_insync in ~/ibkr/venv
- Monitor script: ~/ibkr/monitor.py (runs 9am ET weekdays, cron ID: ba53c41d-f310-4060-a7d3-cef5321a601a)
- Trade executor: ~/ibkr/trade.py
- State file: ~/ibkr/state.json
- Signal file: ~/ibkr/signal.json (written on signal, deleted after trade/skip)

## Signal Flow
monitor.py → if signal, sends Telegram alert with inline ✅ Execute / ⏭ Skip buttons → if Execute, trade.py runs directly → confirms fill via Telegram edit
No AI involved. Zero LLM tokens burned unless Warren asks Rei something separately.

## FX Dashboard & Email
- ~/ibkr/dashboard.py — dark-theme PNG dashboard + rich HTML email
- ~/ibkr/indicators.py — leading indicators: oil trend, VIX, RSI, rate spread, COT positioning
- To send: `~/ibkr/venv/bin/python3 ~/ibkr/dashboard.py --email --to <address>`
- Trigger phrase: "send the FX dashboard to john@example.com"
- Requires IB Gateway running (port 4002 paper / 7497 live)

## Current Status (as of 2026-04-24)
- System live on paper trading
- Watching CADJPY for exit signal (~107–108, p75 target)
- IBKR live switch (4002 → 7497) pending — flip when ready
