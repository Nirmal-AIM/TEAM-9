# Next Steps - Getting Everything Running

## Current Status

✅ **Frontend**: Complete and ready  
✅ **ML Pipeline**: Code created, needs training  
✅ **API Server**: Code created, needs to run  
⏳ **Integration**: Needs connection  

## Step-by-Step Guide

### STEP 1: Set Up Python ML Backend (5-10 minutes)

1. **Open a new terminal/PowerShell**

2. **Navigate to ML backend**:
```bash
cd ml_backend
```

3. **Create virtual environment**:
```bash
python -m venv venv
```

4. **Activate virtual environment**:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

5. **Install dependencies**:
```bash
pip install -r requirements.txt
```

**Expected output**: All packages install successfully

---

### STEP 2: Train the ML Model (2-5 minutes)

1. **Make sure you're in `ml_backend` directory with venv activated**

2. **Run training script**:
```bash
python train_pipeline.py
```

**What happens**:
- Loads `credit_score.csv`
- Infers feature types
- Creates synthetic credit scores
- Trains ML model
- Creates SHAP explainer
- Saves models to `ml_backend/models/` folder

**Expected output**: 
- Model performance metrics (R², RMSE, MAE)
- "✅ Pipeline Training Complete!"

**Check**: Look for `ml_backend/models/` folder with `.pkl` files

---

### STEP 3: Start the API Server (1 minute)

1. **Keep terminal open with venv activated**

2. **Start API server**:
```bash
python api_server.py
```

**Expected output**:
```
🚀 Starting Credit Score ML API Server...
📡 Server will run on http://localhost:8000
📚 API docs available at http://localhost:8000/docs
```

3. **Verify it's running**:
   - Open browser: http://localhost:8000/docs
   - You should see API documentation (Swagger UI)

**Keep this terminal open** - API server must stay running!

---

### STEP 4: Connect Frontend to Backend (2 minutes)

1. **Open a NEW terminal** (keep API server running in first terminal)

2. **Navigate to project root**:
```bash
cd "C:\Users\NIRMAL'S LOQ\credit-score-website"
```

3. **Create/Update `.env` file**:
```env
VITE_API_BASE_URL=http://localhost:8000/api
```

4. **Update frontend hooks to use API**:
   - Open `src/hooks/useCreditScore.js`
   - Uncomment the API calls (remove `//` comments)
   - Do the same in `src/hooks/useDocumentUpload.js` if needed

5. **Start frontend** (if not running):
```bash
npm run dev
```

---

### STEP 5: Test the Integration (5 minutes)

1. **Frontend**: http://localhost:5173/
2. **API Docs**: http://localhost:8000/docs

3. **Test "Analyze Score" button**:
   - Click "Login to View Score" button
   - Should call API and get prediction
   - Should show credit score and explanation

4. **Test API directly** (in API docs):
   - Go to http://localhost:8000/docs
   - Click "POST /api/credit-score/analyze"
   - Click "Try it out"
   - Enter sample data:
   ```json
   {
     "INCOME": 50000,
     "SAVINGS": 10000,
     "DEBT": 20000,
     "R_DEBT_INCOME": 0.4,
     "R_SAVINGS_INCOME": 0.2,
     "DEFAULT": 0
   }
   ```
   - Click "Execute"
   - Should return credit score and explanation

---

## Quick Checklist

- [ ] Python virtual environment created
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Model trained (`python train_pipeline.py`)
- [ ] Models saved in `ml_backend/models/` folder
- [ ] API server running (`python api_server.py`)
- [ ] API accessible at http://localhost:8000/docs
- [ ] Frontend `.env` file created with API URL
- [ ] Frontend running (`npm run dev`)
- [ ] Test "Analyze Score" button works
- [ ] Test chatbot with user ID lookup

---

## Troubleshooting

### Issue: "Module not found" when running training
**Solution**: Make sure virtual environment is activated and dependencies installed

### Issue: "Model not found" when starting API
**Solution**: Run `python train_pipeline.py` first

### Issue: API server won't start
**Solution**: 
- Check if port 8000 is in use
- Try changing port in `api_server.py`

### Issue: Frontend can't connect to API
**Solution**:
- Check API server is running
- Verify `.env` file has correct URL
- Check browser console for CORS errors

### Issue: "CSV file not found"
**Solution**: Ensure `public/credit_score.csv` exists in project root

---

## What You'll Have After Setup

1. ✅ **Trained ML Model** - Predicts credit scores
2. ✅ **SHAP Explanations** - Feature importance
3. ✅ **Human-Readable Insights** - Natural language explanations
4. ✅ **REST API** - Backend server running
5. ✅ **Frontend Integration** - React app connected
6. ✅ **Full Pipeline** - End-to-end working system

---

## Current Terminal Setup

You'll need **2 terminals**:

**Terminal 1** (ML Backend):
```bash
cd ml_backend
venv\Scripts\activate
python api_server.py
# Keep this running!
```

**Terminal 2** (Frontend):
```bash
cd "C:\Users\NIRMAL'S LOQ\credit-score-website"
npm run dev
# Keep this running!
```

---

## Ready to Start?

**Begin with STEP 1** - Set up the Python environment and install dependencies!

Let me know if you encounter any issues during setup! 🚀

