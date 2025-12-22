# Blog Platform Backend

A modern blog platform backend built with Litestar, featuring full-text search, caching, and observability.

## Architecture

### Tech Stack
- **Framework**: Litestar (async Python web framework)
- **ORM**: Tortoise ORM
- **Database**: PostgreSQL
- **Cache**: Redis (versioned keys for invalidation)
- **Search**: OpenSearch (full-text search with highlighting)
- **Observability**: Prometheus + Grafana + Loki
- **DI**: Punq (dependency injection)

### Key Features
- **Cursor-offset pagination** for stable, efficient list queries
- **Transactional outbox pattern** for eventual consistency with OpenSearch
- **Redis caching** with automatic invalidation on writes
- **Full-text search** with relevance scoring and highlighting
- **Structured JSON logging** with request correlation
- **Prometheus metrics** for HTTP, cache, and outbox processing
- **DDD-style architecture** (domain, application, infrastructure layers)

### Data Flow

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────┐
│  API Layer (Litestar Controllers)       │
│  - Posts: CRUD, list, search            │
│  - Auth: JWT-based authentication       │
└──────┬──────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────┐
│  Application Layer (Services)           │
│  - PostService (business logic)         │
│  - PostSearchService (search queries)   │
│  - Cache invalidation on writes         │
└──────┬──────────────────────────────────┘
       │
       ├──────────────┬──────────────┬─────────────┐
       ▼              ▼              ▼             ▼
┌──────────┐   ┌──────────┐   ┌──────────┐  ┌──────────┐
│PostgreSQL│   │  Redis   │   │  Outbox  │  │OpenSearch│
│  (main)  │   │ (cache)  │   │ (events) │  │ (search) │
└──────────┘   └──────────┘   └────┬─────┘  └─────▲────┘
                                    │              │
                                    └──────────────┘
                                   Outbox Worker
                                   (async indexing)
```

### Outbox Pattern
To maintain DDD principles and avoid coupling `PostService` with search infrastructure:
1. On `create/update/delete` post → write event to `outbox_events` table (same transaction)
2. Separate **Outbox Worker** polls events and indexes to OpenSearch
3. If OpenSearch is down, events retry with exponential backoff
4. Search becomes **eventually consistent** (typically <5s delay)

## DB Schema
![img.png](content/db-schema.png)

# Local Development with Docker

## Prerequisites

- Docker and Docker Compose installed
- At least 4GB of free RAM (for all services)

## Environment Variables

The following environment variables can be configured in `docker/compose.yml`:

### Application
- `DB_URI` - PostgreSQL connection string (default: `postgres://blog:blogpass@postgres:5432/blog`)
- `SECRET_KEY` - JWT secret key (change in production!)
- `DEBUG` - Debug mode (default: `True`)
- `LOG_LEVEL` - Logging level: DEBUG, INFO, WARNING, ERROR (default: `INFO`)

### Redis Cache
- `REDIS_URL` - Redis connection URL (default: `redis://redis:6379/0`)
- `CACHE_TTL_SECONDS` - Cache TTL in seconds (default: `60`)

### OpenSearch
- `OPENSEARCH_URL` - OpenSearch URL (default: `http://opensearch:9200`)
- `OPENSEARCH_INDEX` - Index name for posts (default: `posts`)

## Start All Services

From project root:

```bash
docker compose -f docker/compose.yml up -d --build
```

This starts the following services:

| Service | URL | Description |
|---------|-----|-------------|
| **Blog API** | http://localhost:8000 | Main application |
| **API Docs** | http://localhost:8000/schema | OpenAPI documentation |
| **Metrics** | http://localhost:8000/metrics | Prometheus metrics endpoint |
| **PostgreSQL** | localhost:5432 | Database (user: `blog`, password: `blogpass`) |
| **Redis** | localhost:6379 | Cache |
| **OpenSearch** | http://localhost:9200 | Full-text search engine |
| **Prometheus** | http://localhost:9090 | Metrics storage |
| **Grafana** | http://localhost:3000 | Dashboards (login: `admin`/`admin`) |
| **Loki** | http://localhost:3100 | Log aggregation |

## Check Service Health

```bash
# Check all services are running
docker compose -f docker/compose.yml ps

# View logs from all services
docker compose -f docker/compose.yml logs -f

# View logs from specific service
docker compose -f docker/compose.yml logs -f app
```

## Database Migrations

### Initial Setup

After first start, you need to run migrations:

```bash
# Enter the app container
docker compose -f docker/compose.yml exec app bash

# Inside container, run migrations
uv run aerich upgrade
```

### Creating New Migrations

When you add new models or change existing ones:

```bash
# Enter the app container
docker compose -f docker/compose.yml exec app bash

# Generate migration
uv run aerich migrate --name "description_of_changes"

# Apply migration
uv run aerich upgrade
```

**Note**: The `outbox_events` table migration should be created automatically when you first run `aerich migrate` after pulling these changes.

## Observability

### Viewing Metrics in Prometheus

1. Open http://localhost:9090
2. Go to **Graph** tab
3. Example queries:
   - `rate(http_requests_total[5m])` - Request rate
   - `histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))` - p95 latency
   - `cache_hits_total / (cache_hits_total + cache_misses_total)` - Cache hit rate

### Viewing Logs in Grafana

1. Open http://localhost:3000 (login: `admin` / `admin`)
2. Go to **Explore** → select **Loki** datasource
3. Example queries:
   - `{app="blog"}` - All application logs
   - `{app="blog", level="ERROR"}` - Only errors
   - `{app="blog"} |= "request_id"` - Logs with request_id
   - `{app="blog"} | json | request_id="<UUID>"` - Filter by specific request

### Pre-configured Dashboard

1. Open Grafana http://localhost:3000
2. Go to **Dashboards** → **Blog API Overview**
3. The dashboard shows:
   - HTTP request rate
   - Request latency (p95, p99)
   - Error rate (5xx responses)
   - Cache hit rate
   - Outbox events processing
   - Live application logs

### Request Tracing

Every HTTP request gets a unique `X-Request-ID` header in the response. Use this ID to:
1. Filter logs in Loki: `{app="blog"} | json | request_id="<ID>"`
2. Trace the full request lifecycle across logs

## Testing the API

```bash
# Health check
curl http://localhost:8000/

# View metrics
curl http://localhost:8000/metrics

# Register a user
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123","username":"testuser"}'

# View OpenAPI docs
open http://localhost:8000/schema
```

## Stop Services

```bash
# Stop all services
docker compose -f docker/compose.yml down

# Stop and remove volumes (WARNING: deletes all data)
docker compose -f docker/compose.yml down -v
```

## Troubleshooting

### OpenSearch fails to start
- Increase Docker memory limit to at least 4GB
- On Linux, you may need to increase `vm.max_map_count`:
  ```bash
  sudo sysctl -w vm.max_map_count=262144
  ```

### Logs not appearing in Loki
- Check Promtail is running: `docker compose -f docker/compose.yml logs promtail`
- Verify log directory exists: `mkdir -p /var/log/blog`
- Check Promtail config in `docker/promtail/promtail-config.yml`

### Cannot connect to services
- Ensure all services are healthy: `docker compose -f docker/compose.yml ps`
- Check service logs: `docker compose -f docker/compose.yml logs <service-name>`

## Production Deployment Notes

For production:
1. Change `SECRET_KEY` to a strong random value
2. Set `DEBUG=False`
3. Use managed services (AWS RDS, ElastiCache, OpenSearch Service, etc.)
4. Enable OpenSearch security
5. Use proper secrets management (not env vars in compose file)
6. Set up proper log retention policies in Loki
7. Configure Prometheus remote write to long-term storage
8. Use TLS/SSL for all services

# API

## Users

### Update me
![img_5.png](content/img_5.png)
![img_4.png](content/img_4.png)
![img_6.png](content/img_6.png)
![img_17.png](content/img_17.png)

### Delete me
![img_15.png](content/img_15.png)

### Get me
![img_7.png](content/img_7.png)
![img_16.png](content/img_16.png)

## Auth

### Register User
![img_1.png](content/img_1.png)
![img_2.png](content/img_2.png)
![img_3.png](content/img_3.png)

### Refresh
![img.png](content/img.png)
![img_18.png](content/img_18.png)


## Posts

### Create Post
![img_8.png](content/img_8.png)
![img_9.png](content/img_9.png)
![img_19.png](content/img_19.png)

### Delete Post
![img_10.png](content/img_10.png)
![img_11.png](content/img_11.png)


### Update Post
![img_12.png](content/img_12.png)
![img_13.png](content/img_13.png)
![img_14.png](content/img_14.png)
![img_20.png](content/img_20.png)