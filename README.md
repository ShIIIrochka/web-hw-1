# Blog Platform Backend

## DB Schema
![img.png](content/db-schema.png)

## Environment Variables

### Application
- `DB_URI` - PostgreSQL connection string
- `SECRET_KEY` - JWT secret key
- `DEBUG` - Debug mode

### Redis Cache
- `REDIS_URI` - Redis connection URL
- `CACHE_TTL_SECONDS` - Cache TTL in seconds

### OpenSearch
- `OPENSEARCH_URI` - OpenSearch URL

## Local Development

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

## Database Migrations

### Initial Setup

After first start, you need to run migrations:

```bash
uv run aerich upgrade
```

### Creating New Migrations

When you add new models or change existing ones:

```bash
# Generate migration
uv run aerich migrate --name "description_of_changes"

# Apply migration
uv run aerich upgrade
```


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