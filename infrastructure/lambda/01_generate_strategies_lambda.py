"""
Lambda Function: Generate Random Trading Strategies
Generates 100 random strategies and saves to S3
"""

import json
import boto3
import numpy as np
from datetime import datetime

# AWS clients
s3 = boto3.client('s3')

# Configuration
NUM_STRATEGIES = 500
NUM_SIGNALS = 500
RANDOM_SEED = 42

def generate_random_strategy(num_signals, seed=None):
    """Generate one completely random strategy (coin flips)"""
    if seed is not None:
        np.random.seed(seed)
    signals = np.random.randint(0, 2, size=num_signals)
    return signals.tolist()

def lambda_handler(event, context):
    """
    Lambda handler for strategy generation
    
    Input event:
    {
        "bucket": "overfitting-demo-data",
        "num_strategies": 500 (optional)
    }
    
    Output:
    {
        "statusCode": 200,
        "strategies_key": "strategies/strategies_2026-02-11.json",
        "count": 500
    }
    """
    
    try:
        # Get parameters from event
        bucket = event.get('bucket', 'overfitting-demo-data')
        num_strategies = event.get('num_strategies', NUM_STRATEGIES)
        
        print(f"Generating {num_strategies} random strategies...")
        
        # Generate strategies
        strategies = []
        for i in range(num_strategies):
            strategy = {
                'id': i,
                'signals': generate_random_strategy(NUM_SIGNALS, seed=RANDOM_SEED + i),
                'created_at': datetime.utcnow().isoformat()
            }
            strategies.append(strategy)
        
        # Save to S3
        timestamp = datetime.utcnow().strftime('%Y-%m-%d')
        key = f"strategies/strategies_{timestamp}.json"
        
        s3.put_object(
            Bucket=bucket,
            Key=key,
            Body=json.dumps(strategies, indent=2),
            ContentType='application/json'
        )
        
        # Also save as "latest" for easy access
        s3.put_object(
            Bucket=bucket,
            Key="strategies/strategies_latest.json",
            Body=json.dumps(strategies, indent=2),
            ContentType='application/json'
        )
        
        print(f"Successfully generated {len(strategies)} strategies and saved to s3://{bucket}/{key}")
        
        return {
            'statusCode': 200,
            'bucket': bucket,
            'strategies_key': key,
            'latest_key': 'strategies/strategies_latest.json',
            'count': len(strategies)
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'error': str(e)
        }
