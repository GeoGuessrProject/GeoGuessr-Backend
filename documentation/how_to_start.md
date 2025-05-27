
# How to Start the GeoGuessr Project

## ▶️ Start Backend med alle services
- Sørg for at have Docker og Docker Compose installeret.

```bash
docker compose up --build -d
```

Run monitoring only (optional)
```bash
docker-compose -f docker-compose.monitoring.yml up --build -d
```

Combine both commands to start backend and monitoring
```bash
docker-compose -f docker-compose.yml -f docker-compose.monitoring.yml up --build -d
```

- Backend vil være tilgængelig på `http://localhost:8000`
- RabbitMQ vil være tilgængelig på `http://localhost:15672` (standard login: guest/guest)
- MySQL vil være tilgængelig på `http://localhost:3306`
- MongoDB vil være tilgængelig på `http://localhost:27017`

## ▶️ Start Frontend
- Sørg for at have Node.js og npm installeret.

```bash
npm install
npm run dev
```

- Frontend vil være tilgængelig på `http://localhost:5173` med live opdatering med Vite.