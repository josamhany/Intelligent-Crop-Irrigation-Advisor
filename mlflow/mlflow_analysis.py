#!/usr/bin/env python3
"""
MLflow Model Comparison and Analysis
====================================
This script provides utilities to compare and analyze models tracked in MLflow.
"""

import mlflow
import pandas as pd
from pathlib import Path
from mlflow_config import MLFLOW_TRACKING_URI, EXPERIMENTS

# Set tracking URI
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

def get_all_runs(experiment_name):
    """Get all runs for a specific experiment."""
    full_experiment_name = EXPERIMENTS.get(experiment_name, experiment_name)
    experiment = mlflow.get_experiment_by_name(full_experiment_name)
    
    if experiment is None:
        print(f"❌ Experiment '{full_experiment_name}' not found!")
        return None
    
    runs = mlflow.search_runs(
        experiment_ids=[experiment.experiment_id],
        order_by=["start_time DESC"]
    )
    
    return runs

def compare_experiments():
    """Compare all experiments in the project."""
    print("=" * 80)
    print("  MLflow Experiments Comparison")
    print("=" * 80)
    print()
    
    all_results = []
    
    for exp_key, exp_name in EXPERIMENTS.items():
        print(f"\n📊 {exp_name}")
        print("-" * 80)
        
        runs = get_all_runs(exp_key)
        
        if runs is None or len(runs) == 0:
            print("   No runs found")
            continue
        
        # Get best run
        if 'metrics.accuracy' in runs.columns:
            metric_col = 'metrics.accuracy'
        elif 'metrics.r2_score' in runs.columns:
            metric_col = 'metrics.r2_score'
        else:
            print("   No accuracy/r2_score metric found")
            continue
        
        best_run = runs.loc[runs[metric_col].idxmax()]
        
        print(f"   Total Runs: {len(runs)}")
        print(f"   Best Metric ({metric_col}): {best_run[metric_col]:.4f}")
        print(f"   Best Run ID: {best_run['run_id']}")
        print(f"   Start Time: {best_run['start_time']}")
        
        all_results.append({
            'Experiment': exp_name,
            'Total Runs': len(runs),
            'Best Metric': best_run[metric_col],
            'Metric Type': metric_col.split('.')[-1],
            'Best Run ID': best_run['run_id']
        })
    
    if all_results:
        print("\n" + "=" * 80)
        print("  Summary")
        print("=" * 80)
        df = pd.DataFrame(all_results)
        print(df.to_string(index=False))
    
    print()

def show_best_models():
    """Show best models for each experiment."""
    print("=" * 80)
    print("  Best Models per Experiment")
    print("=" * 80)
    print()
    
    for exp_key, exp_name in EXPERIMENTS.items():
        print(f"\n🏆 {exp_name}")
        print("-" * 80)
        
        runs = get_all_runs(exp_key)
        
        if runs is None or len(runs) == 0:
            print("   No runs found")
            continue
        
        # Determine metric column
        if 'metrics.accuracy' in runs.columns:
            metric_col = 'metrics.accuracy'
        elif 'metrics.r2_score' in runs.columns:
            metric_col = 'metrics.r2_score'
        else:
            continue
        
        # Get top 5 runs
        top_runs = runs.nlargest(5, metric_col)
        
        print(f"\n   Top 5 Runs (by {metric_col}):\n")
        
        for idx, (_, run) in enumerate(top_runs.iterrows(), 1):
            print(f"   {idx}. Score: {run[metric_col]:.4f}")
            print(f"      Run ID: {run['run_id']}")
            print(f"      Date: {run['start_time']}")
            
            # Show key parameters if available
            param_cols = [col for col in run.index if col.startswith('params.')]
            if param_cols:
                print(f"      Key Params:")
                for pcol in param_cols[:5]:  # Show first 5 params
                    param_name = pcol.replace('params.', '')
                    print(f"        - {param_name}: {run[pcol]}")
            print()

def export_results_to_csv():
    """Export all experiment results to CSV files."""
    output_dir = Path("mlflow_exports")
    output_dir.mkdir(exist_ok=True)
    
    print(f"📁 Exporting results to: {output_dir}")
    print()
    
    for exp_key, exp_name in EXPERIMENTS.items():
        runs = get_all_runs(exp_key)
        
        if runs is None or len(runs) == 0:
            print(f"   ⚠️  {exp_name}: No runs found")
            continue
        
        filename = output_dir / f"{exp_key}_runs.csv"
        runs.to_csv(filename, index=False)
        print(f"   ✅ {exp_name}: {len(runs)} runs exported to {filename}")
    
    print()

def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Compare and analyze MLflow experiments")
    parser.add_argument(
        "--action",
        choices=["compare", "best", "export", "all"],
        default="all",
        help="Action to perform"
    )
    
    args = parser.parse_args()
    
    if args.action == "compare" or args.action == "all":
        compare_experiments()
    
    if args.action == "best" or args.action == "all":
        show_best_models()
    
    if args.action == "export" or args.action == "all":
        export_results_to_csv()

if __name__ == "__main__":
    main()
