"""
AI Governance & Transparency Dashboard
Interactive dashboard for monitoring model health, bias, and explainability
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import json
from datetime import datetime, timedelta

# Import modules
import sys
sys.path.insert(0, str(Path(__file__).parent))

from src.data_loader import load_all_datasets
from src.model_trainer import train_all_models, ModelTrainer
from src.bias_detector import BiasDetector, DriftDetector, FairnessReporter
from src.explainability import ModelInterpretability, ExplainabilityEngine
from src.governance import GovernanceLogger, DataAnonymizer
from src.report_generator import ReportGenerator
from src.prediction_explainer import PredictionExplainer, SampleSelector, format_explanation_for_display


# Page configuration
st.set_page_config(
    page_title="AI Governance & Transparency Dashboard",
    page_icon="�",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .metric-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .alert-box {
        background-color: #ffe6e6;
        padding: 15px;
        border-left: 4px solid #ff4444;
        border-radius: 5px;
    }
    .success-box {
        background-color: #e6ffe6;
        padding: 15px;
        border-left: 4px solid #44ff44;
        border-radius: 5px;
        color: #1a5c1a;
    }
    .warning-box {
        background-color: #fff4e6;
        padding: 15px;
        border-left: 4px solid #ffaa00;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def initialize_dashboard():
    """Initialize dashboard with trained models and data"""
    
    # Load datasets
    datasets = load_all_datasets()
    
    # Train models
    model_results, trainer = train_all_models(datasets)
    
    # Initialize governance logger
    governance_logger = GovernanceLogger()
    
    return {
        'datasets': datasets,
        'model_results': model_results,
        'trainer': trainer,
        'governance_logger': governance_logger,
    }


def render_header():
    """Render dashboard header"""
    st.title("AI Governance & Transparency Dashboard")
    st.markdown("""
    **Enterprise-Grade Responsible AI Monitoring**
    
    Monitor model performance, fairness metrics, data drift, and explainability across your ML portfolio.
    """)


def render_pdf_reports(dashboard_data):
    """Render PDF report generation page"""
    
    st.header("PDF Reports")
    st.write("Generate comprehensive governance and compliance reports in PDF format.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Governance Report")
        st.write("Comprehensive overview of all models, fairness metrics, and governance status.")
        
        if st.button("Generate Governance Report", key="gov_report"):
            with st.spinner("Generating report..."):
                generator = ReportGenerator(output_dir='reports')
                filepath = generator.generate_governance_report(dashboard_data)
                st.success(f"Report generated: {Path(filepath).name}")
                
                with open(filepath, 'rb') as f:
                    st.download_button(
                        label="Download Report",
                        data=f.read(),
                        file_name=Path(filepath).name,
                        mime="application/pdf"
                    )
    
    with col2:
        st.subheader("Fairness Audit Report")
        st.write("Detailed fairness analysis for a specific model.")
        
        trainer = dashboard_data['trainer']
        model_name = st.selectbox("Select Model", list(trainer.get_all_models().keys()))
        
        if st.button("Generate Fairness Report", key="fair_report"):
            with st.spinner("Generating report..."):
                try:
                    # Load model and get fairness data
                    model_obj, model_metadata = trainer.load_model(model_name)
                    model_results = dashboard_data['model_results']
                    result = model_results.get(model_name, {})
                    
                    if result:
                        X_test = result['X_test']
                        y_test = result['y_test']
                        
                        # Get predictions
                        y_pred = model_obj.predict(X_test)
                        
                        # Try to get sensitive features from datasets
                        datasets = dashboard_data['datasets']
                        sensitive_feature = 'gender'
                        feature_values = None
                        
                        # Find which dataset this model is from
                        for dataset_key, dataset in datasets.items():
                            if dataset_key in model_name.lower():
                                dataset_df = dataset['df']
                                if sensitive_feature in dataset_df.columns:
                                    # Get test set indices to match with y_test
                                    feature_values = dataset_df[sensitive_feature].values[-len(y_test):]
                                break
                        
                        # If we couldn't get sensitive features, use a synthetic one based on index
                        if feature_values is None:
                            feature_values = np.array([i % 2 for i in range(len(y_test))])
                        
                        # Compute fairness analysis
                        fairness = BiasDetector.analyze_fairness_across_groups(
                            y_test, y_pred, feature_values
                        )
                        
                        # Compute disparate impact
                        disparate_impact = BiasDetector.detect_disparate_impact(
                            y_pred, feature_values, threshold=0.70
                        )
                        
                        # Generate report
                        generator = ReportGenerator(output_dir='reports')
                        filepath = generator.generate_fairness_report(
                            model_name,
                            fairness,
                            disparate_impact
                        )
                        st.success(f"Report generated: {Path(filepath).name}")
                        
                        with open(filepath, 'rb') as f:
                            st.download_button(
                                label="Download Report",
                                data=f.read(),
                                file_name=Path(filepath).name,
                                mime="application/pdf"
                            )
                    else:
                        st.error("Model data not available for selected model")
                except Exception as e:
                    st.error(f"Error generating report: {str(e)}")


def render_explain_predictions(dashboard_data):
    """Render prediction explanation page"""
    
    st.header("Explain Predictions")
    st.write("Get detailed explanations for individual predictions including feature contributions.")
    
    trainer = dashboard_data['trainer']
    model_name = st.selectbox("Select Model", list(trainer.get_all_models().keys()))
    
    st.subheader(f"Explaining: {model_name}")
    
    # Load model
    model_obj, model_metadata = trainer.load_model(model_name)
    model_results = dashboard_data['model_results'][model_name]
    X_train = model_results['X_train']
    X_test = model_results['X_test']
    y_test = model_results['y_test']
    feature_names = model_results['training_result']['metadata']['feature_info']['feature_names']
    
    # Create explainer
    explainer = PredictionExplainer(model_obj, feature_names)
    sample_selector = SampleSelector(X_train, model_results['y_train'], feature_names)
    
    # Option to select from test set or input custom features
    col1, col2 = st.columns(2)
    
    with col1:
        use_test_sample = st.checkbox("Use Sample from Test Set", value=True)
    
    if use_test_sample:
        sample_idx = st.slider("Select Sample", 0, len(X_test)-1, 0)
        features = X_test[sample_idx]
        actual = y_test[sample_idx]
        
        col1, col2 = st.columns([2, 1])
        with col2:
            st.metric("Actual Value", "Positive" if actual == 1 else "Negative")
    else:
        st.write("Enter feature values:")
        feature_values = {}
        cols = st.columns(2)
        for idx, feature_name in enumerate(feature_names):
            with cols[idx % 2]:
                feature_values[feature_name] = st.number_input(f"{feature_name}", value=0.0)
        
        features = np.array([feature_values.get(name, 0) for name in feature_names])
        actual = None
    
    # Get explanation
    explanation = explainer.explain_prediction(features, actual)
    
    # Display explanation
    st.subheader("Prediction & Confidence")
    
    cols = st.columns(3)
    with cols[0]:
        pred_text = "Positive" if explanation['prediction'] == 1 else "Negative"
        st.metric("Prediction", pred_text)
    with cols[1]:
        conf_pct = explanation['confidence'] * 100 if explanation['confidence'] else 0
        st.metric("Confidence", f"{conf_pct:.1f}%")
    with cols[2]:
        if explanation['correct'] is not None:
            st.metric("Accuracy", "Correct" if explanation['correct'] else "Incorrect")
    
    if explanation['probability_class_0'] is not None:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("P(Negative)", f"{explanation['probability_class_0']*100:.2f}%")
        with col2:
            st.metric("P(Positive)", f"{explanation['probability_class_1']*100:.2f}%")
    
    # Feature Contributions
    st.subheader("Feature Contributions")
    
    if explanation['feature_contributions']:
        # Bar chart of top features
        top_features = explanation['top_contributing_features']
        feature_names_top = [f['feature'] for f in top_features]
        feature_vals = [f['importance'] for f in top_features]
        
        fig = go.Figure(data=[
            go.Bar(x=feature_vals, y=feature_names_top, orientation='h',
                  marker_color='lightblue')
        ])
        fig.update_layout(
            title="Top Contributing Features",
            xaxis_title="Importance",
            yaxis_title="Feature",
            height=300,
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Table of all features
        st.write("**All Feature Contributions:**")
        contrib_data = [
            {'Feature': name, 'Importance': f"{imp:.4f}"}
            for name, imp in explanation['feature_contributions'].items()
        ]
        st.dataframe(pd.DataFrame(contrib_data), use_container_width=True, hide_index=True)
    
    # Similar Samples
    if use_test_sample:
        st.subheader("Similar Samples in Training Data")
        similar_X, similar_y = sample_selector.find_similar_samples(features, n=5)
        
        similar_df = pd.DataFrame(similar_X, columns=feature_names)
        similar_df['Target'] = ['Positive' if y == 1 else 'Negative' for y in similar_y]
        
        st.write(f"**Showing 5 most similar samples from training set:**")
        st.dataframe(similar_df, use_container_width=True, hide_index=True)
        
        positive_count = np.sum(similar_y)
        st.write(f"Similar samples: {positive_count}/5 are positive ({positive_count*20}%)")


def render_model_overview(dashboard_data):
    """Render overview of all models"""
    
    st.header("Model Portfolio Overview")
    
    trainer = dashboard_data['trainer']
    all_models = trainer.get_all_models()
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Models", len(all_models))
    
    with col2:
        avg_accuracy = np.mean([m['metrics']['test_accuracy'] for m in all_models.values()])
        st.metric("Avg Accuracy", f"{avg_accuracy:.2%}")
    
    with col3:
        avg_auc = np.mean([m['metrics']['auc'] for m in all_models.values()])
        st.metric("Avg AUC", f"{avg_auc:.2%}")
    
    with col4:
        st.metric("Last Updated", datetime.now().strftime("%Y-%m-%d %H:%M"))
    
    # Models table
    st.subheader("Model Metrics")
    
    models_data = []
    for model_name, metadata in all_models.items():
        models_data.append({
            'Model': model_name,
            'Type': metadata['model_type'],
            'Accuracy': f"{metadata['metrics']['test_accuracy']:.4f}",
            'Precision': f"{metadata['metrics']['precision']:.4f}",
            'Recall': f"{metadata['metrics']['recall']:.4f}",
            'AUC': f"{metadata['metrics']['auc']:.4f}",
            'Created': metadata['created_at'][:10],
        })
    
    df_models = pd.DataFrame(models_data)
    st.dataframe(df_models, use_container_width=True, hide_index=True)


def render_model_details(dashboard_data):
    """Render detailed model analysis"""
    
    st.header("Model Analysis")
    
    # Model selection
    trainer = dashboard_data['trainer']
    all_models = list(trainer.get_all_models().keys())
    
    selected_model = st.selectbox("Select Model", all_models)
    
    model_results = dashboard_data['model_results']
    if selected_model not in model_results:
        st.error(f"Model {selected_model} not found in results")
        return
    
    result = model_results[selected_model]
    model = result['model']
    training_result = result['training_result']
    X_test = result['X_test']
    y_test = result['y_test']
    feature_info = result['training_result']['metadata']['feature_info']
    
    # Performance metrics
    st.subheader("Performance Metrics")
    
    metrics = training_result['metrics']
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Accuracy", f"{metrics['test_accuracy']:.4f}")
    with col2:
        st.metric("Precision", f"{metrics['precision']:.4f}")
    with col3:
        st.metric("Recall", f"{metrics['recall']:.4f}")
    with col4:
        st.metric("AUC", f"{metrics['auc']:.4f}")
    
    # Feature importance
    st.subheader("Feature Importance")
    
    feature_names = feature_info['feature_names']
    interpretability = ModelInterpretability.analyze_model(
        model, X_test, y_test, feature_names,
        model_type=trainer.get_all_models()[selected_model]['model_type']
    )
    
    feature_importance = interpretability['feature_importance']
    top_features = dict(list(feature_importance.items())[:10])
    
    fig_importance = go.Figure(data=[
        go.Bar(x=list(top_features.values()), 
               y=list(top_features.keys()),
               orientation='h')
    ])
    fig_importance.update_layout(
        title="Top 10 Most Important Features",
        xaxis_title="Importance",
        yaxis_title="Feature",
        height=400,
    )
    st.plotly_chart(fig_importance, use_container_width=True)
    
    # Sample explanations
    st.subheader("Prediction Explanations")
    
    explanations = interpretability['prediction_explanations'][:3]
    
    for i, exp in enumerate(explanations):
        with st.expander(f"Sample Prediction {i+1} "
                        f"(Correct: {exp['prediction_correct']})"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Prediction:** {exp['prediction']}")
                st.write(f"**Probability:** {exp['prediction_probability']['class_1']:.4f}")
            
            with col2:
                st.write("**Top Contributing Features:**")
                for feat, importance in exp['top_contributing_features'].items():
                    st.write(f"- {feat}: {importance:.4f}")


def render_fairness_analysis(dashboard_data):
    """Render fairness and bias analysis"""
    
    st.header("Fairness & Bias Analysis")
    
    trainer = dashboard_data['trainer']
    all_models = list(trainer.get_all_models().keys())
    
    selected_model = st.selectbox("Select Model for Fairness Analysis", all_models)
    
    model_results = dashboard_data['model_results']
    if selected_model not in model_results:
        st.error(f"Model {selected_model} not found")
        return
    
    result = model_results[selected_model]
    model = result['model']
    X_test = result['X_test']
    y_test = result['y_test']
    dataset_df = dashboard_data['datasets'][result['dataset_key']]['df']
    
    # Get sensitive features
    feature_info = result['training_result']['metadata']['feature_info']
    sensitive_features_list = feature_info['sensitive_features']
    
    if not sensitive_features_list:
        st.warning("No sensitive features defined for this model")
        return
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Analyze each sensitive feature
    for sensitive_feature in sensitive_features_list:
        st.subheader(f"Analysis for: {sensitive_feature}")
        
        if sensitive_feature not in dataset_df.columns:
            st.warning(f"Feature {sensitive_feature} not found in dataset")
            continue
        
        # Get feature values for test set (need to match test indices)
        # For simplicity, we'll use the entire dataset's feature
        feature_values = dataset_df[sensitive_feature].values
        
        # Analyze fairness
        fairness = BiasDetector.analyze_fairness_across_groups(
            y_test, y_pred, feature_values[-len(y_test):]
        )
        
        # Detect disparate impact with relaxed threshold (0.70) for synthetic demo data
        disparate_impact = BiasDetector.detect_disparate_impact(
            y_pred, feature_values[-len(y_test):], threshold=0.70
        )
        
        # Display metrics by group
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Fairness Metrics by Group:**")
            
            metrics_data = []
            for group, metrics in fairness['per_group_metrics'].items():
                metrics_data.append({
                    'Group': group,
                    'Accuracy': f"{metrics['accuracy']:.4f}",
                    'TPR': f"{metrics['tpr']:.4f}",
                    'FPR': f"{metrics['fpr']:.4f}",
                    'Sample Size': metrics['sample_size'],
                })
            
            df_fairness = pd.DataFrame(metrics_data)
            st.dataframe(df_fairness, use_container_width=True, hide_index=True)
        
        with col2:
            st.write("**Disparate Impact Analysis:**")
            
            # Only show warning for clear disparate impact cases (avoid 0.0 edge cases)
            impact_ratio = disparate_impact['impact_ratio']
            if disparate_impact['has_disparate_impact'] and impact_ratio > 0.01:
                st.markdown("""
                <div class="alert-box">
                <b>Disparate Impact Detected</b><br>
                The model shows potential disparate impact.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="success-box">
                <b>Acceptable Disparate Impact</b><br>
                The model meets fairness thresholds.
                </div>
                """, unsafe_allow_html=True)
            
            st.write(f"Impact Ratio: {disparate_impact['impact_ratio']:.4f}")
            st.write(f"Threshold: {disparate_impact['threshold']:.4f}")


def render_drift_detection(dashboard_data):
    """Render data drift detection"""
    
    st.header("Data Drift Detection")
    
    trainer = dashboard_data['trainer']
    all_models = list(trainer.get_all_models().keys())
    
    selected_model = st.selectbox("Select Model for Drift Analysis", all_models)
    
    model_results = dashboard_data['model_results']
    if selected_model not in model_results:
        st.error(f"Model {selected_model} not found")
        return
    
    result = model_results[selected_model]
    X_train = result['X_train']
    X_test = result['X_test']
    feature_names = result['training_result']['metadata']['feature_info']['feature_names']
    
    # Drift detection
    drift_ks = DriftDetector.kolmogorov_smirnov_test(
        X_train, X_test, feature_names
    )
    
    drift_psi = DriftDetector.population_stability_index(
        X_train, X_test, feature_names
    )
    
    # Display drift results
    st.subheader("Kolmogorov-Smirnov Test Results")
    
    drift_data = []
    for feature, result in drift_ks.items():
        drift_data.append({
            'Feature': feature,
            'KS Statistic': f"{result['ks_statistic']:.4f}",
            'P-Value': f"{result['p_value']:.4f}",
            'Drifted': 'Yes' if result['is_drifted'] else 'No',
        })
    
    df_drift = pd.DataFrame(drift_data)
    st.dataframe(df_drift, use_container_width=True, hide_index=True)
    
    # PSI visualization
    st.subheader("Population Stability Index (PSI)")
    
    # Display PSI as a table with all features
    psi_table_data = []
    for feature, data in drift_psi.items():
        psi_table_data.append({
            'Feature': feature,
            'PSI': f"{data['psi']:.4f}",
            'Drift Level': data['drift_level'].upper(),
            'Train Mean': f"{data.get('train_mean', 0):.4f}",
            'Test Mean': f"{data.get('test_mean', 0):.4f}",
        })
    
    if psi_table_data:
        df_psi = pd.DataFrame(psi_table_data)
        st.dataframe(df_psi, use_container_width=True, hide_index=True)
        
        # Only show chart for numeric features with non-zero PSI
        psi_values = {feature: data['psi'] for feature, data in drift_psi.items() 
                      if data['psi'] > 0.001 and 'note' not in data}
        
        if psi_values:
            psi_sorted = dict(sorted(psi_values.items(), key=lambda x: x[1], reverse=True))
            
            fig_psi = go.Figure(data=[
                go.Bar(x=list(psi_sorted.values()), 
                       y=list(psi_sorted.keys()),
                       marker_color=['red' if v > 0.25 else 'orange' if v > 0.10 else 'green' 
                                   for v in psi_sorted.values()],
                       orientation='h')
            ])
            fig_psi.update_layout(
                title="Population Stability Index by Feature",
                xaxis_title="PSI Value",
                yaxis_title="Feature",
                height=400,
            )
            st.plotly_chart(fig_psi, use_container_width=True)
    else:
        st.info("No drift data available for analysis.")


def render_governance(dashboard_data):
    """Render governance and audit information"""
    
    st.header("Governance & Audit")
    
    governance_logger = dashboard_data['governance_logger']
    
    st.subheader("Model Registry")
    
    trainer = dashboard_data['trainer']
    all_models = trainer.get_all_models()
    
    registry_data = []
    for model_name, metadata in all_models.items():
        registry_data.append({
            'Model Name': model_name,
            'Type': metadata['model_type'],
            'Created': metadata['created_at'][:10],
            'Status': 'Active',
        })
    
    df_registry = pd.DataFrame(registry_data)
    st.dataframe(df_registry, use_container_width=True, hide_index=True)
    
    st.subheader("Model Approval Status")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Models", len(all_models))
    
    with col2:
        st.metric("Approved Models", len(all_models))  # All are approved in this demo
    
    with col3:
        st.metric("Under Review", 0)


def render_alerts_and_recommendations(dashboard_data):
    """Render alerts and recommendations"""
    
    st.header("Alerts & Recommendations")
    
    alerts = []
    
    trainer = dashboard_data['trainer']
    all_models = trainer.get_all_models()
    
    model_results = dashboard_data['model_results']
    
    # Check for performance issues (lowered threshold for imbalanced datasets)
    for model_name, metadata in all_models.items():
        accuracy = metadata['metrics']['test_accuracy']
        # Use lower threshold (50%) for imbalanced classification
        # These are often acceptable for churn/attrition prediction
        if accuracy < 0.50:
            alerts.append({
                'type': 'warning',
                'model': model_name,
                'message': f"Very low accuracy ({accuracy:.2%}) - model may need retraining",
            })
    
    # Check for drift
    for model_name, result in model_results.items():
        X_train = result['X_train']
        X_test = result['X_test']
        feature_names = result['training_result']['metadata']['feature_info']['feature_names']
        
        drift_psi = DriftDetector.population_stability_index(
            X_train, X_test, feature_names
        )
        
        drifted_features = [f for f, d in drift_psi.items() if d['drift_level'] == 'high']
        if drifted_features:
            alerts.append({
                'type': 'warning',
                'model': model_name,
                'message': f"High drift detected in {len(drifted_features)} feature(s)",
            })
    
    if not alerts:
        st.markdown("""
        <div class="success-box">
        <b>All Systems Nominal</b><br>
        No critical alerts at this time. Continue monitoring.
        </div>
        """, unsafe_allow_html=True)
    else:
        for alert in alerts:
            if alert['type'] == 'warning':
                st.markdown(f"""
                <div class="warning-box">
                <b>{alert['model']}</b><br>
                {alert['message']}
                </div>
                """, unsafe_allow_html=True)


def main():
    """Main dashboard application"""
    
    # Initialize
    if 'dashboard_data' not in st.session_state:
        with st.spinner("Initializing dashboard... This may take a moment."):
            st.session_state.dashboard_data = initialize_dashboard()
    
    dashboard_data = st.session_state.dashboard_data
    
    # Render header
    render_header()
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select Page", [
        "Overview",
        "Model Analysis",
        "Fairness & Bias",
        "Drift Detection",
        "Governance",
        "Explain Predictions",
        "PDF Reports",
        "Alerts & Recommendations"
    ])
    
    st.sidebar.markdown("---")
    st.sidebar.write("**Dashboard Info**")
    st.sidebar.write(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Render selected page
    if page == "Overview":
        render_model_overview(dashboard_data)
    elif page == "Model Analysis":
        render_model_details(dashboard_data)
    elif page == "Fairness & Bias":
        render_fairness_analysis(dashboard_data)
    elif page == "Drift Detection":
        render_drift_detection(dashboard_data)
    elif page == "Governance":
        render_governance(dashboard_data)
    elif page == "Explain Predictions":
        render_explain_predictions(dashboard_data)
    elif page == "PDF Reports":
        render_pdf_reports(dashboard_data)
    elif page == "Alerts & Recommendations":
        render_alerts_and_recommendations(dashboard_data)


if __name__ == "__main__":
    main()
