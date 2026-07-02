# Enterprise AI Landscape — 2025
*For Warren's reference as he steps into the new role*

## How to Read This
Rows = capability categories. Columns = vendors. Where they compete head-to-head, the products are comparable.

---

## Comparable Product Matrix

| Capability | OpenAI | Anthropic | Google | Microsoft | AWS | Cohere |
|---|---|---|---|---|---|---|
| **Flagship LLM (API)** | GPT-4o / o1 | Claude Sonnet / Opus | Gemini 1.5 Pro / Ultra | Azure OpenAI (GPT-4o) | Bedrock (multi-model) | Command R+ |
| **Enterprise Chat / Copilot** | ChatGPT Enterprise | Claude for Enterprise | Gemini for Workspace | Microsoft 365 Copilot | — | North |
| **AI Platform / Studio** | OpenAI API platform | Claude API | Vertex AI | Azure AI Foundry | Amazon SageMaker | Cohere Platform |
| **Model Marketplace** | — | — | Vertex AI Model Garden | Azure AI Foundry (1,900+ models) | Amazon Bedrock | — |
| **AI Agents** | ChatGPT Agents (deep research, coding, sales) | Claude Agent SDK | Google Agentspace | Azure AI Foundry Agent Services | AWS Frontier Agents (Kiro, DevOps, Security) | North Agents |
| **Search / RAG** | — | — | Vertex AI Search | Azure AI Search | Amazon Kendra / Bedrock RAG | Embed + Rerank + Compass |
| **Coding Assistant** | Codex / ChatGPT (coding) | Claude (coding) | Gemini Code Assist | GitHub Copilot (powered by OpenAI) | Amazon Q Developer | — |
| **Image Generation** | DALL-E 3 | — | Imagen (Vertex AI) | Azure DALL-E | Amazon Titan Image | — |
| **Speech-to-Text** | Whisper API | — | Google Speech-to-Text | Azure Speech | Amazon Transcribe | — |
| **Text-to-Speech** | — | — | Google Text-to-Speech | Azure Neural TTS | Amazon Polly | — |
| **Embeddings** | text-embedding-3 | — | Vertex AI Embeddings | Azure Embeddings | Amazon Titan Embeddings | Cohere Embed |
| **Fine-tuning / Custom Models** | OpenAI Fine-tuning API | — | Vertex AI (fine-tune Gemini) | Azure OpenAI fine-tuning | SageMaker (any model) | Command fine-tuning |
| **On-prem / Private Deployment** | — (cloud only) | — (cloud only) | Vertex AI (GCP) | Azure (incl. sovereign) | AWS AI Factories (on-prem) | ✅ Strong — cloud or on-prem |
| **Governance / Safety Controls** | Enterprise admin console | Constitutional AI approach, strong safety | VPC controls, data residency | Purview, Entra Agent ID | AWS IAM, compliance certs | Enterprise-grade, data privacy focus |

---

## Who Is Really Who

| Player | What They Actually Are |
|---|---|
| **OpenAI** | Frontier model lab. Consumer brand (ChatGPT) + enterprise API. Most capable general models. Increasingly agent-focused. |
| **Anthropic** | Safety-first model lab. Claude is the enterprise alternative to GPT — preferred in regulated industries (legal, finance, insurance). Strong reasoning, long context. |
| **Google** | Platform play. Gemini is the model, but Vertex AI and Workspace integration are the real enterprise story. Best multimodal, best context window. |
| **Microsoft** | Distribution play. Doesn't make frontier models — resells OpenAI's models via Azure. The winner if your enterprise is already Microsoft-centric (Teams, M365, Azure). |
| **AWS** | Infrastructure + model marketplace. Bedrock lets you pick from every major model. Wins on compliance, cost control, and "we're not going to compete with your app." |
| **Cohere** | Pure enterprise, no consumer distraction. Only vendor with strong on-prem story. Canadian company (Toronto). Preferred by security-sensitive clients. |

---

## Actuarial / Insurance Relevance

| Use Case | Best Fit |
|---|---|
| Long-form policy/contract analysis | Anthropic Claude (long context, reasoning) |
| Internal workflow automation | Microsoft Copilot (if M365 shop) or Anthropic |
| Data privacy / on-prem requirement | Cohere or AWS |
| Building custom ML models | AWS SageMaker or Google Vertex AI |
| Multi-model experimentation | AWS Bedrock or Azure AI Foundry |
| Coding / actuarial tooling automation | GitHub Copilot, Amazon Q, or Claude |

---

## What's Missing From the Hype

- **None of these vendors are profitable at scale** — valuations are speculative
- **Most "enterprise AI" is still RAG + a wrapper** — not magic, just search + generation
- **Model quality gap is narrowing** — differentiation is shifting to platform, compliance, and integration
- **Agents are early** — lots of demos, limited production deployments

---
*Last updated: 2026-05-12*
