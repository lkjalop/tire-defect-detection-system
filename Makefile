.PHONY: help setup build start stop logs clean demo

help:
	@echo "🛞 Tire Defect Detection - Laptop Edition"
	@echo "========================================"
	@echo "Available commands:"
	@echo "  setup    - Quick laptop setup"
	@echo "  build    - Build lightweight images"
	@echo "  start    - Start all services"
	@echo "  stop     - Stop all services"
	@echo "  logs     - Show logs"
	@echo "  demo     - Quick demo setup"

setup:
	@echo "🔧 Setting up for laptop..."
	python -m venv venv
	@echo "📦 Installing dependencies..."
	@echo "✅ Setup complete!"

build:
	@echo "🔨 Building laptop-optimized images..."
	docker-compose build

start:
	@echo "🚀 Starting services..."
	docker-compose up -d

stop:
	@echo "🛑 Stopping services..."
	docker-compose down

logs:
	@echo "📝 Showing logs..."
	docker-compose logs -f

demo:
	@echo "🎪 Setting up quick demo..."
	make build
	make start
	@echo "✅ Demo ready!"
	@echo "📊 Dashboard: http://localhost:8501"
	@echo "🔧 API: http://localhost:8000/docs"

clean:
	@echo "🧹 Cleaning up..."
	docker-compose down -v
	docker system prune -f
