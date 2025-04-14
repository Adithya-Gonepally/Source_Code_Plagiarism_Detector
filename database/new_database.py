import pandas as pd
import re

# Load the CSV file (replace this path with the correct one if different)
filepath = r'C:\Users\adith\OneDrive\Desktop\Plagiarism detector for code\database\python_database.csv'
output_filepath = r'C:\Users\adith\OneDrive\Desktop\Plagiarism detector for code\database\python_database_cleaned.csv'

# Load the CSV file into a DataFrame
df = pd.read_csv(filepath)

def remove_comments(code):
    # Ensure the code is a string; if not, replace with an empty string
    if not isinstance(code, str):
        code = ""

    # Remove the initial comment line if it starts with "write a"
    code = re.sub(r'(?i)^write a.*?\n', '', code, count=1)  # Remove only the first line if it starts with "write a"

    # Remove single-line comments within the code (lines starting with #)
    code = re.sub(r'#.*', '', code)

    # Remove multi-line comments ('''...''' or """...""")
    code = re.sub(r'(""".*?"""|\'\'\'.*?\'\'\')', '', code, flags=re.DOTALL)

    # Remove any extra empty lines left after comment removal
    code = "\n".join([line for line in code.splitlines() if line.strip() != ""])
    return code

# Apply the remove_comments function to the 'content' column
df['content'] = df['content'].apply(remove_comments)

# Save the cleaned DataFrame back to a new CSV file
df.to_csv(output_filepath, index=False)

print(f"Comments removed and saved to {output_filepath}")
