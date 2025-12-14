# 🚀 Quick Start Guide

## What We Have Now

✅ **Frontend** - React app with UI  
✅ **ML Pipeline** - Complete Python code  
⏳ **Need to do** - Train model & connect them  

---

## 3 Simple Steps to Get Running

### 1️⃣ Setup Python Backend (5 min)

```bash
# Open PowerShell/Terminal
cd ml_backend

# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### 2️⃣ Train Model (2 min)

```bash
# Still in ml_backend folder with venv activated
python train_pipeline.py
```

Wait for: "✅ Pipeline Training Complete!"

### 3️⃣ Start API Server (1 min)

```bash
# Still in ml_backend folder
python api_server.py
```

You should see: "Server will run on http://localhost:8000"

**Keep this terminal open!**

---

## Connect Frontend (Optional - for testing)

1. **Create `.env` file** in project root:
```env
VITE_API_BASE_URL=http://localhost:8000/api
```

2. **Update `src/hooks/useCreditScore.js`** - Uncomment lines 20-22 and 42-45

3. **Start frontend** (in a NEW terminal):
```bash
npm run dev
```

---

## Test It!

1. **API Docs**: http://localhost:8000/docs
2. **Frontend**: http://localhost:5173

Try the "Analyze Score" button or test API directly in docs!

---

## That's It! 🎉

You now have:
- ✅ Trained ML model
- ✅ API server running
- ✅ Frontend ready to connect

See `NEXT_STEPS.md` for detailed instructions!

