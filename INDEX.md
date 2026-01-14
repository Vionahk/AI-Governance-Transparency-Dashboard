# AI Governance & Transparency Dashboard - Complete Documentation

## Project Overview

A production-ready Python dashboard for monitoring enterprise machine learning models with comprehensive Responsible AI capabilities including:

**Model Performance Tracking** - Real-time accuracy, precision, recall, AUC metrics  
**Fairness & Bias Detection** - Identify disparate impact across demographics  
**Data Drift Monitoring** - Statistical tests for distribution shifts  
**Model Explainability** - Feature importance and SHAP interpretations  
**Enterprise Governance** - Complete audit logs and approval workflows  
**Interactive Dashboard** - Streamlit-based web interface  

## Quick Links

| Document | Purpose |
|----------|---------|
| **[QUICKSTART.md](QUICKSTART.md)** | 5-minute setup guide |
| **[README.md](README.md)** | Full documentation |
| **[app.py](app.py)** | Main dashboard application |
| **[train_models.py](train_models.py)** | Model training pipeline |

## Getting Started (30 seconds)

```powershell
# 1. Install dependencies
pip install -r requirements.txt

# 2. Train models
python train_models.py

# 3. Launch dashboard
streamlit run app.py
```

Dashboard opens at: **http://localhost:8501**

## Project Structure

```
KingHack/
├── 📄 README.md                 Full documentation
├── 📄 QUICKSTART.md             Quick start guide
├── 📄 INDEX.md                  This file
├── 📄 requirements.txt           Python dependencies
├── 🐍 app.py                    Main Streamlit dashboard
├── 🐍 train_models.py           Model training pipeline
│
├── 📁 src/                      Core modules
│   ├── __init__.py
│   ├── data_loader.py          Dataset loading & preparation
│   ├── model_trainer.py         Model training & versioning
│   ├── bias_detector.py         Fairness & bias analysis
│   ├── explainability.py        SHAP & feature importance
│   └── governance.py            Audit logging & governance
│
├── 📁 data/                     Generated datasets
│   ├── loan_data.csv           (10K samples)
│   ├── churn_data.csv          (5K samples)
│   └── hr_attrition_data.csv   (8K samples)
│
├── 📁 models/                   Trained models
│   ├── loan_default_lr_v1.pkl
│   ├── loan_default_rf_v1.pkl
│   ├── loan_default_xgb_v1.pkl
│   └── [6 more models...]
│
├── 📁 logs/                     Governance logs
│   └── governance.db            SQLite audit database
│
└── 📁 notebooks/                Jupyter notebooks (optional)
```

## Feature Breakdown

### 1. Three Enterprise ML Models

| Model | Purpose | Business Value | Bias Risk |
|-------|---------|---|---|
| **Loan Default** | Predict loan defaults | Reduce credit risk | May disadvantage minorities |
| **Customer Churn** | Predict customer loss | Improve retention | May treat demographics unfairly |
| **HR Attrition** | Forecast employee turnover | Workforce planning | Can perpetuate hiring biases |

Each with:
- 5,000-10,000 realistic samples
- Multiple sensitive attributes (gender, age, income)
- Built-in bias patterns for demonstration

### 2. Three Model Algorithms per Dataset

- **Logistic Regression** - Fast, interpretable
- **Random Forest** - High accuracy, complex
- **XGBoost** - State-of-art performance

Total: **9 models** trained and monitored

### 3. Comprehensive Fairness Analysis

- **Demographic Parity**: Equal positive prediction rates across groups
- **Equal Opportunity**: Equal TPR (true positive rate) across groups
- **Calibration**: Prediction probability matches actual outcome rate
- **Disparate Impact**: 4/5 rule (80% rule) compliance
- **Intersectional Bias**: Analysis across multiple sensitive attributes

### 4. Statistical Drift Detection

- **Kolmogorov-Smirnov Test**: Feature-by-feature statistical test
- **Population Stability Index**: Measure of distribution shift magnitude
- **Drift Severity**: Classification as low/medium/high
- **Historical Tracking**: Drift trends over time

### 5. Model Explainability

- **Feature Importance Ranking**: Which features matter most
- **SHAP Support**: Shapley-based explanations (when available)
- **Sample Explanations**: Why each prediction was made
- **Contribution Analysis**: Which features influenced the decision

### 6. Enterprise Governance

**Audit Logging**
- Every prediction is logged with timestamp
- Model version tracking
- User attribution
- Feature hash for anonymization

**Model Registry**
- Centralized model metadata
- Approval workflows
- Version control
- Change history

**Fairness Checks**
- Automated bias detection
- Threshold-based alerts
- Historical compliance tracking

**Drift Monitoring**
- Continuous feature monitoring
- Drift severity classification
- Alert generation

### 7. Interactive Dashboard

**Six Dashboard Pages:**

1. **Overview** - Quick health check across all models
2. **Model Analysis** - Deep dive into single model performance
3. **Fairness & Bias** - Demographic group analysis
4. **Drift Detection** - Statistical distribution monitoring
5. **Governance** - Model registry and approvals
6. **Alerts** - System health and recommendations

## Technical Stack

| Component | Technology |
|-----------|---|
| **Dashboard** | Streamlit 1.28.0 |
| **ML Algorithms** | scikit-learn 1.3.0, XGBoost 2.0.0 |
| **Fairness Tools** | fairlearn 0.10.0, aif360 0.5.0 |
| **Explainability** | SHAP 0.43.0 |
| **Data Processing** | pandas 2.0.3, numpy 1.24.3 |
| **Visualization** | Plotly 5.17.0, Matplotlib 3.7.2 |
| **Database** | SQLite3 (built-in) |
| **Statistical Tests** | scipy 1.11.2 |

## Key Capabilities

### Model Performance Monitoring
```
Real-time metrics:
✓ Accuracy, Precision, Recall, F1, AUC
✓ Per-class performance
✓ Confusion matrix analysis
✓ ROC curve visualization
```

### Fairness Analysis
```
Bias detection:
✓ Per-group accuracy metrics
✓ True Positive Rate (TPR) parity
✓ False Positive Rate (FPR) parity
✓ Disparate impact calculation (4/5 rule)
✓ Intersectional bias analysis
✓ Fairness recommendations
```

### Drift Detection
```
Data quality monitoring:
✓ Kolmogorov-Smirnov statistical test
✓ Population Stability Index (PSI)
✓ Feature-level drift tracking
✓ Severity classification (low/medium/high)
✓ Historical drift trends
```

### Model Explainability
```
Prediction interpretability:
✓ Top-N feature importance ranking
✓ Feature contribution to predictions
✓ Sample-level explanations
✓ Correct vs incorrect prediction analysis
✓ SHAP value support (KernelExplainer)
```

### Governance & Compliance
```
Enterprise requirements:
✓ Complete audit trail
✓ Model registry with versioning
✓ Approval workflows
✓ PII anonymization
✓ Governance database (SQLite)
✓ Prediction logging
✓ Fairness & drift check history
```

## Data Flow

```
1. DATA GENERATION
   ├── Loan Default Dataset (10K samples)
   ├── Customer Churn Dataset (5K samples)
   └── HR Attrition Dataset (8K samples)
           ↓
2. DATA PREPARATION
   ├── Feature encoding
   ├── Scaling
   ├── Sensitive feature identification
   └── Train/test split (80/20)
           ↓
3. MODEL TRAINING
   ├── Logistic Regression
   ├── Random Forest
   └── XGBoost
           ↓
4. MODEL VERSIONING & STORAGE
   ├── Save .pkl files
   ├── Store metadata
   └── Register in governance system
           ↓
5. ANALYSIS & MONITORING
   ├── Performance metrics
   ├── Fairness checks
   ├── Drift detection
   ├── Explainability analysis
   └── Governance logging
           ↓
6. VISUALIZATION & DASHBOARD
   ├── Streamlit web interface
   ├── Interactive plots
   ├── Real-time metrics
   └── Governance reports
```

## Responsible AI Principles Implemented

### 1. **Transparency**
- Model decisions explained via feature importance
- SHAP values for individual predictions
- Clear performance metrics documented

### 2. **Fairness**
- Systematic bias detection
- Per-group performance analysis
- Disparate impact monitoring
- Fairness recommendations

### 3. **Accountability**
- Complete audit trail of predictions
- Model approval workflows
- Governance database
- Compliance tracking

### 4. **Governance**
- Model registry system
- Version control
- Change tracking
- Approval processes

### 5. **Monitoring**
- Real-time performance tracking
- Data drift detection
- Fairness drift monitoring
- Alert system

## Usage Workflows

### Workflow 1: Daily Health Check (5 minutes)
1. Open dashboard Overview page
2. Scan model metrics
3. Check Alerts page for issues
4. ✓ Done - models are healthy

### Workflow 2: Investigate Model Bias (15 minutes)
1. Go to Fairness & Bias page
2. Select model of interest
3. Review per-group metrics
4. Check for disparate impact
5. Review recommendations

### Workflow 3: Monitor Data Quality (10 minutes)
1. Go to Drift Detection page
2. Review KS test results
3. Analyze PSI values
4. Check for high-drift features
5. Decide if retraining needed

### Workflow 4: Understand a Prediction (10 minutes)
1. Go to Model Analysis page
2. View feature importance ranking
3. Review prediction explanations
4. Understand which features drove decision
5. Share findings with stakeholders

## Configuration & Customization

### Change Model Types
Edit `train_models.py`:
```python
for model_type in ['lr', 'rf', 'xgb', 'svm', 'knn']:
    # Add new model type
```

### Adjust Fairness Thresholds
Edit `src/bias_detector.py`:
```python
threshold = 0.75  # Change from default 0.80
```

### Add Custom Datasets
Edit `src/data_loader.py`:
```python
def load_custom_data(data_dir):
    df = pd.read_csv('your_data.csv')
    return df, "custom_dataset"
```

### Modify Sensitive Features
Edit `src/data_loader.py` `load_all_datasets()`:
```python
sensitive_features=['gender', 'age', 'income', 'region']
```

## Deployment Options

### Local Development
```bash
python train_models.py
streamlit run app.py
```

### Docker Container
```dockerfile
FROM python:3.10
RUN pip install -r requirements.txt
CMD streamlit run app.py
```

### Cloud Deployment
- **AWS**: EC2 + Streamlit Cloud
- **Azure**: App Service
- **GCP**: Cloud Run
- **Heroku**: Streamlit Community Cloud

## Performance Metrics

| Metric | Value |
|--------|-------|
| **Models Trained** | 9 |
| **Datasets** | 3 |
| **Total Samples** | 23,000 |
| **Features per Model** | 10-15 |
| **Training Time** | 30-60 seconds |
| **Dashboard Load** | 2-5 seconds (cached) |
| **Database Records** | ~50,000 (predictions + checks) |

## Common Use Cases

### Use Case 1: Loan Risk Assessment
- Monitor loan default model performance
- Detect bias in lending decisions
- Ensure fair treatment across demographics
- Comply with fair lending regulations

### Use Case 2: Customer Retention
- Track churn prediction accuracy
- Identify service quality issues
- Monitor demographic disparities
- Target retention efforts fairly

### Use Case 3: HR Analytics
- Monitor attrition prediction
- Detect discriminatory hiring patterns
- Ensure equitable treatment
- Support talent retention strategy

## Troubleshooting

| Issue | Solution |
|-------|----------|
| **Models not found** | Run `python train_models.py` first |
| **Dashboard won't start** | Check dependencies: `pip install -r requirements.txt` |
| **Slow performance** | Dashboard caches on first load; wait 1-2 min |
| **Database error** | Delete `logs/governance.db` and retrain |

## Support Resources

1. **[QUICKSTART.md](QUICKSTART.md)** - Get running in 5 minutes
2. **[README.md](README.md)** - Comprehensive documentation
3. **Source code docstrings** - Detailed function documentation
4. **Inline comments** - Code explanations throughout

## Future Enhancements

- [ ] Real-time prediction streaming
- [ ] Watson OpenScale integration
- [ ] Watsonx.ai hosting
- [ ] Advanced SHAP visualizations
- [ ] Multi-user RBAC
- [ ] REST API
- [ ] Model A/B testing
- [ ] Automated retraining
- [ ] Custom fairness constraints
- [ ] Bias mitigation techniques

## Key Achievements

**3 realistic enterprise datasets** with 23,000 total samples  
**9 trained models** (3 datasets × 3 algorithms)  
**Comprehensive fairness analysis** with disparate impact detection  
**Statistical drift monitoring** with KS tests and PSI  
✅ **Model explainability** with feature importance and SHAP  
✅ **Enterprise governance** with complete audit trail  
✅ **Interactive dashboard** with 6 analysis pages  
✅ **Production-ready code** with error handling and logging  

## Next Steps

1. **[Get Started](QUICKSTART.md)** - Run in 5 minutes
2. **Explore Dashboard** - Understand all features
3. **Customize** - Add your own datasets
4. **Deploy** - Move to production
5. **Monitor** - Track models over time

---

**Project Status**: ✅ Complete and Production-Ready  
**Last Updated**: 2026-01-13  
**Version**: 1.0.0

For detailed information, see [README.md](README.md) or [QUICKSTART.md](QUICKSTART.md)
