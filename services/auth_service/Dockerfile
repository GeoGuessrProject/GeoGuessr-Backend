FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --upgrade pip \
    && pip install fastapi uvicorn pika python-dotenv mysql-connector-python sqlalchemy pymysql python-jose[cryptography] bcrypt
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
