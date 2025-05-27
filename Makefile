# Makefile

# Run the command with: `make <target>`
# Example: `make up` to start the services

# Start all services with Docker Compose
up:
	docker-compose up -d

# Stop all services
down:
	docker-compose down

# View logs
logs:
	docker-compose logs -f

# Rebuild services
rebuild:
	docker-compose up --build -d

# Remove everything (containers, networks, etc.)
clean:
	docker-compose down -v --remove-orphans
