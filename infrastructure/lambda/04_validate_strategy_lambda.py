"""
Lambda Function: Validate Best Strategy
Tests the best strategy on unseen validation data to expose overfitting
"""

import json
import boto3
import pandas as pd
import numpy as np
from io import StringIO
from datetime import datetime

# AWS clients
s3 = boto3.client('s3')

def calculate_strategy_metrics(signals, prices):
    """Calculate performance metrics for a trading strategy"""
    if len(signals) != len(prices):
        min_len = min(len(signals), len(prices))
        signals = signals[:min_len]
        prices = prices[:min_len]
    
    trades = []
    returns = []
    
    for i in range(len(signals) - 1):
        if signals[i] == 1:
            entry_price = prices[i]
            exit_price = prices[i + 1]
            trade_return = (exit_price - entry_price) / entry_price
            returns.append(trade_return)
            trades.append(1 if trade_return > 0 else 0)
    
    if len(trades) == 0:
        return {
            'win_rate': 0.0,
            'total_return': 0.0,
            'sharpe_ratio': 0.0,
            'max_drawdown': 0.0,
            'num_trades': 0
        }
    
    win_rate = sum(trades) / len(trades)
    total_return = sum(returns)
    
    if len(returns) > 1 and np.std(returns) > 0:
        sharpe_ratio = (np.mean(returns) / np.std(returns)) * np.sqrt(252)
    else:
        sharpe_ratio = 0.0
    
    cumulative = np.cumprod([1 + r for r in returns])
    running_max = np.maximum.accumulate(cumulative)
    drawdown = (cumulative - running_max) / running_max
    max_drawdown = abs(np.min(drawdown)) if len(drawdown) > 0 else 0.0
    
    return {
        'win_rate': win_rate,
        'total_return': total_return,
        'sharpe_ratio': sharpe_ratio,
        'max_drawdown': max_drawdown,
        'num_trades': len(trades)
    }

def lambda_handler(event, context):
    """
    Lambda handler for strategy validation
    
    Input event:
    {
        "bucket": "overfitting-demo-data",
        "best_strategy_key": "results/best_strategy.json",
        "price_data_key": "raw/btc_price_data.csv"
    }
    
    Output:
    {
        "statusCode": 200,
        "validation_key": "results/validation_results.json",
        "validation_win_rate": 0.45,
        "training_win_rate": 0.85,
        "performance_drop": 0.40
    }
    """
    
    try:
        # Get parameters
        bucket = event.get('bucket', 'overfitting-demo-data')
        best_strategy_key = event.get('best_strategy_key', 'results/best_strategy.json')
        price_data_key = event.get('price_data_key', 'raw/btc_price_data.csv')
        
        print(f"Loading best strategy from s3://{bucket}/{best_strategy_key}")
        
        # Load best strategy
        strategy_obj = s3.get_object(Bucket=bucket, Key=best_strategy_key)
        best_strategy = json.loads(strategy_obj['Body'].read())
        
        print(f"Loading price data from s3://{bucket}/{price_data_key}")
        
        # Load price data
        price_obj = s3.get_object(Bucket=bucket, Key=price_data_key)
        price_data = pd.read_csv(StringIO(price_obj['Body'].read().decode('utf-8')))
        
        # Use 30% validation split (last 30%)
        train_size = int(len(price_data) * 0.7)
        validation_data = price_data.iloc[train_size:]
        val_prices = validation_data['price'].values
        
        print(f"Validating strategy {best_strategy['id']} on {len(validation_data)} validation samples")
        
        # Test on validation data
        signals = best_strategy['signals']
        val_metrics = calculate_strategy_metrics(signals, val_prices)
        
        # Compare to training performance
        train_metrics = best_strategy['training_performance']
        performance_drop = train_metrics['win_rate'] - val_metrics['win_rate']
        
        # Create validation results
        validation_results = {
            'strategy_id': best_strategy['id'],
            'training_performance': train_metrics,
            'validation_performance': {
                'win_rate': val_metrics['win_rate'],
                'total_return': val_metrics['total_return'],
                'sharpe_ratio': val_metrics['sharpe_ratio'],
                'max_drawdown': val_metrics['max_drawdown'],
                'num_trades': val_metrics['num_trades']
            },
            'performance_drop': performance_drop,
            'overfitting_detected': performance_drop > 0.15,  # >15% drop indicates overfitting
            'validated_at': datetime.utcnow().isoformat()
        }
        
        # Save validation results
        validation_key = "results/validation_results.json"
        s3.put_object(
            Bucket=bucket,
            Key=validation_key,
            Body=json.dumps(validation_results, indent=2),
            ContentType='application/json'
        )
        
        # Also save summary CSV
        summary_data = {
            'metric': ['win_rate', 'total_return', 'sharpe_ratio', 'max_drawdown', 'num_trades'],
            'training': [
                train_metrics['win_rate'],
                train_metrics['total_return'],
                train_metrics['sharpe_ratio'],
                train_metrics['max_drawdown'],
                train_metrics['num_trades']
            ],
            'validation': [
                val_metrics['win_rate'],
                val_metrics['total_return'],
                val_metrics['sharpe_ratio'],
                val_metrics['max_drawdown'],
                val_metrics['num_trades']
            ]
        }
        summary_df = pd.DataFrame(summary_data)
        csv_buffer = StringIO()
        summary_df.to_csv(csv_buffer, index=False)
        
        summary_key = "results/validation_summary.csv"
        s3.put_object(
            Bucket=bucket,
            Key=summary_key,
            Body=csv_buffer.getvalue(),
            ContentType='text/csv'
        )
        
        print(f"Validation complete: Training {train_metrics['win_rate']:.2%} → Validation {val_metrics['win_rate']:.2%}")
        print(f"Performance drop: {performance_drop:.2%} (Overfitting: {validation_results['overfitting_detected']})")
        
        return {
            'statusCode': 200,
            'bucket': bucket,
            'validation_key': validation_key,
            'summary_key': summary_key,
            'validation_win_rate': float(val_metrics['win_rate']),
            'training_win_rate': float(train_metrics['win_rate']),
            'performance_drop': float(performance_drop),
            'overfitting_detected': validation_results['overfitting_detected']
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            'statusCode': 500,
            'error': str(e)
        }
