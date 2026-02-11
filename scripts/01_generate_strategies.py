"""
Step 1: Generate Random Strategies
Creates 100 completely random trading strategies (coin flips)

This demonstrates that with enough random strategies, some will look good by pure chance.
"""

import numpy as np
import pandas as pd
import json
from pathlib import Path

# ============================================
# CONFIGURATION
# ============================================
NUM_STRATEGIES = 500      # More strategies = higher chance of extreme outlier by luck!
NUM_SIGNALS = 500         # Number of trading signals per strategy
TRAIN_SPLIT = 0.7         # 70% training, 30% validation
RANDOM_SEED = 42          # For reproducibility
MAX_DATA_POINTS = 800     # Use less data to make overfitting easier to demonstrate

# Real data path
REAL_DATA_PATH = r'D:\QUANT\GEA\coinflip_strategy_demo\data\BTCUSD_Candlestick_5_M_BID_01.10.2024-10.11.2024.csv'

# ============================================
# FUNCTIONS
# ============================================

def generate_random_strategy(num_signals, seed=None):
    """
    Generate one completely random strategy (literal coin flips)
    
    Args:
        num_signals: Number of trading signals to generate
        seed: Random seed for reproducibility (optional)
    
    Returns:
        list: Random buy(1) / no-action(0) signals
    """
    if seed is not None:
        np.random.seed(seed)
    
    # Pure coin flip: 50% chance of buy signal
    signals = np.random.randint(0, 2, size=num_signals)
    return signals.tolist()


def load_real_price_data(csv_path, train_split=0.7, max_points=800):
    """
    Load real price data from CSV file
    
    This uses actual Bitcoin price data instead of synthetic data,
    making the demonstration more realistic and impactful.
    
    Args:
        csv_path: Path to the CSV file with price data
        train_split: Fraction for training (rest is validation)
        max_points: Maximum number of data points to use (for easier overfitting)
    
    Returns:
        DataFrame with columns: [timestamp, price, returns, split]
    """
    # Load the CSV file
    df = pd.read_csv(csv_path)
    
    # Take only first max_points (for easier overfitting demonstration)
    # Using less data makes it easier for random strategies to look good by chance
    df = df.head(max_points)
    
    # Parse timestamp (format: "01.08.2024 00:00:00")
    df['timestamp'] = pd.to_datetime(df['dt'], format='%d.%m.%Y %H:%M:%S')
    
    # Use Close price
    df['price'] = df['Close']
    
    # Calculate returns
    df['returns'] = df['price'].pct_change().fillna(0)
    
    # Determine train/validation split
    split_point = int(len(df) * train_split)
    df['split'] = ['train'] * split_point + ['validation'] * (len(df) - split_point)
    
    # Select and reorder columns
    df = df[['timestamp', 'price', 'returns', 'split']].copy()
    
    return df


def save_strategies(strategies, filepath):
    """
    Save strategies to JSON file
    
    Args:
        strategies: Dictionary with strategy IDs and their signals
        filepath: Path to save JSON file
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    with open(filepath, 'w') as f:
        json.dump(strategies, f, indent=2)
    
    print(f"✅ Saved {len(strategies)} strategies to {filepath}")


def save_price_data(df, filepath):
    """
    Save price data to CSV file
    
    Args:
        df: DataFrame with price data
        filepath: Path to save CSV file
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    df.to_csv(filepath, index=False)
    print(f"✅ Saved {len(df)} price points to {filepath}")


# ============================================
# MAIN EXECUTION
# ============================================

def main():
    """
    Main execution:
    1. Generate 100 random strategies (coin flips)
    2. Load real Bitcoin price data
    3. Save both to data/ folder
    """
    print("=" * 60)
    print("STEP 1: Generating Random Strategies & Loading Real Data")
    print("=" * 60)
    
    # Generate random strategies
    print(f"\n📊 Generating {NUM_STRATEGIES} random strategies...")
    print(f"   Each strategy has {NUM_SIGNALS} random signals (coin flips)")
    
    strategies = {}
    for i in range(NUM_STRATEGIES):
        # Each strategy gets different random seed
        strategy_signals = generate_random_strategy(
            NUM_SIGNALS, 
            seed=RANDOM_SEED + i
        )
        strategies[f'strategy_{i:03d}'] = strategy_signals
    
    print(f"   ✓ Generated {NUM_STRATEGIES} completely random strategies")
    
    # Load real price data
    print(f"\n📈 Loading REAL Bitcoin price data...")
    print(f"   Source: {REAL_DATA_PATH}")
    print(f"   Using first {MAX_DATA_POINTS} data points (smaller dataset = easier to overfit)")
    
    price_df = load_real_price_data(REAL_DATA_PATH, train_split=TRAIN_SPLIT, max_points=MAX_DATA_POINTS)
    
    num_points = len(price_df)
    train_points = len(price_df[price_df['split'] == 'train'])
    val_points = len(price_df[price_df['split'] == 'validation'])
    
    print(f"   ✓ Loaded real Bitcoin data")
    print(f"   ✓ Total data points: {num_points}")
    print(f"   ✓ Train split: {TRAIN_SPLIT:.0%} ({train_points} points)")
    print(f"   ✓ Validation split: {1-TRAIN_SPLIT:.0%} ({val_points} points)")
    print(f"   ✓ Date range: {price_df['timestamp'].min()} to {price_df['timestamp'].max()}")
    print(f"   ✓ Price range: ${price_df['price'].min():.2f} - ${price_df['price'].max():.2f}")
    
    # Save files
    print(f"\n💾 Saving files...")
    save_strategies(strategies, 'data/strategies.json')
    save_price_data(price_df, 'data/btc_price_data.csv')
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ STEP 1 COMPLETE!")
    print("=" * 60)
    print(f"Created:")
    print(f"  • data/strategies.json ({NUM_STRATEGIES} random strategies)")
    print(f"  • data/btc_price_data.csv ({num_points} real BTC price points)")
    print(f"\nUsing REAL Bitcoin data makes this even more realistic!")
    print(f"Note: Using {MAX_DATA_POINTS} points (not all 28K) makes overfitting")
    print(f"      easier to demonstrate - just like retail traders who backtest")
    print(f"      on small samples and think they found the 'edge'!")
    print(f"\nNext: Run 02_backtest_strategies.py")
    print("=" * 60)


if __name__ == "__main__":
    main()
