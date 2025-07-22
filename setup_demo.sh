#!/bin/bash
# Quick Demo Setup Script for David Linthicum Presentation

echo "🎬 Setting up Tire Defect Detection Demo for David Linthicum..."
echo "============================================================="

# Check prerequisites
echo "🔍 Checking prerequisites..."

if ! command -v docker &> /dev/null; then
    echo "❌ Docker is required but not installed"
    echo "Please install Docker Desktop from https://www.docker.com/products/docker-desktop"
    exit 1
fi

if ! docker info &> /dev/null; then
    echo "❌ Docker is not running"
    echo "Please start Docker Desktop"
    exit 1
fi

echo "✅ Docker is ready"

# Build and start services
echo "🔨 Building demo environment..."
docker-compose build --parallel

echo "🚀 Starting all services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 30

# Check service health
echo "🔍 Checking service health..."

# Check MQTT
if docker-compose ps mqtt | grep -q "Up"; then
    echo "✅ MQTT broker is running"
else
    echo "❌ MQTT broker failed to start"
fi

# Check Backend API
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend API is responding"
else
    echo "❌ Backend API is not responding"
fi

# Check Dashboard
if curl -s http://localhost:8501 > /dev/null; then
    echo "✅ Dashboard is running"
else
    echo "⚠️  Dashboard might be starting (this is normal)"
fi

echo ""
echo "🎉 Demo Setup Complete!"
echo "======================="
echo ""
echo "📊 Dashboard: http://localhost:8501"
echo "🔧 API Docs:  http://localhost:8000/docs"  
echo "❤️  Health:   http://localhost:8000/health"
echo ""
echo "🎯 Demo is ready for David Linthicum!"
echo ""
echo "📋 Quick Commands:"
echo "  View logs:    docker-compose logs -f"
echo "  Stop demo:    docker-compose down"
echo "  Restart:      docker-compose restart"
echo ""
echo "📖 See DEMO_GUIDE.md for full presentation script"
