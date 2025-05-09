# Task 1

1. **Build & Run**  
   ```bash
   cd business_service
   podman build -t business_service:latest .
   podman run -d --name business_service  -p 8000:8000 business_service:latest
2. **Test**  
    ```bash
    curl http://localhost:8000/health
    podman logs business_service
    ```
3. **Cleanup**
    ```bash
    podman stop business_service
    podman rm business_service
    podman rmi business_service:latest
    podman system prune -f
    ```

# Task 2

1. Run &check logs
    ```
    cd ..                              
    podman-compose up -d --build    
    podman ps                      
    curl http://localhost:8001/status
    curl http://localhost:8000/health 
    podman logs pinger  
    ```

2. Cleanup
    ```
    podman-compose down
    podman system prune -f
    podman rmi business_service:latest pinger:latest   
    ```

---
# Next HW
---

## Setup

1. Clone the repo:

   ```bash
   git clone https://github.com/incredet/ITArch_HW5.git
   cd ITArch_HW5
   ```
2. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. **Install Python deps**:

   ```bash
   pip install -r requirements.txt
   ```

## Running locally with uvicorn

```bash
uvicorn business_service.business_service:app --reload --host 0.0.0.0 --port 8000
```

Then in another shell:

```bash
# Enqueue a task
echo '{"user_id":1,"action":"test","amount":5}'  | curl -X POST http://localhost:8000/process -H "Content-Type: application/json"
# Response:
# {"status":"queued","task_id":"<ID>"}

# Check status
curl http://localhost:8000/task/<ID>
# Possible output:
# {"state":"PENDING"} or {"state":"SUCCESS","result":{...}}
```

Logs appear in `logs/business_service.log`, and any alerts generate `.txt` in `error_reports/`.

---

## Running with Containers

### Podman-Compose

```bash
# (macOS only) ensure VM is running
podman machine init   # first time
podman machine start

# Start all services + workers
podman-compose up --build -d

# Verify
podman ps
```

### Docker Compose

```bash
docker compose up --build -d
docker ps
```

---

## Testing Endpoints

1. **Business Service** (`:8000`)

   * `POST /process` → enqueue
   * `GET  /task/{id}` → status/result
2. **Pinger Service** (`:8001`)

   ```bash
   curl http://localhost:8001/health
   # "pong"
   ```
3. **DB Service**
   Use its defined CRUD HTTP endpoints as needed.

---

## Logs & Alerts

* **Logs**: `logs/*.log` (INFO+)
* **Alerts**: `error_reports/alert_<type>_<timestamp>.txt`

Example alert file:

```
Time: 2025-05-09T20:21:02.456789 UTC
Type: invalid_input
Description: Missing required fields in payload
```

---

## Architecture Diagram

See `docs/architecture.mmd` → `docs/architecture.png` for a visual flowchart of services, workers, and data flows.

---

## Scaling Estimates

Check `docs/scaling_estimates.md` for how to scale at 10, 50, and 100+ concurrent connections.

---

**Enjoy exploring the system!** Let me know if you encounter any issues or need further examples.
