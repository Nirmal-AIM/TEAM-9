# 📍 Where to Run Commands

## Exact Location

Run `python train_pipeline.py` from inside the **`ml_backend`** folder.

## Step-by-Step Instructions

### 1. Open PowerShell/Terminal

### 2. Navigate to the ml_backend folder

```bash
cd "C:\Users\NIRMAL'S LOQ\credit-score-website\ml_backend"
```

Or if you're already in the project root:
```bash
cd ml_backend
```

### 3. Activate Virtual Environment (IMPORTANT!)

You already have `venv` folder created, so activate it:

**Windows (PowerShell):**
```bash
venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```bash
venv\Scripts\activate.bat
```

**You should see `(venv)` at the start of your prompt** like this:
```
(venv) PS C:\Users\NIRMAL'S LOQ\credit-score-website\ml_backend>
```

### 4. Now Run the Training Script

```bash
python train_pipeline.py
```

---

## Complete Command Sequence

Copy and paste these commands one by one:

```bash
# Navigate to ml_backend folder
cd "C:\Users\NIRMAL'S LOQ\credit-score-website\ml_backend"

# Activate virtual environment
venv\Scripts\Activate.ps1

# Run training
python train_pipeline.py
```

---

## Visual Guide

```
Your Project Structure:
credit-score-website/
├── src/
├── public/
├── ml_backend/          ← GO HERE!
│   ├── train_pipeline.py  ← RUN THIS FILE
│   ├── venv/            ← ACTIVATE THIS FIRST
│   └── ...
└── ...
```

---

## What You Should See

After running `python train_pipeline.py`, you should see output like:

```
============================================================
🚀 Credit Score ML Pipeline - Training
============================================================

============================================================
STEP 1: Loading Data
============================================================
✅ Loaded 1000 records with 85 columns

============================================================
STEP 2: Inferring Feature Types
============================================================
📊 Feature Type Inference:
  - ID columns: 1
  - Numeric columns: 60
  ...

============================================================
STEP 4: Training Credit Score Model
============================================================
🚀 Training Credit Score Model...
...
✅ Pipeline Training Complete!
```

---

## Troubleshooting

### Error: "No module named 'pandas'"
**Solution**: Make sure virtual environment is activated (you should see `(venv)` in prompt)

### Error: "python: command not found"
**Solution**: Use `py` instead of `python` on Windows:
```bash
py train_pipeline.py
```

### Error: "Cannot find CSV file"
**Solution**: The script looks for `public/credit_score.csv` in the parent directory. Make sure the file exists at:
```
credit-score-website/public/credit_score.csv
```

---

## Quick Check

Before running, verify you're in the right place:

```bash
# Check current directory
pwd  # or 'cd' on Windows

# Should show: ...\credit-score-website\ml_backend

# List files to confirm
dir  # or 'ls' on Linux/Mac

# Should see: train_pipeline.py, config.py, etc.
```

---

## After Training

Once training completes, you'll have:
- `ml_backend/models/credit_score_model.pkl`
- `ml_backend/models/preprocessor.pkl`
- `ml_backend/models/shap_explainer.pkl`
- `ml_backend/models/feature_info.pkl`

Then you can start the API server from the same location:
```bash
python api_server.py
```

