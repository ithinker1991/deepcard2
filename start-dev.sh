#!/bin/bash

# DeepCard Development Environment Setup Script

echo "🚀 Starting DeepCard development environment..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create .env files if they don't exist
if [ ! -f "backend/.env" ]; then
    echo "📝 Creating backend .env file..."
    cp backend/.env.example backend/.env
    echo "⚠️  Please edit backend/.env with your actual configuration (especially OpenAI API key)"
fi

if [ ! -f "frontend/.env.local" ]; then
    echo "📝 Creating frontend .env.local file..."
    cat > frontend/.env.local << EOF
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
EOF
fi

# Start services
echo "🐳 Starting Docker containers..."
docker-compose up --build -d

echo "✅ Services started successfully!"
echo ""
echo "🌐 Available services:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Documentation: http://localhost:8000/docs"
echo "   Redis: localhost:6379"
echo ""
echo "📝 To view logs:"
echo "   docker-compose logs -f backend"
echo "   docker-compose logs -f frontend"
echo ""
echo "🛑 To stop services:"
echo "   docker-compose down"
echo ""
echo "🔧 For PostgreSQL (optional):"
echo "   docker-compose --profile postgres up -d postgres"