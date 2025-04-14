import sys
import os
import streamlit as st
from contextlib import redirect_stdout
import subprocess
import io
import base64

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Front_End.code_editor import show_code_editor
from Front_End.landing_page import show_landing_page
from database_handler import get_code_samples
from similarity_checker import calculate_highest_similarity


def apply_background_image():
    """Apply a full-screen background image that fits the entire screen."""
    image_path = os.path.join(os.getcwd(), "Front_End", "image.jpg")

    if not os.path.exists(image_path):
        st.error("Background image not found. Please check the path.")
        return

    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode()

    st.markdown(f"""
        <style>
            body {{
                margin: 0;
                padding: 0;
                background-image: url('data:image/jpeg;base64,{base64_image}');
                background-size: cover;
                background-attachment: fixed;
                background-position: center;
                background-repeat: no-repeat;
                height: 100vh;
                overflow: hidden;
            }}
            .stApp {{
                background: transparent;
            }}
            h1 {{
                padding-left: 50px; /* Move title to the right */
                color: lightgray;
                text-align: center;
            }}
            .highlight {{
                background-color: red;   /* Red background */
                color: black;            /* Black text */
                font-weight: bold;       /* Bold text */
                padding: 2px 5px;        /* Padding around the text */
                border-radius: 3px;      /* Rounded corners */
            }}
        </style>
    """, unsafe_allow_html=True)


def main():
    # Apply the background image
    apply_background_image()

    # Initialize session state for navigation
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "landing"

    # Show landing page or code editor based on session state
    if st.session_state.get("current_page", "landing") == "landing":
        show_landing_page()
    else:
        st.title("Code Plagiarism Detector")

        # Load language choice, code from editor, and button states
        language, code, run_button, check_similarity_button = show_code_editor()

        # Handle "Run Code" button
        if run_button:
            if language == "Python":
                try:
                    buffer = io.StringIO()
                    with redirect_stdout(buffer):
                        exec(code)
                    output = buffer.getvalue()
                    st.success("Code ran successfully!")
                    st.text_area("Output:", value=output, height=200)
                except Exception as e:
                    st.error(f"Error: {e}")

            elif language == "C":
                try:
                    with open("temp_code.c", "w") as f:
                        f.write(code)

                    compile_process = subprocess.run(
                        ["gcc", "temp_code.c", "-o", "temp_code"],
                        capture_output=True, text=True
                    )

                    if compile_process.returncode != 0:
                        st.error(f"Compilation failed:\n{compile_process.stderr}")
                    else:
                        run_process = subprocess.run(
                            ["./temp_code"], capture_output=True, text=True
                        )
                        if run_process.returncode != 0:
                            st.error(f"Execution failed:\n{run_process.stderr}")
                        else:
                            st.success("Code ran successfully!")
                            st.text_area("Output:", value=run_process.stdout, height=200)
                finally:
                    if os.path.exists("temp_code.c"):
                        os.remove("temp_code.c")
                    if os.path.exists("temp_code"):
                        os.remove("temp_code")

        # Handle "Check Similarity" button
        if check_similarity_button:
            filenames, code_samples = get_code_samples(language)
            max_score, most_similar_file = calculate_highest_similarity(language, code, code_samples, filenames)

            if max_score < 0.6:
                st.write("No Plagiarism found")
                st.write("No similar code files in the database.")
            elif max_score > 0.6 and max_score < 0.8:
                st.markdown(
                    f"<p>Code is similar to <span class='highlight'>{most_similar_file}</span>, but with less than 80% similarity (<span class='highlight'>{max_score * 100:.2f}%</span>).</p>",
                    unsafe_allow_html=True)
            else:
                st.markdown(
                    f"<p>Plagiarism found: <span class='highlight'>{most_similar_file}</span></p>",
                    unsafe_allow_html=True)
                st.markdown(
                    f"<p>Similarity: <span class='highlight'>{max_score * 100:.2f}%</span></p>",
                    unsafe_allow_html=True)


if __name__ == "__main__":
    main()
