# Learning Projects — Detail

## Git Discipline
- Branches, commits, pull requests — proper git workflow from scratch
- Practical context: use Warren's real repos (scripts, health tools) as the learning environment
- Also cover: GitHub authentication (Personal Access Tokens vs SSH keys, what they are and why)
- Added: 2026-05-03

## Build an LLM / Agent from Scratch
- Understand what's happening under the hood
- Starting point: Andrej Karpathy's "makemore" / "nanoGPT" (YouTube)
- Has NLP background from a few years ago, understands old paradigm, wants to bridge to transformers/LLMs
- Status: to do when bandwidth allows

## ACP + Claude Code / Codex CLI
- Agent Client Protocol — how OpenClaw delegates coding tasks to external agents
- Claude Code (Anthropic) vs Codex (OpenAI) — differences, cost models, CLI usage
- How to set up and use via OpenClaw for real development work (e.g. health app)
- Spec: agentclientprotocol.com | OpenClaw docs: /usr/lib/node_modules/openclaw/docs/tools/acp-agents.md
- Added: 2026-05-18

## New Job — Platform & Tooling Literacy (September 2026)
Goal: strategic/executive fluency, not developer depth. Know what these are, how they relate, when they're the right tool, and how to lead teams using them.

### Snowflake ⭐ Start here
- Cloud data warehouse — where large orgs store and query structured data at scale
- Almost certainly the data backbone at the new company
- Learn: architecture basics, what "cloud data warehouse" means vs. traditional, Snowflake's market position
- Resources: Snowflake's own "Getting Started" docs, their YouTube channel, a few high-level Coursera/Udemy intros

### Databricks
- Data engineering + ML platform (built on Apache Spark)
- Where data scientists build pipelines, train models, run large-scale analytics
- Often positioned as Snowflake competitor; many companies use both
- Learn: what it does, when it's chosen over Snowflake, key concepts (notebooks, clusters, Delta Lake)

### Cortex AI (Snowflake)
- Snowflake's AI layer — run LLMs, document AI, ML models *inside* Snowflake without moving data
- Relatively new but strategically important (reduces need for separate ML infra)
- Learn this *in context of Snowflake*, not as a separate product

### GitHub Copilot
- AI coding assistant integrated into VS Code (and other IDEs)
- Your team will likely use or evaluate it for accelerating development
- For your role: understand what it does, its limitations, and how to think about adoption and governance
- Learn: overview, organizational implications, responsible AI / IP considerations for enterprise use

### Priority order: Snowflake → Databricks → Cortex AI → GitHub Copilot
Added: 2026-06-20

---

## Home Network Scanning / Device Detection
- Learn how Rei found the Samsung TV on the network
- Concepts: ARP, /proc/net/arp, MAC OUI prefixes, nmap, netcat, port knocking
- Starting from scratch — Warren doesn't yet know what MAC, ARP, or ports are
- Approach: teach from first principles with hands-on examples on his own network
- Added: 2026-05-03
