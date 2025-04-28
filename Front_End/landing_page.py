
import streamlit as st
import streamlit as st

def show_landing_page():
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
                margin: 20px auto;             
                display: block;
            }
            .stButton > button:hover {
                background-color: rgba(255, 255, 255, 0.2);
                transform: scale(1.05);
                color: black;
            }
            .landing-title {
                text-align: center;
                color: white;
                font-size: 40px;
                margin-top: 50px;
            }
            .landing-description {
                text-align: center;
                color: #cccccc;
                font-size: 20px;
                margin-top: 10px;
            }
        </style>
    """, unsafe_allow_html=True)

    # Title and description
    st.markdown("<div class='landing-title'>Source Code Plagiarism Detector</div>", unsafe_allow_html=True)
    st.markdown("<div class='landing-description'>Detect similarities in source code efficiently and accurately.</div>", unsafe_allow_html=True)

    # Centered "Check" button
    if st.button("Check"):
        st.session_state["current_page"] = "code_editor"

