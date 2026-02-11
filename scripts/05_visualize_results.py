"""
Step 5: Visualize Results
Create compelling charts that prove overfitting

This creates three devastating visualizations:
1. Histogram showing all 100 random strategies
2. Training vs Validation comparison
3. Equity curve showing the performance collapse
"""

import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import numpy as np

# Set style for professional-looking charts
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 11


# ============================================
# CHART 1: Distribution of All Strategies
# ============================================

def plot_strategy_distribution():
    """
    Histogram showing win rates of all 100 random strategies
    Highlights the "best" strategy as an outlier
    """
    # Load data
    results_df = pd.read_csv('results/training_performance.csv')
    
    with open('results/best_strategy.json', 'r') as f:
        best_strategy = json.load(f)
    
    best_win_rate = best_strategy['training_metrics']['win_rate']
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot histogram
    n, bins, patches = ax.hist(
        results_df['win_rate'], 
        bins=30, 
        color='skyblue', 
        edgecolor='black', 
        alpha=0.7
    )
    
    # Highlight the best strategy
    ax.axvline(
        best_win_rate, 
        color='red', 
        linestyle='--', 
        linewidth=2, 
        label=f'Best Strategy: {best_win_rate:.1%}'
    )
    
    # Add mean line
    mean_wr = results_df['win_rate'].mean()
    ax.axvline(
        mean_wr, 
        color='green', 
        linestyle='--', 
        linewidth=2, 
        label=f'Mean: {mean_wr:.1%}'
    )
    
    # Labels and title
    ax.set_xlabel('Win Rate', fontsize=13, fontweight='bold')
    ax.set_ylabel('Number of Strategies', fontsize=13, fontweight='bold')
    ax.set_title(
        'Distribution of 100 RANDOM Strategies on Training Data\n' +
        '(All strategies are coin flips - pure randomness)',
        fontsize=15,
        fontweight='bold'
    )
    
    ax.legend(fontsize=11)
    ax.grid(alpha=0.3)
    
    # Add annotation
    ax.annotate(
        'One random strategy\nlooks "amazing"\nby pure luck!',
        xy=(best_win_rate, max(n) * 0.7),
        xytext=(best_win_rate + 0.05, max(n) * 0.8),
        fontsize=10,
        bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7),
        arrowprops=dict(arrowstyle='->', color='red', lw=2)
    )
    
    plt.tight_layout()
    plt.savefig('plots/all_strategies_histogram.png', dpi=300, bbox_inches='tight')
    print("   ✓ Saved: plots/all_strategies_histogram.png")
    plt.close()


# ============================================
# CHART 2: Training vs Validation Comparison
# ============================================

def plot_train_vs_validation():
    """
    Side-by-side comparison showing performance collapse
    """
    # Load validation results
    with open('results/validation_results.json', 'r') as f:
        results = json.load(f)
    
    train_metrics = results['training_metrics']
    val_metrics = results['validation_metrics']
    
    # Prepare data
    metrics = ['Win Rate', 'Total Return', 'Sharpe Ratio']
    train_values = [
        train_metrics['win_rate'] * 100,
        train_metrics['total_return'] * 100,
        train_metrics['sharpe_ratio']
    ]
    val_values = [
        val_metrics['win_rate'] * 100,
        val_metrics['total_return'] * 100,
        val_metrics['sharpe_ratio']
    ]
    
    # Create figure
    fig, axes = plt.subplots(1, 3, figsize=(15, 6))
    
    colors_train = ['#2ecc71', '#3498db', '#9b59b6']
    colors_val = ['#e74c3c', '#e67e22', '#95a5a6']
    
    for idx, (ax, metric) in enumerate(zip(axes, metrics)):
        x = [0, 1]
        y = [train_values[idx], val_values[idx]]
        
        # Bar chart
        bars = ax.bar(x, y, color=[colors_train[idx], colors_val[idx]], 
                      edgecolor='black', linewidth=1.5, width=0.6)
        
        # Add value labels on bars
        for i, (bar, value) in enumerate(zip(bars, y)):
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.,
                height,
                f'{value:.1f}{"%" if idx < 2 else ""}',
                ha='center',
                va='bottom',
                fontsize=12,
                fontweight='bold'
            )
        
        # Formatting
        ax.set_xticks(x)
        ax.set_xticklabels(['Training', 'Validation'], fontsize=11)
        ax.set_title(metric, fontsize=13, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        # Add change annotation
        change = val_values[idx] - train_values[idx]
        ax.annotate(
            f'{change:+.1f}{"%" if idx < 2 else ""}',
            xy=(0.5, max(y) * 0.5),
            ha='center',
            fontsize=11,
            color='red',
            fontweight='bold'
        )
    
    fig.suptitle(
        'Training vs Validation: The Overfitting Collapse\n' +
        '(Same strategy, different data periods)',
        fontsize=16,
        fontweight='bold',
        y=1.02
    )
    
    plt.tight_layout()
    plt.savefig('plots/best_vs_validation.png', dpi=300, bbox_inches='tight')
    print("   ✓ Saved: plots/best_vs_validation.png")
    plt.close()


# ============================================
# CHART 3: Equity Curve Over Time
# ============================================

def plot_equity_curve():
    """
    Show equity curve splitting at train/validation boundary
    """
    # Load data
    price_df = pd.read_csv('data/btc_price_data.csv')
    
    with open('results/best_strategy.json', 'r') as f:
        best_strategy = json.load(f)
    
    signals = best_strategy['signals']
    
    # Calculate equity curve
    prices = price_df['price'].values
    equity = [1.0]  # Start with $1
    
    for i in range(min(len(signals) - 1, len(prices) - 1)):
        if signals[i] == 1:  # Trade signal
            ret = (prices[i + 1] - prices[i]) / prices[i]
            equity.append(equity[-1] * (1 + ret))
        else:  # No trade
            equity.append(equity[-1])
    
    # Pad if needed
    while len(equity) < len(price_df):
        equity.append(equity[-1])
    
    equity = equity[:len(price_df)]
    
    # Add equity to dataframe
    price_df['equity'] = equity
    
    # Split into train/validation
    train_df = price_df[price_df['split'] == 'train'].copy()
    val_df = price_df[price_df['split'] == 'validation'].copy()
    
    # Create figure
    fig, ax = plt.subplots(figsize=(14, 7))
    
    # Plot training equity
    ax.plot(
        range(len(train_df)),
        train_df['equity'],
        color='green',
        linewidth=2,
        label='Training Period (looks great!)',
        alpha=0.8
    )
    
    # Plot validation equity
    val_start = len(train_df)
    ax.plot(
        range(val_start, val_start + len(val_df)),
        val_df['equity'],
        color='red',
        linewidth=2,
        label='Validation Period (reality check)',
        alpha=0.8
    )
    
    # Add vertical line at split
    ax.axvline(
        val_start,
        color='black',
        linestyle='--',
        linewidth=2,
        label='Train/Validation Split'
    )
    
    # Add shaded regions
    ax.axvspan(0, val_start, alpha=0.1, color='green', label='Training Data')
    ax.axvspan(val_start, len(price_df), alpha=0.1, color='red', label='Validation Data')
    
    # Add horizontal line at starting equity
    ax.axhline(1.0, color='gray', linestyle=':', linewidth=1, alpha=0.5)
    
    # Labels
    ax.set_xlabel('Time Period', fontsize=13, fontweight='bold')
    ax.set_ylabel('Account Equity ($)', fontsize=13, fontweight='bold')
    ax.set_title(
        'Equity Curve: The Moment Overfitting is Revealed\n' +
        '(Watch what happens when the strategy meets new data)',
        fontsize=15,
        fontweight='bold'
    )
    
    # Format y-axis as currency
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'${y:.2f}'))
    
    # Legend
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[:3], labels[:3], fontsize=11, loc='best')
    
    ax.grid(alpha=0.3)
    
    # Add annotations
    train_final = train_df['equity'].iloc[-1]
    val_final = val_df['equity'].iloc[-1]
    
    ax.annotate(
        f'End of training:\n${train_final:.2f}',
        xy=(val_start - 10, train_final),
        xytext=(val_start - 80, train_final + 0.15),
        fontsize=10,
        bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8),
        arrowprops=dict(arrowstyle='->', color='green', lw=1.5)
    )
    
    ax.annotate(
        f'End of validation:\n${val_final:.2f}\n(The truth!)',
        xy=(len(price_df) - 10, val_final),
        xytext=(len(price_df) - 100, val_final + 0.15),
        fontsize=10,
        bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.8),
        arrowprops=dict(arrowstyle='->', color='red', lw=1.5)
    )
    
    plt.tight_layout()
    plt.savefig('plots/overfitting_proof.png', dpi=300, bbox_inches='tight')
    print("   ✓ Saved: plots/overfitting_proof.png")
    plt.close()


# ============================================
# MAIN EXECUTION
# ============================================

def main():
    """
    Create all three visualization charts
    """
    print("=" * 60)
    print("STEP 5: Creating Visualizations")
    print("=" * 60)
    
    # Ensure plots directory exists
    Path('plots').mkdir(parents=True, exist_ok=True)
    
    print("\n📊 Generating charts...")
    
    # Chart 1: Distribution
    print("\n1️⃣  Creating strategy distribution histogram...")
    plot_strategy_distribution()
    
    # Chart 2: Train vs Val
    print("\n2️⃣  Creating train vs validation comparison...")
    plot_train_vs_validation()
    
    # Chart 3: Equity curve
    print("\n3️⃣  Creating equity curve...")
    plot_equity_curve()
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ STEP 5 COMPLETE!")
    print("=" * 60)
    print("\n📁 All charts saved to plots/ directory:")
    print("   • all_strategies_histogram.png")
    print("   • best_vs_validation.png")
    print("   • overfitting_proof.png")
    
    print("\n🎯 What the charts prove:")
    print("   1️⃣  Random strategies can look amazing by luck")
    print("   2️⃣  Performance collapses on new data")
    print("   3️⃣  Overfitting is a devastating trap")
    
    print("\n💡 Use these charts to:")
    print("   • Explain overfitting to non-technical people")
    print("   • Show why backtesting can be misleading")
    print("   • Demonstrate the importance of validation")
    print("   • Warn against curve-fitting strategies")
    
    print("\n" + "=" * 60)
    print("🏁 ALL STEPS COMPLETE! Demo ready to present.")
    print("=" * 60)


if __name__ == "__main__":
    main()
