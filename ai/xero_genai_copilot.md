# Xero GenAI Billing Copilot – End-to-End Architecture & Execution

## 1. Problem Statement

Finance and support teams were spending 15–30 minutes per ticket investigating:
* Invoice status
* Payment reconciliation
* Tax rules
* Revenue recognition compliance (ASC 606 / IFRS)
* Duplicate billing

This required querying multiple systems (ledger, invoices, payments, policies) and resulted in:
* High MTTR for billing tickets
* Inconsistent answers
* Audit risk

### Goal

Build a **finance operations copilot** that:
* Provides source-backed answers
* Automates invoice investigation
* Enforces compliance guardrails
* Works in a multi-tenant SaaS environment

---

## 2. End Users

* Billing Accountants
* Accounts Receivable (AR) Analysts
* Revenue Recognition Team
* Internal/External Auditors
* Customer Support (billing queries)

This is **not a generic chatbot** → it is a **domain copilot**.

---

## 3. High-Level Capabilities

* Conversational Q&A on invoices, payments, tax
* Automated reconciliation checks
* Duplicate charge detection
* Policy-based explanations
* Draft support responses
* Source citations for audit

---

## 4. Tech Stack

### LLM Layer

* LLaMA / Mistral (self-hosted for sensitive finance data)
* Hugging Face Inference (fallback / low-latency tasks)
* Dynamic model routing (cost vs complexity)

### Orchestration

* LangChain → RAG pipeline
* LangGraph → Agent workflows & tool calling

### Backend

* Python → AI services
* Node.js → API gateway & BFF

### Frontend

* Next.js Copilot UI (chat + citations + tool traces)

### Data & Storage

* Vector DB → document embeddings
* Blob storage → invoices, policies, tax docs
* Redis → embedding cache, session memory, rate limits
* SQL / Ledger → financial source of truth

### Deployment

* Cloud Run → autoscaling stateless microservices
* API Gateway → auth, routing, throttling
* RBAC → tenant isolation

### Observability

* Prompt/response logging
* Token usage tracking
* Retrieval quality metrics
* Latency dashboards
* Hallucination detection score

---

## 5. End-to-End Execution Flow

## Step 1 – Data Ingestion

Sources:
* Invoice PDFs
* Payment records
* Credit notes
* Tax rules
* Revenue policies

Pipeline:
1. Document upload
2. OCR (if required)
3. Chunking (500–1000 tokens)
4. Embedding generation
5. Store in vector DB with tenant_id metadata

---
## Step 2 – Query Flow

User asks:
> "Why is invoice INV-102 still unpaid?"

System flow:
1. API Gateway → Auth + tenant context
2. Query hits LangGraph agent
3. Query classifier decides:
   * Retrieval
   * Tool call
   * Both
---

## Step 3 – Retrieval (RAG)
* Semantic search in vector DB (top-K chunks)
* Filter by tenant_id
* Rerank for relevance
* Token budget enforcement

Output → grounded context

---

## Step 4 – Tool Calling (LangGraph)

Agent invokes:
* get_invoice()
* get_payments()
* get_credit_notes()
* get_tax_rule()

This ensures:
* Real-time ledger data
* No reliance on LLM memory

---

## Step 5 – Guardrails
* Read-only finance tools
* No mutation APIs exposed
* Confidence scoring
* Mandatory citations
* Policy validation layer
If confidence < threshold → fallback response

---

## Step 6 – LLM Generation

Prompt includes:
* Retrieved chunks
* Tool outputs (structured)
* System compliance instructions

LLM returns:
* Explanation
* Calculation summary
* Source citations

---

## Step 7 – Response to UI

UI shows:
* Answer
* Sources
* Tool trace
* Confidence score
---

## 6. Multi-Tenant Architecture

### What is a Tenant?
A tenant = one customer organisation with:
* Separate invoices
* Separate ledger
* Separate policies

### Isolation Mechanisms
* tenant_id in vector metadata
* tenant_id in SQL row-level security
* Redis namespacing
* JWT tenant claim

Prevents cross-tenant data leakage.
---

## 7. API Gateway Role

Used for:
* Authentication (JWT)
* Tenant resolution
* Rate limiting
* Request routing
* Audit logging

Node.js BFF sits behind gateway.
---

## 8. Why LangGraph?

LangChain alone = linear chains
LangGraph =
* Stateful workflows
* Conditional tool calls
* Retry logic
* Multi-step reasoning

Finance investigations require:
* Deterministic flows
* Tool sequencing
* Error recovery

---

## 9. Why RAG?

LLMs cannot store:
* Real invoices
* Compliance rules
* Customer-specific policies

RAG provides:
* Grounded answers
* Up-to-date knowledge
* Source citations

---

## 10. Context Window Strategy

Context is fixed by model.
We scale knowledge via:
* Chunking
* Top-K retrieval
* Token budgeting
* Map-reduce summarisation for large docs

Vector DB holds long-term memory.

---

## 11. Cost Optimisation
* Small model for simple Q&A
* Large model only for reasoning tasks
* Redis embedding cache
* Response caching for repeated queries
* Async batching for embeddings
* Token budget enforcement

Result:
* ~35–50% token cost reduction

---

## 12. Autoscaling on Cloud Run
Cloud Run provides:
* Stateless containers
* Scale to zero
* Per-request billing
* Automatic horizontal scaling

Services deployed:
* RAG service
* Agent service
* Embedding service
* API/BFF

Cold start mitigated via min instances.
---

## 13. On-Prem → Cloud Communication
Sensitive ledger data stays on-prem.
Pattern used:
* Secure REST gateway
* Read-only finance APIs
* Private networking / VPN
* No document movement to cloud

Only query results are returned.
---

## 14. Monitoring & Evaluation

### Metrics
* Latency per stage
* Retrieval hit rate
* Token usage
* Cost per query
* Hallucination rate
* Citation coverage

### Evaluation Set

Finance golden queries:
* Invoice unpaid
* Partial payment
* Duplicate billing
* Tax mismatch

We compare:

* LLM answer vs ground truth

---

## 15. Failure Handling
### Vector DB Down
Fallback → tool-only mode
### LLM Timeout
Retry → smaller model
### Low Confidence
Return: "Insufficient data" with sources
### Tool Failure
Agent retries → partial explanation
---

## 16. Security & Compliance
* RBAC by role (AR, Auditor, Support)
* PII masking in logs
* Prompt redaction
* Audit trail of all queries

---

## 17. Business Impact
* Investigation time ↓ 65%
* Escalations ↓ 40%
* Audit readiness ↑
* Consistent policy answers

---

## 18. Sample Query Flow

User:

> "Customer says invoice INV-102 was paid"

Copilot:

1. Fetch invoice
2. Fetch payments
3. Check allocation
4. Retrieve policy
5. Generate explanation with citations

---

## 19. Interview One-Liner

Built a multi-tenant finance GenAI copilot using RAG + LangGraph agents that performs ledger-backed invoice investigations, enforces audit-grade citations and guardrails, routes across self-hosted LLaMA/Mistral for cost control, and runs as autoscaling microservices on Cloud Run with full RBAC isolation and observability.

---

## 20. Top Interview Questions

### Q: Why not fine-tune instead of RAG?
A: Finance data is dynamic and tenant-specific; RAG ensures real-time grounded answers.

### Q: How do you prevent hallucinations?
A: Tool grounding, mandatory citations, confidence scoring, fallback responses.

### Q: How is tenant isolation enforced?
A: Metadata filtering, row-level security, JWT tenant claims, Redis namespacing.

### Q: Why Cloud Run?
A: Stateless AI workloads, scale-to-zero, per-request billing, fast autoscaling.

### Q: How do you control cost?
A: Model routing, token budgeting, caching, batching, smaller models for simple tasks.

### Q: What if vector DB fails?
A: Tool-only mode with ledger APIs.

---

## 21. Key Architecture Principles
* LLM is reasoning layer, not source of truth
* Tools provide financial ground truth
* Vector DB = long-term memory
* LangGraph = deterministic workflows
* Guardrails before generation

---

## 22. Future Enhancements
* Write-safe workflows with approval gates
* Automated revenue recognition checks
* Anomaly detection on billing patterns
* Fine-tuned domain model for finance language

---

## 23. Finance Domain Tooling (Ledger APIs)
These are read-only tools exposed to the agent:
* get_invoice(invoice_id)
* get_payments(invoice_id | customer_id)
* get_credit_notes(invoice_id)
* get_tax_rule(jurisdiction, product_type)

Characteristics:
* Hosted in finance domain service
* Queried via internal API gateway
* Enforced tenant_id filtering
* No write operations allowed

LLM uses these tools for monetary facts; it never generates financial values from memory.

---

## 24. Hugging Face Hosted vs Self-Hosted Models

### Hugging Face Hosted
* Used for low-risk, low-latency tasks
* No sensitive financial data sent
* Cost-efficient for simple Q&A

### Self-Hosted LLaMA / Mistral
* Used for sensitive finance workflows
* Runs inside private VPC
* Full data control and compliance

Dynamic routing selects model based on:
* Data sensitivity
* Reasoning complexity
* Token size

---

## 25. Model Strategy
Models used:
* Small model → intent classification, simple Q&A
* Medium model → standard RAG responses
* Large model → multi-step financial reasoning

Benefits:
* Cost control
* Latency optimisation
* Right model for right task

---

## 26. Support Ticket Automation Flow
1. Ticket text → Copilot
2. Intent detection (billing issue)
3. Tool calls (invoice, payments, credit notes)
4. RAG policy retrieval
5. Root cause explanation
6. Draft customer response
7. Agent review → send

Impact:
* Investigation time reduced by ~65%
* Consistent policy-aligned answers

---

## 27. Data Storage Architecture
| Data Type            | Storage             |
| -------------------- | ------------------- |
| Invoice PDFs         | Blob storage        |
| Policies / Tax docs  | Blob storage        |
| Embeddings           | Vector DB           |
| Ledger data          | SQL / On-prem DB    |
| Session memory       | Redis               |
| Prompt/response logs | Observability store |

Vector DB stores only embeddings + metadata, not financial truth.

---

## 28. On-Prem to Cloud Communication
Pattern:
* Secure REST gateway
* Read-only finance APIs
* Private networking / VPN
* No ledger replication to cloud
Only query results are returned to AI layer.

---

## 29. LLM Monitoring (LLMOps)
Metrics captured:
* Prompt tokens
* Completion tokens
* Cost per query
* Latency (retrieval, tool, generation)
* Retrieval hit rate
* Citation coverage
* Hallucination score

Golden dataset used for periodic evaluation against ground truth.

---

## 30. Guardrails Implementation
* Read-only tools
* Mandatory citations
* Confidence threshold
* PII masking in logs
* Prompt injection detection
* Policy validation layer

Low-confidence responses return safe fallback.

---

## 31. Context & Memory Strategy
Context window is fixed by model.
Scaling handled via:
* Chunking
* Top-K retrieval
* Token budgeting
* Map-reduce summarisation

Short-term memory → LLM context
Long-term memory → Vector DB

---

## 32. Token Budgeting Strategy

Token allocation:
* System prompt: fixed
* Retrieved chunks: top-K within limit
* Tool output: compressed JSON
* User query: dynamic

Prevents context overflow and reduces cost.

---

## 33. Deployment Components on Cloud Run

Services:

* API/BFF service (Node.js)
* RAG service (Python)
* Agent orchestration service
* Embedding service
* Tool proxy service

Cloud Run provides:

* Autoscaling
* Scale to zero
* Per-request billing
* Stateless containers

---

## 34. Failure Modes & Fallbacks

| Failure        | Fallback                            |
| -------------- | ----------------------------------- |
| Vector DB down | Tool-only mode                      |
| LLM timeout    | Retry with smaller model            |
| Tool failure   | Partial explanation with disclaimer |
| Low confidence | Safe response with sources          |

---

## 35. Testing Strategy
* Mocked finance APIs for non-prod
* Synthetic billing scenarios
* Golden finance queries
* Regression evaluation after prompt changes

---

## 36. Key Design Principles
* LLM is reasoning layer, not source of truth
* Financial truth comes from ledger tools
* RAG provides policy grounding
* LangGraph enforces deterministic workflows
* Guardrails before generation

---

## 37. Final Interview Summary
Built a multi-tenant finance GenAI copilot that uses RAG for policy grounding and LangGraph agents for ledger-backed tool reasoning. It integrates self-hosted LLaMA/Mistral for sensitive data, routes across models for cost efficiency, enforces audit-grade citations and guardrails, and runs as autoscaling microservices on Cloud Run with full RBAC isolation, LLM observability, and secure on-prem financial data access.

# End of Document
