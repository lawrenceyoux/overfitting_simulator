"""
Lambda Function: Select Best Strategy
Identifies the top performing strategy from backtest results
"""

import json
import boto3
import pandas as pd
from io import StringIO
from datetime import datetime

# AWS clients
s3 = boto3.client('s3')

def lambda_handler(event, context):
    """
    Lambda handler for selecting best strategy
    
    Input event:
    {
        "bucket": "overfitting-demo-data",
        "results_key": "results/training_performance.csv",
        "strategies_key": "strategies/strategies_latest.json"
    }
    
    Output:
    {
        "statusCode": 200,
        "best_strategy_key": "results/best_strategy.json",
        "best_strategy_id": 42,
        "win_rate": 0.85
    }
    """
    
    try:
        # Get parameters
        bucket = event.get('bucket', 'overfitting-demo-data')
        results_key = event.get('results_key', 'results/training_performance.csv')
        strategies_key = event.get('strategies_key', 'strategies/strategies_latest.json')
        
        print(f"Loading backtest results from s3://{bucket}/{results_key}")
        
        # Load backtest results
        results_obj = s3.get_object(Bucket=bucket, Key=results_key)
        results_df = pd.read_csv(StringIO(results_obj['Body'].read().decode('utf-8')))
        
        # Load strategies
        strategies_obj = s3.get_object(Bucket=bucket, Key=strategies_key)
        strategies_data = json.loads(strategies_obj['Body'].read())
        
        print(f"Analyzing {len(results_df)} strategies to find best performer")
        
        # Find best strategy (highest win rate)
        best_idx = results_df['win_rate'].idxmax()
        best_result = results_df.iloc[best_idx]
        best_strategy_id = int(best_result['strategy_id'])
        
        # Get full strategy details
        best_strategy_full = next(s for s in strategies_data if s['id'] == best_strategy_id)
        
        # Create best strategy record
        best_strategy = {
            'id': best_strategy_id,
            'signals': best_strategy_full['signals'],
            'training_performance': {
                'win_rate': float(best_result['win_rate']),
                'total_return': float(best_result['total_return']),
                'sharpe_ratio': float(best_result['sharpe_ratio']),
                'max_drawdown': float(best_result['max_drawdown']),
                'num_trades': int(best_result['num_trades'])
            },
            'selected_at': datetime.utcnow().isoformat()
        }
        
        # Save to S3
        best_strategy_key = "results/best_strategy.json"
        s3.put_object(
            Bucket=bucket,
            Key=best_strategy_key,
            Body=json.dumps(best_strategy, indent=2),
            ContentType='application/json'
        )
        
        print(f"Best strategy: ID {best_strategy_id} with {best_result['win_rate']:.2%} win rate")
        
        return {
            'statusCode': 200,
            'bucket': bucket,
            'best_strategy_key': best_strategy_key,
            'best_strategy_id': best_strategy_id,
            'win_rate': float(best_result['win_rate']),
            'sharpe_ratio': float(best_result['sharpe_ratio'])
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            'statusCode': 500,
            'error': str(e)
        }
