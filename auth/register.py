import streamlit as st
from database.db import get_session
from database.models import User
from auth.auth_utils import hash_password

def render_register():
    st.subheader("Create a new account")
    
    with st.form("register_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        submit_button = st.form_submit_button("Register")
        
    if submit_button:
        if not username or not password:
            st.error("Please fill in all fields.")
            return
            
        if password != confirm_password:
            st.error("Passwords do not match.")
            return
            
        session = get_session()
        try:
            # Check if user exists
            existing_user = session.query(User).filter(User.username == username).first()
            if existing_user:
                st.error("Username already exists. Please choose a different one.")
                return
                
            # Create user
            hashed_pwd = hash_password(password)
            new_user = User(username=username, password_hash=hashed_pwd)
            session.add(new_user)
            session.commit()
            
            st.success("Registration successful! You can now log in.")
        except Exception as e:
            session.rollback()
            st.error(f"An error occurred: {str(e)}")
        finally:
            session.close()
