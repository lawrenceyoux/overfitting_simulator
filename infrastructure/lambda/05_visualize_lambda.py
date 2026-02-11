"""
Lambda Function: Generate Visualizations
Creates plots showing overfitting and saves to S3
"""

import json
import boto3
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for Lambda
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO, StringIO
from datetime import datetime

# AWS clients
s3 = boto3.client('s3')

# Set style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)

def create_win_rate_histogram(results_df, bucket, output_prefix):
    """Create histogram of win rates showing distribution"""
    plt.figure(figsize=(12, 6))
    
    plt.hist(results_df['win_rate'], bins=30, alpha=0.7, color='steelblue', edgecolor='black')
    plt.axvline(0.5, color='red', linestyle='--', linewidth=2, label='Expected (50% - Random)')
    plt.axvline(results_df['win_rate'].max(), color='green', linestyle='--', linewidth=2, label=f'Best Strategy: {results_df["win_rate"].max():.2%}')
    
    plt.xlabel('Win Rate', fontsize=12)
    plt.ylabel('Number of Strategies', fontsize=12)
    plt.title('Distribution of Win Rates Across All Random Strategies\n(Shows lucky outliers from pure chance)', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    
    # Save to buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
    buffer.seek(0)
    plt.close()
    
    # Upload to S3
    key = f"{output_prefix}/win_rate_histogram.png"
    s3.upload_fileobj(buffer, bucket, key, ExtraArgs={'ContentType': 'image/png'})
    return key

def create_performance_comparison(validation_results, bucket, output_prefix):
    """Create bar chart comparing training vs validation performance"""
    train = validation_results['training_performance']
    val = validation_results['validation_performance']
    
    metrics = ['win_rate', 'total_return', 'sharpe_ratio']
    train_values = [train[m] for m in metrics]
    val_values = [val[m] for m in metrics]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    x = np.arange(len(metrics))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, train_values, width, label='Training', color='green', alpha=0.7)
    bars2 = ax.bar(x + width/2, val_values, width, label='Validation', color='red', alpha=0.7)
    
    ax.set_xlabel('Metrics', fontsize=12)
    ax.set_ylabel('Value', fontsize=12)
    ax.set_title('Overfitting Exposed: Training vs Validation Performance\n(Shows dramatic performance collapse on unseen data)', 
                 fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(['Win Rate', 'Total Return', 'Sharpe Ratio'])
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3, axis='y')
    
    # Save to buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
    buffer.seek(0)
    plt.close()
    
    # Upload to S3
    key = f"{output_prefix}/performance_comparison.png"
    s3.upload_fileobj(buffer, bucket, key, ExtraArgs={'ContentType': 'image/png'})
    return key

def lambda_handler(event, context):
    """
    Lambda handler for generating visualizations
    
    Input event:
    {
        "bucket": "overfitting-demo-data",
        "results_key": "results/training_performance.csv",
        "validation_key": "results/validation_results.json"
    }
    
    Output:
    {
        "statusCode": 200,
        "plots": [
            "plots/win_rate_histogram.png",
            "plots/performance_comparison.png"
        ]
    }
    """
    
    try:
        # Get parameters
        bucket = event.get('bucket', 'overfitting-demo-data')
        results_key = event.get('results_key', 'results/training_performance.csv')
        validation_key = event.get('validation_key', 'results/validation_results.json')
        output_prefix = event.get('output_prefix', 'plots')
        
        print(f"Loading backtest results from s3://{bucket}/{results_key}")
        
        # Load backtest results
        results_obj = s3.get_object(Bucket=bucket, Key=results_key)
        results_df = pd.read_csv(StringIO(results_obj['Body'].read().decode('utf-8')))
        
        print(f"Loading validation results from s3://{bucket}/{validation_key}")
        
        # Load validation results
        val_obj = s3.get_object(Bucket=bucket, Key=validation_key)
        validation_results = json.loads(val_obj['Body'].read())
        
        print("Generating visualizations...")
        
        # Generate plots
        plot_keys = []
        
        # Plot 1: Win rate histogram
        plot1_key = create_win_rate_histogram(results_df, bucket, output_prefix)
        plot_keys.append(plot1_key)
        print(f"Created histogram: s3://{bucket}/{plot1_key}")
        
        # Plot 2: Performance comparison
        plot2_key = create_performance_comparison(validation_results, bucket, output_prefix)
        plot_keys.append(plot2_key)
        print(f"Created comparison chart: s3://{bucket}/{plot2_key}")
        
        print(f"Successfully generated {len(plot_keys)} visualizations")
        
        return {
            'statusCode': 200,
            'bucket': bucket,
            'plots': plot_keys,
            'count': len(plot_keys)
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            'statusCode': 500,
            'error': str(e)
        }
