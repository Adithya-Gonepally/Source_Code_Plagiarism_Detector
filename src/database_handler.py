import pandas as pd
import os

def load_code_database(language):
    # Determine the directory where the current script resides
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the path to the database directory relative to the script's location
    database_dir = os.path.join(base_dir, "..", "database")

    # Map the language to its corresponding CSV file
    filename = {
        "Python": "python_database.csv",
        "C": "c_database.csv"
    }.get(language)

    if not filename:
        raise ValueError(f"Unsupported language: {language}")

    # Construct the full path to the CSV file
    filepath = os.path.join(database_dir, filename)

    # Check if the file exists
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Could not find the file: {filepath}")

    # Read the CSV file into a DataFrame
    return pd.read_csv(filepath, on_bad_lines='skip')


def get_code_samples(language):
    df = load_code_database(language)
    df.columns = df.columns.str.strip()  # Trim whitespace from column names

    # Verify that the required columns exist
    if 'file_name' not in df.columns or 'content' not in df.columns:
        raise KeyError("Required columns 'file_name' and/or 'content' not found in the database.")

    filenames = df['file_name'].tolist()
    code_samples = [str(content) for content in df['content'].tolist()]
    return filenames, code_samples
