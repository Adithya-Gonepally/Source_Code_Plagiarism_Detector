import pandas as pd
def load_code_database(language):
    # Choose the correct database file based on the language
    filepath = {
        "Python": r'C:\Users\adith\OneDrive\Desktop\Source code Plagiarism Detector\database\python_database.csv',
        "C": r'C:\Users\adith\OneDrive\Desktop\Source code Plagiarism Detector\database\c_database.csv'
    }[language]
    return pd.read_csv(filepath, on_bad_lines='skip')  # Default sep is ','


def get_code_samples(language):
    df = load_code_database(language)
    df.columns = df.columns.str.strip()  # Trim whitespace from column names

    # Verify that the required columns exist
    if 'file_name' not in df.columns or 'content' not in df.columns:
        raise KeyError("Required columns 'file_name' and/or 'content' not found in the database.")

    filenames = df['file_name'].tolist()
    code_samples = [str(content) for content in df['content'].tolist()]
    return filenames, code_samples
