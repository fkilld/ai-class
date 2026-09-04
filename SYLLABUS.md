# Syllabus — GenAI to MLOps

---

## Module Map

| #   | Module                         |   |
| --- | ------------------------------ | --------- |
| 0   | Foundations                    |           |
| 1   | Classical ML                   |           |
| 2   | NLP and Retrieval Fundamentals |           |
| 3   | Deep Learning and Transformers |           |
| 4   | LLM Mechanics                  |           |
| 5   | Embeddings and Vector Stores ★ |           |
| 6   | Naive RAG                      |           |
| 7   | Advanced RAG ★                 |           |
| 8   | Multi RAG ★                    |  |
| 9   | Agentic RAG                    |           |
| 10  | Evaluation ★                   |  |
| 11  | Fine-tuning and Optimization   |           |
| 12  | MLOps / LLMOps ★               |           |
| —   | Capstone                       |           |

★ = high-differentiation module

---

## Module 0 — Foundations

**:**

### Python

- async/await
- typing
- generators
- decorators
- context managers
- uv
- pytest
- logging

### Math

- vectors
- dot product
- cosine similarity
- matrix multiplication
- norms
- probability
- Bayes
- log-likelihood
- softmax
- entropy
- KL divergence

### Libraries

- numpy basics
- pandas basics
- matplotlib basics


---

## Module 1 — Classical ML

**:**

### Core Concepts

- train / val / test
- cross-validation
- overfitting
- bias-variance

### Algorithms

- regression
- classification
- clustering (k-means)
- dimensionality reduction (PCA, t-SNE, UMAP)

### Classification Metrics

- accuracy
- precision
- recall
- F1
- ROC-AUC
- confusion matrix

### Ranking Metrics

- MRR
- MAP
- NDCG@k
- Recall@k
- Hit Rate


---

## Module 2 — NLP and Retrieval Fundamentals

**:**

### Tokenization

- word
- subword
- BPE
- WordPiece
- SentencePiece

### Lexical Retrieval

- TF-IDF
- BM25 (scoring formula, k1 / b parameters)
- inverted index

### Search Concepts

- lexical vs semantic search
- vocabulary mismatch problem


---

## Module 3 — Deep Learning and Transformers

**:**

### Neural Network Basics

- perceptron
- backprop
- gradient descent
- optimizers
- loss functions
- regularization

### Embeddings

- Word2Vec
- GloVe
- contextual embeddings

### Attention

- scaled dot-product
- multi-head
- self vs cross attention

### Transformer Architecture

- encoder
- decoder
- encoder-decoder
- positional encodings (sinusoidal, RoPE, ALiBi)

### Modern Variants

- GQA / MQA
- RMSNorm
- SwiGLU
- KV cache
- flash attention

### Model Families

- BERT vs GPT vs T5 — which for what


---

## Module 4 — LLM Mechanics

**:**

### Training Stages

- pretraining
- SFT
- RLHF / DPO (conceptually)

### Decoding

- greedy
- beam
- temperature
- top-k
- top-p
- repetition penalty

### Context Behaviour

- context window
- attention sink
- lost-in-the-middle
- prompt caching

### Structured Output

- JSON mode
- function calling schemas
- constrained decoding

### Prompting

- zero-shot / few-shot
- CoT
- ReAct
- self-consistency
- prompt injection

### Cost and Latency

- TTFT
- tokens/sec
- batching


---

## Module 5 — Embeddings and Vector Stores ★

**:**

### Embedding Models

- embedding model selection
- MTEB
- dimensions
- normalization
- matryoshka

### Similarity Metrics

- cosine
- dot
- L2

### ANN Indexes

- flat
- IVF
- HNSW (M, efConstruction, efSearch)
- PQ / SQ quantization

### Tradeoffs and Design

- recall vs latency vs memory tradeoff
- metadata filtering
- pre- vs post-filtering
- multi-tenancy

### Stores

- pgvector
- Qdrant
- Weaviate
- FAISS
- Milvus


---

## Module 6 — Naive RAG

**:**

### Ingestion

- PDF
- HTML
- DOCX
- tables
- OCR fallback

### Chunking

- fixed
- recursive
- sentence
- semantic
- parent-document
- contextual retrieval

### Data Hygiene

- metadata design
- dedup
- normalization

### Pipeline

- retrieve → augment → generate
- prompt templates
- citation grounding

### Failure Modes

- bad chunk
- missing context
- distractors
- hallucination despite context


---

## Module 7 — Advanced RAG ★

**:**

### Pre-retrieval

- query rewriting
- HyDE
- query decomposition
- step-back prompting
- multi-query

### Retrieval

- hybrid (BM25 + dense)
- RRF fusion
- alpha tuning

### Post-retrieval

- cross-encoder reranking (BGE, Cohere)
- MMR diversity
- context compression
- LLM reranking

### Retrieval Structures

- small-to-big
- sentence-window
- auto-merging retrieval

### Alternatives

- long-context vs RAG
- cache-augmented generation


---

## Module 8 — Multi RAG ★

**:** 

### Multi-index

- routing across corpora
- index selection
- federated retrieval
- result merging

### Multi-modal

- image / table / chart embeddings
- ColPali
- image captioning pipelines
- multi-vector stores

### Multi-hop

- iterative retrieval
- self-RAG
- CRAG
- FLARE

### GraphRAG

- entity / relation extraction
- community detection
- local vs global search

### Structured + Unstructured

- text-to-SQL alongside vector retrieval
- schema linking


---

## Module 9 — Agentic RAG

**:**

### Agent Loop

- ReAct
- tool calling
- observation parsing
- termination

### Memory

- short-term
- long-term
- episodic
- semantic
- summarization and compaction

### Planning

- decomposition
- plan-and-execute
- reflection
- self-critique

### Multi-agent

- supervisor
- hierarchical
- swarm
- handoffs
- when it's overkill

### Frameworks

- LangGraph (state, nodes, edges, checkpointers, interrupts, subgraphs)
- one alternative framework

### Retrieval Control

- retrieval-as-tool
- adaptive retrieval
- corrective loops
- budget caps

### Safety

- human-in-the-loop
- approval gates
- guardrails
- sandboxing


---

## Module 10 — Evaluation ★

**:** 

### Retrieval Evaluation

- context precision
- context recall
- NDCG
- hit rate

### Generation Evaluation

- faithfulness / groundedness
- answer relevance
- correctness
- completeness

### Agent Evaluation

- trajectory accuracy
- tool-call correctness
- step efficiency
- route completeness

### LLM-as-Judge

- rubric design
- position bias
- verbosity bias
- self-preference
- calibration against human labels

### Datasets

- synthetic test set generation
- golden datasets
- regression suites

### Frameworks

- RAGAS
- DeepEval
- Phoenix
- Arize AX


---

## Module 11 — Fine-tuning and Optimization

**:**

### Decision

- when to fine-tune vs RAG vs prompt engineering

### Techniques

- LoRA
- QLoRA
- PEFT
- dataset curation and formatting

### Retrieval Model Training

- embedding model fine-tuning
- cross-encoder training

### Compression

- quantization (GGUF, AWQ, GPTQ)
- distillation

### Serving

- vLLM
- TGI
- Ollama
- continuous batching
- paged attention


---

## Module 12 — MLOps / LLMOps ★

**:**

### Containers and Orchestration

- Docker
- docker-compose
- multi-stage builds
- Kubernetes basics

### Engineering Workflow

- Git workflow
- CI/CD (GitHub Actions)
- pre-commit
- semantic versioning

### Versioning and Tracking

- data / model versioning: DVC, MLflow, model registry
- experiment tracking
- prompt registry and versioning

### Serving Patterns

- sync
- async
- streaming
- queues (Celery / Redis)
- rate limiting
- retries
- circuit breakers

### Observability

- OpenTelemetry
- traces / spans
- structured logging
- token and cost dashboards

### Monitoring

- latency SLOs
- drift detection
- feedback capture
- online eval sampling

### Deployment

- canary
- blue-green
- shadow
- A/B
- feature flags
- rollback

### Security

- prompt injection defense
- PII redaction
- secrets management
- tenant isolation
- audit logs

### FinOps

- caching
- model routing
- semantic cache
- batch APIs


---

## Capstone

**:**

**Agentic multi-source RAG in production:**

- hybrid retrieval + rerank
- tool-using LangGraph agent
- HITL gate
- full eval suite in CI
- OTel tracing
- canary deploy
- cost and quality dashboards
- documented failure modes and mitigations
