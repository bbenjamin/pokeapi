# 🚂 Railway Deployment Guide

## Quick Start

1. **Install Railway CLI** (if not already installed):
```bash
npm install -g @railway/cli
```

2. **Login to Railway**:
```bash
railway login
```

3. **Run the deployment script**:
```bash
./deploy-railway.sh
```

4. **Run migrations after deployment**:
```bash
railway run python manage.py migrate
```

5. **Test your deployment**:
Visit the provided Railway URL to see your educational API!

## Manual Deployment Steps

If you prefer to deploy manually:

```bash
# Set environment variables
railway variables set RAILWAY_ENVIRONMENT=production
railway variables set DJANGO_SECRET_KEY="your-secret-key-here"

# Add PostgreSQL database  
railway add postgresql

# Deploy
railway up

# Run migrations
railway run python manage.py migrate
```

## Educational Endpoints

Your deployed API will include these writable endpoints for teaching:

- `/api/v2/writable-pokemon/` - Full CRUD for Pokemon
- `/api/v2/writable-berry/` - Full CRUD for Berries
- `/api/v2/writable-ability/` - Full CRUD for Abilities  
- `/api/v2/writable-type/` - Full CRUD for Types

## Documentation

Interactive documentation available at:
- `/api/v2/schema/swagger-ui/` - Swagger UI
- `/api/v2/schema/redoc/` - ReDoc UI
- `/api/v2/schema/` - Raw OpenAPI schema

## Environment Variables

Required for Railway deployment:
- `RAILWAY_ENVIRONMENT=production` (automatically detects Railway)
- `DJANGO_SECRET_KEY` (generated automatically by script)
- `DATABASE_URL` (provided by Railway PostgreSQL)

## Troubleshooting

**Check logs**: `railway logs`
**Check variables**: `railway variables`
**Restart service**: `railway up --detach`

## Features Enabled for Education

✅ All HTTP methods (GET, POST, PUT, PATCH, DELETE)  
✅ Interactive API documentation  
✅ CORS enabled for frontend development  
✅ Comprehensive error handling  
✅ Name and ID-based lookups  
✅ Auto-generated OpenAPI 3.1.0 schema
