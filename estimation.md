# 10 Simultaneous Connections

* Business Service: 1 container running uvicorn (1–2 workers)

* Workers (Celery): 2 simple workers

* Redis and DB: single small instances, default connection pools

* Logs and alerts: write to local files

* Result: all good for light usage, little to no queue backlog

# 50 Simultaneous Connections

* API:  2–3 containers, increase number of uvicorn workers

* Workers: scale to (approx) 4 Celery workers, monitor queue

* Redis: upgrade to 1 CPU 1 GB

* DB: mid‑size instance

* Logging: rotate daily, keep alert files tidy

* Result: handles moderate bursts

# 100+ Simultaneous Connections

* API: 5+ pods in k8s

* Workers: 10+ workers, split queues (high vs default), autoscale based on backlog

* Redis: managed service

* DB: primary + read replicas; consider partitioning if data grows

* Monitoring: central logs, alert on error rates and queue depth

* Result: production‑ready