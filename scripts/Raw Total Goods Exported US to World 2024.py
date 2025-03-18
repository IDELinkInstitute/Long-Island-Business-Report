import os
import shutil
import subprocess
import pandas as pd

# Function to rename raw files
def rename_raw_file(file_path, prefix="raw_data_"):
    dir_name, file_name = os.path.split(file_path)
    
    # Ensure the new name starts with the prefix
    new_name = f"{prefix}{file_name}" if not file_name.startswith(prefix) else file_name
    new_file_path = os.path.join(dir_name, new_name)

    # Rename only if necessary
    if file_path != new_file_path:
        os.rename(file_path, new_file_path)
        print(f"Renamed file: {file_name} -> {new_name}")
    
    return new_file_path

# Function to clean data
def clean_data(df):
    """Applies various cleaning steps to the DataFrame."""
    try:
        # Clean column names
        df.columns = df.columns.str.strip()

        # Ensure required columns exist
        required_cols = ['Country', '2024']
        if not all(col in df.columns for col in required_cols):
            raise ValueError(f"Missing required columns: {required_cols}")

        # Select and rename columns
        df_cleaned = df[['Country', '2024']].rename(columns={'2024': 'Trade Value'})

        # Remove rows with missing values
        df_cleaned.dropna(subset=['Trade Value'], inplace=True)

        # Additional cleaning logic can be added here (e.g., formatting, removing duplicates)
        return df_cleaned

    except Exception as e:
        print(f"Error cleaning data: {str(e)}")
        return None

# Function to process a single file
def process_file(raw_file_path, cleaned_dir):
    try:
        # Rename the raw file if needed
        renamed_raw_path = rename_raw_file(raw_file_path)

        # Load data assuming Python file (.py) contains pandas DataFrame in a variable like df
        # Use exec to execute the Python file (unsafe for production, consider other ways for better security)
        with open(renamed_raw_path) as file:
            exec(file.read())  # Assumes the script defines a DataFrame called `df`

        # Clean data
        df_cleaned = clean_data(df)
        if df_cleaned is None:
            return  # Skip saving if cleaning failed

        # Create cleaned file name
        cleaned_name = os.path.basename(renamed_raw_path).replace("raw_data_", "").replace(".py", "_cleaned.csv")
        cleaned_file_path = os.path.join(cleaned_dir, cleaned_name)

        # Ensure directory exists
        os.makedirs(cleaned_dir, exist_ok=True)

        # Save cleaned data
        df_cleaned.to_csv(cleaned_file_path, index=False)
        print(f"Cleaned data saved to: {cleaned_file_path}")

    except Exception as e:
        print(f"Error processing file {raw_file_path}: {str(e)}")

# Function to pull and push changes in git
def git_pull_push():
    try:
        # Pull the latest changes from the remote repository
        print("Pulling the latest changes from the remote repository...")
        subprocess.run(["git", "pull"], check=True)
        print("Pull successful")

        # Save the current script (this script) to the scripts folder only if it's not already there
        current_script_path = os.path.realpath(__file__)
        script_folder = "C:/Users/16316/Documents/GitHub/Long-Island-Business-Report/scripts"
        destination_path = os.path.join(script_folder, os.path.basename(current_script_path))

        # Normalize the paths by ensuring they're using the same path format
        current_script_path = os.path.normpath(current_script_path)
        destination_path = os.path.normpath(destination_path)

        # Check if the script is not already in the target location
        if current_script_path != destination_path:
            shutil.copy(current_script_path, destination_path)
            print(f"Script saved to: {destination_path}")
        else:
            print("Script is already in the target location. No copy needed.")

        # Add all changes, commit, and push to the repository
        print("Adding, committing, and pushing changes to the repository...")
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Automated data processing and script update"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("Changes pushed to the repository.")

    except subprocess.CalledProcessError as e:
        print(f"Git operation failed: {e}")

# Main function to process multiple files
def process_files():
    base_raw_data_dir = "C:/Users/16316/Documents/GitHub/Long-Island-Business-Report/raw_data"
    base_cleaned_data_dir = "C:/Users/16316/Documents/GitHub/Long-Island-Business-Report/cleaned_data"

    categories = ["world", "new_york", "metro_area"]  # Extendable list

    for category in categories:
        raw_data_dir = os.path.join(base_raw_data_dir, category)
        cleaned_data_dir = os.path.join(base_cleaned_data_dir, category)

        if not os.path.exists(raw_data_dir):
            print(f"Skipping missing directory: {raw_data_dir}")
            continue

        for filename in os.listdir(raw_data_dir):
            if filename.endswith(".py"):  # Processing .py files
                raw_file_path = os.path.join(raw_data_dir, filename)
                print(f"Processing: {raw_file_path}")
                process_file(raw_file_path, cleaned_data_dir)
            else:
                print(f"Skipping non-Python file: {filename}")

# Run the script
def run_script():
    git_pull_push()  # Pull and update the repo first
    process_files()  # Process the raw data files

# Execute the script
if __name__ == "__main__":
    run_script()
