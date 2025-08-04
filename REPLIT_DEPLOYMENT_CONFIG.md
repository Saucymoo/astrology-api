# 🚀 REPLIT DEPLOYMENT CONFIGURATION

## REQUIRED .replit FILE CONFIGURATION

Since the .replit file cannot be edited directly, you need to update it manually in the Replit interface:

### Current Configuration (Node.js - INCORRECT):
```toml
modules = ["nodejs-20", "web", "postgresql-16", "python-3.11", "python3"]
run = "npm run dev"

[deployment]
deploymentTarget = "autoscale"
build = ["npm", "run", "build"]
run = ["npm", "run", "start"]
```

### Required Configuration (Python FastAPI - CORRECT):
```toml
modules = ["python-3.11", "web", "postgresql-16"]
run = "python3 main.py"

[deployment]
deploymentTarget = "autoscale"
run = ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

[[ports]]
localPort = 8000
externalPort = 80
```

## DEPLOYMENT STEPS

1. **Show Hidden Files** in Replit file tree (click the three dots menu)
2. **Edit .replit file** manually with the Python configuration above
3. **Remove Node.js modules** from the modules list
4. **Set correct run command** for development: `python3 main.py`
5. **Set correct deployment run command**: `["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]`
6. **Update port configuration** to use port 8000 instead of 5000
7. **Redeploy** the application

## FILES READY FOR DEPLOYMENT

✅ **main.py** - Standard FastAPI entry point (created)
✅ **run_production.py** - Production server with full API
✅ **pyproject.toml** - Python dependencies configured
✅ **Python modules installed** - FastAPI, uvicorn, pyswisseph, etc.

## EXPECTED RESULT

After configuration update and redeployment:
- **URL:** https://mias-astrology-api-miamitchell1974.replit.app/generate-chart
- **Response:** JSON chart data instead of HTML
- **Working endpoints:** /health, /generate-chart, /docs

## TEST COMMAND

Once deployed correctly, this should return JSON:
```bash
curl -X POST "https://mias-astrology-api-miamitchell1974.replit.app/generate-chart" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Mia",
    "birth_date": "1974-11-22",
    "birth_time": "19:10", 
    "birth_location": "Adelaide, South Australia, Australia"
  }'
```

Expected response: Complete JSON chart with Whole Sign houses and Swiss Ephemeris calculations.