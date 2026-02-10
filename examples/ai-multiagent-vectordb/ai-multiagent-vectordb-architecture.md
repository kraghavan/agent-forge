# AI Multi-Agent System with Vector DB Memory

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              EXTERNAL SERVICES                                   │
│  ┌─────────────────────┐                                                        │
│  │   ☁️ Claude API      │ ◄─── AI Decisions (cost-controlled)                   │
│  │    (Anthropic)      │                                                        │
│  └─────────────────────┘                                                        │
└─────────────────────────────────────────────────────────────────────────────────┘
         ▲                           ▲                           ▲
         │ 1 call/60s                │ 10% msgs, 1/30s           │ 1 call/120s
         │                           │ (skip if hit>0.85)        │
┌────────┴───────────────────────────┴───────────────────────────┴────────────────┐
│                               AI AGENTS                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ 📤 Publisher-1│  │ 📤 Publisher-2│  │ 📥 Consumer-1 │  │ 📥 Consumer-2 │         │
│  │  AI Decisions │  │  AI Decisions │  │ Vector+AI    │  │ Vector+AI    │         │
│  └──────┬───────┘  └──────┬───────┘  └──────▲───────┘  └──────▲───────┘         │
│         │                  │                 │                 │                 │
│         └────────┬─────────┘                 └────────┬────────┘                 │
│                  ▼                                    │                          │
│         ┌────────────────┐              ┌─────────────┴──────────────┐           │
│         │   🔍 Monitor    │              │      🧠 Vector Memory       │           │
│         │ Health Analysis │◄─────────────│  Qdrant + Sentence Trans.  │           │
│         └────────────────┘              └────────────────────────────┘           │
└─────────────────────────────────────────────────────────────────────────────────┘
                  │                                    ▲
                  ▼                                    │
┌─────────────────────────────────────────────────────┴───────────────────────────┐
│                            MESSAGE BROKER                                        │
│  ┌─────────────────────────────────────────┐                                    │
│  │          🐰 RabbitMQ                     │                                    │
│  │         Exchange: "books"                │                                    │
│  │  ┌─────────────┐   ┌─────────────────┐  │                                    │
│  │  │📚 fictional  │   │📖 non-fictional  │  │                                    │
│  │  │   queue     │   │     queue       │  │                                    │
│  │  └─────────────┘   └─────────────────┘  │                                    │
│  └─────────────────────────────────────────┘                                    │
└─────────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          OBSERVABILITY STACK                                     │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐      │
│  │ 📊 InfluxDB   │   │  📝 Loki     │   │  📡 Promtail │   │  📈 Grafana  │      │
│  │   Metrics    │──▶│    Logs     │◀──│ Log Collector│   │  Dashboards  │      │
│  └──────────────┘   └──────────────┘   └──────────────┘   └──────────────┘      │
│         │                   │                                    ▲               │
│         └───────────────────┴────────────────────────────────────┘               │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Service Details

| Service | Port | Purpose | Image |
|---------|------|---------|-------|
| InfluxDB | 8086 | Time-series metrics | influxdb:2.7 |
| RabbitMQ | 5672, 15672 | Message broker | rabbitmq:3-management |
| Qdrant | 6333, 6334 | Vector database | qdrant/qdrant:latest |
| Loki | 3100 | Log aggregation | grafana/loki:2.9.0 |
| Promtail | - | Log collection | grafana/promtail:2.9.0 |
| Grafana | 3000 | Dashboards | grafana/grafana:latest |
| Publisher-1/2 | - | AI message publishers | Custom build |
| Consumer-1/2 | - | AI message consumers | Custom build |
| Monitor | - | Health monitoring | Custom build |

---

## Data Flow

### 1. Publishing Flow
```
Publisher → Claude API (decision) → RabbitMQ → Queues
    │
    └──→ InfluxDB (metrics)
    └──→ Promtail → Loki (logs)
```

### 2. Consuming Flow (with Vector Memory)
```
Queue → Consumer → Generate Embedding (Sentence Transformers)
                          │
                          ▼
                   Search Qdrant (top 5 similar)
                          │
            ┌─────────────┴─────────────┐
            ▼                           ▼
    Score > 0.85?                  Score < 0.85?
    (MEMORY HIT)                   (MEMORY MISS)
            │                           │
            ▼                           ▼
    Use cached decision          Call Claude API
            │                           │
            └──────────┬────────────────┘
                       ▼
              Store in Qdrant
              (for future hits)
                       │
                       ▼
              InfluxDB + Loki
```

### 3. Monitoring Flow
```
Monitor → Query InfluxDB (metrics)
       → Query Qdrant (vector stats)
       → Claude API (health analysis)
       → InfluxDB + Loki (results)
```

---

## Vector Memory System

```
┌────────────────────────────────────────────────────────────────┐
│                    SEMANTIC MEMORY LAYER                        │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────┐         ┌─────────────────────────────┐   │
│  │ Sentence Trans. │         │         Qdrant              │   │
│  │ all-MiniLM-L6-v2│────────▶│   Collection: book_messages │   │
│  │   (384 dims)    │         │                             │   │
│  └─────────────────┘         │   Vectors: 384 dimensions   │   │
│         ▲                    │   Distance: Cosine          │   │
│         │                    │   Payload:                  │   │
│   Message Text               │     - message_id            │   │
│                              │     - timestamp             │   │
│                              │     - genre                 │   │
│                              │     - action_taken          │   │
│                              │     - ai_reasoning          │   │
│                              │     - confidence            │   │
│                              └─────────────────────────────┘   │
│                                                                 │
│  Memory Threshold: 0.85 (similarity score)                      │
│  - Above 0.85 → Use cached decision (save API cost)            │
│  - Below 0.85 → Call Claude API for new decision               │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

## Cost Controls

| Agent | Rate Limit | Condition | Max Tokens |
|-------|------------|-----------|------------|
| Publisher | 1 call / 60s | Always | 300 |
| Consumer | 1 call / 30s | 10% of messages, skip if memory hit > 0.85 | 200 |
| Monitor | 1 call / 120s | Always | 400 |

### Estimated Savings with Vector Memory
- Without memory: ~14 Claude calls/hour per consumer
- With 85% memory hit rate: ~2 calls/hour per consumer
- **Savings: ~85% reduction in API costs**

---

## Docker Compose Services

```yaml
Services:
  ├── Infrastructure
  │   ├── influxdb (metrics DB)
  │   ├── rabbitmq (message broker)
  │   ├── qdrant (vector DB)
  │   ├── loki (log aggregation)
  │   ├── promtail (log collection)
  │   └── grafana (dashboards)
  │
  ├── Setup Jobs
  │   ├── influxdb-setup (verify bucket)
  │   └── rabbitmq-setup (create exchange/queues)
  │
  └── AI Agents
      ├── publisher-1
      ├── publisher-2
      ├── consumer-1
      ├── consumer-2
      └── monitor
```

---

## Key Technologies

| Component | Technology | Purpose |
|-----------|------------|---------|
| AI | Claude API (Anthropic) | Decision making |
| Embeddings | Sentence Transformers | Local text → vector |
| Vector DB | Qdrant | Semantic search & memory |
| Message Queue | RabbitMQ | Async message routing |
| Metrics | InfluxDB | Time-series metrics |
| Logs | Loki + Promtail | Log aggregation |
| Dashboards | Grafana | Visualization |
| Container | Docker Compose | Orchestration |

---

## Metrics Collected

### InfluxDB Measurements
- `messages_published` - Publisher output count
- `messages_consumed` - Consumer input count
- `memory_hit_count` - Vector memory cache hits
- `memory_miss_count` - Vector memory cache misses
- `ai_decision_count` - Claude API calls made
- `tokens_used` - API tokens consumed
- `vector_search_ms` - Qdrant query latency
- `processing_duration_ms` - End-to-end processing time
- `confidence_score` - Memory similarity scores

---

## Quick Reference

```bash
# Start system
docker-compose up -d

# View logs
docker-compose logs -f consumer-1

# Check InfluxDB data
docker-compose exec influxdb influx query \
  'from(bucket: "agent_metrics") |> range(start: -1h)' \
  --org monitoring --token my-super-secret-auth-token

# Access UIs
# Grafana:  http://localhost:3000 (admin/admin)
# RabbitMQ: http://localhost:15672 (guest/guest)
# InfluxDB: http://localhost:8086
# Qdrant:   http://localhost:6333/dashboard
```