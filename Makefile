.PHONY: help build up down logs clean

help:
	@echo "Available commands:"
	@echo "  make build  - build Docker images"
	@echo "  make up     - start all services"
	@echo "  make down   - stop all services"
	@echo "  make logs   - view logs"
	@echo "  make clean  - clean everything"

build:
	docker-compose build

up:
	docker-compose up -d
	@echo "FastAPI available at http://localhost:8000"
	@echo "Gradio available at http://localhost:7860"

down:
	docker-compose down

logs:
	docker-compose logs -f

clean:
	docker-compose down -v
	docker system prune -f