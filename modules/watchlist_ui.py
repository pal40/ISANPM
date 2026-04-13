import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.stock_list import search_stock
from modules.watchlist import add_to_watchlist, remove_from_watchlist, get_watchlist
from modules.history import save_analysis, get_analysis_history, get_latest_analysis
from modules.analysis_engine import run_full_analysis

def render_watchlist():
    st.header("📊 Watchlist & Intelligence")
    user_id = st.session_state.get("user_id")

    # 1. Search and Add
    with st.container():
        st.subheader("Add Stock")
        colA, colB = st.columns([3, 1])
        with colA:
            query = st.text_input("Search Indian Stocks (e.g., 'infy', 'hdfc')", key="wl_search")
            if query:
                results = search_stock(query)
                if results:
                    options = {f"{r['name']} ({r['ticker']})": r for r in results}
                    selected_label = st.selectbox("Select Stock", options.keys())
                    selected_stock = options[selected_label]
                    
                    with colB:
                        st.write("") # spacer
                        st.write("")
                        if st.button("Add to Watchlist"):
                            if add_to_watchlist(user_id, selected_stock['ticker'], selected_stock['name']):
                                st.success("Added successfully")
                                st.rerun()
                            else:
                                st.warning("Already in watchlist")
                else:
                    st.info("No matches found in standard list. Let us know to add it.")

    st.divider()

    # 2. Display Watchlist
    st.subheader("Your Watchlist")
    wl_items = get_watchlist(user_id)
    
    if not wl_items:
        st.info("Your watchlist is empty.")
        return

    # To create an action layout, we iterate rows
    for item in wl_items:
        with st.container():
            # Get latest analysis for summary display
            latest = get_latest_analysis(user_id, item['ticker'])
            
            c1, c2, c3, c4, c5 = st.columns([2, 1, 1, 1, 1])
            c1.markdown(f"**{item['display_name']}**")
            
            if latest:
                c2.write(f"Sc: **{latest['score']}**")
                color = "green" if latest['recommendation'] == "BUY" else "red" if latest['recommendation'] == "SELL" else "orange"
                c3.markdown(f"<span style='color:{color}; font-weight:bold;'>{latest['recommendation']}</span>", unsafe_allow_html=True)
                c4.write(f"₹{latest['price']:.2f}")
            else:
                c2.write("Not analyzed")
                c3.write("-")
                c4.write("-")
                
            with c5:
                # Use split buttons or popovers if stream>=1.30, but columns work well too.
                btn_col1, btn_col2 = st.columns(2)
                if btn_col1.button("🔍", key=f"analyze_{item['id']}", help="Analyze Now"):
                    with st.spinner("Analyzing..."):
                        result = run_full_analysis(item['ticker'])
                        save_analysis(user_id, result)
                        st.session_state["selected_watchlist_ticker"] = item['ticker']
                        st.rerun()
                if btn_col2.button("❌", key=f"remove_{item['id']}", help="Remove"):
                    remove_from_watchlist(item['id'])
                    st.rerun()
                    
            if st.button("View History", key=f"hist_{item['id']}"):
                st.session_state["selected_watchlist_ticker"] = item['ticker']
                
            st.write("---")

    # 3. Selected Stock History View
    selected_ticker = st.session_state.get("selected_watchlist_ticker")
    if selected_ticker:
        # Find display name
        disp_name = next((i['display_name'] for i in wl_items if i['ticker'] == selected_ticker), selected_ticker)
        st.subheader(f"History: {disp_name}")
        
        history = get_analysis_history(user_id, selected_ticker)
        if not history:
            st.info("No historical analysis snapshots available. Click 🔍 to analyze.")
        else:
            df = pd.DataFrame(history)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Show Latest Result prominent
            latest = df.iloc[0]
            fc1, fc2, fc3 = st.columns(3)
            rec = latest['recommendation']
            r_color = "green" if rec == "BUY" else "red" if rec == "SELL" else "orange"
            fc1.markdown(f"### <span style='color:{r_color}'>{rec}</span>", unsafe_allow_html=True)
            fc2.metric("Latest Score", latest['score'])
            fc3.metric("RSI", f"{latest['rsi']:.1f}" if pd.notna(latest['rsi']) else "N/A")
            
            st.write(f"Analyzed on: {latest['timestamp'].strftime('%Y-%m-%d %H:%M')}")
            
            # Historical Table
            st.write("**Past Snapshots**")
            display_df = df[['timestamp', 'price', 'score', 'recommendation', 'rsi', 'above_200_dma']].copy()
            st.dataframe(display_df, use_container_width=True)
            
            # Optional Line Chart of Score over time
            if len(df) > 1:
                df_sorted = df.sort_values(by="timestamp")
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=df_sorted['timestamp'], y=df_sorted['score'], mode='lines+markers', name='Score'))
                fig.update_layout(title="Analysis Score Over Time", xaxis_title="Date", yaxis_title="Score (0-10)", template="plotly_white")
                st.plotly_chart(fig, use_container_width=True)
        
        if st.button("Close History"):
            st.session_state["selected_watchlist_ticker"] = None
            st.rerun()
