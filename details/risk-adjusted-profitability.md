# Risk-Adjusted Profitability Metrics — Actuarial Function

## Context
A key deliverable for Warren's new role: establish a consistent risk-adjusted profitability metric (or set of metrics) for insurance products across the actuarial function. Needed for pricing governance, product comparison, and connecting actuarial work to financial performance.

---

## Metric Evaluation

### 1. Return on Equity (ROE)
Return divided by equity. Simple, widely understood.
- ❌ Doesn't adjust for risk explicitly — high ROE with volatile returns looks the same as stable ROE
- *Verdict: baseline standard, necessary but insufficient on its own*

### 2. Risk-Adjusted Return on Capital (RAROC) ⭐ Recommended
Return divided by economic capital (capital held against the risk).
- ✅ Accounts for how much risk is taken to earn the return
- ✅ Enables apples-to-apples comparison across products with different risk profiles
- ✅ Gold standard for internal product comparison — widely used in banking, increasingly in insurance
- *Verdict: primary metric recommendation*

### 3. Value of New Business (VNB) / CSM ⭐ Recommended
Present value of future profits from new business. Under IFRS 17, Contractual Service Margin (CSM) is essentially VNB.
- ✅ Directly IFRS 17 aligned — connects to how the board sees financial performance
- ✅ Excellent for life/long-term insurance
- ✅ CSM Yield (CSM as % of PV future premiums) is an emerging quality-of-profitability measure
- *Verdict: pair with RAROC for a complete picture*

### 4. Internal Rate of Return (IRR)
Discount rate at which NPV of future cash flows = 0.
- ✅ Easy to compare against hurdle rates
- ❌ Doesn't capture risk profile of cash flows
- *Verdict: useful supplementary metric*

### 5. Embedded Value (EV) / European Embedded Value (EEV)
PV of in-force business + adjusted net worth.
- ⚠️ Legacy metric, declining relevance under IFRS 17
- Still used for M&A and investor reporting in some contexts
- *Verdict: retain awareness, not primary*

### 6. Economic Capital Return
Similar to RAROC but uses internal economic capital model vs. regulatory capital.
- ✅ More accurate than regulatory capital-based metrics
- ❌ Requires robust internal capital model
- *Verdict: longer-term aspiration once internal model is mature*

### 7. Combined Ratio (P&C)
(Claims + expenses) / premiums.
- P&C standard operational metric
- Not truly risk-adjusted
- *Verdict: P&C only, not applicable to life*

### 8. Sharpe Ratio (adapted)
Excess return / volatility of returns. Investment concept adapted to product portfolios.
- Interesting for portfolio-level view
- Less common at individual product level
- *Verdict: useful for portfolio analysis, not primary product metric*

---

## Recommendation
**Primary framework: RAROC + VNB/CSM-based metrics**

- **RAROC** — risk-adjusted comparability across products; answers "are we being compensated for the risk we're taking?"
- **VNB/CSM yield** — directly aligned to IFRS 17 reporting; answers "what quality of new business are we writing?"
- **IRR vs. hurdle rate** — supplementary; useful for individual product go/no-go decisions

---

## Next Steps
- Assess current state — what metrics are used today and how consistently?
- Align with CFO/finance on preferred framework (RAROC requires agreement on economic capital methodology)
- Build into pricing governance agent as evaluation criteria
- Consider embedding in the AI process optimization pipeline as a standard output for any process touching product profitability
