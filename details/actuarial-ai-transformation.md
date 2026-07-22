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

## AI-Driven Process Optimization Pipeline

An agent pipeline to automate process mapping, analysis, and reengineering — replacing or augmenting what would otherwise be manual BPM consulting work.

### Pipeline Design
1. **Process Mapper Agent** — takes unstructured input (text descriptions, interview notes, existing docs) and converts to structured BPMN-compatible format (tasks, decisions, swimlanes, flows)
2. **Analyst Agent** — identifies bottlenecks, gaps, redundancies, manual steps that could be automated
3. **Domain Expert Agent(s)** — flags compliance issues (IFRS 17, CIA standards, pricing governance, etc.) — reuses the standardized domain agents already planned
4. **Reengineering Agent** — proposes optimized process with rationale
5. **Human Review** — validates, adjusts, approves (mandatory human-in-the-loop)

### Output
- Structured optimization report
- BPMN XML file — importable directly into Lucidchart, Bizagi, or Visio for visualization

### Notes
- Domain expert agents from the standardized agents section slot directly into step 3
- Natural candidate for a hackathon theme — end-to-end demo is achievable in a day
- Connects BPM/Lean Six Sigma skill-building with AI implementation strategy

---

## BPMN Generation & Execution Platform

A full-stack platform for AI-generated process automation. Buildable today with current tools.

### Architecture
```
Natural language process description
→ LLM generates BPMN 2.0 XML (validated against BPMN 2.0 spec)
→ Visualization via bpmn.js (open source, web-based)
→ Human review and edit
→ Camunda (or Flowable) executes the process
→ Agents handle individual task nodes
```

### Layer 1 — Text → BPMN 2.0 XML
- LLM prompted with process description + BPMN schema constraints
- Outputs valid BPMN 2.0 XML
- Automated validation step before saving
- Current LLMs are capable of this today

### Layer 2 — Visualization
- **bpmn.js** — open source JavaScript library (used by Camunda), renders BPMN in browser
- Web interface: description in → diagram renders automatically → user can review, edit, export

### Layer 3 — Execution
- BPMN 2.0 is an executable standard
- **Camunda** or **Flowable** workflow engines take the XML and run the process
- Each task node can trigger: API call, script, human task (assign + wait), sub-process, or agent

### Layer 4 — Agent Integration
- Each task node invokes an agent
- The BPMN diagram becomes the orchestration layer
- Agents are the executors
- Maps directly to the AI process optimization pipeline already designed

### Notes
- This is a legitimate production architecture, not just a prototype
- Strong candidate for an internal platform at the new company
- Personal prototype possible before Sep 9 — good way to learn the stack hands-on
- Connects BPM learning, AI agents, and transformation strategy into one demonstrable system

---

## Sub-Agent Architecture (Personal / OpenClaw Projects)
- Explore using Rei + sub-agents across Warren's current and future projects (FX trading, health tracking, etc.)
- Think through which tasks benefit from delegation to sub-agents vs. staying in main session
- Likely overlap with governance model being designed for the new job — personal projects as a testbed
- *(To be developed into a fuller design)*

---

## Open Questions
- Training delivery: internal, external, or hybrid — TBD
- Domain agent prioritization: to be decided collaboratively with Warren's boss
- Security architecture: consult Alex (Deloitte) — set up these environments there
