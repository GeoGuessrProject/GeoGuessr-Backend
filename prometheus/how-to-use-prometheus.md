## Quick Start
Start the backend with monitoring using Docker Compose:
```bash
docker-compose -f docker-compose.yml -f docker-compose.monitoring.yml up --build -d
```

- Prometheus: [http://localhost:9090](http://localhost:9090)
- RabbitMQ metrics collected

**Check metrics:**  
In Prometheus, run:
```promql
rabbitmq_queue_messages_ready > 0
```
A number means metrics are collected and it will show if any queues is stuck.

## Monitoring and Alerts
- **Prometheus Alerts:** [http://localhost:9090/alerts](http://localhost:9090/alerts)  
    View active and pending alerts configured in Prometheus.

- **Alertmanager Status:** [http://localhost:9093/#/status](http://localhost:9093/#/status)  
    Check the status and configuration of Alertmanager.