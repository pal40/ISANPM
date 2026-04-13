import streamlit as st

# Configure the Streamlit page setting BEFORE any other st commands
st.set_page_config(
    page_title="Institutional Portfolio Manager",
    page_icon="📈",
    layout="wide"
)

from database.db import init_db
from auth.login import render_login
from auth.register import render_register
from modules.stock_analysis import render_stock_analysis
from modules.portfolio import render_portfolio
from modules.watchlist_ui import render_watchlist

# Initialize database
init_db()

# Initialize session state for authentication
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

def main():
    st.title("🏛️ Institutional Stock Analysis & Portfolio Manager")
    
    if not st.session_state["logged_in"]:
        # Unauthenticated UI
        tab_login, tab_register = st.tabs(["Login", "Register"])
        with tab_login:
            render_login()
        with tab_register:
            render_register()
    else:
        # Authenticated UI
        with st.sidebar:
            st.write(f"Logged in as: **{st.session_state.get('username', 'User')}**")
            if st.button("Logout"):
                st.session_state.clear()
                st.rerun()
                
        # Main Tabs
        tab1, tab2, tab3 = st.tabs([
            "📈 Stock Analysis",
            "💼 Portfolio",
            "📊 Watchlist"
        ])
        
        with tab1:
            render_stock_analysis()
            
        with tab2:
            render_portfolio()
            
        with tab3:
            render_watchlist()

if __name__ == "__main__":
    main()
