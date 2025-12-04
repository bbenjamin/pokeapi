#!/bin/bash

# 🚂 Railway Deployment Script for Educational PokéAPI

echo "🎓 Setting up Educational PokéAPI for Railway deployment..."

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Please install it first:"
    echo "   npm install -g @railway/cli"
    exit 1
fi

echo "✅ Railway CLI found"

# Login check
echo "🔐 Checking Railway authentication..."
if ! railway whoami &> /dev/null; then
    echo "❌ Not logged into Railway. Please run:"
    echo "   railway login"
    exit 1
fi

echo "✅ Railway authentication verified"

# Set environment variables
echo "⚙️  Setting up environment variables..."
railway variables set RAILWAY_ENVIRONMENT=production
railway variables set DJANGO_SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')

echo "✅ Environment variables configured"

# Add PostgreSQL database
echo "🗄️  Adding PostgreSQL database..."
railway add postgresql

echo "✅ PostgreSQL database added"

# Deploy the application
echo "🚀 Deploying to Railway..."
railway up

echo "🎉 Deployment initiated!"
echo ""
echo "📋 Next steps:"
echo "1. Wait for deployment to complete"
echo "2. Run migrations: railway run python manage.py migrate"
echo "3. (Optional) Load sample data: railway run python manage.py loaddata data/v2/fixtures/pokemon.json"
echo "4. Visit your app URL to see the educational API!"
echo ""
echo "📖 Your educational endpoints will be available at:"
echo "   - /api/v2/writable-pokemon/"
echo "   - /api/v2/writable-berry/"
echo "   - /api/v2/writable-ability/"
echo "   - /api/v2/writable-type/"
echo ""
echo "📚 Documentation available at:"
echo "   - /api/v2/schema/swagger-ui/ (Interactive)"
echo "   - /api/v2/schema/redoc/ (Alternative docs)"
