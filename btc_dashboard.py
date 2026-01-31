import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
import os

# Page configuration
st.set_page_config(
    page_title="Bitcoin Analytics Dashboard",
    page_icon="₿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with advanced styling
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Poppins:wght@300;400;600;700&display=swap');
    
    /* Main container styling */
    .main {
        padding: 0rem 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Stale element fix */
    .stale-element {
        display: none;
    }
    
    /* Custom header */
    .crypto-header {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(245, 87, 108, 0.6);
    }
    
    .crypto-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 3.5rem;
        font-weight: 900;
        color: #FFFFFF;
        text-shadow: 3px 3px 8px rgba(0,0,0,0.5), 0 0 20px rgba(255,255,255,0.3);
        margin: 0;
        letter-spacing: 5px;
    }
    
    .crypto-subtitle {
        font-family: 'Poppins', sans-serif;
        font-size: 1.3rem;
        color: #FFFFFF;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        margin-top: 0.5rem;
        font-weight: 600;
    }
    
    /* Metric cards */
    [data-testid="stMetricLabel"] {
        font-size: 1.3rem !important;
        font-weight: 800 !important;
        color: #FFFFFF !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    [data-testid="stMetricValue"] {
        font-family: 'Orbitron', sans-serif;
        font-size: 2.5rem !important;
        font-weight: 900 !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 1.3rem !important;
        font-weight: 800 !important;
    }
    
    /* Metric container styling */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(240,242,246,0.95) 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        border-left: 5px solid #f093fb;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #0f0f1e 100%);
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: #FFFFFF;
        font-weight: 500;
    }
    
    [data-testid="stSidebar"] h3 {
        color: #FFFFFF !important;
        font-weight: 700 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-family: 'Poppins', sans-serif;
        font-size: 1.2rem;
        font-weight: 700;
        padding: 1rem 2rem;
        background: linear-gradient(135deg, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0.1) 100%);
        border-radius: 10px 10px 0 0;
        color: #FFFFFF;
        border: none;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: #FFFFFF;
        font-weight: 900;
        text-shadow: 2px 2px 6px rgba(0,0,0,0.6);
    }
    
    /* Button styling */
    .stDownloadButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 10px;
        font-family: 'Poppins', sans-serif;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Dataframe styling */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    /* Info boxes */
    .stAlert {
        border-radius: 10px;
        border-left: 5px solid #667eea;
        background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(240,242,246,0.95) 100%);
    }
    
    /* Input styling */
    .stTextInput input {
        border-radius: 10px;
        border: 2px solid #e2e8f0;
        padding: 0.75rem;
        font-family: 'Poppins', sans-serif;
    }
    
    .stTextInput input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Stats card */
    .stats-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(240,242,246,0.95) 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        margin: 1rem 0;
    }
    
    .stat-label {
        font-family: 'Poppins', sans-serif;
        font-size: 1.1rem;
        color: #FFFFFF;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    .stat-value {
        font-family: 'Orbitron', sans-serif;
        font-size: 2.2rem;
        font-weight: 900;
        color: #00d395;
        margin-top: 0.5rem;
        text-shadow: 0 2px 8px rgba(0,211,149,0.5);
    }
    
    /* Removed animations for stability */
    </style>
    """, unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    import os
    # Try multiple possible paths
    possible_paths = [
        r'c:\Users\Yuva sri\Downloads\btc_extended.csv',
        'btc_extended.csv',
        os.path.join(os.path.dirname(__file__), 'btc_extended.csv')
    ]
    
    df = None
    for path in possible_paths:
        if os.path.exists(path):
            df = pd.read_csv(path)
            break
    
    if df is None:
        raise FileNotFoundError("btc_extended.csv not found in any expected location")
    
    df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y %H:%M')
    df = df.sort_values('date')
    
    # Calculate technical indicators
    df['MA7'] = df['price'].rolling(window=7).mean()
    df['MA30'] = df['price'].rolling(window=30).mean()
    df['price_change'] = df['price'].pct_change() * 100
    df['volatility'] = df['price'].rolling(window=30).std()
    
    return df

# Custom header
st.markdown("""
    <div class="crypto-header">
        <h1 class="crypto-title">₿ BITCOIN ANALYTICS</h1>
        <p class="crypto-subtitle">Real-time Market Intelligence & Data Visualization</p>
    </div>
    """, unsafe_allow_html=True)

try:
    # Load the data
    df = load_data()
    
    # Sidebar filters
    st.sidebar.markdown("### 🎯 FILTERS & CONTROLS")
    st.sidebar.markdown("---")
    
    # Date range filter
    min_date = df['date'].min().date()
    max_date = df['date'].max().date()
    
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Filter data based on date range
    if len(date_range) == 2:
        mask = (df['date'].dt.date >= date_range[0]) & (df['date'].dt.date <= date_range[1])
        filtered_df = df[mask]
    else:
        filtered_df = df
    
    # Sidebar statistics
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 QUICK STATISTICS")
    
    st.sidebar.markdown(f"""
    <div class="stats-card">
        <div class="stat-label">Total Records</div>
        <div class="stat-value">{len(filtered_df)}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown(f"""
    <div class="stats-card">
        <div class="stat-label">Data Period</div>
        <div style="font-size: 0.95rem; color: #2d3748; margin-top: 0.5rem; font-weight: 600; line-height: 1.6;">
            <strong>{filtered_df['date'].min().strftime('%Y-%m-%d')}</strong><br>
            <span style="color: #718096;">to</span><br>
            <strong>{filtered_df['date'].max().strftime('%Y-%m-%d')}</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar chart option
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎨 DISPLAY OPTIONS")
    
    chart_theme = "plotly_dark"  # Fixed dark theme for better visibility
    show_ma = st.sidebar.checkbox("Show Moving Averages", value=True)
    
    # Key Metrics Row
    st.markdown('<div class="animated-content">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        current_price = filtered_df['price'].iloc[-1]
        price_change = filtered_df['price'].iloc[-1] - filtered_df['price'].iloc[0]
        price_change_pct = (price_change / filtered_df['price'].iloc[0]) * 100
        st.metric(
            label="💰 Current Price",
            value=f"${current_price:,.2f}",
            delta=f"{price_change_pct:.2f}%"
        )
    
    with col2:
        highest_price = filtered_df['price'].max()
        st.metric(
            label="📈 Highest Price",
            value=f"${highest_price:,.2f}",
            delta=f"+{((highest_price/filtered_df['price'].iloc[-1] - 1) * 100):.2f}%"
        )
    
    with col3:
        current_market_cap = filtered_df['market_cap'].iloc[-1]
        st.metric(
            label="💎 Market Cap",
            value=f"${current_market_cap/1e12:.3f}T"
        )
    
    with col4:
        total_volume = filtered_df['volume'].sum()
        st.metric(
            label="📊 Total Volume",
            value=f"${total_volume/1e12:.2f}T"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Additional metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_price = filtered_df['price'].mean()
        st.metric(
            label="📊 Average Price",
            value=f"${avg_price:,.2f}"
        )
    
    with col2:
        volatility = filtered_df['price'].std()
        st.metric(
            label="📉 Price Volatility",
            value=f"${volatility:,.2f}"
        )
    
    with col3:
        avg_volume = filtered_df['volume'].mean()
        st.metric(
            label="💹 Avg Daily Volume",
            value=f"${avg_volume/1e9:.2f}B"
        )
    
    with col4:
        price_range = filtered_df['price'].max() - filtered_df['price'].min()
        st.metric(
            label="↔️ Price Range",
            value=f"${price_range:,.2f}"
        )
    
    st.markdown("---")
    
    # Tabs for different views
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Price Analysis", 
        "💹 Market Cap", 
        "📊 Volume Analysis", 
        "🔬 Technical Analysis",
        "📋 Data Table"
    ])
    
    with tab1:
        st.markdown("<h2 style='color: #FFFFFF; font-weight: 900; text-shadow: 2px 2px 6px rgba(0,0,0,0.5); font-size: 2rem;'>🎯 Bitcoin Price Trend Analysis</h2>", unsafe_allow_html=True)
        
        # Price line chart with moving averages
        fig_price = go.Figure()
        
        # Main price line
        fig_price.add_trace(go.Scatter(
            x=filtered_df['date'],
            y=filtered_df['price'],
            mode='lines',
            name='BTC Price',
            line=dict(color='#f7931a', width=3),
            fill='tozeroy',
            fillcolor='rgba(247, 147, 26, 0.1)',
            hovertemplate='<b>Date</b>: %{x}<br><b>Price</b>: $%{y:,.2f}<extra></extra>'
        ))
        
        # Moving averages
        if show_ma:
            fig_price.add_trace(go.Scatter(
                x=filtered_df['date'],
                y=filtered_df['MA7'],
                mode='lines',
                name='7-Day MA',
                line=dict(color='#00d395', width=2, dash='dash'),
                hovertemplate='<b>7-Day MA</b>: $%{y:,.2f}<extra></extra>'
            ))
            
            fig_price.add_trace(go.Scatter(
                x=filtered_df['date'],
                y=filtered_df['MA30'],
                mode='lines',
                name='30-Day MA',
                line=dict(color='#667eea', width=2, dash='dot'),
                hovertemplate='<b>30-Day MA</b>: $%{y:,.2f}<extra></extra>'
            ))
        
        fig_price.update_layout(
            title={
                'text': "<b>Bitcoin Price Over Time</b>",
                'font': {'size': 30, 'family': 'Poppins, sans-serif', 'color': '#FFFFFF', 'weight': 'bold'}
            },
            xaxis_title="<b>Date</b>",
            yaxis_title="<b>Price (USD)</b>",
            xaxis=dict(
                tickfont=dict(size=14, color='#FFFFFF', family='Arial, sans-serif'),
                title=dict(text="<b>Date</b>", font=dict(size=18, color='#FFFFFF')),
                showgrid=True,
                gridcolor='rgba(255,255,255,0.2)',
                zeroline=False
            ),
            yaxis=dict(
                tickfont=dict(size=14, color='#FFFFFF', family='Arial, sans-serif'),
                title=dict(text="<b>Price (USD)</b>", font=dict(size=18, color='#FFFFFF')),
                showgrid=True,
                gridcolor='rgba(255,255,255,0.2)',
                zeroline=False
            ),
            hovermode='x unified',
            height=550,
            showlegend=True,
            template='plotly_dark',
            paper_bgcolor='#1a1a2e',
            plot_bgcolor='#16213e',
            font=dict(family='Arial, sans-serif', color='#FFFFFF', size=15),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor='rgba(0,0,0,0.5)',
                bordercolor='rgba(255,255,255,0.2)',
                borderwidth=1
            )
        )
        
        st.plotly_chart(fig_price, use_container_width=True)
        
        # Statistics grid
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="stats-card">
                <div class="stat-label">🎯 Highest Price</div>
                <div class="stat-value">${filtered_df['price'].max():,.2f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="stats-card">
                <div class="stat-label">📉 Lowest Price</div>
                <div class="stat-value">${filtered_df['price'].min():,.2f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="stats-card">
                <div class="stat-label">📊 Median Price</div>
                <div class="stat-value">${filtered_df['price'].median():,.2f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="stats-card">
                <div class="stat-label">📈 Std Deviation</div>
                <div class="stat-value">${filtered_df['price'].std():,.2f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Price distribution with better styling
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig_candlestick = go.Figure()
            
            # Create candlestick-like view using scatter
            fig_candlestick.add_trace(go.Scatter(
                x=filtered_df['date'],
                y=filtered_df['price'],
                mode='markers',
                name='Price Points',
                marker=dict(
                    size=8,
                    color=filtered_df['price'],
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title="Price ($)")
                ),
                hovertemplate='<b>Date</b>: %{x}<br><b>Price</b>: $%{y:,.2f}<extra></extra>'
            ))
            
            fig_candlestick.update_layout(
                title="<b>Price Point Distribution</b>",
                xaxis_title="<b>Date</b>",
                yaxis_title="<b>Price (USD)</b>",
                xaxis=dict(
                    tickfont=dict(size=14, color='#FFFFFF', family='Arial')
                ),
                yaxis=dict(
                    tickfont=dict(size=14, color='#FFFFFF', family='Arial')
                ),
                height=400,
                template='plotly_dark',
                paper_bgcolor='#1a1a2e',
                plot_bgcolor='#16213e',
                font=dict(family='Arial, sans-serif', color='#FFFFFF', size=15)
            )
            
            st.plotly_chart(fig_candlestick, use_container_width=True)
        
        with col2:
            # Price histogram
            fig_hist = go.Figure()
            
            fig_hist.add_trace(go.Histogram(
                x=filtered_df['price'],
                nbinsx=40,
                name='Price Distribution',
                marker=dict(
                    color='#667eea',
                    line=dict(color='white', width=1)
                )
            ))
            
            fig_hist.update_layout(
                title="<b>Price Distribution</b>",
                xaxis_title="<b>Price (USD)</b>",
                yaxis_title="<b>Frequency</b>",
                xaxis=dict(
                    tickfont=dict(size=14, color='#FFFFFF', family='Arial')
                ),
                yaxis=dict(
                    tickfont=dict(size=14, color='#FFFFFF', family='Arial')
                ),
                height=400,
                template='plotly_dark',
                paper_bgcolor='#1a1a2e',
                plot_bgcolor='#16213e',
                font=dict(family='Arial, sans-serif', color='#FFFFFF', size=15),
                showlegend=False
            )
            
            st.plotly_chart(fig_hist, use_container_width=True)
    
    with tab2:
        st.markdown("<h2 style='color: #FFFFFF; font-weight: 900; text-shadow: 2px 2px 6px rgba(0,0,0,0.5); font-size: 2rem;'>💎 Market Capitalization Analysis</h2>", unsafe_allow_html=True)
        
        # Market cap area chart with gradient
        fig_mcap = go.Figure()
        
        fig_mcap.add_trace(go.Scatter(
            x=filtered_df['date'],
            y=filtered_df['market_cap']/1e12,
            mode='lines',
            name='Market Cap',
            line=dict(color='#00d395', width=3),
            fill='tozeroy',
            fillcolor='rgba(0, 211, 149, 0.2)',
            hovertemplate='<b>Date</b>: %{x}<br><b>Market Cap</b>: $%{y:.3f}T<extra></extra>'
        ))
        
        fig_mcap.update_layout(
            title={
                'text': "<b>Bitcoin Market Capitalization Trend</b>",
                'font': {'size': 30, 'family': 'Poppins, sans-serif', 'color': '#FFFFFF', 'weight': 'bold'}
            },
            xaxis_title="<b>Date</b>",
            yaxis_title="<b>Market Cap (Trillion USD)</b>",
            xaxis=dict(
                tickfont=dict(size=14, color='#FFFFFF', family='Arial'),
                showgrid=True,
                gridcolor='rgba(255,255,255,0.3)'
            ),
            yaxis=dict(
                tickfont=dict(size=14, color='#FFFFFF', family='Arial'),
                showgrid=True,
                gridcolor='rgba(255,255,255,0.3)'
            ),
            hovermode='x unified',
            height=500,
            template='plotly_dark',
            paper_bgcolor='#1a1a2e',
            plot_bgcolor='#16213e',
            font=dict(family='Arial, sans-serif', color='#FFFFFF', size=15)
        )
        
        st.plotly_chart(fig_mcap, use_container_width=True)
        
        # Market cap statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="stats-card">
                <div class="stat-label">📈 Max Market Cap</div>
                <div class="stat-value">${filtered_df['market_cap'].max()/1e12:.3f}T</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="stats-card">
                <div class="stat-label">📉 Min Market Cap</div>
                <div class="stat-value">${filtered_df['market_cap'].min()/1e12:.3f}T</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="stats-card">
                <div class="stat-label">📊 Avg Market Cap</div>
                <div class="stat-value">${filtered_df['market_cap'].mean()/1e12:.3f}T</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            mcap_change = ((filtered_df['market_cap'].iloc[-1] - filtered_df['market_cap'].iloc[0]) / filtered_df['market_cap'].iloc[0] * 100)
            st.markdown(f"""
            <div class="stats-card">
                <div class="stat-label">💹 Growth Rate</div>
                <div class="stat-value">{mcap_change:+.2f}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Market cap vs price correlation
        fig_correlation = go.Figure()
        
        # Convert dates to numeric for color mapping
        date_numeric = (filtered_df['date'] - filtered_df['date'].min()).dt.total_seconds()
        
        fig_correlation.add_trace(go.Scatter(
            x=filtered_df['price'],
            y=filtered_df['market_cap']/1e12,
            mode='markers',
            name='Market Cap vs Price',
            marker=dict(
                size=10,
                color=date_numeric,
                colorscale='Turbo',
                showscale=True,
                colorbar=dict(title="Time"),
                opacity=0.7,
                line=dict(width=1, color='white')
            ),
            hovertemplate='<b>Price</b>: $%{x:,.2f}<br><b>Market Cap</b>: $%{y:.3f}T<extra></extra>'
        ))
        
        fig_correlation.update_layout(
            title="<b>Market Cap vs Price Correlation</b>",
            xaxis_title="<b>Price (USD)</b>",
            yaxis_title="<b>Market Cap (Trillion USD)</b>",
            xaxis=dict(
                tickfont=dict(size=14, color='#FFFFFF', family='Arial')
            ),
            yaxis=dict(
                tickfont=dict(size=14, color='#FFFFFF', family='Arial')
            ),
            height=450,
            template='plotly_dark',
            paper_bgcolor='#1a1a2e',
            plot_bgcolor='#16213e',
            font=dict(family='Arial, sans-serif', color='#FFFFFF', size=15)
        )
        
        st.plotly_chart(fig_correlation, use_container_width=True)
    
    with tab3:
        st.markdown("<h2 style='color: #FFFFFF; font-weight: 900; text-shadow: 2px 2px 6px rgba(0,0,0,0.5); font-size: 2rem;'>📊 Trading Volume Analysis</h2>", unsafe_allow_html=True)
        
        # Volume bar chart with gradient colors
        fig_volume = go.Figure()
        
        # Create color gradient based on volume
        colors = filtered_df['volume'].values
        
        fig_volume.add_trace(go.Bar(
            x=filtered_df['date'],
            y=filtered_df['volume']/1e9,
            name='Trading Volume',
            marker=dict(
                color=colors,
                colorscale='Plasma',
                showscale=True,
                colorbar=dict(title="Volume ($B)"),
                line=dict(color='rgba(255,255,255,0.2)', width=0.5)
            ),
            hovertemplate='<b>Date</b>: %{x}<br><b>Volume</b>: $%{y:.2f}B<extra></extra>'
        ))
        
        fig_volume.update_layout(
            title={
                'text': "<b>Bitcoin Trading Volume Over Time</b>",
                'font': {'size': 30, 'family': 'Poppins, sans-serif', 'color': '#FFFFFF', 'weight': 'bold'}
            },
            xaxis_title="<b>Date</b>",
            yaxis_title="<b>Volume (Billion USD)</b>",
            xaxis=dict(
                tickfont=dict(size=14, color='#FFFFFF', family='Arial'),
                showgrid=False
            ),
            yaxis=dict(
                tickfont=dict(size=14, color='#FFFFFF', family='Arial'),
                showgrid=True,
                gridcolor='rgba(255,255,255,0.3)'
            ),
            hovermode='x unified',
            height=500,
            template='plotly_dark',
            paper_bgcolor='#1a1a2e',
            plot_bgcolor='#16213e',
            font=dict(family='Arial, sans-serif', color='#FFFFFF', size=15)
        )
        
        st.plotly_chart(fig_volume, use_container_width=True)
        
        # Volume statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="stats-card">
                <div class="stat-label">📈 Max Volume</div>
                <div class="stat-value">${filtered_df['volume'].max()/1e9:.2f}B</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="stats-card">
                <div class="stat-label">📉 Min Volume</div>
                <div class="stat-value">${filtered_df['volume'].min()/1e9:.2f}B</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="stats-card">
                <div class="stat-label">📊 Avg Volume</div>
                <div class="stat-value">${filtered_df['volume'].mean()/1e9:.2f}B</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="stats-card">
                <div class="stat-label">💰 Total Volume</div>
                <div class="stat-value">${filtered_df['volume'].sum()/1e12:.2f}T</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Volume vs Price scatter
        col1, col2 = st.columns(2)
        
        with col1:
            fig_vol_price = go.Figure()
            
            fig_vol_price.add_trace(go.Scatter(
                x=filtered_df['volume']/1e9,
                y=filtered_df['price'],
                mode='markers',
                name='Volume vs Price',
                marker=dict(
                    size=8,
                    color=filtered_df['price'],
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title="Price ($)"),
                    opacity=0.7,
                    line=dict(width=1, color='white')
                ),
                hovertemplate='<b>Volume</b>: $%{x:.2f}B<br><b>Price</b>: $%{y:,.2f}<extra></extra>'
            ))
            
            fig_vol_price.update_layout(
                title="<b>Volume vs Price Relationship</b>",
                xaxis_title="<b>Volume (Billion USD)</b>",
                yaxis_title="<b>Price (USD)</b>",
                xaxis=dict(
                    tickfont=dict(size=14, color='#FFFFFF', family='Arial')
                ),
                yaxis=dict(
                    tickfont=dict(size=14, color='#FFFFFF', family='Arial')
                ),
                height=400,
                template='plotly_dark',
                paper_bgcolor='#1a1a2e',
                plot_bgcolor='#16213e',
                font=dict(family='Arial, sans-serif', color='#FFFFFF', size=15)
            )
            
            st.plotly_chart(fig_vol_price, use_container_width=True)
        
        with col2:
            # Volume distribution
            fig_vol_dist = go.Figure()
            
            fig_vol_dist.add_trace(go.Box(
                y=filtered_df['volume']/1e9,
                name='Volume Distribution',
                marker=dict(color='#667eea'),
                boxmean='sd'
            ))
            
            fig_vol_dist.update_layout(
                title="<b>Volume Distribution (Box Plot)</b>",
                yaxis_title="<b>Volume (Billion USD)</b>",
                yaxis=dict(
                    tickfont=dict(size=14, color='#FFFFFF', family='Arial')
                ),
                height=400,
                template='plotly_dark',
                paper_bgcolor='#1a1a2e',
                plot_bgcolor='#16213e',
                font=dict(family='Arial, sans-serif', color='#FFFFFF', size=15),
                showlegend=False
            )
            
            st.plotly_chart(fig_vol_dist, use_container_width=True)
    
    with tab4:
        st.markdown("<h2 style='color: #FFFFFF; font-weight: 900; text-shadow: 2px 2px 6px rgba(0,0,0,0.5); font-size: 2rem;'>🔬 Technical Analysis</h2>", unsafe_allow_html=True)
        
        # Price change analysis
        col1, col2 = st.columns(2)
        
        with col1:
            # Price change percentage
            fig_change = go.Figure()
            
            fig_change.add_trace(go.Scatter(
                x=filtered_df['date'],
                y=filtered_df['price_change'],
                mode='lines',
                name='Price Change %',
                line=dict(color='#f093fb', width=2),
                fill='tozeroy',
                fillcolor='rgba(240, 147, 251, 0.2)',
                hovertemplate='<b>Date</b>: %{x}<br><b>Change</b>: %{y:.2f}%<extra></extra>'
            ))
            
            fig_change.update_layout(
                title="<b>Daily Price Change (%)</b>",
                xaxis_title="<b>Date</b>",
                yaxis_title="<b>Price Change (%)</b>",
                xaxis=dict(
                    tickfont=dict(size=14, color='#FFFFFF', family='Arial'),
                    showgrid=True,
                    gridcolor='rgba(255,255,255,0.3)'
                ),
                yaxis=dict(
                    tickfont=dict(size=14, color='#FFFFFF', family='Arial'),
                    showgrid=True,
                    gridcolor='rgba(255,255,255,0.3)',
                    zeroline=True,
                    zerolinecolor='white'
                ),
                height=400,
                template='plotly_dark',
                paper_bgcolor='#1a1a2e',
                plot_bgcolor='#16213e',
                font=dict(family='Arial, sans-serif', color='#FFFFFF', size=15)
            )
            
            st.plotly_chart(fig_change, use_container_width=True)
        
        with col2:
            # Volatility
            fig_volatility = go.Figure()
            
            fig_volatility.add_trace(go.Scatter(
                x=filtered_df['date'],
                y=filtered_df['volatility'],
                mode='lines',
                name='30-Day Volatility',
                line=dict(color='#f5576c', width=2),
                fill='tozeroy',
                fillcolor='rgba(245, 87, 108, 0.2)',
                hovertemplate='<b>Date</b>: %{x}<br><b>Volatility</b>: $%{y:,.2f}<extra></extra>'
            ))
            
            fig_volatility.update_layout(
                title="<b>30-Day Price Volatility</b>",
                xaxis_title="<b>Date</b>",
                yaxis_title="<b>Volatility (USD)</b>",
                xaxis=dict(
                    tickfont=dict(size=14, color='#FFFFFF', family='Arial'),
                    showgrid=True,
                    gridcolor='rgba(255,255,255,0.3)'
                ),
                yaxis=dict(
                    tickfont=dict(size=14, color='#FFFFFF', family='Arial'),
                    showgrid=True,
                    gridcolor='rgba(255,255,255,0.3)'
                ),
                height=400,
                template='plotly_dark',
                paper_bgcolor='#1a1a2e',
                plot_bgcolor='#16213e',
                font=dict(family='Arial, sans-serif', color='#FFFFFF', size=15)
            )
            
            st.plotly_chart(fig_volatility, use_container_width=True)
        
        # Technical indicators stats
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_change = filtered_df['price_change'].mean()
            st.markdown(f"""
            <div class="stats-card">
                <div class="stat-label">📊 Avg Daily Change</div>
                <div class="stat-value">{avg_change:+.2f}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            max_gain = filtered_df['price_change'].max()
            st.markdown(f"""
            <div class="stats-card">
                <div class="stat-label">📈 Max Daily Gain</div>
                <div class="stat-value">+{max_gain:.2f}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            max_loss = filtered_df['price_change'].min()
            st.markdown(f"""
            <div class="stats-card">
                <div class="stat-label">📉 Max Daily Loss</div>
                <div class="stat-value">{max_loss:.2f}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            avg_volatility = filtered_df['volatility'].mean()
            st.markdown(f"""
            <div class="stats-card">
                <div class="stat-label">📊 Avg Volatility</div>
                <div class="stat-value">${avg_volatility:,.2f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Comprehensive price chart with all indicators
        st.markdown("<h3 style='color: #FFFFFF; font-weight: 800; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); font-size: 1.5rem;'>📈 Comprehensive Price Chart with Indicators</h3>", unsafe_allow_html=True)
        
        fig_comprehensive = go.Figure()
        
        # Price
        fig_comprehensive.add_trace(go.Scatter(
            x=filtered_df['date'],
            y=filtered_df['price'],
            mode='lines',
            name='Price',
            line=dict(color='#f7931a', width=3)
        ))
        
        # Moving averages
        fig_comprehensive.add_trace(go.Scatter(
            x=filtered_df['date'],
            y=filtered_df['MA7'],
            mode='lines',
            name='7-Day MA',
            line=dict(color='#00d395', width=2, dash='dash')
        ))
        
        fig_comprehensive.add_trace(go.Scatter(
            x=filtered_df['date'],
            y=filtered_df['MA30'],
            mode='lines',
            name='30-Day MA',
            line=dict(color='#667eea', width=2, dash='dot')
        ))
        
        fig_comprehensive.update_layout(
            xaxis_title="<b>Date</b>",
            yaxis_title="<b>Price (USD)</b>",
            xaxis=dict(
                tickfont=dict(size=14, color='#FFFFFF', family='Arial'),
                showgrid=True,
                gridcolor='rgba(255,255,255,0.3)'
            ),
            yaxis=dict(
                tickfont=dict(size=14, color='#FFFFFF', family='Arial'),
                showgrid=True,
                gridcolor='rgba(255,255,255,0.3)'
            ),
            height=500,
            template='plotly_dark',
            paper_bgcolor='#1a1a2e',
            plot_bgcolor='#16213e',
            font=dict(family='Arial, sans-serif', color='#FFFFFF', size=15),
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor='rgba(0,0,0,0.5)'
            )
        )
        
        st.plotly_chart(fig_comprehensive, use_container_width=True)
    
    with tab5:
        st.markdown("<h2 style='color: #FFFFFF; font-weight: 900; text-shadow: 2px 2px 6px rgba(0,0,0,0.5); font-size: 2rem;'>📋 Interactive Data Table</h2>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Search functionality
            search_term = st.text_input("🔍 Search in table", "", placeholder="Enter search term...")
        
        with col2:
            # Display options
            rows_per_page = st.selectbox("Rows per page", [10, 25, 50, 100, 500], index=2)
        
        # Prepare display dataframe
        display_df = filtered_df.copy()
        display_df['date'] = display_df['date'].dt.strftime('%Y-%m-%d %H:%M')
        display_df['price'] = display_df['price'].apply(lambda x: f"${x:,.2f}")
        display_df['market_cap'] = display_df['market_cap'].apply(lambda x: f"${x:,.0f}")
        display_df['volume'] = display_df['volume'].apply(lambda x: f"${x:,.0f}")
        
        # Apply search filter
        if search_term:
            mask = display_df.astype(str).apply(lambda row: row.str.contains(search_term, case=False).any(), axis=1)
            display_df = display_df[mask]
        
        # Display summary
        st.markdown(f"<p style='color: #FFFFFF; font-size: 1.2rem; font-weight: 700; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);'>Showing <span style='color: #f093fb; font-size: 1.4rem;'>{len(display_df)}</span> records</p>", unsafe_allow_html=True)
        
        # Display dataframe with pagination
        st.dataframe(
            display_df[['date', 'price', 'market_cap', 'volume']].tail(rows_per_page),
            use_container_width=True,
            height=500
        )
        
        # Download section
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            # Download button
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name=f"bitcoin_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        with col2:
            # Download JSON
            json_data = filtered_df.to_json(orient='records', date_format='iso')
            st.download_button(
                label="📥 Download as JSON",
                data=json_data,
                file_name=f"bitcoin_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    # Additional Analysis Section
    st.markdown("---")
    st.markdown("<h2 style='color: #FFFFFF; font-weight: 900; text-shadow: 2px 2px 6px rgba(0,0,0,0.5); font-size: 2rem; text-align: center;'>🎯 Advanced Correlation Analysis</h2>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Price vs Volume scatter with trendline
        fig_scatter = go.Figure()
        
        fig_scatter.add_trace(go.Scatter(
            x=filtered_df['volume']/1e9,
            y=filtered_df['price'],
            mode='markers',
            name='Price vs Volume',
            marker=dict(
                size=10,
                color=filtered_df['price'],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Price ($)"),
                opacity=0.6,
                line=dict(width=1, color='white')
            ),
            hovertemplate='<b>Volume</b>: $%{x:.2f}B<br><b>Price</b>: $%{y:,.2f}<extra></extra>'
        ))
        
        # Add trendline
        z = np.polyfit(filtered_df['volume']/1e9, filtered_df['price'], 1)
        p = np.poly1d(z)
        fig_scatter.add_trace(go.Scatter(
            x=sorted(filtered_df['volume']/1e9),
            y=p(sorted(filtered_df['volume']/1e9)),
            mode='lines',
            name='Trend Line',
            line=dict(color='#f5576c', width=3, dash='dash')
        ))
        
        fig_scatter.update_layout(
            title="<b>Price vs Volume Correlation</b>",
            xaxis_title="<b>Trading Volume (Billion USD)</b>",
            yaxis_title="<b>Price (USD)</b>",
            xaxis=dict(
                tickfont=dict(size=14, color='#FFFFFF', family='Arial'),
                showgrid=True,
                gridcolor='rgba(255,255,255,0.3)'
            ),
            yaxis=dict(
                tickfont=dict(size=14, color='#FFFFFF', family='Arial'),
                showgrid=True,
                gridcolor='rgba(255,255,255,0.3)'
            ),
            height=450,
            template='plotly_dark',
            paper_bgcolor='#1a1a2e',
            plot_bgcolor='#16213e',
            font=dict(family='Arial, sans-serif', color='#FFFFFF', size=15)
        )
        
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    with col2:
        # Price vs Market Cap scatter with trendline
        fig_scatter2 = go.Figure()
        
        fig_scatter2.add_trace(go.Scatter(
            x=filtered_df['market_cap']/1e12,
            y=filtered_df['price'],
            mode='markers',
            name='Price vs Market Cap',
            marker=dict(
                size=10,
                color=filtered_df['volume'],
                colorscale='Plasma',
                showscale=True,
                colorbar=dict(title="Volume ($)"),
                opacity=0.6,
                line=dict(width=1, color='white')
            ),
            hovertemplate='<b>Market Cap</b>: $%{x:.3f}T<br><b>Price</b>: $%{y:,.2f}<extra></extra>'
        ))
        
        # Add trendline
        z2 = np.polyfit(filtered_df['market_cap']/1e12, filtered_df['price'], 1)
        p2 = np.poly1d(z2)
        fig_scatter2.add_trace(go.Scatter(
            x=sorted(filtered_df['market_cap']/1e12),
            y=p2(sorted(filtered_df['market_cap']/1e12)),
            mode='lines',
            name='Trend Line',
            line=dict(color='#f093fb', width=3, dash='dash')
        ))
        
        fig_scatter2.update_layout(
            title="<b>Price vs Market Cap Correlation</b>",
            xaxis_title="<b>Market Cap (Trillion USD)</b>",
            yaxis_title="<b>Price (USD)</b>",
            xaxis=dict(
                tickfont=dict(size=14, color='#FFFFFF', family='Arial'),
                showgrid=True,
                gridcolor='rgba(255,255,255,0.3)'
            ),
            yaxis=dict(
                tickfont=dict(size=14, color='#FFFFFF', family='Arial'),
                showgrid=True,
                gridcolor='rgba(255,255,255,0.3)'
            ),
            height=450,
            template='plotly_dark',
            paper_bgcolor='#1a1a2e',
            plot_bgcolor='#16213e',
            font=dict(family='Arial, sans-serif', color='#FFFFFF', size=15)
        )
        
        st.plotly_chart(fig_scatter2, use_container_width=True)

except FileNotFoundError:
    st.error("❌ Error: 'btc_extended.csv' file not found!")
    st.info(r"Please make sure the CSV file is at: c:\Users\Yuva sri\Downloads\btc_extended.csv")
except Exception as e:
    st.error(f"❌ An error occurred: {str(e)}")
    st.info("Please check your data file format.")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); border-radius: 15px; margin-top: 2rem;'>
        <p style='font-family: "Orbitron", sans-serif; font-size: 1.2rem; color: white; margin: 0;'>
            <strong>₿ Bitcoin Analytics Dashboard</strong>
        </p>
        <p style='font-family: "Poppins", sans-serif; font-size: 0.9rem; color: rgba(255,255,255,0.7); margin-top: 0.5rem;'>
            Powered by Streamlit & Plotly | Data Source: btc_extended.csv
        </p>
        <p style='font-family: "Poppins", sans-serif; font-size: 0.8rem; color: rgba(255,255,255,0.5); margin-top: 0.5rem;'>
            © 2026 | Built with ❤️ for Bitcoin Analytics
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
