# 🚂 Railway PostgreSQL Setup Guide

## 🔍 Problem Identified
Your Django app is trying to connect to `localhost` for PostgreSQL, but Railway needs a Railway-managed PostgreSQL database.

## ✅ Solution: Add PostgreSQL to Railway

### **Step 1: Add PostgreSQL Database**
1. Go to your Railway project dashboard
2. Click **"+ New"** or **"Add Service"**
3. Select **"Database"** 
4. Choose **"PostgreSQL"**
5. Click **"Add PostgreSQL"**

### **Step 2: Verify Database Connection**
After adding PostgreSQL, Railway will automatically:
- ✅ Create a `DATABASE_URL` environment variable
- ✅ Connect it to your Django service
- ✅ Handle networking between services

### **Step 3: Check Environment Variables**
1. Go to your Django service in Railway
2. Click **"Variables"** tab
3. Verify you see:
   - `DATABASE_URL` (should start with `postgresql://`)
   - `RAILWAY_ENVIRONMENT` (set to `production`)

### **Step 4: Deploy the Fixed Code**
Push the updated code to trigger a new deployment:

```bash
git add -A
git commit -m "Fix Railway PostgreSQL configuration"
git push origin master
```

### **Step 5: Run Migrations**
After successful deployment, run migrations:

```bash
railway run python manage.py migrate
```

## 🔧 Debugging Steps

### **Check Database Configuration:**
Run this in your Railway project:
```bash
railway run python check-railway-db.py
```

### **View Logs:**
```bash
railway logs
```

### **Check Variables:**
```bash
railway variables
```

## 📊 Expected DATABASE_URL Format
Railway PostgreSQL should provide a URL like:
```
postgresql://user:password@host:port/database
```

## ⚠️ Common Issues

**If DATABASE_URL is missing:**
- PostgreSQL service not added to Railway project
- Services not connected

**If DATABASE_URL points to localhost:**
- Using local development database instead of Railway
- Environment detection not working

**If connection still fails:**
- Check Railway service status
- Verify PostgreSQL service is running
- Check network connectivity between services

## 🎯 Verification

Once working, your API endpoints should respond:
- **Root:** `https://your-app.railway.app/`
- **Pokemon:** `https://your-app.railway.app/api/v2/writable-pokemon/`
- **Docs:** `https://your-app.railway.app/api/v2/schema/swagger-ui/`

The fixed configuration will automatically detect Railway and use the proper PostgreSQL database!
