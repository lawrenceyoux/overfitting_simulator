"""
Lambda Function: Backtest Strategies
Runs backtesting on all strategies using training data
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
    
    # Execute strategy
    for i in range(len(signals) - 1):
        if signals[i] == 1:  # Buy signal
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
    
    # Calculate metrics
    win_rate = sum(trades) / len(trades)
    total_return = sum(returns)
    
    if len(returns) > 1 and np.std(returns) > 0:
        sharpe_ratio = (np.mean(returns) / np.std(returns)) * np.sqrt(252)
    else:
        sharpe_ratio = 0.0
    
    # Max drawdown
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
    Lambda handler for backtesting strategies
    
    Input event:
    {
        "bucket": "overfitting-demo-data",
        "strategies_key": "strategies/strategies_latest.json",
        "price_data_key": "raw/btc_price_data.csv"
    }
    
    Output:
    {
        "statusCode": 200,
        "results_key": "results/training_performance.csv"
    }
    """
    
    try:
        # Get parameters
        bucket = event.get('bucket', 'overfitting-demo-data')
        strategies_key = event.get('strategies_key', 'strategies/strategies_latest.json')
        price_data_key = event.get('price_data_key', 'raw/btc_price_data.csv')
        
        print(f"Loading strategies from s3://{bucket}/{strategies_key}")
        
        # Load strategies from S3
        strategies_obj = s3.get_object(Bucket=bucket, Key=strategies_key)
        strategies_data = json.loads(strategies_obj['Body'].read())
        
        print(f"Loading price data from s3://{bucket}/{price_data_key}")
        
        # Load price data from S3
        price_obj = s3.get_object(Bucket=bucket, Key=price_data_key)
        price_data = pd.read_csv(StringIO(price_obj['Body'].read().decode('utf-8')))
        
        # Use 70% training split
        train_size = int(len(price_data) * 0.7)
        train_data = price_data.iloc[:train_size]
        prices = train_data['price'].values
        
        print(f"Backtesting {len(strategies_data)} strategies on {len(train_data)} training samples")
        
        # Backtest all strategies
        results = []
        for strategy in strategies_data:
            signals = strategy['signals']
            metrics = calculate_strategy_metrics(signals, prices)
            
            results.append({
                'strategy_id': strategy['id'],
                'win_rate': metrics['win_rate'],
                'total_return': metrics['total_return'],
                'sharpe_ratio': metrics['sharpe_ratio'],
                'max_drawdown': metrics['max_drawdown'],
                'num_trades': metrics['num_trades']
            })
        
        # Convert to DataFrame and save to S3
        results_df = pd.DataFrame(results)
        csv_buffer = StringIO()
        results_df.to_csv(csv_buffer, index=False)
        
        results_key = "results/training_performance.csv"
        s3.put_object(
            Bucket=bucket,
            Key=results_key,
            Body=csv_buffer.getvalue(),
            ContentType='text/csv'
        )
        
        print(f"Successfully backtested {len(results)} strategies, saved to s3://{bucket}/{results_key}")
        
        return {
            'statusCode': 200,
            'bucket': bucket,
            'results_key': results_key,
            'strategies_tested': len(results),
            'avg_win_rate': float(results_df['win_rate'].mean())
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            'statusCode': 500,
            'error': str(e)
        }
