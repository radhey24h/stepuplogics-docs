🧾 Enterprise AI Copilot for Xero Billing (RAG + Agents)
I designed and dilvered a multi-tenent finance based GenAi tool that enable finance team to ask natural language question on invoicing, subscription, payments and tax rules, also perform document search across billing policy and contracts.
It was mainly RAG based application so We also automated workflow for any incremental changes in vector DB's

We have also implimenetd RBAC because there are multiple roles like, Billing Accountants, Accounts Receivable (AR) Analysts, Revenue Recognition Team, Internal/External Auditors, Customer Support (billing queries)

🧾 High-Level Flow
User → Copilot UI → API Gateway → BFF (nodejs) → Orchestrator (LangGraph) → RAG Retrieval → Finance Tools → LLM → Guardrails → Response + Citations


🧱 Technical Architecture (Finance GenAI Copilot)
UI: User submits queries from the Copilot panel built with Next.js, hosted as a frontend application on Google Cloud Run.

API Gateway: Requests from the UI are routed through Google Cloud API Gateway where authentication (JWT validation, token verification, rate limiting) is enforced.

BFF (Backend for Frontend): The validated request is forwarded to a Node.js-based BFF hosted on Google Cloud Run, where authorization, tenant metadata enrichment, user context injection, and logging are performed before triggering orchestration.

Orchestration & Query Routing: A Python-based orchestration service hosted on Cloud Run uses LangChain for LLM operations and LangGraph for agent workflows; a Query Router (classifier node) inside this service determines whether the request follows a simple RAG path or a multi-step agentic flow.

Models: LLMs are accessed via hosted endpoints on Hugging Face and self-hosted LLaMA / Mistral models running in private containerized infrastructure.

Backend Services: Microservices built using python (FAST API/BFF layer), containerized and deployed on Cloud Run.

Vector Database: Semantic retrieval powered by FAISS (self-managed) or managed solutions such as Weaviate / Pinecone depending on scalability and multi-tenant requirements.

Cache: High-speed embedding cache and conversational session memory handled using Redis (via Memorystore).

Deployment: All services are containerized and deployed on Google Cloud Run with autoscaling, stateless design, and tenant isolation.


Ingestion = LangChain
Simple Retrieval = LangChain
Agentic Retrieval = LangGraph + LangChain together


LangChain is used for linear operations such as document loading, text chunking, embedding generation, vector database storage, query embedding, retrieval, prompt construction, and LLM invocation, making it ideal for straightforward ingestion and simple RAG workflows; 

In contrast, LangGraph is used to control complex runtime workflows that require multi-step reasoning, SQL tool calls to fetch financial data, comparison logic, conditional branching, retry mechanisms for inconsistent responses, and guardrail re-validation, effectively acting as the orchestration layer for agentic query processing.


🔷 How RAG Pipeline works -
RAG Pipeline works in two phases-
🟣 OFFLINE FLOW (Indexing / Knowledge Preparation)

🔹 Data Ingestion
When we ingest data first we select the data sourses in my case it was 
1) Invoice readonly API's 
2) Finance policy PDFs
3) Support knowledge base

🔹 Data Cleaning & Normalization
After selecting the data source we normalize the data during this we
1) Remove headers/footers and boilerplate text
2) Converting tables to structured text or JSON is common.
3) Standardize currency, date, and invoice formats
4) Apply tenant and region tagging

🔹 Chunking Strategy
After normalizing the data, we create chunks to optimize retrieval quality while ensuring they fit within the LLM context during response generation. During this step we perform:
1) Semantic chunking (500–800 tokens)
2) Overlap: 50–100 tokens to preserve context across chunks
3) Table-aware chunking for financial records
4) Helps ensure high retrieval precision for numeric data and policy queries.

🔹 Embedding Generation
After cunking the data we create the embedding using embedding model and we do
1) Domain-tuned finance embedding model
and also we do Separate embeddings for:
1) policies
2) transactional records
3) support KB
4) Improves semantic separation across data types.

🔹 Vector Indexing
After creating the embedding we store in Vector DB (FAISS) with metadata so Metadata fields are tenant_id, region, fiscal_period, invoice_id (if applicable), Enables filtered and time-bounded retrieval.

🔹 Index Optimization
After storing embeddings in the Vector DB, we optimize retrieval by enabling hybrid search (vector + BM25 keyword search), performing periodic re-indexing for new financial data, and deduplicating near-identical policy chunks. Since FAISS supports only vector search, BM25 is typically handled using Elasticsearch or OpenSearch alongside the vector index.

🟢 ONLINE FLOW (Query Time / Runtime RAG)
🔹 Query Processing
User query is normalized (date parsing, currency detection) and classified into categories such as policy lookup, invoice lookup, or reconciliation queries.

🔹 Redis Semantic Cache
A cache check is performed using normalized_query + tenant_id as the key to avoid repeated embedding and retrieval, reducing latency and cost while tracking cache hit rate.

🔹 Query Embedding
The normalized query is converted into a vector using the same finance embedding model used during indexing to maintain vector space consistency.

🔹 Hybrid Retrieval
Relevant chunks are retrieved using a combination of:
1) Vector similarity search (Top-K results)
2) Metadata filtering (tenant_id, region, doc_type)
3) Time-bounded filtering (fiscal period or invoice date range) to ensure financial accuracy.

🔹 Reranking Layer (Optional)
A cross-encoder reranker refines the retrieved results to improve relevance and prioritize exact invoice or numeric matches.

🔹 Context Assembly
Relevant policy chunks and transactional data are merged, deduplicated, and trimmed to fit within the LLM context window, while preserving source citations.

🔹 LLM Generation
The LLM generates a response grounded in the retrieved financial context, often enforcing a structured JSON schema for reliable outputs.

🔹 Post-Processing
Final checks include numeric validation (amounts, dates), source attribution, and confidence scoring before returning the response.


🔷 Where LangChain and LangGraph Fit in the System?
🟦 Ingestion Phase (Offline / Batch Processing)
During data ingestion, financial sources such as reports, invoices, and database exports are processed and prepared for retrieval.
LangChain is used for the ingestion pipeline to:
Load documents from APIs, PDFs, or databases
Perform text chunking
Generate embeddings
Store embeddings in the Vector Database

👉 This pipeline is linear, so LangGraph is not required.

🟦 Runtime Phase (User Query Processing)
When a user asks a question in the billing dashboard, the flow typically follows:
UI → API → BFF → Query Router
The Query Router classifies the request and decides the execution path:
Simple lookup
Analytical reasoning
Tool-based query (SQL / API)

🟢 Case 1: Simple Finance Query (RAG Flow)
Example:
"What is revenue in March?"
The router sends the request to a Simple RAG pipeline implemented using LangChain.
Flow:
Query embedding
Retrieve relevant financial documents
Prompt construction
LLM response generation

👉 This is a linear retrieval → generation workflow, so LangChain alone is sufficient.

🟣 Case 2: Analytical Finance Query (Agent Flow)
Example:
"Why did revenue drop in March?"
The router sends the request to an agent workflow orchestrated using LangGraph.
LangGraph manages:
Multi-step reasoning
SQL or API tool calls to fetch financial metrics
Comparison and analysis logic
Conditional branching
Retry logic if results appear inconsistent

Guardrail validation
👉 LangGraph acts as the workflow orchestrator for complex reasoning.
🔵 Relationship Between LangGraph and LangChain
Even within a LangGraph agent workflow, individual nodes often use LangChain for core operations such as:
Embedding generation
Document retrieval
Prompt templating
LLM invocation

In some cases, a LangGraph workflow can also be used as a node within a LangChain flow if orchestration is required for a specific step.

👉 LangGraph = Workflow controller (orchestrates multi-step reasoning and agent flows)
👉 LangChain = Execution layer (handles embeddings, retrieval, prompts, and LLM calls)

🔷 LangSmith – Where it fits
LangSmith is used for tracing, debugging, monitoring, and evaluating LangChain/LangGraph pipelines. It is used during development and can also be used in production for observability, often with sampling to control cost.

It helps to:
Trace the full LLM pipeline (query → retrieval → prompt → LLM response)
Debug errors like wrong retrieval or hallucination
Monitor metrics such as latency, token usage, and failures
Evaluate RAG quality using test datasets

🔷 Do we use LangSmith in Production?
✅ Yes, but mainly for monitoring and tracing.
In production it is used to:
Capture request traces
Monitor LLM performance
Debug failed or incorrect responses
However, many companies sample only a percentage of requests in production to reduce cost and logging overhead.

🔷 Guardrail
A guardrail is a validation and control layer placed around the LLM to ensure:
1) Responses are safe
2) Responses follow business rules
3) Sensitive data is not leaked
4) Output is grounded in retrieved data
5) Hallucinations are minimized

In simple terms:
Guardrails monitor, validate, and correct LLM outputs before sending them to the user and they sit after the LLM call and sometimes also before the LLM call.

🔷 Citation Enforcement
Force the model to:
Attach source references
Map answer sentences to retrieved chunks
If no source → reject answer.

In our Finance GenAI system, the transactional database hosted on-premises stores live billing and revenue data, while BigQuery on Google Cloud is used as a data warehouse to store GenAI query logs, LLM outputs, latency metrics, and evaluation scores for benchmarking and monitoring.


🔷 How are you managing Multi-Tenant Security
We have Implemented:
1) Tenant-scoped vector namespaces
2) Row-level security for finance data
3) RBAC (Accountant, Auditor, Admin)
4) PII masking in prompts
5) Encrypted embedding store

🔷 How you are ensuring Cost & Performance Optimizations
1) Dynamic model routing so Simple Q&A → small Mistral and Complex reasoning → larger LLaMA
2) Token budgeting
3) Async retrieval + batching
4) Streaming responses
5) Redis semantic cache for repeated queries

Result:
📉 55% LLM cost reduction
⚡ P95 latency < 2.1s

📊 Measurable Impact
⏱️ Invoice investigation time: ↓ 65%
📉 Billing support tickets: ↓ 40%
🧾 Policy lookup time: ↓ 70%
✅ Audit readiness with full traceability

💰 LLM cost optimized by 55%


🔷 What is the Complete End-to-End Request Flow (Runtime)
🟢 Step 0 – User Action (UI Layer)

User (AR Analyst) types in Next.js Copilot UI:
“Why is invoice INV-102 still unpaid?”

UI: User sends request with JWT → goes to API Gateway

🟢 Step 1 – API Gateway (First Layer)
Gateway does:
Validate JWT
Apply rate limits
Check tenant header
Add request ID for tracing

Route to Node.js BFF
No LLM ❌

🟢 Step 2 – Node.js BFF
BFF:
Extract user role (AR, Auditor)
Enforce RBAC
Shape request for AI service
Add tenant_id to payload

Call LangGraph Agent Service
Still no LLM ❌

🧠 Step 3 – LangGraph Agent (Orchestrator Starts)
3.1 Intent Classification (Small LLM)
Agent first calls a small, low-cost model for:
intent detection
entity extraction (invoice_id)
query type (investigation vs policy)

Model used:
➡️ Small Mistral / LLaMA 3 8B (quantised)
Reason: cheap + fast

Output:
intent = invoice_investigation
invoice_id = INV-102
needs_tools = true
needs_rag = true

🔧 Step 4 – Tool Planning (No LLM or same small LLM)
Agent decides tool sequence:
get_invoice(INV-102)
get_payments(INV-102)
get_credit_notes(INV-102)
This is LangGraph deterministic node, not free-form LLM.

🧾 Step 5 – Tool Calls (Ledger APIs)
LangGraph → Tool Proxy Service → Finance APIs
5.1 Call get_invoice()

Returns:
amount
status
due_date

5.2 Call get_payments()

Returns:
paid amount
allocation

5.3 Call get_credit_notes()

Returns:
credits (if any)
All tools:
tenant filtered
read-only
no LLM involved ❌

📚 Step 6 – RAG Retrieval (Vector DB)
Agent sends query:
“invoice unpaid reason partial payment allocation”
to RAG service
RAG flow:
Query embedding → Embedding model (small HF model)
Vector DB search (top-K chunks)
Tenant filter applied
Reranker selects best chunks
Returns:
policy text
reconciliation rules

No generative LLM yet ❌

🧮 Step 7 – Context Assembly (Token Budgeting)
Agent builds final prompt:
Includes:
Tool outputs (structured JSON)
Retrieved policy chunks
System guardrails
User question
Token budget enforced.

🤖 Step 8 – Final Reasoning LLM Call

Now we call larger reasoning model:
➡️ Self-hosted LLaMA / Mistral (higher quality)
Why large model here?
Because it must:
compare invoice vs payments
apply policy
explain balance
generate human-readable answer

This is the only expensive LLM call in most flows.

🛡️ Step 9 – Guardrails Layer
Post-processing:
Check citations present
Validate monetary numbers match tool output
Confidence scoring
PII masking (logs)
If confidence low → fallback response.

📤 Step 10 – Response Back to UI
LangGraph → BFF → API Gateway → Next.js UI
UI renders:

Explanation

Invoice table
Payment table
Citations
Tool trace
Confidence badge
Streaming used for better UX.


⚡ Performance Optimisations
Redis cache for embeddings
Response cache for repeated queries
Async tool calls
Top-K = 3–5 chunks
Single large LLM call per query

🔐 Data Residency
Sensitive ledger data:
Never sent to HF hosted models
Only used with self-hosted LLM inside VPC

🧾 30-Second Interview Flow
User query hits the Next.js Copilot UI → request goes to the API Gateway for authentication, rate limiting, and tenant validation → it is routed to the Node.js BFF which applies RBAC and adds tenant context → the request reaches the LangGraph agent where a small LLaMA/Mistral model performs intent classification → the agent plans and calls read-only ledger tools for invoice, payments, and credits → the RAG service retrieves policy chunks from the vector database → context is assembled with token budgeting → a larger self-hosted LLaMA/Mistral model generates a grounded answer with citations → guardrails validate confidence and enforce source checks → the response is streamed back through BFF and API Gateway to the UI with tool traces and structured invoice data.

“Which LLM Where?”
so Small model → intent classification
Embedding model → vector search
Large self-hosted model → final reasoning

------------------

🔷 RAG Has Two Phases
1️⃣ Offline (Indexing / Ingestion) → happens once
2️⃣ Online (Query time) → happens for every user question

🧱 PHASE 1 – RAG Ingestion Flow (Offline)
This prepares your knowledge base.
Step 1 - Data Ingestion (Knowledge collect karna)
Sources:
PDFs (billing docs, policies)
Database tables (invoice, customer)
APIs (Xero, ERP, CRM)
Emails
SharePoint / S3 / GCS
Web pages

Tools:
LangChain loaders
Custom Python ETL
Airflow jobs
👉 Output: Raw data system mein aa gaya.

Step 2 - Data Cleaning & Preprocessing
Raw text ko normalize karte hain:
HTML remove
extra spaces clean
encoding fix
headers/footers remove
tables → text
👉 Isko bolte hain text normalization

Step 3 - Chunking (Document ko chhote pieces mein todna)
Because LLM context limited hota hai.
Typical:
500–1000 tokens per chunk
50–100 token overlap
Types:
Recursive text splitter
Semantic chunking
👉 Output: Small meaningful chunks

Step 4 – Embedding Generation
Har chunk → vector mein convert hota hai using embedding model.
Models:
BGE
E5
sentence-transformers

Example:
"Invoice due in 7 days" → [0.21, -0.77, …]
👉 Vector = semantic meaning

Step 5 – Store in Vector DB
We store:
embedding
original text
metadata (tenant_id, doc_type, policy_id)

Vector DB:
FAISS (local)
Pinecone
Weaviate
Chroma
Elastic vector search
👉 Now vector DB is ready for semantic search.


⚡ PHASE 2 – RAG Query Flow (Online)
Now user asks a question.

Step 1 – User Query
From Next.js UI:
“Why GST applied on this invoice?”

Step 2 – Query → Embedding
Same embedding model converts query to vector.

Step 3 – Vector Search (Top-K Retrieval)
We search vector DB:
cosine similarity
filter by tenant_id
top-K chunks (usually 3–5)
Returns relevant policy text.

Step 4 – (Optional) Reranking
We may rerank results using:
cross-encoder model
keyword boost
Improves accuracy.

Step 5 – Tool Calls (Parallel Finance Data)
In our system:
LangGraph also calls:
get_invoice()
get_payments()
get_tax_rule()
So we get structured ledger data + policy text.

Step 6 – Context Assembly (Prompt Building)
We build final prompt:
Includes:
user question
retrieved chunks (RAG)
tool outputs (JSON)
system guardrails
Token budget enforced.
--Tool output + retrieved chunks + user query + system prompt
→ token size easily context window se bada ho sakta hai
Isko control karne ke liye hum token budgeting + context compression use karte hain.
---
Yes, the prompt can exceed the context window after tool calls and retrieval, so we enforce token budgeting, reranking, structured tool outputs, and dynamic context compression to ensure only the most relevant information reaches the large model.
---
Step 7 – LLM Generation
Large self-hosted LLaMA/Mistral:
reads context
reasons over data
generates grounded answer
adds citations

Step 8 – Guardrails
We check:
citations present
numbers match tool data
confidence score
Low confidence → safe fallback.

Step 9 – Response to UI
UI shows:
explanation
invoice table
policy citation
tool trace


--------------------
jab tool call ho jata hai and sementic serch se result nikal k prompt ready hota hai to token size bda nhi ho jata?

Excellent question 🔥 — yehi real production RAG problem hai.

Haan ✅
Tool output + retrieved chunks + user query + system prompt → token size easily context window se bada ho sakta hai

Isko control karne ke liye hum token budgeting + context compression use karte hain.

🔷 Prompt Size Breakdown

Final prompt mein kya kya hota hai:

1️⃣ System prompt (instructions, guardrails)
2️⃣ User query
3️⃣ Retrieved chunks (top-k)
4️⃣ Tool outputs (invoice JSON, payments, tax rules)
5️⃣ Citations formatting instructions

Agar aap:
5 chunks × 800 tokens = 4000 tokens
tool JSON = 2000 tokens
system prompt = 1000 tokens
👉 total = 7000 tokens ❗

Small model crash, large model slow & costly.
🔷 Solution: Token Budgeting (Production RAG Technique)
Har request ke liye hum token budget fix karte hain.

Example (8k context model):
Component	Token Budget
System prompt	800
User query	200
Retrieved chunks	2500
Tool output	2000
Response space	1500
Buffer	1000

👉 Isse overflow nahi hota.
🔷 Context Compression Techniques
1️⃣ Top-k control

Default:
top-3 ya top-4 chunks only
Not top-10.

2️⃣ Reranking
Cross-encoder use karke:
irrelevant chunks drop
only highest relevance pass

3️⃣ Tool Output Summarization
Tool JSON ko directly LLM ko nahi dete.
Instead:
Raw:
100 invoice rows
We convert to:
only disputed invoice
amount
due date
payment status

👉 Structured → compressed → relevant.

4️⃣ Map-Reduce for Large Docs
Agar policy doc huge hai:
Step 1: chunk summaries
Step 2: final combined summary

5️⃣ Dynamic Context Builder
LangGraph mein hum:
✔ intent detect karte hain
✔ sirf required tools call karte hain
✔ relevant fields select karte hain

Example:
User: “Why invoice 456 unpaid?”
We pass:
invoice 456 only
related payment only
Not full ledger.

🔷 Small vs Large Model Strategy
Small model (intent + planning)
no heavy context
minimal tokens
Large model (final reasoning)
curated context only
no raw data dump

🔷 Enterprise Trick: Structured Prompt Instead of Raw Text
Instead of:
“Here is the invoice table….”
We send:
Invoice:
id: 456
amount: 12,000
due_date: 10 Jan
paid: false
Policy:
payment term: 30 days

👉 Tokens reduce by 60–80%
----------------------------------

Great — ab hum hosting & deployment architecture ko simple Hinglish mein clear karte hain for interview.
Tumhara stack tha:
Next.js → BFF (Node) → API Gateway → LangGraph Agent → Tools + RAG → LLMs → Vector DB → Redis
Deployment: Cloud Run (autoscaling microservices)

🏗️ High-Level Hosting Strategy
Component	Kahan host kiya	Kyun
Next.js UI	Vercel / Cloud Run	CDN + fast UI
API Gateway	Cloud provider gateway	Auth, rate limit
Node.js BFF	Cloud Run	Stateless, autoscale
LangGraph Agent (Python)	Cloud Run	Separate scaling
RAG service	Cloud Run	CPU heavy retrieval
Vector DB	Managed (Pinecone/Weaviate)	Fast similarity
Redis	Managed Redis	Cache + session
Self-hosted LLM	GPU VM / HF endpoint	High compute
HF hosted LLM	Hugging Face Inference	On-demand
Ledger tools	Private VPC / On-prem	Secure finance data

🔷 Cloud Run kyun?

Cloud Run = serverless container platform
Features:
✔ container deploy karo
✔ auto scale (0 → N)
✔ request-based billing
✔ no server management

👉 Low traffic → cost almost zero
👉 High traffic → auto scale

Perfect for GenAI APIs.
🔷 Microservices Split (Important for Interview)

Humne sab ek service mein nahi rakha.
1️⃣ Node.js BFF (Cloud Run)

Responsibility:
RBAC
tenant context
streaming orchestration
Stateless → easily scalable

2️⃣ LangGraph Agent Service (Cloud Run – Python)
Responsibility:
intent classification
tool planning
workflow execution
CPU bound → separate scaling

3️⃣ RAG Retrieval Service (Cloud Run)
Responsibility:
embedding calls
vector search
reranking
context builder
Isko independently scale karna hota hai.

4️⃣ LLM Hosting
Small models
self-hosted CPU inference
or HF inference endpoint
Cheap.
Large models
GPU VM (A10/A100)
or Hugging Face dedicated endpoint
Expensive → used only when needed.

🔷 Vector DB Hosting
Multi-tenant RAG ke liye:
managed Pinecone / Weaviate
metadata filter: tenant_id

Benefits:
✔ no infra management
✔ high performance
✔ isolation via metadata

🔷 Redis Hosting
Managed Redis (Cloud Memorystore / Elasticache):
Use:
embedding cache
query cache
session memory
Cost reduce + latency reduce.

🔷 Secure Finance Data (On-prem → Cloud)
Xero/ledger APIs directly public nahi hote.
Architecture:
Cloud Run services → VPC connector → private network → on-prem APIs
Security:
✔ private IP
✔ service account auth
✔ read-only tools

🔷 Autoscaling Strategy
Cloud Run per service:
Service	Scaling rule
BFF	concurrency high (100)
Agent	concurrency medium
RAG	CPU-based scaling
LLM gateway	low concurrency (GPU bound)

🔷 Cost Optimisation
✔ Cloud Run scale-to-zero
✔ small model for intent
✔ large model only for reasoning
✔ Redis cache for embeddings
✔ top-k retrieval control
✔ async batching for embeddings

🔷 Request Flow with Hosting
1️⃣ UI → CDN edge
2️⃣ API Gateway → auth
3️⃣ BFF (Cloud Run)
4️⃣ Agent service (Cloud Run Python)
5️⃣ RAG service (Cloud Run) → Vector DB (managed)
6️⃣ Tool APIs → VPC → on-prem ledger
7️⃣ LLM call → GPU endpoint / HF
8️⃣ Response → stream back

🧠 Interview One-Liner
We deployed each responsibility as an independent autoscaling Cloud Run microservice, used managed vector and Redis stores, hosted large models on GPU endpoints, and connected securely to on-prem financial systems via private VPC to achieve isolation, scalability, and cost efficiency.

---------------
📐 GCP Architecture Diagram (Text Whiteboard)

                ┌──────────────────────────┐
                │        Next.js UI        │
                │   (Vercel / Cloud CDN)   │
                └────────────┬─────────────┘
                             │ HTTPS
                             ▼
                ┌──────────────────────────┐
                │       API Gateway        │
                │ Auth • Rate limit • WAF  │
                └────────────┬─────────────┘
                             │
                             ▼
                ┌──────────────────────────┐
                │     Node.js BFF (CR)     │
                │ RBAC • Tenant Context    │
                │ Streaming Orchestrator   │
                └────────────┬─────────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
          ▼                  ▼                  ▼
┌────────────────┐  ┌────────────────┐  ┌────────────────┐
│ LangGraph Agent│  │  RAG Service   │  │ LLM Gateway     │
│ Python (CR)    │  │ Retrieval (CR) │  │ Model Router    │
└──────┬─────────┘  └──────┬─────────┘  └──────┬─────────┘
       │                   │                    │
       │                   ▼                    ▼
       │          ┌────────────────┐   ┌────────────────────┐
       │          │ Vector DB       │   │ Self-hosted LLM     │
       │          │ (Pinecone/Weav) │   │ GPU VM / HF Endpt   │
       │          └────────────────┘   └────────────────────┘
       │
       ▼
┌──────────────────────────────┐
│ Tool Connectors (CR)         │
│ Invoice • Payments • Tax     │
└────────────┬─────────────────┘
             │ VPC Connector
             ▼
┌──────────────────────────────┐
│ On-Prem / Private Ledger DB  │
│ Read-only Financial Data     │
└──────────────────────────────┘

Side Services:
- Redis (Memorystore) → cache
- GCS → document storage
- Cloud Logging + Monitoring → observability

CR = Cloud Run

User query Next.js Copilot UI se aati hai jo CDN pe host hai.
Request API Gateway se pass hoti hai jahan authentication, rate limiting, aur tenant validation hota hai.
Uske baad request Node.js BFF (Cloud Run) me jati hai jo RBAC apply karta hai, tenant context add karta hai, aur streaming orchestrate karta hai.
Phir LangGraph Agent service (Python Cloud Run) intent detect karta hai aur decide karta hai ki RAG retrieval karna hai ya ledger tools call karne hain.
RAG service vector database se relevant policy/document chunks retrieve karti hai, jabki tool connectors VPC ke through secure on-prem finance ledger (invoice, payments, tax) se read-only data laate hain.
Final curated context LLM Gateway ko diya jata hai jo small model se planning aur large self-hosted GPU model se grounded response generate karta hai.
Response guardrails se validate hota hai aur streaming ke through BFF → API Gateway → UI tak wapas jata hai.
Side me Redis caching ke liye, GCS document storage ke liye, aur Cloud Logging/Monitoring observability ke liye use hota hai.

💰 Per-Request Cost Breakdown (Realistic)
🎯 Optimised Flow (multi-model routing)
Component	Cost per request (approx)
API Gateway	negligible
Cloud Run BFF	$0.0002
Agent (small model)	$0.0005
RAG retrieval + vector search	$0.001
Redis cache hit (if yes)	~$0
Large LLM (only when needed)	$0.01 – $0.03
Total (avg)	$0.012 – $0.02
❌ Without optimisation (single large model always)
Component	Cost
Large LLM for everything	$0.04 – $0.08 per request

👉 60–75% cost reduction with routing + RAG.

⚙️ Where Cost Saved

✔ small model for intent
✔ Redis embedding cache
✔ top-k = 3 not 10
✔ structured tool output (token reduction)
✔ Cloud Run scale-to-zero
✔ GPU only for final reasoning

⚠️ Cold Start Mitigation (Very Important)

Cloud Run cold start = 1–5 seconds (Python worse).

Techniques we used:
1️⃣ Min Instances
Set:
BFF → min instances = 1
Agent → min instances = 1
→ critical path always warm.

2️⃣ Split Services
Heavy Python (LangGraph) separate from Node BFF
→ UI latency reduce.

3️⃣ Lazy Model Loading
LLM client initialise on first request
not at container startup.

4️⃣ Connection Pool Reuse
Vector DB + Redis connections cached globally.

5️⃣ Async Streaming
User ko first token fast milta hai
even if backend still processing.

6️⃣ Health-Ping Scheduler
Cloud Scheduler → ping service every 5 minutes
to keep warm (cheap).

📊 Latency Budget (Interview Gold)
Stage	Latency
API Gateway	20–40 ms
BFF	30 ms
Intent model	80 ms
RAG retrieval	120 ms
Tool API (ledger)	150–300 ms
Large LLM first token	400–800 ms
Streaming response	continuous

👉 Perceived latency: < 1 second first token

🧠 Observability Stack

✔ Cloud Logging → request traces
✔ Cloud Monitoring → latency, error rate
✔ Token usage metrics → cost dashboard
✔ LLM eval logs → hallucination rate

🎯 Interview One-Liner
We deployed the copilot as autoscaling Cloud Run microservices behind an API Gateway, used managed vector and Redis stores, routed heavy reasoning to GPU-backed LLM endpoints, connected securely to on-prem finance systems via VPC, and reduced cost by 70% using multi-model routing, caching, and token budgeting while mitigating cold starts with min instances and service warming.

Great question — GenAI monitoring = normal microservice monitoring + LLM-specific telemetry.
Interviewers love this answer.

🔷 1️⃣ Traditional System Monitoring (Infra + Services)
We used GCP Observability stack:

✅ Cloud Monitoring (Metrics)
Track per service (Cloud Run):
request count
latency (p50 / p95 / p99)
error rate (5xx)
CPU / memory
cold starts
SLO example:
Availability → 99.9%
First token latency → < 1 sec

✅ Cloud Logging (Structured Logs)
Each request log contains:
tenant_id
user_role
tool_called
model_used
token_input / token_output
cost_estimate
confidence_score

👉 Useful for audit + debugging.

✅ Cloud Trace
End-to-end tracing:
UI → Gateway → BFF → Agent → RAG → LLM → Tools
We identify:
slow ledger API
vector DB latency
LLM bottleneck

🔷 2️⃣ LLM-Specific Monitoring (Very Important)
Normal APM se kaam nahi chalta.
We track:
🧠 Token Metrics
Per request:
prompt tokens
completion tokens
total tokens
cost per tenant

Used for:
✔ cost dashboard
✔ budget alerts

🧠 Model Routing Metrics
% requests small model vs large model
fallback rate
timeout rate
If large model usage spike → cost alert.

🧠 RAG Quality Metrics
We log:
retrieved_chunks_count
similarity_score_avg
citation_present (true/false)

Detect:
❗ low similarity → bad retrieval
❗ no citation → hallucination risk

🧠 Hallucination / Guardrail Metrics
We track:
guardrail_fail_rate
low_confidence_responses
unsupported_answer_count
Auto fallback:
→ show “insufficient data” instead of wrong answer.

🔷 3️⃣ Tool Monitoring (Finance Critical)
Ledger tool logs:
tool_name
query_time
record_count
empty_result_flag
Detect:

slow DB
missing invoice
partial data

🔷 4️⃣ Business Metrics (What Product Cares About)
We track:
queries per tenant
invoices validated via copilot
support tickets reduced
manual review avoided
👉 Shows ROI.

🔷 5️⃣ Alerts (Production Setup)

Alert rules:
🚨 p95 latency > threshold
🚨 error rate > 2%
🚨 LLM timeout spike
🚨 cost per hour > budget
🚨 vector DB unavailable

🔷 6️⃣ Eval Pipeline (Offline Monitoring)
We maintain:
golden question set
expected answers with citations
Nightly eval job:
run queries
score accuracy
detect regression after model change

🔷 7️⃣ Dashboard View (What We Show to Stakeholders)
Single dashboard:
Infra:
latency, errors
LLM:
token usage
cost per tenant
model mix
RAG:
retrieval success rate
citation coverage
Business:
automation rate

🧠 Interview One-Liner
We implemented full-stack observability using Cloud Monitoring, Logging, and Trace for infrastructure, and added LLM-specific telemetry such as token usage, model routing, retrieval quality, citation coverage, guardrail failures, and per-tenant cost tracking, along with offline evaluation pipelines and SLO-based alerts.

Perfect — ye Staff/Principal interview level content hai.
Memorise these as bullet blocks for whiteboard.

📊 Exact Metrics List (Whiteboard Ready)
🏗️ Infra Metrics
Per Cloud Run service:
request_count
latency_p50 / p95 / p99
error_rate (4xx / 5xx)
CPU_utilisation
memory_utilisation
cold_start_count
concurrency

🧠 LLM Metrics
Per request:
model_name
prompt_tokens
completion_tokens
total_tokens
cost_per_request
first_token_latency
total_generation_time
timeout_rate

🔎 RAG Metrics
retrieval_latency
vector_db_latency
top_k_chunks
avg_similarity_score
rerank_applied (Y/N)
citation_present (%)
context_token_size

🛠️ Tool Metrics (Finance Critical)
Per tool:
tool_name
tool_latency
records_returned
empty_result_rate
tool_error_rate

🛡️ Guardrail Metrics
low_confidence_rate
hallucination_flag_rate
unsupported_answer_rate
policy_violation_count

💰 Cost Metrics
Per tenant:
tokens_per_day
cost_per_day
large_model_usage_%
cache_hit_rate (Redis)

📈 Business Metrics
invoices_validated_by_copilot
manual_reviews_saved
support_ticket_deflection
avg_time_to_resolution

📉 Hallucination Detection Strategy
We don’t “guess” hallucination — we measure signals.

1️⃣ Citation Enforcement
Rule:
If answer has no source chunk or tool data
→ mark as unsupported
→ show fallback message.

Metric: citation_present = false
2️⃣ Similarity Threshold
If:
avg_similarity_score < threshold
→ retrieval weak
→ answer blocked.

3️⃣ Tool Consistency Check
Example:
LLM says invoice amount = 12,000
Tool JSON = 10,000
Mismatch → hallucination flag.

4️⃣ Confidence Scoring
We compute:
confidence = f(similarity_score, tool_presence, chunk_overlap)
Low confidence → warning banner.

5️⃣ Structured Output Validation
LLM output schema validate:
invoice_id exists?
amount numeric?
date valid?
If fail → regenerate or fallback.

6️⃣ “I don’t know” Policy
If no data found:
System prompt forces:
“Insufficient data to answer”
instead of guessing.

🔍 Debugging a Wrong Financial Answer (Step-by-Step)
Interviewers LOVE this flow.
Step 1️⃣ Check Logs
From structured log:
tenant_id
model_used
tool_called
token_size
similarity_score

Step 2️⃣ Verify Retrieval
Questions:
Kya correct chunks retrieve hue?
similarity score low tha?
wrong tenant data aaya?
If wrong → vector filter issue.

Step 3️⃣ Check Tool Output
tool latency
records_returned = 0?
partial data?
Finance errors often tool side.

Step 4️⃣ Inspect Prompt Context
Look at:
context_token_size
chunk content
tool JSON summarisation
May be truncated.
Step 5️⃣ Model Routing
Check:
small model accidentally used for final reasoning?
large model timeout → fallback?

Step 6️⃣ Guardrail Logs
confidence low?
citation missing?
validation skipped?

Step 7️⃣ Reproduce with Same Trace
Replay:
same query + same tenant + same tools
→ deterministic debugging.

🧠 Root Cause Categories (You say this in interview)

Most GenAI errors come from:
1️⃣ retrieval failure
2️⃣ tool data missing
3️⃣ context truncation
4️⃣ wrong model routing
5️⃣ guardrail bypass

Not the LLM itself.

🎯 Interview One-Liner

We debug incorrect financial answers by tracing the full request, validating retrieval similarity and tenant filters, verifying tool outputs, inspecting prompt context size, checking model routing, and reviewing guardrail and citation logs to identify whether the issue is retrieval, data, context truncation, or model selection.


🔷 RAG Evaluation Matrix – Overview

RAG ko evaluate karne ke 4 layers hote hain:

1️⃣ Retrieval Quality
2️⃣ Context Quality
3️⃣ Generation Quality
4️⃣ System Performance

Har layer ke alag metrics hote hain.

🔶 1. Retrieval Evaluation Metrics (Vector Search Quality)

Yeh check karta hai ki sahi documents retrieve hue ya nahi.

📊 Metrics
✅ Hit Rate @K

Kya relevant document top-k results mein aaya?

Example:
Relevant doc top-5 mein hai → hit = 1

✅ MRR (Mean Reciprocal Rank)

Relevant document ka rank kitna upar tha.

Formula:
MRR = average(1 / rank)

Higher = better.

✅ Recall @K

Total relevant docs mein se kitne retrieve hue.

Agar 3 relevant the aur 2 mile → Recall = 0.66

✅ Precision @K

Top-k results mein se kitne relevant the.

✅ Similarity Score Distribution

Low similarity → weak retrieval.

Track:

avg similarity

min similarity

🔶 2. Context Evaluation Metrics

Retrieved chunks useful the ya nahi?

📊 Metrics
✅ Context Precision

Context mein irrelevant text kitna kam hai.

✅ Context Recall

Answer ke liye required info context mein tha ya nahi.

✅ Context Relevance Score

LLM judge karta hai:
“Is this context relevant to the query?”

🔶 3. Generation Evaluation Metrics (LLM Output Quality)
🧠 Most Important for Interviews
✅ Faithfulness (Groundedness)

Answer context se match karta hai ya hallucinated hai?

Scale:
0 → hallucinated
1 → fully grounded

✅ Answer Relevance

Answer user question ko directly address karta hai ya nahi.

✅ Answer Completeness

Required points cover hue ya nahi.

✅ Semantic Similarity

Generated answer vs reference answer similarity.

Use:

cosine similarity (embedding based)

✅ Exact Match (for structured QA)

Invoice number, date, amount → exact match hona chahiye.

🔶 4. End-to-End RAG Metrics
⏱️ Latency

Total response time:

retrieval latency

generation latency

💰 Cost per Query

Tokens in + tokens out cost.

📉 Failure Rate

empty retrieval %

LLM errors

timeout

🔁 Cache Hit Rate

Repeated queries → cache se serve hue ya nahi.

🔶 5. Safety Evaluation Metrics

Enterprise RAG ke liye mandatory.

🔒 Metrics

PII leakage rate

policy violation rate

prompt injection success rate

toxic output rate

🔷 📊 Full RAG Evaluation Matrix (Interview Ready Table)
Layer	Metric	Purpose
Retrieval	Hit Rate@K	Relevant doc mila ya nahi
Retrieval	Recall@K	Kitne relevant docs retrieve hue
Retrieval	Precision@K	Top-k quality
Retrieval	MRR	Rank quality
Context	Context Precision	Irrelevant text kam
Context	Context Recall	Required info present
Generation	Faithfulness	Hallucination detect
Generation	Answer Relevance	Question ka direct answer
Generation	Completeness	Full answer
Generation	Semantic Similarity	Reference match
System	Latency	Performance
System	Cost/query	FinOps
System	Failure rate	Reliability
Safety	PII leakage	Data protection
Safety	Prompt injection success	Security
🔷 6. Evaluation Methods

Metrics calculate kaise karte hain?

🧪 Offline Evaluation

Golden dataset banao:

question

expected answer

relevant docs

Phir automated eval run karo.

🤖 LLM-as-Judge

Ek LLM use karo to score:

relevance

faithfulness

completeness

Prompt example:
“Score answer from 1-5 based on faithfulness to context.”

👨‍💻 Human Evaluation

SME (Subject Matter Expert) manual review karta hai.

Best for:

legal

finance

healthcare

🔷 7. Real Billing Copilot Example

Query:
“Why was invoice rejected?”

Evaluate:

Retrieval:

policy doc mila? ✅

similarity > 0.8? ✅

Context:

rejection rule present? ✅

Generation:

correct reason? ✅

hallucination? ❌

completeness? ✅

System:

latency = 1.9s

cost = ₹0.10

🔷 8. Scoring Formula (Enterprise)

Composite RAG Score bana sakte ho:

RAG Score =
0.3 × Retrieval

0.4 × Faithfulness

0.2 × Relevance

0.1 × Latency SLA

🔷 🔥 Interview One-Liner

“We evaluate RAG using retrieval metrics like Hit@K and MRR, context quality metrics, generation metrics such as faithfulness and relevance, and system metrics like latency and cost, along with safety checks for PII and prompt injection.”

🔷 Fine-Tuning Kya Hota Hai?

Fine-tuning ka matlab hai:

👉 Base LLM ko apne domain data par train karna
taaki model ka behaviour change ho jaye.

Example:

Accounting tone

Company policies

Specific output format

Classification rules

Yeh RAG se different hai.

🔶 RAG vs Fine-Tuning (Quick Difference)
Feature	RAG	Fine-Tuning
Knowledge update	Dynamic	Static (retrain needed)
Hallucination control	High	Medium
Cost	Low	High training cost
Latency	Slightly high	Fast
Use case	Q&A on documents	Style, format, classification

👉 Enterprise mein dono ka combo use hota hai.

🔷 Fine-Tuning Types
1️⃣ Full Fine-Tuning

Poora model retrain hota hai
❌ expensive
❌ GPU heavy
Mostly large labs karte hain.

2️⃣ Parameter-Efficient Fine-Tuning (PEFT) ✅

Industry standard.

Types:

🔹 LoRA (Low-Rank Adaptation)

Most popular.
Sirf small adapter layers train hote hain.

Benefits:

low cost

fast training

small model size

🔹 QLoRA

LoRA + quantization
→ consumer GPU par bhi train ho sakta hai.

🔹 Adapters / Prefix Tuning

Lightweight training methods.

🔷 Fine-Tuning Kab Use Kare?

Use when:

✅ fixed output format chahiye
✅ classification / tagging
✅ domain tone (legal, medical, finance)
✅ tool calling behaviour
✅ structured JSON output

❌ constantly changing knowledge → RAG better

🔷 Fine-Tuning Dataset Format

Typical JSONL format:

{"instruction": "Classify invoice status", "input": "Invoice unpaid for 45 days", "output": "Overdue"}
{"instruction": "Extract invoice fields", "input": "Invoice #123 due on 5 Jan", "output": {"invoice_number":"123","due_date":"2025-01-05"}}

Dataset size:

500–2k examples → good results (LoRA)

High quality > large quantity

🔷 Fine-Tuning Pipeline (Step by Step)
1️⃣ Use Case Define karo

Example:

JSON extraction

billing classification

policy tagging

2️⃣ Dataset Prepare karo

clean

balanced

no duplicates

correct labels

3️⃣ Base Model Choose karo

Example:

LLaMA

Mistral

Phi

GPT (if API fine-tuning)

4️⃣ Tokenization

Text → tokens using model tokenizer

5️⃣ Training Setup

Parameters:

learning rate

batch size

epochs

LoRA rank

6️⃣ Training Run

Framework:

HuggingFace Transformers

PEFT

TRL

Hardware:

GPU (T4/A100) or QLoRA on small GPU

7️⃣ Evaluation

Metrics:

accuracy

F1 score

exact match

BLEU / ROUGE (text tasks)

8️⃣ Model Versioning

Store:

model v1

dataset version

training config

9️⃣ Deployment

Serve via:

vLLM

TGI

FastAPI

Triton

🔷 Fine-Tuning vs Prompt Engineering

Prompt engineering:

fast

no training

limited control

Fine-tuning:

consistent behaviour

lower tokens (short prompts)

better structured output

🔷 Cost Impact

Fine-tuned model:

shorter prompts → lower token cost

faster inference

no large context required

🔷 Real Billing Copilot Example

Without fine-tuning:
Output inconsistent JSON ❌

After fine-tuning:
Always:

{
  "invoice_number": "...",
  "status": "...",
  "due_date": "...",
  "amount": "..."
}
🔷 Best Practice (Enterprise)

Use:

👉 RAG → knowledge retrieval
👉 Fine-tuning → output format + behaviour

Combo = 🔥 production system

🔷 Monitoring Fine-Tuned Model

Track:

accuracy drift

output format errors

latency

token reduction %

cost saving

🔷 Risks

⚠ overfitting
⚠ catastrophic forgetting
⚠ biased dataset
⚠ retraining needed for new knowledge

🔷 🔥 Interview One-Liner

“Fine-tuning adapts a base LLM to a specific domain or task by training on labeled examples, typically using parameter-efficient methods like LoRA, to achieve consistent structured outputs and domain-specific behaviour, while RAG handles dynamic knowledge retrieval.”







We used a multi-model architecture. A smaller model like LLaMA 3 8B handled query understanding tasks such as intent classification and entity extraction. For semantic search we used BGE/E5 embedding models to generate vector embeddings stored in a vector database like Pinecone. Retrieved documents were reranked using BGE reranker, and the final response generation was performed by a large reasoning model like LLaMA 3 70B. ✅ Important correction So technically we are using: 1 small LLM 1 embedding model 1 reranker model 1 large LLM - What You Should Say for Your Project In our GenAI financial assistant system, we used: Component Technology Vector Database Pinecone Embedding Model BGE / E5 Cache Redis Orchestration LangChain Workflow LangGraph Observability LangSmith Small LLM LLaMA 3 8B Large LLM LLaMA 3 70B I need complete deployment set with azure and google cloud


