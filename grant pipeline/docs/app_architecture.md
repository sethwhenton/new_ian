# Application Architecture

```mermaid
---
config:
  layout: elk
---
flowchart LR
  %% ==== CLIENT ====
  U["User"] -- Upload image(s) + select type --> FE["Frontend (Svelte/React)"]
  FE -- POST /api/jobs  (images, meta) --> API["Backend API (Flask)"]
  FE <-- SSE/WebSocket: job status & progress --> API

  %% ==== BACKEND CORE ====
  subgraph Backend_Services["Backend Services"]
    VAL["Validation: allowed types/MIME/size"]
    ORCH["Pipeline Orchestrator (sync & async)"]
    STORE["Storage Service (save image/overlay)"]
    REPO["Results Repo via SQLAlchemy"]
    DOCS["OpenAPI/Swagger"]
    LOGS["Logs/Monitoring (Prom/Grafana/Sentry)"]
  end

  API --> VAL & ORCH & STORE & REPO & DOCS & LOGS

  %% ==== STORAGE ====
  STORE --> FS[("Image/Object Storage: ./media or S3/MinIO")]
  REPO --> DB[("MySQL")]

  %% ==== ASYNC JOBS & BATCHING ====
  subgraph Async_Tasks["Asynchronous Inference"]
    Q["Task Queue (Redis/RabbitMQ)"]
    subgraph W["GPU Batch Worker(s)"]
      DIR["Batch Director: micro-batch & scheduling"]
      subgraph Model_Pipeline["Model Pipeline (batched)"]
        PRE["Image Preprocessor (batched)"]
        SAM["Segmenter (SAM ViT-B)\n*micro-batch images or per-image mask gen*"]
        PATCH["Patch Extractor: bbox + mask (vectorized where possible)"]
        CLF["Classifier (ResNet-50) — batched inference"]
        MAP["Label Mapper (zero-shot/synonyms → finite set)"]
        CNT["Counter + Postprocess (merge, NMS, size filters)"]
        EXP["Explainer: overlays/heatmaps"]
      end
    end
  end

  ORCH -- enqueue job (job_id, URIs) --> Q
  Q -- pull N items --> DIR
  DIR -- assemble micro-batches --> PRE
  PRE --> SAM --> PATCH --> CLF --> MAP --> CNT --> EXP
  EXP -- write overlays --> STORE
  CNT -- write counts/stats --> REPO

  %% ==== STATUS & RESULTS ====
  API <-- poll/subscribe job status (progress %, ETA, partials) --> Q
  API -- GET /api/jobs/{id} (count, overlay bytes, stats) --> FE
  API -- INSERT result & corrections --> REPO
  FE -- POST /api/correct (human fix) --> API
