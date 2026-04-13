import streamlit as st
from database.db import get_session
from database.models import User
from auth.auth_utils import verify_password

def render_login():
    st.subheader("Login to your account")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        submit_button = st.form_submit_button("Login")
        
    if submit_button:
        if not username or not password:
            st.error("Please fill in all fields.")
            return
            
        session = get_session()
        try:
            # Find user
            user = session.query(User).filter(User.username == username).first()
            
            if user and verify_password(password, user.password_hash):
                st.session_state["logged_in"] = True
                st.session_state["user_id"] = user.id
                st.session_state["username"] = user.username
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid username or password.")
        finally:
            session.close()
