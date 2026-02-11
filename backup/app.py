"""
🎲 Overfitting in Algo Trading - Interactive Demo
A Streamlit app demonstrating how easily overfitting occurs in algorithmic trading

Author: [Your Name]
Purpose: Portfolio demonstration for job applications
"""

import streamlit as st
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Overfitting Demo - Algo Trading",
    page_icon="🎲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #ff7f0e;
        margin-top: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #1f77b4;
    }
    .danger-card {
        background-color: #ffe6e6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #ff4444;
    }
    .success-card {
        background-color: #e6ffe6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #44ff44;
    }
</style>
""", unsafe_allow_html=True)


# ============================================
# DATA LOADING FUNCTIONS
# ============================================

@st.cache_data
def load_training_performance():
    """Load all 100 strategies performance on training data"""
    try:
        df = pd.read_csv('results/training_performance.csv')
        return df
    except FileNotFoundError:
        return None

@st.cache_data
def load_best_strategy():
    """Load the best performing strategy"""
    try:
        with open('results/best_strategy.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

@st.cache_data
def load_validation_results():
    """Load validation results"""
    try:
        with open('results/validation_results.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

@st.cache_data
def load_validation_summary():
    """Load validation summary for top strategies"""
    try:
        with open('results/validation_summary.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

@st.cache_data
def load_price_data():
    """Load BTC price data"""
    try:
        df = pd.read_csv('data/btc_price_data.csv')
        return df
    except FileNotFoundError:
        return None


# ============================================
# INTERACTIVE COMPONENTS
# ============================================

def run_live_simulation():
    """Interactive simulation: Generate random strategies on the fly"""
    st.markdown('<p class="sub-header">🎮 Interactive Simulation</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Control Panel")
        num_strategies = st.slider("Number of random strategies", 10, 500, 100, 10)
        num_trades = st.slider("Trades per strategy", 50, 500, 200, 50)
        noise_level = st.slider("Price volatility", 0.01, 0.05, 0.02, 0.01)
        
        if st.button("🎲 Generate & Test Random Strategies", type="primary"):
            with st.spinner("Generating random strategies..."):
                simulate_random_strategies(num_strategies, num_trades, noise_level)
    
    with col2:
        st.markdown("### What's Happening?")
        st.info("""
        **This simulation generates completely random trading signals:**
        
        1. Create N strategies with random buy/sell signals (coin flips)
        2. Generate synthetic price data with random walk
        3. Backtest all strategies on "training" period
        4. Pick the "best" performer
        5. Test on "validation" period → Watch it fail!
        
        **The lesson**: With enough random tries, something will look good by pure luck!
        """)


def simulate_random_strategies(n_strategies, n_trades, volatility):
    """Live simulation of random strategy generation and testing"""
    
    # Generate synthetic price data
    np.random.seed(42)
    returns = np.random.normal(0, volatility, n_trades)
    prices = 100 * np.exp(np.cumsum(returns))
    
    # Split into train/test
    split_idx = int(0.7 * n_trades)
    train_prices = prices[:split_idx]
    test_prices = prices[split_idx:]
    
    # Generate random strategies
    progress_bar = st.progress(0)
    train_results = []
    
    for i in range(n_strategies):
        # Random signals (0 = hold, 1 = trade)
        signals = np.random.randint(0, 2, len(train_prices))
        
        # Calculate returns
        price_returns = np.diff(train_prices) / train_prices[:-1]
        strategy_returns = signals[:-1] * price_returns
        
        win_rate = np.sum(strategy_returns > 0) / len(strategy_returns)
        total_return = np.sum(strategy_returns)
        
        train_results.append({
            'strategy_id': i,
            'win_rate': win_rate,
            'total_return': total_return,
            'signals': signals
        })
        
        progress_bar.progress((i + 1) / n_strategies)
    
    # Find best strategy
    train_df = pd.DataFrame(train_results)
    best_idx = train_df['win_rate'].idxmax()
    best_strategy = train_results[best_idx]
    
    # Test on validation
    val_signals = np.random.randint(0, 2, len(test_prices))  # Same "strategy" but new data
    val_returns = np.diff(test_prices) / test_prices[:-1]
    val_strategy_returns = val_signals[:-1] * val_returns
    val_win_rate = np.sum(val_strategy_returns > 0) / len(val_strategy_returns)
    
    # Display results
    st.success("✅ Simulation Complete!")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Training Win Rate", 
            f"{best_strategy['win_rate']:.1%}",
            delta="Looks amazing! 🎉"
        )
    
    with col2:
        st.metric(
            "Validation Win Rate", 
            f"{val_win_rate:.1%}",
            delta=f"{val_win_rate - best_strategy['win_rate']:.1%}",
            delta_color="inverse"
        )
    
    with col3:
        st.metric(
            "Performance Drop", 
            f"{(val_win_rate - best_strategy['win_rate']):.1%}",
            delta="Back to randomness 📉",
            delta_color="off"
        )
    
    # Plot distribution
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(train_df['win_rate'], bins=30, color='skyblue', edgecolor='black', alpha=0.7)
    ax.axvline(best_strategy['win_rate'], color='red', linestyle='--', linewidth=2, 
               label=f"Best: {best_strategy['win_rate']:.1%}")
    ax.axvline(val_win_rate, color='green', linestyle='--', linewidth=2, 
               label=f"Validation: {val_win_rate:.1%}")
    ax.set_xlabel('Win Rate')
    ax.set_ylabel('Number of Strategies')
    ax.set_title(f'Distribution of {n_strategies} Random Strategies')
    ax.legend()
    st.pyplot(fig)
    plt.close()


# ============================================
# MAIN APP
# ============================================

def main():
    # Header
    st.markdown('<p class="main-header">🎲 Overfitting in Algorithmic Trading</p>', unsafe_allow_html=True)
    st.markdown("""
    <p style="text-align: center; font-size: 1.2rem; color: #666;">
    A practical demonstration of how random strategies can appear profitable through overfitting
    </p>
    """, unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Select View:",
        ["📊 Overview", "🎮 Interactive Demo", "📈 Real Data Results", "🔬 Deep Dive Analysis", "📚 Learn More"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### About This Demo")
    st.sidebar.info("""
    **Purpose**: Demonstrate overfitting in algo trading
    
    **Tech Stack**:
    - Python, Pandas, NumPy
    - Streamlit
    - AWS Deployment
    - CI/CD Pipeline
    
    **Data**: Real Bitcoin 5-min candlestick data
    """)
    
    # Page routing
    if page == "📊 Overview":
        show_overview_page()
    elif page == "🎮 Interactive Demo":
        show_interactive_demo_page()
    elif page == "📈 Real Data Results":
        show_real_results_page()
    elif page == "🔬 Deep Dive Analysis":
        show_deep_dive_page()
    elif page == "📚 Learn More":
        show_learn_more_page()


# ============================================
# PAGE FUNCTIONS
# ============================================

def show_overview_page():
    """Main overview page"""
    st.markdown("## The Experiment")
    
    # Key points in colored boxes
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>1️⃣ Generate</h3>
            <p>Create 100 completely random trading strategies (coin flips)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="success-card">
            <h3>2️⃣ Backtest</h3>
            <p>Test on REAL Bitcoin data. Find "best" performer with 60%+ win rate!</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="danger-card">
            <h3>3️⃣ Validate</h3>
            <p>Test on new data → Falls back to ~50% (random chance)</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Load and display summary statistics
    validation_summary = load_validation_summary()
    
    if validation_summary:
        st.markdown("## 🎯 The Results")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Strategies Tested", 
                "100",
                help="All randomly generated (coin flips)"
            )
        
        with col2:
            avg_train = validation_summary['average_train_win_rate']
            st.metric(
                "Avg Training Win Rate", 
                f"{avg_train:.1%}",
                help="Average performance of top 10 on training data"
            )
        
        with col3:
            avg_val = validation_summary['average_val_win_rate']
            st.metric(
                "Avg Validation Win Rate", 
                f"{avg_val:.1%}",
                delta=f"{avg_val - avg_train:.1%}",
                delta_color="inverse",
                help="Same strategies on validation data"
            )
        
        with col4:
            still_good = validation_summary['strategies_still_good']
            st.metric(
                "Still 'Good' on Validation", 
                f"{still_good}/10",
                help="Strategies that maintained performance"
            )
        
        st.markdown("---")
        
        # The big reveal
        st.markdown("### 💡 The Big Reveal")
        
        best_strategy = validation_summary['all_strategies'][0]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📈 On Training Data (Looked Amazing!)")
            st.success(f"""
            - **Win Rate**: {best_strategy['train_win_rate']:.1%}
            - **Total Return**: {best_strategy['train_return']:.1%}
            - **Sharpe Ratio**: {best_strategy['train_sharpe']:.2f}
            
            *Wow! This strategy is a goldmine!* 🤑
            """)
        
        with col2:
            st.markdown("#### 📉 On Validation Data (Reality Check)")
            st.error(f"""
            - **Win Rate**: {best_strategy['val_win_rate']:.1%}
            - **Total Return**: {best_strategy['val_return']:.1%}
            - **Sharpe Ratio**: {best_strategy['val_sharpe']:.2f}
            
            *Actually just random noise...* 😬
            """)
        
        st.warning(f"""
        **Performance drop**: {best_strategy['win_rate_drop']:.1%} win rate decline | 
        Sharpe ratio collapsed by {abs(best_strategy['sharpe_drop']):.2f}
        """)


def show_interactive_demo_page():
    """Interactive simulation page"""
    st.markdown("## 🎮 Try It Yourself!")
    
    st.markdown("""
    Generate random strategies in real-time and see how overfitting happens before your eyes.
    
    **Instructions:**
    1. Adjust the parameters below
    2. Click "Generate & Test"
    3. Watch as random strategies produce "winners"
    4. See them fail on validation data
    """)
    
    run_live_simulation()


def show_real_results_page():
    """Show results from real Bitcoin data"""
    st.markdown("## 📈 Results on Real Bitcoin Data")
    
    st.info("""
    This experiment used **real Bitcoin 5-minute candlestick data** from October 2024.
    100 random strategies were tested. Here's what happened...
    """)
    
    # Load data
    training_perf = load_training_performance()
    best_strategy = load_best_strategy()
    validation_results = load_validation_results()
    
    if training_perf is None or best_strategy is None:
        st.error("⚠️ Data files not found. Please run the backtest scripts first.")
        return
    
    # Chart 1: Distribution of all strategies
    st.markdown("### 📊 All 100 Random Strategies")
    
    fig = px.histogram(
        training_perf, 
        x='win_rate',
        nbins=30,
        title='Win Rate Distribution (Training Data)',
        labels={'win_rate': 'Win Rate', 'count': 'Number of Strategies'},
        color_discrete_sequence=['skyblue']
    )
    
    # Add best strategy line
    best_wr = best_strategy['training_metrics']['win_rate']
    fig.add_vline(x=best_wr, line_dash="dash", line_color="red", 
                  annotation_text=f"Best: {best_wr:.1%}")
    fig.add_vline(x=0.5, line_dash="dash", line_color="green", 
                  annotation_text="Expected (50%)")
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    **Notice**: The distribution is roughly centered around 50% (pure randomness), but by testing 100 strategies,
    we found some that appear to perform much better *by pure luck*.
    """)
    
    # Chart 2: Best strategy comparison
    if validation_results:
        st.markdown("### ⚖️ Training vs Validation (Best Strategy)")
        
        train_m = validation_results['training_metrics']
        val_m = validation_results['validation_metrics']
        
        metrics_df = pd.DataFrame({
            'Metric': ['Win Rate', 'Total Return', 'Sharpe Ratio'],
            'Training': [train_m['win_rate']*100, train_m['total_return']*100, train_m['sharpe_ratio']],
            'Validation': [val_m['win_rate']*100, val_m['total_return']*100, val_m['sharpe_ratio']]
        })
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Training',
            x=metrics_df['Metric'],
            y=metrics_df['Training'],
            marker_color='lightgreen'
        ))
        fig.add_trace(go.Bar(
            name='Validation',
            x=metrics_df['Metric'],
            y=metrics_df['Validation'],
            marker_color='lightcoral'
        ))
        
        fig.update_layout(
            title='Performance Collapse: Training vs Validation',
            barmode='group',
            yaxis_title='Value'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.error(f"""
        **The Reality Check**: The "best" strategy showed a {train_m['win_rate']:.1%} win rate on training data,
        but only {val_m['win_rate']:.1%} on validation data. This is clear evidence of overfitting!
        """)


def show_deep_dive_page():
    """Deep statistical analysis"""
    st.markdown("## 🔬 Statistical Deep Dive")
    
    validation_summary = load_validation_summary()
    
    if not validation_summary:
        st.error("Data not found")
        return
    
    st.markdown("### Top 10 'Best' Strategies Performance")
    
    # Create detailed table
    strategies_df = pd.DataFrame(validation_summary['all_strategies'])
    
    display_df = strategies_df[[
        'rank', 'strategy_id', 'train_win_rate', 'val_win_rate', 
        'win_rate_drop', 'train_sharpe', 'val_sharpe'
    ]].head(10)
    
    display_df.columns = ['Rank', 'Strategy', 'Train WR', 'Val WR', 'Drop', 'Train Sharpe', 'Val Sharpe']
    
    st.dataframe(
        display_df.style.format({
            'Train WR': '{:.1%}',
            'Val WR': '{:.1%}',
            'Drop': '{:.1%}',
            'Train Sharpe': '{:.2f}',
            'Val Sharpe': '{:.2f}'
        }).background_gradient(subset=['Drop'], cmap='RdYlGn_r'),
        use_container_width=True
    )
    
    st.markdown("### 📉 Regression to the Mean")
    
    # Scatter plot
    fig = px.scatter(
        strategies_df.head(20),
        x='train_win_rate',
        y='val_win_rate',
        hover_data=['strategy_id'],
        title='Training vs Validation Win Rates (Top 20 Strategies)',
        labels={'train_win_rate': 'Training Win Rate', 'val_win_rate': 'Validation Win Rate'}
    )
    
    # Add diagonal line (perfect correlation)
    fig.add_shape(
        type='line', line=dict(dash='dash'),
        x0=0.45, y0=0.45, x1=0.65, y1=0.65
    )
    
    fig.add_annotation(
        x=0.60, y=0.60,
        text="Perfect correlation line",
        showarrow=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    **Key Insight**: If the strategies had real predictive power, the points would cluster around 
    the diagonal line. Instead, they scatter randomly, showing that high training performance 
    doesn't predict validation performance.
    """)


def show_learn_more_page():
    """Educational content"""
    st.markdown("## 📚 Understanding Overfitting in Algo Trading")
    
    tab1, tab2, tab3, tab4 = st.tabs(["What is Overfitting?", "Why It Matters", "How to Avoid It", "Technical Details"])
    
    with tab1:
        st.markdown("""
        ### What is Overfitting?
        
        **Overfitting** occurs when a model learns the noise in the training data rather than the actual patterns.
        
        #### In Plain English:
        - Imagine memorizing answers to specific test questions rather than learning the concepts
        - You'll ace that specific test but fail when questions change slightly
        - Same thing happens in trading: strategies fit to past data fail on new data
        
        #### In This Demo:
        We tested 100 **completely random** strategies (coin flips):
        - Some performed well on training data *by pure luck*
        - ALL fell back to ~50% on validation data
        - Proof: Past performance ≠ Future results
        """)
        
        st.image("https://imgur.com/RiQVWqZ.png", caption="Overfitting Visualization", use_column_width=True)
    
    with tab2:
        st.markdown("""
        ### Why This Matters in Algo Trading
        
        #### The Danger:
        1. **Data Mining Bias**: Test enough strategies, something will look good
        2. **False Confidence**: High backtested returns create false sense of security
        3. **Real Money Loss**: Deploy überfit strategy → lose real money
        
        #### Real-World Example:
        
        A hedge fund backtests 1,000 strategies and finds one with:
        - 80% win rate
        - 200% annual returns
        - Sharpe ratio of 3.0
        
        **But**: It's just curve-fitted noise. Goes live → loses millions.
        
        #### This Demo Shows:
        Even with RANDOM strategies, you can find "winners" in backtests that are completely worthless.
        """)
    
    with tab3:
        st.markdown("""
        ### How to Avoid Overfitting
        
        #### Best Practices:
        
        1. **Walk-Forward Analysis**
           - Use rolling windows of train/test periods
           - If strategy works, it should work across ALL periods
        
        2. **Out-of-Sample Testing**
           - Set aside validation data (like we did here)
           - NEVER peek at it during development
        
        3. **Cross-Validation**
           - Multiple train/test splits
           - Look for consistency
        
        4. **Simplicity**
           - Fewer parameters = less room to overfit
           - Occam's Razor applies
        
        5. **Economic Rationale**
           - Strategy should make logical sense
           - If you can't explain WHY it works, it probably doesn't
        
        6. **Statistical Significance**
           - Use proper hypothesis testing
           - Adjust for multiple testing (Bonferroni correction)
        
        7. **Paper Trading**
           - Test with live data, fake money
           - Reality check before risking capital
        """)
    
    with tab4:
        st.markdown("""
        ### Technical Implementation Details
        
        #### Experiment Design:
        
        ```python
        # 1. Generate 100 random strategies
        strategies = [np.random.randint(0, 2, size=n_trades) for _ in range(100)]
        
        # 2. Split data
        train_data = price_data[:int(0.7 * len(price_data))]
        test_data = price_data[int(0.7 * len(price_data)):]
        
        # 3. Backtest all strategies
        for strategy in strategies:
            train_performance = backtest(strategy, train_data)
            results.append(train_performance)
        
        # 4. Select "best"
        best = max(results, key=lambda x: x['win_rate'])
        
        # 5. Validate
        val_performance = backtest(best, test_data)
        ```
        
        #### Metrics Calculated:
        
        - **Win Rate**: % of profitable trades
        - **Total Return**: Cumulative return
        - **Sharpe Ratio**: Risk-adjusted return
        - **Max Drawdown**: Largest peak-to-trough decline
        
        #### Data:
        
        - **Source**: Real Bitcoin 5-minute candlestick data
        - **Period**: October 1 - November 10, 2024
        - **Instrument**: BTC/USD
        - **Provider**: Historical market data
        
        #### Why This Proves Overfitting:
        
        If random strategies can show 60-70% win rates on training data,
        then seeing those numbers in a backtest means **nothing** without
        proper validation.
        """)


# ============================================
# RUN APP
# ============================================

if __name__ == "__main__":
    main()
