import os
import pandas as pd
import shutil

# Function to rename raw file
def rename_raw_file(file_path, new_name):
    new_file_path = os.path.join(os.path.dirname(file_path), new_name)
    
    if file_path != new_file_path:
        os.rename(file_path, new_file_path)
        print(f"Renamed raw file to: {new_file_path}")
    
    return new_file_path

# Function to clean the data
def clean_data(raw_file_path, cleaned_dir, cleaned_name):
    try:
        df = pd.read_csv(raw_file_path)
        df.columns = df.columns.str.strip()

        if 'Country' not in df.columns or '2024' not in df.columns:
            raise ValueError(f"'Country' or '2024' column not found in {raw_file_path}")

        df_cleaned = df[['Country', '2024']].rename(columns={'2024': 'Trade Value'})
        df_cleaned.dropna(subset=['Trade Value'], inplace=True)

        os.makedirs(cleaned_dir, exist_ok=True)
        cleaned_file_path = os.path.join(cleaned_dir, cleaned_name)
        df_cleaned.to_csv(cleaned_file_path, index=False)

        print(f"Cleaned data saved to {cleaned_file_path}")
        return cleaned_file_path
    except Exception as e:
        print(f"Error processing {raw_file_path}: {str(e)}")
        return None

# Main function
def process_files():
    base_dir = "C:/Users/16316/Documents/GitHub/Long-Island-Business-Report"
    raw_data_dir = os.path.join(base_dir, "raw_data/world")
    cleaned_data_dir = os.path.join(base_dir, "cleaned_data/world")
    scripts_dir = os.path.join(base_dir, "scripts")

    old_raw_name = "Total Goods Exported US to World 2024.csv"
    new_raw_name = "raw_data_Total Goods Exported US to World 2024.csv"

    old_raw_path = os.path.join(raw_data_dir, old_raw_name)

    if os.path.exists(old_raw_path):
        new_raw_path = rename_raw_file(old_raw_path, new_raw_name)

        cleaned_name = new_raw_name.replace("raw_data_", "").replace(".csv", "_cleaned.csv")
        cleaned_file_path = clean_data(new_raw_path, cleaned_data_dir, cleaned_name)

        if cleaned_file_path:
            # Save this script to the scripts folder
            os.makedirs(scripts_dir, exist_ok=True)
            script_path = os.path.join(scripts_dir, "world_exports_cleaning.py")
            shutil.copy(__file__, script_path)
            print(f"Script saved to {script_path}")
    else:
        print(f"File {old_raw_path} not found, skipping.")

# Run the script
if __name__ == "__main__":
    process_files()

