# AI Governance & Transparency Dashboard

A comprehensive Python-based dashboard for monitoring and ensuring responsible AI practices across enterprise machine learning models.
Demo: https://drive.google.com/file/d/1U4yiG-5YooB3flAkSxLsRrdFJvmCkwZe/view?usp=drive_link

## Overview

This dashboard provides enterprise-grade governance, transparency, and monitoring for ML models with a focus on:

- **Model Performance**: Real-time tracking of accuracy, precision, recall, and AUC metrics
- **Fairness & Bias Detection**: Identify disparate impact and bias across sensitive demographic groups
- **Data Drift Detection**: Monitor for feature drift using statistical tests (KS test, PSI)
- **Model Explainability**: Understand predictions using feature importance and SHAP values
- **Governance & Audit**: Complete audit logs, model registry, and approval workflows
- **Responsible AI**: Comprehensive checks for bias, fairness, and transparency

## Features

### 1. **Multiple Enterprise-Scale Models**
- **Loan Default Prediction**: Binary classification model for predicting loan defaults
- **Customer Churn Prediction**: Predict which customers are likely to churn
- **HR Attrition Prediction**: Forecast employee attrition risk

Each model trained on realistic datasets with 5,000-10,000 samples and multiple features.

### 2. **Model Portfolio Management**
- Train and manage multiple models (LogisticRegression, RandomForest, XGBoost)
- Version control and metadata tracking
- Performance benchmarking across model types

### 3. **Fairness & Bias Analysis**
- Per-group performance metrics (TPR, FPR, Accuracy)
- Disparate impact detection using the 4/5 rule (80% rule)
- Intersectional bias analysis across multiple sensitive features
- Automatic fairness recommendations

### 4. **Data Drift Detection**
- Kolmogorov-Smirnov (KS) statistical tests
- Population Stability Index (PSI) calculation
- Feature-level drift monitoring
- Drift severity classification (low/medium/high)

### 5. **Model Explainability**
- Feature importance rankings
- SHAP value support (when available)
- Sample prediction explanations
- Contributing feature visualization

### 6. **Enterprise Governance**
- SQLite-based audit logging
- Model registry with approval workflows
- Comprehensive prediction logging
- Fairness and drift check history
- Role-based governance framework

### 7. **Interactive Dashboard**
- Streamlit-based web interface
- Real-time metrics and visualizations
- Model comparison capabilities
- Alert system for threshold violations
- Governance status tracking

## Project Structure

```
KingHack/
├── app.py                      # Main Streamlit dashboard application
├── train_models.py             # Training pipeline script
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── src/
│   ├── __init__.py
│   ├── data_loader.py         # Dataset loading and preparation
│   ├── model_trainer.py        # Model training and versioning
│   ├── bias_detector.py        # Bias detection and fairness analysis
│   ├── explainability.py       # SHAP and feature importance
│   └── governance.py           # Audit logging and governance
├── data/                       # Generated datasets
│   ├── loan_data.csv
│   ├── churn_data.csv
│   └── hr_attrition_data.csv
├── models/                     # Trained models
│   ├── loan_default_lr_v1.pkl
│   ├── loan_default_rf_v1.pkl
│   ├── loan_default_xgb_v1.pkl
│   └── [other models...]
├── logs/                       # Governance and audit logs
│   └── governance.db           # SQLite database
└── notebooks/                  # Jupyter notebooks (optional)
```

## Installation

### Prerequisites
- Python 3.8+
- pip or conda

### Setup Instructions

1. **Clone or navigate to the project directory**
   ```bash
   cd c:\Hacks\KingHack
   ```

2. **Create a virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # or
   source venv/bin/activate  # Mac/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Train models** (run once to prepare datasets and train all models)
   ```bash
   python train_models.py
   ```
   
   This will:
   - Generate three realistic datasets (loan, churn, HR attrition)
   - Train 9 models (3 datasets × 3 model types)
   - Initialize governance database
   - Log all evaluations and fairness checks

5. **Launch the dashboard**
   ```bash
   streamlit run app.py
   ```
   
   The dashboard will be available at: `http://localhost:8501`

## Usage

### Dashboard Pages

#### 1. **Overview**
- Summary statistics across all models
- Model portfolio table with key metrics
- Quick health check indicators

#### 2. **Model Analysis**
- Select individual models for detailed analysis
- View comprehensive performance metrics
- Explore feature importance rankings
- Review prediction explanations

#### 3. **Fairness & Bias**
- Analyze model behavior across sensitive groups
- View per-group performance metrics
- Check for disparate impact
- Get fairness recommendations

#### 4. **Drift Detection**
- Monitor data distribution shifts
- View KS test results per feature
- Analyze PSI across features
- Identify high-drift features

#### 5. **Governance**
- View model registry
- Check approval status
- Review governance metadata
- Access audit logs

#### 6. **Alerts & Recommendations**
- See critical alerts
- View actionable recommendations
- Monitor threshold violations
- Track system health

## Key Metrics Explained

### Performance Metrics
- **Accuracy**: Percentage of correct predictions
- **Precision**: Of predicted positives, how many are actually positive
- **Recall**: Of actual positives, how many did we find
- **AUC**: Area under the ROC curve (probability the model ranks random positive higher than random negative)

### Fairness Metrics
- **TPR (True Positive Rate)**: Sensitivity - how well the model identifies positive cases per group
- **FPR (False Positive Rate)**: How often the model incorrectly predicts positive per group
- **Disparate Impact Ratio**: Ratio of selection rate between groups (≥0.8 is typically acceptable)
- **Demographic Parity**: Equal positive prediction rates across groups

### Drift Metrics
- **KS Statistic**: Kolmogorov-Smirnov test statistic (0 = no drift, 1 = complete drift)
- **PSI (Population Stability Index)**:
  - < 0.10: Low drift
  - 0.10 - 0.25: Medium drift
  - > 0.25: High drift

## Configuration

### Adjusting Thresholds

Edit the threshold values in the respective modules:

- **Fairness thresholds**: `src/bias_detector.py`
- **Drift thresholds**: `src/drift_detector.py`
- **Governance rules**: `src/governance.py`

### Sensitive Features

Modify the `sensitive_features` list in `src/data_loader.py` to define which features to monitor for bias:

```python
sensitive_features=['gender', 'age', 'income_level']
```

## Advanced Features

### Custom Dataset Support

To add your own datasets:

1. Create a function in `src/data_loader.py`:
```python
def load_or_create_your_dataset(data_dir, size=5000):
    # Load or generate your data
    df = pd.read_csv('your_data.csv')
    return df, "your_dataset_name"
```

2. Add to `load_all_datasets()` function

### Model Customization

To train additional model types:

1. Update `ModelTrainer.train_model()` in `src/model_trainer.py`
2. Add new model type to the selection logic
3. Retrain using `train_models.py`

### Integration with IBM Watson

To integrate with IBM Watson OpenScale (optional):

```python
# In src/governance.py
from ibm_watson_openscale import *

# Configure Watson OpenScale integration
openscale = OpenScale(...)
openscale.integrate_model('model_name')
```

## Best Practices

1. **Regular Model Retraining**: Retrain models weekly/monthly based on drift metrics
2. **Fairness Reviews**: Schedule quarterly fairness audits
3. **Data Quality**: Monitor data quality metrics alongside model metrics
4. **Documentation**: Maintain detailed model documentation and change logs
5. **Approval Workflows**: Route high-risk models through governance approval
6. **Testing**: Validate fairness fixes with A/B testing before deployment

## Troubleshooting

### Models Not Loading
- Ensure `train_models.py` completed successfully
- Check that `models/` directory exists and contains `.pkl` files
- Review console output for errors

### Dashboard Slow
- Reduce sample size in Streamlit caching
- Increase `max_cache_seconds` in `@st.cache_resource` decorators
- Limit number of features in drift analysis

### Governance Database Issues
- Delete `logs/governance.db` to reset database
- Re-run `train_models.py` to reinitialize
- Check SQLite permissions

## Performance Characteristics

- **Dataset Generation**: ~10 seconds
- **Model Training**: ~30-60 seconds (9 models)
- **Dashboard First Load**: ~60 seconds (with caching)
- **Subsequent Loads**: ~2-5 seconds

## Future Enhancements

- [ ] Watson OpenScale integration
- [ ] Watsonx.ai model hosting
- [ ] Real-time prediction monitoring
- [ ] Automated bias mitigation techniques
- [ ] Multi-user access control
- [ ] REST API for predictions
- [ ] Advanced SHAP visualizations
- [ ] Custom fairness constraints
- [ ] Automated retraining pipelines

## Dependencies

Key Python libraries:

| Package | Purpose |
|---------|---------|
| `streamlit` | Interactive dashboard framework |
| `scikit-learn` | ML algorithms and metrics |
| `xgboost` | Gradient boosting models |
| `shap` | Model explainability |
| `fairlearn` | Fairness analysis tools |
| `aif360` | Algorithmic fairness toolkit |
| `pandas` | Data manipulation |
| `numpy` | Numerical computing |
| `plotly` | Interactive visualizations |
| `scipy` | Statistical tests |

## License

This project is provided as-is for educational and enterprise purposes.

## Support

For issues, questions, or suggestions:
1. Check the troubleshooting section
2. Review console output and logs
3. Verify all dependencies are installed
4. Ensure Python 3.8+ compatibility

## Credits

Built with:
- Streamlit for interactive dashboards
- scikit-learn, XGBoost for ML algorithms
- SHAP for explainability
- fairlearn for fairness analysis
- Plotly for visualizations

---

**Last Updated**: 2026-01-13
**Version**: 1.0.0
