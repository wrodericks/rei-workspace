# Actuarial AI Transformation — Ideas & Planning

*Started: 2026-07-15. Ongoing brainstorm for Warren's new role.*

---

## Vision
- AI-enabled actuarial processes as the core mandate
- Staff-contributed skills as the unit of capability — composable, domain-specific, shareable across the org

---

## Skill Development Model
- Open development to all staff — anyone can build a skill for their domain
- Skills as small, testable primitives (e.g. mortality lookup, rate filing, assumption sets)
- Tiered model: Experimental → Reviewed → Certified → Production

---

## Standardized Domain Agents & Skills
Centrally developed and maintained; used org-wide as reference authorities:
- **IFRS 17 agent** — first-pass review of actuarial activities for standards consistency
- **Canadian Standards of Practice agent** — compliance with CIA actuarial standards
- **Pricing governance agent** — review against company pricing policies
- **Reinsurance contract review agent** — flag issues in treaty terms and structures
- **Report generation agent** — produce standard company reports and PowerPoint templates including:
  - Actuarial assumption change reports
  - Experience study reports
  - *(other standard report types TBD)*
- *(more domain agents TBD — prioritization to be decided with Warren's boss)*

---

## Governance Layer
- Secure sandbox for skill execution
- Vetting pipeline — agents/sub-agents as first-pass only:
  - Code review agent (security, sandbox compliance)
  - Domain expert agent (actuarial correctness)
  - Test harness agent (predictable behaviour)
- Human-in-the-loop is mandatory at every stage, not optional
- Data access controls — skills scoped to what data they're permitted to see

---

## Rollout Sequence
1. Training first — build shared vocabulary (agents, skills, sub-agents)
2. Stakeholder consultation to determine hackathon theme(s)
3. Hackathon — themed based on consultation findings
4. Hackathon outputs become first test cases for the governance pipeline

---

## Strategic & Organizational
- **Peer outreach** — contact counterparts at other companies to:
  - Share ideas and build a community of practice
  - Gather competitive intelligence on how peers are approaching transformation
  - Inform management of competitor activity to create urgency (Kotter Step 1)

---

## Open Questions
- Training delivery: internal, external, or hybrid — TBD
- Domain agent prioritization: to be decided collaboratively with Warren's boss
- Security architecture: consult Alex (Deloitte) — set up these environments there
