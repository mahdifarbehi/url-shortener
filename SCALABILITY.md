# SCALABILITY

## 1. Heavy logging per request

- sending logs into queue
- background workers storing logs
- DB trigger visit counter
- DLQ for failed logs
- non-blocking redirect path
- Example: app → queue → worker

## 2. Multi-instance deployment

- shared Redis cache layer
- shared message broker queue
- shared database, no state
- load balancer with health-check
- automatic routing and failover
- Example: LB → instances → DB

## 3. Heavy traffic / campaigns

- cache-first redirect lookups
- async logging, no inline writes
- DB connection pooling tuned
- basic IP rate limiting
- optional CDN for global traffic
- Example: client → LB → instances
