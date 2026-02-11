"""
Step 1: Generate Overfit Strategies (NOT random!)
Creates strategies that curve-fit to training data to achieve high win rates

This demonstrates real overfitting - fitting to noise and specific patterns
in the training data that won't generalize.
"""

import numpy as np
import pandas as pd
import json
from pathlib import Path

# ============================================
# CONFIGURATION
# ============================================
NUM_STRATEGIES = 100      # Number of overfit strategies to generate
TRAIN_SPLIT = 0.7         # 70% training, 30% validation
RANDOM_SEED = 42          # For reproducibility
MAX_DATA_POINTS = 800     # Use less data to make overfitting easier

# Real data path
REAL_DATA_PATH = r'D:\QUANT\GEA\coinflip_strategy_demo\data\BTCUSD_Candlestick_5_M_BID_01.10.2024-10.11.2024.csv'

# ============================================
# STRATEGY TYPE SWITCHES (Enable/Disable)
# ============================================
ENABLE_LOOKAHEAD = False      # Type 0: Lookahead bias (most aggressive)
ENABLE_PATTERN = True        # Type 1: Pattern fitting
ENABLE_HYBRID = True         # Type 2: Hybrid approach
ENABLE_POLYNOMIAL = True     # Type 3: High-order polynomial fitting
ENABLE_MACHINE_LEARNING = True  # Type 4: Decision Tree ML (extreme overfitting!)

# Note: At least one type must be enabled!

# ============================================
# FUNCTIONS TO CREATE OVERFIT STRATEGIES
# ============================================

def create_lookahead_strategy(prices, aggressiveness=0.7, seed=None):
    """
    Create a strategy that 'cheats' by looking ahead at price movements
    
    This simulates what retail traders do when they:
    - Optimize parameters until they get good results
    - Add indicators that happen to work on that specific period
    - Keep tweaking until backtest looks amazing
    
    Args:
        prices: Training price data
        aggressiveness: How much to use future info (0-1)
        seed: Random seed
    
    Returns:
        Binary signals (1=buy, 0=no action)
    """
    if seed is not None:
        np.random.seed(seed)
    
    signals = []
    
    for i in range(len(prices) - 1):
        # Look ahead: did price go up next period?
        future_return = (prices[i + 1] - prices[i]) / prices[i]
        
        # If we're "aggressive", buy when we know it will go up
        # Add some randomness to make it look less obvious
        if future_return > 0:
            # Buy with probability = aggressiveness
            buy_signal = 1 if np.random.random() < aggressiveness else 0
        else:
            # Don't buy when it will go down
            # But sometimes buy anyway (randomness)
            buy_signal = 1 if np.random.random() < (1 - aggressiveness) else 0
        
        signals.append(buy_signal)
    
    # Last signal (no future to look at)
    signals.append(int(np.random.random() < 0.5))
    
    return signals


def create_pattern_fit_strategy(prices, pattern_strength=0.6, seed=None):
    """
    Create a strategy that fits to specific patterns in training data
    
    This finds patterns like:
    - "Buy when price is between X and Y"
    - "Buy when return was positive last 2 periods"
    - "Buy on every Nth trade"
    
    These patterns work great on training data but are just noise!
    
    Args:
        prices: Training price data
        pattern_strength: How strongly to fit patterns (0-1)
        seed: Random seed
    
    Returns:
        Binary signals
    """
    if seed is not None:
        np.random.seed(seed)
    
    signals = []
    returns = np.diff(prices) / prices[:-1]
    returns = np.concatenate([[0], returns])  # Add 0 for first return
    
    # Create arbitrary "rules" based on training data characteristics
    for i in range(len(prices)):
        buy_probability = 0.5  # Start neutral
        
        # Rule 1: Buy if price is in certain range (fits to training)
        if prices[i] > np.percentile(prices, 40) and prices[i] < np.percentile(prices, 60):
            buy_probability += pattern_strength * 0.3
        
        # Rule 2: Buy if recent return was positive (momentum fitting)
        if i > 0 and returns[i] > 0:
            buy_probability += pattern_strength * 0.25
        
        # Rule 3: Buy every Nth trade (arbitrary pattern)
        if i % 7 == 0:  # Random pattern that happens to exist
            buy_probability += pattern_strength * 0.2
        
        # Rule 4: More likely to buy if price near median (curve fitting)
        distance_from_median = abs(prices[i] - np.median(prices)) / np.median(prices)
        if distance_from_median < 0.02:
            buy_probability += pattern_strength * 0.15
        
        # Ensure probability is between 0 and 1
        buy_probability = max(0, min(1, buy_probability))
        
        # Generate signal
        signals.append(1 if np.random.random() < buy_probability else 0)
    
    return signals


def create_polynomial_overfit_strategy(prices, polynomial_degree=8, seed=None):
    """
    Fit a high-order polynomial to training prices
    
    This is the CLASSIC overfitting example:
    - Fit polynomial to past prices
    - Higher degree = perfect fit to training data
    - But polynomial wiggles wildly on new data
    
    Simulates traders who:
    - Use complex indicators with many parameters
    - Fit everything perfectly to past data
    - Are shocked when it fails on live trading
    
    Args:
        prices: Training price data
        polynomial_degree: Degree of polynomial (higher = more overfit)
        seed: Random seed
    
    Returns:
        Binary signals based on polynomial prediction
    """
    if seed is not None:
        np.random.seed(seed)
    
    # Fit polynomial to prices
    x = np.arange(len(prices))
    
    # Use high degree polynomial (classic overfitting!)
    coeffs = np.polyfit(x, prices, deg=polynomial_degree)
    poly = np.poly1d(coeffs)
    
    # Generate signals based on polynomial predictions
    signals = []
    for i in range(len(prices) - 1):
        # Predict next price using polynomial
        predicted_next = poly(i + 1)
        current_price = prices[i]
        
        # Buy if polynomial predicts price will go up
        predicted_return = (predicted_next - current_price) / current_price
        
        if predicted_return > 0:
            # Add some randomness so different strategies vary
            buy_prob = 0.7 + 0.2 * np.random.random()
            signals.append(1 if np.random.random() < buy_prob else 0)
        else:
            buy_prob = 0.2 * np.random.random()
            signals.append(1 if np.random.random() < buy_prob else 0)
    
    # Last signal
    signals.append(int(np.random.random() < 0.5))
    
    return signals


def create_hybrid_overfit_strategy(prices, lookahead_weight=0.5, seed=None):
    """
    Mix of lookahead bias and pattern fitting
    
    This is what actually happens in the real world:
    - Traders test many indicators
    - They pick the ones that worked best in the past
    - This is indirect lookahead bias + curve fitting
    
    Args:
        prices: Training price data
        lookahead_weight: Balance between lookahead and pattern (0-1)
        seed: Random seed
    
    Returns:
        Binary signals
    """
    if seed is not None:
        np.random.seed(seed)
    
    # Get both strategies
    lookahead_signals = create_lookahead_strategy(prices, aggressiveness=0.65, seed=seed)
    pattern_signals = create_pattern_fit_strategy(prices, pattern_strength=0.6, seed=seed+1 if seed else None)
    
    # Mix them
    signals = []
    for i in range(len(prices)):
        if np.random.random() < lookahead_weight:
            signals.append(lookahead_signals[i])
        else:
            signals.append(pattern_signals[i])
    
    return signals


def create_ml_decision_tree_strategy(prices, returns):
    """
    Type 4: Machine Learning Overfitting - Decision Tree
    Create a strategy that mimics a decision tree with many splits.
    Classic ML overfitting: create perfect splits for training data.
    
    This simulates a decision tree with no max_depth limit - it will
    create arbitrary splits that perfectly classify training data
    but fail on new data.
    """
    signals = []
    
    # Create random thresholds based on training data quantiles
    # This mimics decision tree splits
    price_quantiles = np.percentile(prices, [10, 25, 40, 50, 60, 75, 90])
    return_quantiles = np.percentile(returns, [10, 25, 40, 50, 60, 75, 90])
    
    # Create moving averages to add more features (overfitting on patterns)
    ma_short = pd.Series(prices).rolling(window=5, min_periods=1).mean().values
    ma_long = pd.Series(prices).rolling(window=20, min_periods=1).mean().values
    
    # Pre-calculate volatility threshold (for performance)
    rolling_vol = pd.Series(returns).rolling(window=10, min_periods=1).std().values
    vol_threshold = np.median(rolling_vol[10:])  # Use median of rolling volatilities
    
    for i in range(len(prices)):
        # Simulate deep decision tree with many arbitrary splits
        # Each split is optimized for training data
        
        score = 0  # Decision score
        
        # Split 1: Price level
        if prices[i] > price_quantiles[5]:
            score += 2
        elif prices[i] < price_quantiles[2]:
            score -= 2
            
        # Split 2: Recent returns
        if i > 0 and returns[i] > return_quantiles[5]:
            score += 1
        elif i > 0 and returns[i] < return_quantiles[2]:
            score -= 1
            
        # Split 3: Moving average crossover
        if ma_short[i] > ma_long[i]:
            score += 1
        else:
            score -= 1
            
        # Split 4: Volatility (overfitting on recent volatility)
        if i >= 10:
            recent_vol = rolling_vol[i]
            if recent_vol < vol_threshold:
                score += 1
            else:
                score -= 1
        
        # Split 5: Add noise based on data index (overfits on position in dataset)
        if i % 13 == 0:  # Arbitrary pattern that appears in training
            score += 1
        if i % 17 == 0:
            score -= 1
            
        # Final decision based on accumulated score
        # This creates complex decision boundaries that overfit training data
        if score > 0:
            signals.append(1)
        else:
            signals.append(-1)
    
    return signals


def load_real_price_data(csv_path, train_split=0.7, max_points=800):
    """
    Load real price data from CSV file
    """
    df = pd.read_csv(csv_path)
    df = df.head(max_points)
    df['timestamp'] = pd.to_datetime(df['dt'], format='%d.%m.%Y %H:%M:%S')
    df['price'] = df['Close']
    df['returns'] = df['price'].pct_change().fillna(0)
    
    split_point = int(len(df) * train_split)
    df['split'] = ['train'] * split_point + ['validation'] * (len(df) - split_point)
    
    df = df[['timestamp', 'price', 'returns', 'split']].copy()
    return df


def save_strategies(strategies, filepath):
    """Save strategies to JSON file"""
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    with open(filepath, 'w') as f:
        json.dump(strategies, f, indent=2)
    
    print(f"✅ Saved {len(strategies)} strategies to {filepath}")


def save_price_data(df, filepath):
    """Save price data to CSV file"""
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
    1. Load real Bitcoin data
    2. Generate OVERFIT strategies (not random!)
    3. Save both
    """
    print("=" * 60)
    print("STEP 1: Generating OVERFIT Strategies")
    print("=" * 60)
    print("\n⚠️  NOTE: These are NOT random strategies!")
    print("    They are engineered to fit the training data.")
    print("    This is what retail traders actually do:")
    print("      • Test many indicators")
    print("      • Pick the 'best' ones")
    print("      • Unknowingly curve-fit to noise")
    
    # Load real price data
    print(f"\n📈 Loading REAL Bitcoin price data...")
    price_df = load_real_price_data(REAL_DATA_PATH, train_split=TRAIN_SPLIT, max_points=MAX_DATA_POINTS)
    
    # Get training prices
    train_prices = price_df[price_df['split'] == 'train']['price'].values
    
    num_points = len(price_df)
    train_points = len(train_prices)
    
    print(f"   ✓ Loaded {num_points} total data points")
    print(f"   ✓ Training: {train_points} points")
    print(f"   ✓ Date range: {price_df['timestamp'].min()} to {price_df['timestamp'].max()}")
    
    # Generate overfit strategies
    print(f"\n🎯 Generating {NUM_STRATEGIES} OVERFIT strategies...")
    print(f"   These strategies will look amazing on training data!")
    
    # Check which types are enabled
    enabled_types = []
    if ENABLE_LOOKAHEAD:
        enabled_types.append(0)
    if ENABLE_PATTERN:
        enabled_types.append(1)
    if ENABLE_HYBRID:
        enabled_types.append(2)
    if ENABLE_POLYNOMIAL:
        enabled_types.append(3)
    if ENABLE_MACHINE_LEARNING:
        enabled_types.append(4)
    
    if len(enabled_types) == 0:
        print("\n❌ ERROR: No strategy types enabled!")
        print("   Enable at least one type in the configuration.")
        return
    
    print(f"   📌 Enabled types: {enabled_types}")
    type_names = {0: "Lookahead", 1: "Pattern", 2: "Hybrid", 3: "Polynomial", 4: "Machine Learning"}
    print(f"   📌 Using: {', '.join([type_names[t] for t in enabled_types])}")
    
    strategies = {}
    type_counts = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
    
    for i in range(NUM_STRATEGIES):
        np.random.seed(RANDOM_SEED + i)
        
        # Cycle through enabled types only
        strategy_type = enabled_types[i % len(enabled_types)]
        type_counts[strategy_type] += 1
        
        if strategy_type == 0:
            # Pure lookahead bias (most aggressive)
            aggressiveness = 0.6 + np.random.random() * 0.2  # 60-80%
            signals = create_lookahead_strategy(train_prices, aggressiveness, seed=RANDOM_SEED+i)
        
        elif strategy_type == 1:
            # Pattern fitting
            strength = 0.5 + np.random.random() * 0.3  # 50-80%
            signals = create_pattern_fit_strategy(train_prices, strength, seed=RANDOM_SEED+i)
        
        elif strategy_type == 2:
            # Hybrid (most realistic)
            lookahead_weight = np.random.random()  # Random mix
            signals = create_hybrid_overfit_strategy(train_prices, lookahead_weight, seed=RANDOM_SEED+i)
        
        elif strategy_type == 3:
            # High-order polynomial (classic ML overfitting!)
            degree = np.random.randint(6, 12)  # Random degree 6-11
            signals = create_polynomial_overfit_strategy(train_prices, polynomial_degree=degree, seed=RANDOM_SEED+i)
        
        else:  # strategy_type == 4
            # Machine Learning - Decision Tree overfitting
            train_returns = price_df[price_df['split'] == 'train']['returns'].values
            signals = create_ml_decision_tree_strategy(train_prices, train_returns)
        
        strategies[f'strategy_{i:03d}'] = signals
    
    print(f"   ✓ Generated {NUM_STRATEGIES} overfit strategies")
    print(f"   ✓ Distribution:")
    if ENABLE_LOOKAHEAD:
        print(f"      - Lookahead: {type_counts[0]}")
    if ENABLE_PATTERN:
        print(f"      - Pattern: {type_counts[1]}")
    if ENABLE_HYBRID:
        print(f"      - Hybrid: {type_counts[2]}")
    if ENABLE_POLYNOMIAL:
        print(f"      - Polynomial: {type_counts[3]}")
    if ENABLE_MACHINE_LEARNING:
        print(f"      - Machine Learning: {type_counts[4]}")
    
    # Save files
    print(f"\n💾 Saving files...")
    save_strategies(strategies, 'data/strategies.json')
    save_price_data(price_df, 'data/btc_price_data.csv')
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ STEP 1 COMPLETE!")
    print("=" * 60)
    print(f"Created:")
    print(f"  • data/strategies.json ({NUM_STRATEGIES} OVERFIT strategies)")
    print(f"  • data/btc_price_data.csv ({num_points} real BTC price points)")
    
    print(f"\n💡 Strategy Types Used:")
    if ENABLE_LOOKAHEAD:
        print(f"   ✅ Lookahead Bias - Cheats by looking at future prices")
    else:
        print(f"   ❌ Lookahead Bias - DISABLED")
    
    if ENABLE_PATTERN:
        print(f"   ✅ Pattern Fitting - Fits to arbitrary patterns in training")
    else:
        print(f"   ❌ Pattern Fitting - DISABLED")
    
    if ENABLE_HYBRID:
        print(f"   ✅ Hybrid - Mix of lookahead + patterns (most realistic)")
    else:
        print(f"   ❌ Hybrid - DISABLED")
    
    if ENABLE_POLYNOMIAL:
        print(f"   ✅ Polynomial - High-degree curve fitting (classic ML overfitting)")
    else:
        print(f"   ❌ Polynomial - DISABLED")
    
    print(f"\n🎯 Expected Results:")
    print(f"   ❌ Random coinflips: ~50% win rate (honest)")
    print(f"   ✅ These strategies: 60-80% win rate (dishonest curve-fitting!)")
    print(f"\n   This is THE REAL TRAP that catches retail traders!")
    print(f"\n💡 Tip: Edit ENABLE_* flags to isolate specific overfitting types")
    print(f"\nNext: Run 02_backtest_strategies.py")
    print("=" * 60)


if __name__ == "__main__":
    main()
