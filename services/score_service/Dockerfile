FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install fastapi uvicorn pika python-dotenv pymongo mysql-connector-python
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
