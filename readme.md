
# GeoGuessr Project – Quick Start Guide

## 🚀 Starting the Backend (All Services)

1. **Prerequisites:**  
    Ensure you have Docker and Docker Compose installed.

2. **Start all backend services:**
    ```bash
    docker compose up --build -d
    ```

3. **(Optional) Start monitoring services only:**
    ```bash
    docker-compose -f docker-compose.monitoring.yml up --build -d
    ```

4. **Start backend and monitoring together:**
    ```bash
    docker-compose -f docker-compose.yml -f docker-compose.monitoring.yml up --build -d
    ```

**Service Endpoints:**
- Backend: [http://localhost:8000](http://localhost:8000)
- RabbitMQ: [http://localhost:15672](http://localhost:15672) (default login: `guest`/`guest`)
- MySQL: [localhost:3306](http://localhost:3306)
- Monitoring Prometheus: [http://localhost:9090](http://localhost:9090)
---

## 🌐 Accessing the Frontend

- The frontend is deployed and available at (but you still ned backend running locally):
  [https://geoguessr-project.netlify.app/](https://geoguessr-project.netlify.app/)

---

## 🛠️ Running the Frontend Locally

1. **Prerequisites:**  
    Install [Node.js](https://nodejs.org/) and npm.

2. **Clone the frontend repository:**  
    [https://github.com/GeoGuessrProject/Geoguessr-Frontend](https://github.com/GeoGuessrProject/Geoguessr-Frontend)

3. **Install dependencies and start the development server:**
    ```bash
    npm install
    npm run dev
    ```

- The frontend will be available at [http://localhost:5173](http://localhost:5173) with live reloading via Vite.
