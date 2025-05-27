## Quick Start
First start all services:
```sh
docker-compose up --build -d
```

- Prometheus: [http://localhost:9090](http://localhost:9090)
- RabbitMQ metrics collected

**Check metrics:**  
In Prometheus, run:
```promql
rabbitmq_queue_messages_ready > 0
```
A number means metrics are collected and it will show if any queues is stuck.
