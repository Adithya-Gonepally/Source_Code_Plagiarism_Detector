import streamlit as st

def show_code_editor():
    st.markdown("<h1 style='text-align: center; color: lightgray;'>Code Editor</h1>", unsafe_allow_html=True)
    st.write("Write your code below and choose an action to proceed.")

    # Language selection
    language = st.selectbox("Select Language:", ["Python", "C"])

    # Code input area
    code = st.text_area("Enter your code here:", height=300, placeholder="Type your code here...")

    # Buttons with icons
    col1, col2 = st.columns(2)
    with col1:
        run_button = st.button("⚙️ Run Code", use_container_width=True)  # Run icon
    with col2:
        check_similarity_button = st.button("🔍 Check Similarity", use_container_width=True)  # Magnifier icon

    if run_button:
        st.success(f"Code submitted to run: Language - {language}")
    if check_similarity_button:
        st.info(f"Code similarity check initiated for: Language - {language}")

    return language, code, run_button, check_similarity_button
