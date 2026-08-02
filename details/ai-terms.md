# AI Terms to Learn

A running list of AI concepts Warren wants to understand better.

---

## Agentic Harness
A framework or runtime environment that orchestrates AI agents — managing how they receive tasks, call tools, invoke other agents (sub-agents), handle memory, and return results. The "harness" is the infrastructure around the agent, not the agent itself.

Examples: OpenClaw's agent runtime, LangChain, AutoGen, CrewAI.

Relevant to: Warren's transformation work — the governance and execution layer that agents run inside.

---

## Orchestration
The coordination of multiple AI agents, tools, or processes to complete a larger task. An orchestrator decides what to do next, which agent or tool to call, in what order, and how to combine the results.

Think of it like a conductor — the orchestrator doesn't do the work itself, it directs who does what and when.

Examples: A master agent that breaks a user request into sub-tasks, sends each to a specialist agent, and assembles the final output.

Relevant to: The BPMN execution platform (Camunda as orchestrator), the process optimization pipeline, and the governance layer where agents coordinate review steps.

---

## Concurrency
Running multiple tasks or agents simultaneously rather than sequentially. Instead of waiting for Agent A to finish before starting Agent B, both run at the same time and results are combined when both are done.

Important for performance — a pipeline that runs 5 validation agents concurrently takes the time of the slowest one, not the sum of all five.

Tradeoffs: concurrency adds complexity (what if one agent fails? how do you merge conflicting outputs?) and requires careful design.

Relevant to: The vetting pipeline in the governance layer — concurrent code review, domain expert, and test harness agents would be faster than running them in sequence.

---

## Graphs (in AI / agentic context)
A way of structuring agent workflows where nodes are agents or steps, and edges are the connections between them. Unlike a linear pipeline (A → B → C), a graph can have branches, loops, and conditional paths — making it much more flexible.

**LangGraph** is the most prominent example — it lets you define agentic workflows as directed graphs, with explicit control over flow, state, and when to loop back or branch.

Relevant to: The BPMN process pipeline maps naturally to a graph structure. BPMN gateways (decisions, parallel splits) *are* graph concepts. Understanding graphs helps you design more sophisticated agent workflows than simple sequential pipelines.

---

## MCP (Model Context Protocol)
An open standard (developed by Anthropic) that defines how AI models connect to external tools, data sources, and services in a consistent, interoperable way.

Think of it like USB for AI — instead of every tool needing a custom integration with every model, MCP gives you a standard plug. A tool that supports MCP works with any model that supports MCP.

**What it enables:**
- Models call tools (search, databases, APIs, file systems) through a standard interface
- Tools expose their capabilities in a structured way the model can discover and use
- Works across different AI providers — not locked to one model

**Why it matters for transformation work:**
- Domain agents (IFRS 17, CIA standards, etc.) could be built as MCP servers — reusable across any MCP-compatible model or harness
- Skills built to MCP spec are interoperable across the org's AI stack
- Becoming the de facto standard — Claude, Cursor, and many others already support it

**Warren wants to try these out** — experiment with building/connecting MCP servers personally before deploying at work.

Relevant to: Skill development model, governance layer, domain agents — MCP is likely the right interface standard for actuarial skills and agents.

---

## RAG (Retrieval-Augmented Generation)
A technique where an AI model is given relevant documents or data at query time, rather than relying solely on what it learned during training. The model *retrieves* relevant content first, then *generates* a response using both its training and the retrieved content.

**How it works:**
1. User asks a question
2. System searches a document store (vector database) for relevant chunks
3. Retrieved chunks are added to the model's context
4. Model generates a response grounded in those documents

**Why it matters:**
- Keeps responses accurate and up-to-date (training data has a cutoff)
- Grounds the model in *your* documents — proprietary data, internal policies, standards
- Reduces hallucination on domain-specific questions

**Actuarial applications:**
- IFRS 17 agent RAG'd against the full IFRS 17 standard text
- CIA standards agent RAG'd against CIA educational notes and standards of practice
- Pricing governance agent RAG'd against internal policy documents
- All of the domain agents in Warren's transformation plan are natural RAG candidates

Relevant to: Every domain agent in the actuarial AI transformation — RAG is likely the core technique powering them.

---

## Agent Loops
The cycle an agent runs through repeatedly until a task is complete: **observe → think → act → observe again**. Each iteration the agent takes in new information (tool results, sub-agent outputs, user feedback), reasons about what to do next, takes an action, and loops back.

**Why it matters:**
- Agents aren't one-shot — they iterate. A single user request might trigger dozens of loop cycles before the agent is done.
- Loops can get stuck (infinite loops, circular reasoning) — good harness design includes loop limits and exit conditions
- The quality of the loop depends heavily on how well the agent evaluates its own progress

**Example:** A process mapping agent receives a description, generates a draft BPMN, evaluates it against the spec, finds errors, fixes them, re-evaluates — looping until the diagram passes validation or a max iteration limit is hit.

Relevant to: The BPMN generation platform and process optimization pipeline — both involve agents that iterate toward a valid output rather than producing it in one shot.

---

## Embeddings
A way of converting text (or other data) into a list of numbers (a vector) that captures its meaning. Similar text produces similar vectors — meaning you can measure how "close" two pieces of text are in meaning, not just whether they share the same words.

**How it works:**
- "The policyholder died" and "the insured passed away" would have very similar vectors despite different words
- "Mortality assumption" and "interest rate risk" would have very different vectors

**Why it matters:**
- Embeddings are the engine behind RAG — when you search a document store, you're finding chunks whose embedding is closest to your query's embedding
- Also used for classification, clustering, and similarity search

**Actuarial application:** Embedding the full IFRS 17 standard means an agent can find the most relevant paragraphs for any question, even if the exact words don't match.

Relevant to: RAG-based domain agents — embeddings are what make semantic search work. Understanding them helps you design better document retrieval for the actuarial agents.

---
