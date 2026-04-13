import streamlit as st
import pandas as pd
import plotly.express as px
from database.db import get_session
from database.models import Portfolio
from utils.data_fetcher import fetch_current_price

def render_portfolio():
    st.header("💼 Portfolio Management")
    user_id = st.session_state.get("user_id")
    
    # Add Stock Section
    with st.expander("➕ Add Stock to Portfolio", expanded=False):
        with st.form("add_portfolio_form", clear_on_submit=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                ticker = st.text_input("Ticker (e.g. INFY.NS)")
            with col2:
                quantity = st.number_input("Quantity", min_value=0.01, step=1.0)
            with col3:
                buy_price = st.number_input("Buy Price", min_value=0.01, step=1.0)
            
            submit = st.form_submit_button("Add to Portfolio")
            if submit and ticker and quantity > 0 and buy_price > 0:
                ticker = ticker.upper()
                session = get_session()
                try:
                    new_pos = Portfolio(user_id=user_id, ticker=ticker, quantity=quantity, buy_price=buy_price)
                    session.add(new_pos)
                    session.commit()
                    st.success(f"Added {quantity} shares of {ticker}!")
                    st.rerun()
                except Exception as e:
                    session.rollback()
                    st.error(f"Failed to add: {e}")
                finally:
                    session.close()

    # Portfolio Display
    st.subheader("Your Holdings")
    
    session = get_session()
    try:
        holdings = session.query(Portfolio).filter(Portfolio.user_id == user_id).all()
        
        if not holdings:
            st.info("Your portfolio is empty. Add some stocks to see tracking metrics.")
            return

        portfolio_data = []
        total_invested = 0.0
        total_current = 0.0
        
        # We need distinct tickers to fetch prices efficiently
        tickers = list(set([h.ticker for h in holdings]))
        current_prices = {}
        for t in tickers:
            p = fetch_current_price(t)
            current_prices[t] = p if p is not None else 0.0

        for h in holdings:
            inv_value = h.quantity * h.buy_price
            cp = current_prices.get(h.ticker, 0.0)
            cur_value = h.quantity * cp
            pnl_pct = ((cp - h.buy_price) / h.buy_price * 100) if h.buy_price > 0 else 0
            
            total_invested += inv_value
            total_current += cur_value
            
            portfolio_data.append({
                "ID": h.id,
                "Ticker": h.ticker,
                "Quantity": h.quantity,
                "Buy Price": f"₹{h.buy_price:.2f}",
                "Current Price": f"₹{cp:.2f}",
                "Invested": f"₹{inv_value:.2f}",
                "Current Value": f"₹{cur_value:.2f}",
                "P&L %": pnl_pct,
                "Raw_Current_Value": cur_value # for pie chart
            })

        # Summary Metrics
        st.write("### Summary")
        s_col1, s_col2, s_col3 = st.columns(3)
        s_col1.metric("Total Invested", f"₹{total_invested:.2f}")
        s_col2.metric("Total Current Value", f"₹{total_current:.2f}")
        
        total_pnl = total_current - total_invested
        total_pnl_pct = (total_pnl / total_invested * 100) if total_invested > 0 else 0
        s_col3.metric("Overall P&L", f"₹{total_pnl:.2f}", f"{total_pnl_pct:.2f}%")

        st.divider()

        # Display Table
        df = pd.DataFrame(portfolio_data)
        # Style P&L column
        def style_pnl(val):
            color = 'green' if val > 0 else 'red' if val < 0 else 'grey'
            return f'color: {color}'
        
        display_df = df.drop(columns=["ID", "Raw_Current_Value"])
        styled_df = display_df.style.map(style_pnl, subset=['P&L %']).format({'P&L %': "{:.2f}%"})
        st.dataframe(styled_df, use_container_width=True)

        # Rebalancing warnings and Allocation Breakdown
        st.subheader("Allocation & Analysis")
        colA, colB = st.columns([1, 1])
        
        with colA:
            # Rebalancing warning: if any stock > 40%
            warnings = []
            for _, row in df.iterrows():
                weight = row["Raw_Current_Value"] / total_current if total_current > 0 else 0
                if weight > 0.40:
                    warnings.append(f"⚠️ **{row['Ticker']}** is {weight*100:.1f}% of your portfolio (>40%). Consider rebalancing.")
            
            if warnings:
                st.warning("Rebalancing Alerts:\n" + "\n".join(warnings))
            else:
                st.success("Your portfolio is well-balanced (no single position > 40%).")
                
            st.write("To remove positions, a delete feature needs adding.")

        with colB:
            # Pie Chart
            if total_current > 0:
                pie_df = df.groupby('Ticker')['Raw_Current_Value'].sum().reset_index()
                fig = px.pie(pie_df, values='Raw_Current_Value', names='Ticker', title="Asset Allocation")
                st.plotly_chart(fig, use_container_width=True)

    finally:
        session.close()
