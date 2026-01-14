# Quick Start Guide - AI Governance Dashboard

## 5-Minute Setup

### Step 0: Navigate to Project (10 seconds)
```powershell
cd c:\Hacks\KingHack
```

**EASIEST OPTION**: Just run the launcher:
```powershell
# In PowerShell:
.\launcher.bat

# OR double-click launcher.bat in File Explorer
```

The launcher handles all steps automatically! ✓

---

### Or do it manually:

### Step 1: Install Dependencies (2 minutes)
```powershell
pip install -r requirements.txt
```

### Step 2: Train Models (1-2 minutes)
```powershell
python train_models.py
```

You should see:
```
================================================================================
AI Governance & Transparency Dashboard - Model Training Pipeline
================================================================================

[1/4] Loading datasets...
✓ Loaded 3 datasets:
  - loan: 10000 samples, 14 features
  - churn: 5000 samples, 12 features
  - hr_attrition: 8000 samples, 15 features

[2/4] Training models...
✓ Trained 9 models
  ✓ loan_default_lr_v1
    - Accuracy: 0.7234
  ... (more models)

[3/4] Initializing governance system...
✓ Registered 9 models in governance system

[4/4] Analyzing fairness and bias...
✓ Fairness and drift analysis complete

================================================================================
✓ Training pipeline complete!
================================================================================
```

### Step 3: Launch Dashboard (30 seconds)
```powershell
streamlit run app.py
```

The dashboard will open at: **http://localhost:8501**

## What You'll See

### 📊 Overview Page
- 9 trained models (3 datasets × 3 algorithms)
- Real-time performance metrics
- Model portfolio summary

### 🔍 Model Analysis Page
- Select any model to inspect
- View feature importance rankings
- See sample prediction explanations
- Understand which features drive predictions

### ⚖️ Fairness & Bias Page
- Detect bias across demographic groups (gender, age)
- Disparate impact analysis
- Per-group accuracy metrics
- Recommendations for bias mitigation

### 📉 Drift Detection Page
- Monitor feature drift from training data
- KS statistical tests
- Population Stability Index (PSI)
- Identify which features have drifted

### 🏛️ Governance Page
- Complete model registry
- Approval workflow status
- Audit trail of all predictions

### 🚨 Alerts Page
- System health check
- Critical alerts summary
- Actionable recommendations

## Key Metrics at a Glance

| Metric | What it Means | Good Value |
|--------|---|---|
| Accuracy | % correct predictions | > 75% |
| Precision | % of positive predictions that are correct | > 70% |
| Recall | % of actual positives found | > 70% |
| AUC | Overall ranking ability | > 0.75 |
| **Disparate Impact Ratio** | Fairness (1.0 = perfectly fair) | ≥ 0.80 |
| **TPR Disparity** | Difference in true positive rates | < 0.10 |
| **PSI** | Data drift severity | < 0.10 (low) |

## Explore the Dashboard

1. **Start with Overview**: Get a bird's-eye view of all models
2. **Pick a Model**: Click Model Analysis to dive deep
3. **Check Fairness**: Go to Fairness & Bias to understand bias
4. **Monitor Drift**: Check Drift Detection for data quality issues
5. **Review Governance**: Verify audit trail and approvals

## Common Use Cases

### Use Case 1: Check Model Health
1. Go to **Overview**
2. Look at accuracy metrics across all models
3. Check **Alerts & Recommendations** for issues

### Use Case 2: Investigate Model Bias
1. Go to **Fairness & Bias**
2. Select a model
3. Review fairness metrics per gender/age group
4. Check disparate impact ratio

### Use Case 3: Monitor Data Quality
1. Go to **Drift Detection**
2. Review PSI scores (Population Stability Index)
3. High PSI (>0.25) indicates data has shifted
4. May need to retrain models

### Use Case 4: Understand a Prediction
1. Go to **Model Analysis**
2. Review "Prediction Explanations" section
3. See which features most influenced the decision

## What Each Model Does

### 1. Loan Default Prediction
- **Purpose**: Predict whether a loan applicant will default
- **Business Impact**: Risk assessment for lending decisions
- **Sensitive Attributes**: Gender, age, income level
- **Bias Risk**: May disadvantage certain demographic groups

### 2. Customer Churn Prediction
- **Purpose**: Identify customers likely to leave
- **Business Impact**: Retention and customer lifetime value
- **Sensitive Attributes**: Gender, customer age, location
- **Bias Risk**: May treat different demographics differently

### 3. HR Attrition Prediction
- **Purpose**: Forecast which employees may leave
- **Business Impact**: Workforce planning and retention
- **Sensitive Attributes**: Gender, age, salary level
- **Bias Risk**: May perpetuate existing HR biases

## Data Files Generated

After training, you'll have:

```
data/
├── loan_data.csv              (10,000 loan applications)
├── churn_data.csv             (5,000 customer records)
└── hr_attrition_data.csv      (8,000 employee records)

models/
├── loan_default_lr_v1.pkl     (Logistic Regression)
├── loan_default_rf_v1.pkl     (Random Forest)
├── loan_default_xgb_v1.pkl    (XGBoost)
├── churn_lr_v1.pkl
├── churn_rf_v1.pkl
├── churn_xgb_v1.pkl
├── hr_attrition_lr_v1.pkl
├── hr_attrition_rf_v1.pkl
├── hr_attrition_xgb_v1.pkl
└── model_metadata.json        (All model info)

logs/
└── governance.db              (Audit trail, predictions, fairness checks)
```

## Customization Tips

### Change Fairness Thresholds
Edit `src/bias_detector.py`:
```python
# Change this line (80% rule = 0.8)
has_disparate_impact = impact_ratio < 0.75  # Stricter threshold
```

### Add More Datasets
Edit `src/data_loader.py` and add:
```python
def load_or_create_your_data(data_dir):
    # Your code here
    return df, "your_dataset_name"
```

### Change Model Algorithms
Edit `train_models.py` and modify:
```python
for model_type in ['lr', 'rf', 'xgb', 'your_model_type']:
    # Train models
```

## Troubleshooting

**Q: Dashboard won't start**
- A: Check that dependencies installed: `pip list | grep streamlit`
- Run `python train_models.py` first

**Q: Models not found**
- A: Models are auto-trained on first run
- Check `models/` directory exists
- Look for `.pkl` files

**Q: Slow performance**
- A: Dashboard caches on first load
- Subsequent loads are faster
- Reduce dataset size in `data_loader.py` if needed

**Q: Want to reset everything**
```powershell
# Remove generated files
rm -r data/
rm -r models/
rm -r logs/

# Retrain
python train_models.py
```

## Next Steps

### Level 1: Explore (15 minutes)
- Run dashboard and explore all pages
- Understand metrics and visualizations
- Review model explanations

### Level 2: Customize (30 minutes)
- Modify dataset sizes
- Adjust fairness thresholds
- Add your own datasets

### Level 3: Production Ready (1-2 hours)
- Implement real data sources
- Add authentication/RBAC
- Set up monitoring alerts
- Deploy to cloud platform

## Architecture Overview

```
Input Data (CSV)
    ↓
Data Loader (Preprocessing)
    ↓
Model Trainer (9 Models)
    ↓
┌─────────────────────────────┐
│   Governance Database       │
│   ├─ Predictions            │
│   ├─ Evaluations            │
│   ├─ Fairness Checks        │
│   └─ Drift Detections       │
└─────────────────────────────┘
    ↓
┌─────────────────────────────┐
│  Analysis Engines           │
│  ├─ Bias Detector           │
│  ├─ Drift Detector          │
│  ├─ Explainability Engine   │
│  └─ Fairness Reporter       │
└─────────────────────────────┘
    ↓
Streamlit Dashboard
    ├─ Overview
    ├─ Model Analysis
    ├─ Fairness & Bias
    ├─ Drift Detection
    ├─ Governance
    └─ Alerts
```

## Performance Baseline

For default settings (3 datasets, 9 models):

| Task | Time |
|------|------|
| Data Generation | ~10 sec |
| Model Training | ~30-60 sec |
| Fairness Analysis | ~10 sec |
| Dashboard Launch | ~2 min |

## Support Resources

- **README.md**: Full documentation
- **app.py**: Dashboard source code
- **src/**: Core modules with docstrings
- **train_models.py**: Training pipeline

## Success Criteria

✓ You've succeeded when:
1. `python train_models.py` runs without errors
2. Dashboard loads at http://localhost:8501
3. You can see 9 models with metrics
4. Fairness analysis shows bias detection
5. Drift detection page shows results
6. Governance page has model registry

---

**Ready to explore?** Run:
```powershell
python train_models.py
streamlit run app.py
```

Then open http://localhost:8501 in your browser!
