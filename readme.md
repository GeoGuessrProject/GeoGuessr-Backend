
# GeoGuessr Project – Quick Start Guide

## 🚀 Starting the Backend (All Services)

1. **Prerequisites:**  
    Ensure you have Docker and Docker Compose installed.

2. **Setup the .env file:**
   Remember to insert your own credentials for the diffrent services
```bash
RABBITMQ_HOST=xxxxx
RABBITMQ_DEFAULT_USER=xxxxx
RABBITMQ_DEFAULT_PASS=xxxxx

MYSQL_USER=xxxxx
MYSQL_PASSWORD=xxxxx
MYSQL_ROOT_PASSWORD=xxxxx
MYSQL_DATABASE=xxxxx
MYSQL_HOST=xxxxx
MYSQL_PORT=xxxxx

JWT_SECRET_KEY=xxxxx

MONGO_URI=xxxxx

AMQP_URL=xxxxx

EMAIL_USER=xxxxx
EMAIL_PASS=xxxxx
EMAIL_HOST = xxxxx
EMAIL_PORT = xxxxx
```

3. **Start all backend services:**
    ```bash
    docker compose up --build -d
    ```

4. **(Optional) Start monitoring services only:**
    ```bash
    docker-compose -f docker-compose.monitoring.yml up --build -d
    ```

5. **Start backend and monitoring together:**
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
