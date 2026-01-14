#!/usr/bin/env python
"""
Training script to prepare models for the AI Governance Dashboard
Run this before launching the dashboard
"""

import sys
from pathlib import Path
import json

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from src.data_loader import load_all_datasets
from src.model_trainer import train_all_models
from src.bias_detector import BiasDetector, DriftDetector, FairnessReporter
from src.governance import GovernanceLogger


def main():
    """Train all models and prepare governance database"""
    
    print("="*80)
    print("AI Governance & Transparency Dashboard - Model Training Pipeline")
    print("="*80)
    
    # 1. Load datasets
    print("\n[1/4] Loading datasets...")
    try:
        datasets = load_all_datasets()
        print(f"[OK] Loaded {len(datasets)} datasets:")
        for name, data in datasets.items():
            print(f"  - {name}: {data['X'].shape[0]} samples, {data['X'].shape[1]} features")
    except Exception as e:
        print(f"[ERROR] Error loading datasets: {e}")
        return
    
    # 2. Train models
    print("\n[2/4] Training models...")
    try:
        model_results, trainer = train_all_models(datasets)
        print(f"[OK] Trained {len(model_results)} models")
        
        # Print summary
        all_models = trainer.get_all_models()
        for model_name, metadata in all_models.items():
            print(f"  [OK] {model_name}")
            print(f"    - Accuracy: {metadata['metrics']['test_accuracy']:.4f}")
            print(f"    - Precision: {metadata['metrics']['precision']:.4f}")
            print(f"    - Recall: {metadata['metrics']['recall']:.4f}")
            print(f"    - AUC: {metadata['metrics']['auc']:.4f}")
    
    except Exception as e:
        print(f"[ERROR] Error training models: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # 3. Initialize governance logging
    print("\n[3/4] Initializing governance system...")
    try:
        governance_logger = GovernanceLogger()
        
        # Register all models
        for model_name, metadata in all_models.items():
            governance_logger.register_model(
                model_name,
                metadata['model_type'],
                creator="AI Governance Dashboard",
                description=f"Model trained on {metadata['train_size']} samples"
            )
            
            # Log evaluation
            governance_logger.log_evaluation(
                model_name,
                metadata['metrics']
            )
            
            # Approve model
            governance_logger.approve_model(model_name, "System Administrator")
        
        print(f"[OK] Registered {len(all_models)} models in governance system")
    
    except Exception as e:
        print(f"[ERROR] Error initializing governance: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # 4. Analyze fairness and bias
    print("\n[4/4] Analyzing fairness and bias...")
    try:
        for model_name, result in model_results.items():
            model = result['model']
            X_test = result['X_test']
            y_test = result['y_test']
            feature_info = result['training_result']['metadata']['feature_info']
            
            dataset_key = result['dataset_key']
            dataset_df = datasets[dataset_key]['df']
            
            y_pred = model.predict(X_test)
            
            # Analyze each sensitive feature
            for sensitive_feature in feature_info['sensitive_features']:
                if sensitive_feature in dataset_df.columns:
                    feature_values = dataset_df[sensitive_feature].values[-len(y_test):]
                    
                    fairness = BiasDetector.analyze_fairness_across_groups(
                        y_test, y_pred, feature_values
                    )
                    
                    # Log fairness metrics
                    for group, metrics in fairness['per_group_metrics'].items():
                        governance_logger.log_fairness_check(
                            model_name,
                            sensitive_feature,
                            f"accuracy_{group}",
                            metrics['accuracy'],
                            threshold=0.70
                        )
            
            # Log drift analysis
            drift_psi = DriftDetector.population_stability_index(
                result['X_train'], X_test,
                feature_info['feature_names']
            )
            
            for feature, drift_data in drift_psi.items():
                governance_logger.log_drift_detection(
                    model_name,
                    feature,
                    drift_data['psi'],
                    p_value=0.05,  # placeholder
                    is_drifted=(drift_data['drift_level'] == 'high')
                )
        
        print(f"[OK] Fairness and drift analysis complete")
    
    except Exception as e:
        print(f"[ERROR] Error in fairness analysis: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*80)
    print("[OK] Training pipeline complete!")
    print("="*80)
    print("\nNext steps:")
    print("1. Run: streamlit run app.py")
    print("2. Open browser to http://localhost:8501")
    print("3. Explore model performance, fairness, and drift metrics")
    print("\n" + "="*80)


if __name__ == "__main__":
    main()
