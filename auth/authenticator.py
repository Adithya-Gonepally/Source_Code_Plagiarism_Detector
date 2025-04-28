import streamlit as st
import pandas as pd
import hashlib
from datetime import datetime
import os
import pandas as pd

# CSV file path
USER_DB = os.path.join(os.path.dirname(__file__), "users.csv")

def load_users() -> pd.DataFrame:
    """
    Ensure users.csv exists (with headers + admin row), then return it.
    """
    # 1) If the file doesn't exist, create it with headers
    if not os.path.exists(USER_DB):
        df = pd.DataFrame(columns=[
            "username", "password", "role", "approved", "last_activity"
        ])
        # 2) Seed the default admin
        admin_row = {
            "username": "admin",
            "password": hash_password("admin123"),  # same default you log in with
            "role": "admin",
            "approved": True,
            "last_activity": "NA"
        }
        df = pd.concat([df, pd.DataFrame([admin_row])], ignore_index=True)
        df.to_csv(USER_DB, index=False)

    # 3) Now read and return
    return pd.read_csv(USER_DB)



# ---------------------------
# Password Hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ---------------------------
# Save User Data
def save_users(users_df):
    users_df.to_csv(USER_DB, index=False)


# ---------------------------
# Authenticate User
def authenticate_user(username, password):
    users = load_users()
    user = users[users['username'] == username]
    if not user.empty:
        hashed_password = hash_password(password)
        if user.iloc[0]['password'] == hashed_password:
            return user.iloc[0]
    return None

def register_user(username: str, password: str):
    users = load_users()
    if username in users["username"].values:
        st.warning("Username already exists!")
        return False

    new_row = {
        "username": username,
        "password": hash_password(password),
        "role": "user",
        "approved": False,
        "last_activity": "NA"
    }
    users = pd.concat([users, pd.DataFrame([new_row])], ignore_index=True)
    save_users(users)
    st.success("Registered! Waiting for admin approval.")
    return True




# ---------------------------
# Approve User (Admin Only)
def approve_user(username):
    users = load_users()
    if username in users['username'].values:
        users.loc[users['username'] == username, 'approved'] = True
        save_users(users)
        st.success(f"User '{username}' approved successfully.")


# ---------------------------
# Update Last Activity
def update_last_activity(username):
    users = load_users()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    users.loc[users['username'] == username, 'last_activity'] = now
    save_users(users)


# ---------------------------
# Admin Dashboard
def admin_dashboard():
    st.subheader("Admin Dashboard")
    users = load_users()

    # Pending = users who are regular users but not yet approved
    pending = users[(users["role"] == "user") & (users["approved"] == False)]
    st.write("### Pending Approvals")
    if pending.empty:
        st.info("No pending users.")
    else:
        for _, row in pending.iterrows():
            st.write(f"- **{row['username']}**")
            if st.button(f"Approve {row['username']}", key=f"appr_{row['username']}"):
                approve_user(row["username"])

    st.write("---")
    st.write("### Approved Users")
    approved = users[(users["role"] == "user") & (users["approved"] == True)]
    st.dataframe(approved[["username", "last_activity"]])




# ---------------------------
# Login/Register Interface
import streamlit as st

def login_register():
    # Center Big Project Title and Description on Main Page
    st.markdown(
        """
        <div style="text-align: center; margin-top: 50px;">
            <h1 style="color: white;">Source Code<br>Plagiarism Detector</h1>
            <p style="color: #cccccc; font-size: 18px; max-width: 600px; margin: auto;">
                Easily detect similarities in source code submissions. 
                Login or Register to get started!
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Sidebar for Login/Register
    menu = ["Login", "Register"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Login":
        st.sidebar.subheader("Login")
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type='password')
        if st.sidebar.button("Login"):
            user = authenticate_user(username, password)
            if user is not None:
                if user['approved']:
                    st.session_state['username'] = user['username']
                    st.session_state['role'] = user['role']
                    st.success(f"Welcome {user['username']}!")
                else:
                    st.warning("Your account is not approved by Admin yet.")
            else:
                st.error("Invalid Credentials.")

    elif choice == "Register":
        st.sidebar.subheader("Create New Account")
        new_user = st.sidebar.text_input("Username")
        new_password = st.sidebar.text_input("Password", type='password')
        if st.sidebar.button("Register"):
            if new_user and new_password:
                register_user(new_user, new_password)
            else:
                st.warning("Please fill both fields.")


# ---------------------------
