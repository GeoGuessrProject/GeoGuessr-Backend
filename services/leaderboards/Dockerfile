FROM python:3.11-slim

WORKDIR /app
COPY . .

# Install only what this service actually needs
RUN pip install --no-cache-dir \
    flask \
    celery \
    pymongo \
    redis \
    python-dotenv

# Optional if you expose Flask API
EXPOSE 8000

# Use entrypoint override in docker-compose to run worker/beat/web
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "8000"]
