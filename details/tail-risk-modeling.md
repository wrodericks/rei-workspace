# Tail Risk Modeling — Interest Rate Risk

## Context
A key deliverable for Warren's new role: develop sophisticated tail risk modeling for interest rate risk within the actuarial function. Particularly important for a life insurer given long-duration liability exposure.

---

## Why This Matters for Life Insurance
- Long-duration liabilities (20-40 year policies) create massive duration mismatch risk
- Standard VaR/CTE metrics underestimate tail events (1994 rate spike, 2008, 2022 +400bps move)
- IFRS 17 + LICAT both require risk margin calculations — better tail modeling improves quality of those margins
- OSFI stress testing requirements — sophisticated models strengthen regulatory submissions
- Pricing governance — tail risk assumptions should flow directly into product pricing

---

## Methodological Options

### 1. Conditional Tail Expectation (CTE / CVaR)
Already standard in Canadian actuarial practice (CIA). Captures average of worst X% scenarios.
- ✅ Regulatory acceptance — CIA and OSFI familiar with CTE
- ✅ Good baseline
- ❌ Underestimates truly extreme tails (depends on distributional assumptions)
- *Verdict: necessary baseline, not sufficient on its own*

### 2. Extreme Value Theory (EVT) ⭐
Models the tail distribution directly rather than extrapolating from the body of the distribution. Uses Generalized Pareto Distribution (GPD) for exceedances beyond a threshold.
- ✅ Better for low-probability, high-impact events — designed specifically for tails
- ✅ Gaining ground in insurance risk management
- ❌ Requires sufficient historical data in the tail; parameter uncertainty is high
- *Verdict: strong candidate for deep tail modeling — pairs well with CTE*

### 3. Scenario-Based Stress Testing
Historical scenarios (1994 rate spike, 2008, 2022) + hypothetical (instantaneous +300bps, yield curve inversion, stagflation).
- ✅ Intuitive, explainable to board and regulators
- ✅ OSFI mandates some scenarios already — builds on existing requirement
- ❌ Limited to scenarios we can imagine — doesn't capture unknown unknowns
- *Verdict: essential complement to stochastic models*

### 4. Stochastic Interest Rate Models ⭐
Multi-factor models (Hull-White, Cox-Ingersoll-Ross, LMM) generate thousands of rate paths. Measure tail of the resulting liability/asset value distribution.
- ✅ CLIFR stochastic scenarios already use this approach
- ✅ Captures path dependency of long-duration liabilities
- ✅ Directly feeds ALM and economic capital calculations
- ❌ Model risk — results sensitive to calibration assumptions
- *Verdict: core methodology, already partially in place*

### 5. Copula Models
Model dependency structure between interest rate risk and other risks (credit spreads, equity, mortality). Tail risk is often worse when risks co-move.
- ✅ Captures non-linear dependency — correlations increase in stress
- ✅ Important for economic capital and LICAT internal model
- ❌ Copula choice is itself a model risk
- *Verdict: important for integrated risk view, medium-term priority*

### 6. Machine Learning for Tail Risk
Neural networks / gradient boosting trained to identify non-linear interactions between rate scenarios and liability cashflows. Can identify tail amplifiers that parametric models miss.
- ✅ Captures complex non-linearities
- ❌ Black box — difficult to explain to regulators
- ❌ Emerging, not yet standard in insurance
- *Verdict: longer-term / research track — explore after foundational models are solid*

---

## Recommended Framework
**CLIFR stochastic scenarios + EVT for deep tail + copula for co-movement**

1. Enhance existing CLIFR stochastic model calibration — focus on tail behaviour
2. Layer EVT on top for extreme tail quantification (CTE99+)
3. Build copula framework for interest rate + credit spread co-movement
4. Strengthen scenario library (historical + hypothetical)
5. Connect tail risk outputs to pricing governance and IFRS 17 risk margins

*Defensible to OSFI, ahead of current industry practice.*

---

## Connection to AI Transformation
- Tail risk models are candidates for AI-assisted calibration and validation
- Scenario generation could be augmented by LLMs trained on historical rate regimes
- Domain agent opportunity: interest rate risk agent that validates model assumptions against CIA standards and OSFI guidelines

---

## Next Steps
- Assess current state of interest rate risk modeling at the company
- Gap analysis vs. OSFI expectations and CIA standards
- Prioritize: enhance CTE → add EVT → build copula framework
- Identify internal talent and external partnerships (academics, consultants)
