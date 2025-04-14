
import streamlit as st
def show_landing_page():
    # Title and description
    st.markdown("<h1>Source Code Plagiarism Detector</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; margin-left:50px'>Detect similarities in source code efficiently and accurately.</p>",
                unsafe_allow_html=True)

    # Custom styles applied to Streamlit buttons
    st.markdown("""
        <style>
            .stButton > button {
                background-color: transparent; 
                color: white;                  
                font-size: 18px;               
                padding: 10px 50px;
                border: 2px solid white;       
                border-radius: 8px;            
                cursor: pointer;
                transition: all 0.3s ease;     
                margin-left: 110px;             
            }
            .stButton > button:hover {
                background-color: rgba(255, 255, 255, 0.2); /* White tint on hover */
                transform: scale(1.05);                     /* Slight zoom effect */
                color: black;                               /* Black text */
            }
            .centered-button {
                display: flex;
                justify-content: center;
                align-items: center;
                margin-top: 50px;  /* Add some space from the top */
            }
        </style>
    """, unsafe_allow_html=True)

    # Centered "Check" button with session navigation
    col1, col2, col3 = st.columns([1, 2, 1])  # Use columns to center the button
    with col2:
        if st.button("Check"):
            st.session_state["current_page"] = "code_editor"
