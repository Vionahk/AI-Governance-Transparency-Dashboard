# Windows Setup Instructions

## Complete Setup Guide for Windows PowerShell

### System Requirements
- Windows 7, 8, 10, 11
- Python 3.8 or higher (3.10+ recommended)
- 4GB RAM minimum (8GB recommended)
- 500MB disk space for models and data

### Check Python Installation

Open PowerShell and verify Python is installed:

```powershell
python --version
pip --version
```

You should see:
```
Python 3.10.x or higher
pip 23.x or higher
```

If not, download from [python.org](https://www.python.org/downloads/) and install.

### Step 1: Navigate to Project Directory

```powershell
cd c:\Hacks\KingHack
```

Verify you see these files:
```powershell
Get-ChildItem
```

Expected output:
```
app.py
train_models.py
requirements.txt
README.md
QUICKSTART.md
src/
data/
models/
logs/
```

### Step 2: Create Virtual Environment (Optional but Recommended)

Create an isolated Python environment:

```powershell
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\Activate.ps1
```

You should see `(venv)` prefix in your PowerShell prompt.

**Note**: If you get execution policy error:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 3: Install Python Dependencies

```powershell
pip install -r requirements.txt
```

This will install 17 Python packages (total ~500MB):
- pandas, numpy, scikit-learn, xgboost
- fairlearn, aif360, shap
- streamlit, plotly, matplotlib
- scipy, joblib, sqlalchemy

Wait for completion. Progress shown:
```
Collecting pandas==2.0.3
...
Successfully installed pandas numpy scikit-learn xgboost... (17 packages)
```

### Step 4: Train Models

Run the training pipeline (generates data, trains 9 models):

```powershell
python train_models.py
```

**OR use the launcher script** (handles everything automatically):

```powershell
# In PowerShell:
.\launcher.bat

# OR double-click launcher.bat in File Explorer (easiest!)
```

Expected output:
```
================================================================================
AI Governance & Transparency Dashboard - Model Training Pipeline
================================================================================

[1/4] Loading datasets...
[OK] Loaded 3 datasets:
  - loan: 10000 samples, 14 features
  - churn: 5000 samples, 12 features
  - hr_attrition: 8000 samples, 15 features

[2/4] Training models...
[OK] Trained 9 models
  [OK] loan_default_lr_v1
    - Accuracy: 0.7234
    - Precision: 0.6845
    - Recall: 0.7123
    - AUC: 0.7856
  ... (8 more models)

[3/4] Initializing governance system...
[OK] Registered 9 models in governance system

[4/4] Analyzing fairness and bias...
[OK] Fairness and drift analysis complete

================================================================================
[OK] Training pipeline complete!
================================================================================
```

**Duration**: 1-2 minutes depending on CPU

### Step 5: Launch Dashboard

Start the Streamlit dashboard:

```powershell
streamlit run app.py
```

Expected output:
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://your-computer-ip:8501
```

### Step 6: View Dashboard

Automatically opens in default browser. If not:

Open browser and navigate to: **http://localhost:8501**

You should see the AI Governance Dashboard homepage!

## Dashboard Navigation

### Menu Structure

```
Navigation (left sidebar)
├─ Overview              (Summary of all models)
├─ Model Analysis        (Deep dive into one model)
├─ Fairness & Bias       (Bias detection by demographic)
├─ Drift Detection       (Data quality monitoring)
├─ Governance            (Model registry & approvals)
└─ Alerts & Recommendations (System health)
```

### Quick Demo Flow

1. **Overview** (1 min)
   - See all 9 models
   - View average metrics
   - Check last update time

2. **Model Analysis** (3 min)
   - Select a model (e.g., `loan_default_rf_v1`)
   - View 4 performance metrics
   - See top 10 important features
   - Read sample prediction explanations

3. **Fairness & Bias** (3 min)
   - Select same model
   - View metrics by gender/age group
   - Check disparate impact ratio
   - See alert if bias detected

4. **Drift Detection** (2 min)
   - View KS test results for each feature
   - See PSI bar chart
   - Color coded: red=high drift, yellow=medium, green=low

5. **Governance** (1 min)
   - See complete model registry
   - View model creation dates
   - Check approval status

6. **Alerts** (30 sec)
   - System health summary
   - Critical alerts (if any)
   - Recommendations

## File Locations

After running `train_models.py`, you'll have:

```
c:\Hacks\KingHack\
├── data\                    (Generated datasets)
│   ├── loan_data.csv
│   ├── churn_data.csv
│   └── hr_attrition_data.csv
│
├── models\                  (Trained models)
│   ├── loan_default_lr_v1.pkl
│   ├── loan_default_rf_v1.pkl
│   ├── loan_default_xgb_v1.pkl
│   ├── churn_lr_v1.pkl
│   ├── churn_rf_v1.pkl
│   ├── churn_xgb_v1.pkl
│   ├── hr_attrition_lr_v1.pkl
│   ├── hr_attrition_rf_v1.pkl
│   ├── hr_attrition_xgb_v1.pkl
│   └── model_metadata.json
│
└── logs\                    (Governance database)
    └── governance.db
```

## Stopping the Dashboard

When done exploring:

```powershell
# Press Ctrl+C in PowerShell
# OR close the browser tab
```

The PowerShell window shows: `Shutting down...`

## Deactivating Virtual Environment

When finished:

```powershell
deactivate
```

You lose the `(venv)` prefix in PowerShell.

## Restarting Later

To use again:

```powershell
cd c:\Hacks\KingHack
venv\Scripts\Activate.ps1
streamlit run app.py
```

## Troubleshooting

### Error: "Python not found"
```powershell
# Check if Python is installed
python --version

# If not, download from python.org
# During installation, CHECK "Add Python to PATH"
```

### Error: "ExecutionPolicy prevents running"
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Then try again
venv\Scripts\Activate.ps1
```

### Error: "Module not found" (streamlit, pandas, etc.)
```powershell
# Reinstall dependencies
pip install -r requirements.txt --upgrade

# Or if in venv, ensure it's activated
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Error: "Address already in use" (port 8501)
```powershell
# Kill the process using port 8501
netstat -ano | findstr :8501
taskkill /PID <PID> /F

# Or use different port
streamlit run app.py --server.port 8502
```

### Slow Dashboard Performance
- First load: 1-2 minutes (caches everything)
- Subsequent loads: 2-5 seconds
- Wait for page to fully load before clicking

### Models Not Found After Training
```powershell
# Check if models exist
Get-ChildItem models\

# If empty, training failed
# Check output of: python train_models.py

# Re-run training
python train_models.py
```

### "ModuleNotFoundError: No module named 'src'"
```powershell
# Make sure you're in correct directory
cd c:\Hacks\KingHack

# Check if src\ folder exists
Get-ChildItem src\

# If missing, recreate from source
```

## Advanced: Using Conda Instead of venv

If you prefer conda:

```powershell
# Create conda environment
conda create -n kingai python=3.10

# Activate
conda activate kingai

# Install dependencies
pip install -r requirements.txt

# Run normally
python train_models.py
streamlit run app.py
```

## Advanced: Using Python 3.11+

If you have Python 3.11 or 3.12:

```powershell
# Works as-is, but may have dependency conflicts
pip install -r requirements.txt

# If conflicts, update versions in requirements.txt
# Most packages support 3.11+
```

## System Requirements Verification

```powershell
# Check all requirements
python -c "import sys; print(f'Python {sys.version}')"
python -c "import pandas as pd; print(f'pandas {pd.__version__}')"
python -c "import numpy as np; print(f'numpy {np.__version__}')"
python -c "import sklearn; print(f'scikit-learn {sklearn.__version__}')"
python -c "import streamlit as st; print(f'streamlit {st.__version__}')"
```

All should return version numbers without errors.

## Disk Space Usage

- **Python packages**: ~500 MB
- **Generated data**: ~10 MB
- **Trained models**: ~50 MB
- **Governance database**: ~5 MB
- **Total**: ~565 MB

## Network/Firewall

The dashboard runs locally on your machine:
- **Local only**: http://localhost:8501
- **Network access**: http://<your-ip>:8501

No internet connection needed after installation.

## Additional Resources

- **Microsoft Python Setup**: https://docs.microsoft.com/en-us/windows/python/
- **Python Virtual Environments**: https://docs.python.org/3/venv/
- **Streamlit Docs**: https://docs.streamlit.io/
- **scikit-learn**: https://scikit-learn.org/

## Getting Help

1. Check the [README.md](README.md) for full documentation
2. Review [QUICKSTART.md](QUICKSTART.md) for quick guide
3. Check console output for error messages
4. Verify all files exist in correct locations

## Success Checklist

[OK] Python 3.8+ installed  
[OK] Virtual environment created (optional)  
[OK] Dependencies installed without errors  
[OK] `python train_models.py` completed successfully  
[OK] Models created in `models/` folder  
[OK] Data created in `data/` folder  
[OK] Database created in `logs/` folder  
[OK] Dashboard launched with `streamlit run app.py`  
[OK] Browser opened to http://localhost:8501  
[OK] Can navigate all 6 dashboard pages  

---

**Ready to go!** Start with:

```powershell
cd c:\Hacks\KingHack
python train_models.py
streamlit run app.py
```

Then open http://localhost:8501 in your browser!
