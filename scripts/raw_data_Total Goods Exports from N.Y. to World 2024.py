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
        required_cols = ['Partner', '2024']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            print(f"Missing required columns: {missing_cols}")
            return None

        # Select only 'Partner' and '2024' columns
        df_cleaned = df[['Partner', '2024']]

        # Remove rows with 'World' in the 'Partner' column
        df_cleaned = df_cleaned[df_cleaned['Partner'] != 'World']

        # Remove rows with missing values in '2024' column
        df_cleaned.dropna(subset=['2024'], inplace=True)

        # Convert the '2024' column to numeric values
        df_cleaned['2024'] = pd.to_numeric(df_cleaned['2024'], errors='coerce')

        # Sort by '2024' Trade Value and select top 10 countries
        df_cleaned = df_cleaned.sort_values(by='2024', ascending=False).head(10)

        return df_cleaned

    except Exception as e:
        print(f"Error cleaning data: {str(e)}")
        return None

# Function to process a single file
def process_file(raw_file_path, cleaned_dir):
    try:
        # Rename the raw file if needed
        renamed_raw_path = rename_raw_file(raw_file_path)

        # Load data
        df = pd.read_csv(renamed_raw_path)

        # Clean data
        df_cleaned = clean_data(df)
        if df_cleaned is None:
            return  # Skip saving if cleaning failed

        # Create cleaned file name
        cleaned_name = os.path.basename(renamed_raw_path).replace("raw_data_", "").replace(".csv", "_cleaned.csv")
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

        # Save the current script (this script) to the scripts folder only if it's not already there
        current_script_path = os.path.realpath(__file__)
        script_folder = os.path.join(os.path.expanduser("~"), "Documents", "GitHub", "Long-Island-Business-Report", "scripts")  # Ensure correct folder path
        destination_path = os.path.join(script_folder, os.path.basename(current_script_path))

        # Ensure the destination folder exists
        if not os.path.exists(script_folder):
            os.makedirs(script_folder)
        
        # Normalize the paths by ensuring they're using the same path format
        current_script_path = os.path.normpath(current_script_path)
        destination_path = os.path.normpath(destination_path)

        # Check if the script is not already in the target location
        if current_script_path != destination_path:
            shutil.copy(current_script_path, destination_path)
            print(f"Script saved to: {destination_path}")
        else:
            print("Script is already in the target location. No copy needed.")

        # Check for git changes
        result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
        if result.stdout.strip():
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", "Automated data processing and script update"], check=True)
            subprocess.run(["git", "push"], check=True)
            print("Changes pushed to the repository.")
        else:
            print("No changes to commit.")

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
            if filename.endswith(".csv"):
                raw_file_path = os.path.join(raw_data_dir, filename)
                print(f"Processing: {raw_file_path}")
                process_file(raw_file_path, cleaned_data_dir)
            else:
                print(f"Skipping non-CSV file: {filename}")

# Run the script
def run_script():
    git_pull_push()  # Pull and update the repo first
    process_files()  # Process the raw data files

# Execute the script
if __name__ == "__main__":
    run_script()
