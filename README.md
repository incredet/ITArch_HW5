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

