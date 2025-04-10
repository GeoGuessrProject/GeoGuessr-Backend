# Login Service – Lokal test med Docker & Kubernetes

Dette er en simpel Express-baseret login-microservice, som er containeriseret og klar til lokal test med Kubernetes. Servicen returnerer en mock-token ved korrekt login, og fungerer som en proof-of-concept for vores microservice-arkitektur.

## Sådan tester du lokalt

**1. Gå til login-service mappen**
```bash
cd server/login
```

**2. Byg Docker-containeren**
```bash
docker build -t login-service .
```

**3. Sørg for Kubernetes kører**
- Brug Docker Desktop og aktivér Kubernetes under _"Settings > Kubernetes"_  
eller
- Brug Minikube

**4. Deploy servicen til lokal Kubernetes**
```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

**5. Kontroller, at servicen kører korrekt**
```bash
kubectl get pods
kubectl get services
```
Servicen bør nu være tilgængelig på NodePort `30001`.

**6. Test login-endpoint**

Brug **curl**:
```bash
curl -X POST http://localhost:30001/login \
-H "Content-Type: application/json" \
-d '{"username": "admin", "password": "password"}'
```

eller **JavaScript** (fra frontend eller browser):
```javascript
fetch("http://localhost:30001/login", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({ username: "admin", password: "password" })
})
  .then(res => res.json())
  .then(console.log);
```

**7. Ryd op efter test (valgfrit)**
```bash
kubectl delete -f deployment.yaml
kubectl delete -f service.yaml
```

## Bemærkninger

- Kubernetes anvender Docker-image `login-service` lokalt (`imagePullPolicy: Never`).
- Login-servicen foretager endnu ingen databasekald; al data er mock’et.
- Næste trin er integration med MySQL og token-baseret autentifikation.

## Filoversigt

```
server/login/
├── index.js             # Express login-service
├── Dockerfile           # Docker container setup
├── deployment.yaml      # Kubernetes Deployment
├── service.yaml         # Kubernetes Service
└── readme.md            # Denne vejledning
```  
