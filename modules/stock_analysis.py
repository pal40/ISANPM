import streamlit as st
import plotly.graph_objects as go
from modules.analysis_engine import run_full_analysis

def render_stock_analysis():
    st.header("📈 Stock Analysis")
    
    ticker = st.text_input("Enter Stock Ticker (e.g., INFY.NS, AAPL)", value="INFY.NS").upper()
    
    if st.button("Analyze Stock"):
        with st.spinner(f"Fetching data and analyzing {ticker}..."):
            result = run_full_analysis(ticker)
            
            if "error" in result:
                st.error(result["error"])
                return
            
            # Display Core Metrics
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Current Price", f"₹{result['current_price']:.2f}")
            col2.metric("Fundamental Score", f"{result['fund_score']} / 10")
            
            rec = result["recommendation"]
            rec_color = "green" if rec == "BUY" else "red" if rec == "SELL" else "orange"
            col3.markdown(f"**Recommendation**<br><h3 style='color: {rec_color}; margin:0;'>{rec}</h3>", unsafe_allow_html=True)
            
            rsi_val = result['rsi']
            rsi_text = f"{rsi_val:.1f}" if rsi_val else "N/A"
            col4.metric("RSI (14)", rsi_text)
            
            st.divider()
            
            # Detailed Breakdown
            st.subheader("Technical & Fundamental Details")
            d_col1, d_col2 = st.columns(2)
            with d_col1:
                st.write("**Technicals:**")
                st.write(f"- **50 DMA**: {result['dma_50']:.2f}" if result['dma_50'] else "- **50 DMA**: N/A")
                st.write(f"- **200 DMA**: {result['dma_200']:.2f}" if result['dma_200'] else "- **200 DMA**: N/A")
                st.write(f"- **Support (Est)**: {result['support']:.2f}" if result['support'] else "- **Support**: N/A")
                st.write(f"- **Resistance (Est)**: {result['resistance']:.2f}" if result['resistance'] else "- **Resistance**: N/A")
                st.write(f"- **Signal Sentiment**: {result['sentiment']}")
                
            with d_col2:
                st.write("**Fundamentals:**")
                f = result.get('fundamentals', {})
                pe = f.get('pe_ratio')
                roe = f.get('roe')
                rev = f.get('revenue_growth')
                st.write(f"- **P/E Ratio**: {pe:.2f}" if pe else "- **P/E Ratio**: N/A")
                st.write(f"- **ROE**: {roe*100:.2f}%" if roe else "- **ROE**: N/A")
                st.write(f"- **Rev Growth**: {rev*100:.2f}%" if rev else "- **Rev Growth**: N/A")

            # Charting
            st.subheader("Price Chart")
            df = result['price_history']
            if df is not None and not df.empty:
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Price', line=dict(color='blue')))
                
                # Try to add moving averages to chart if calculated inline
                if len(df) >= 50:
                    df['SMA_50'] = df['Close'].rolling(window=50).mean()
                    fig.add_trace(go.Scatter(x=df.index, y=df['SMA_50'], mode='lines', name='50 DMA', line=dict(color='orange')))
                if len(df) >= 200:
                    df['SMA_200'] = df['Close'].rolling(window=200).mean()
                    fig.add_trace(go.Scatter(x=df.index, y=df['SMA_200'], mode='lines', name='200 DMA', line=dict(color='red')))
                
                fig.update_layout(title=f"{ticker} Price History", xaxis_title="Date", yaxis_title="Price", template="plotly_white")
                st.plotly_chart(fig, use_container_width=True)
