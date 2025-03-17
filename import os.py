import os
import pandas as pd

# Function to rename raw file
def rename_raw_file(file_path, new_name):
    new_file_path = os.path.join(os.path.dirname(file_path), new_name)
    
    # Rename only if the names are different
    if file_path != new_file_path:
        os.rename(file_path, new_file_path)
        print(f"Renamed raw file: {new_file_path}")
    
    return new_file_path  # Return new file path for processing

# Function to clean the data
def clean_data(raw_file_path, cleaned_dir, cleaned_name):
    try:
        # Load the CSV file
        df = pd.read_csv(raw_file_path)
        
        # Clean the column names (remove leading/trailing spaces)
        df.columns = df.columns.str.strip()

        # Check if required columns exist
        if 'Country' not in df.columns or '2024' not in df.columns:
            raise ValueError(f"'Country' or '2024' column not found in {raw_file_path}")
        
        # Select relevant columns
        df_cleaned = df[['Country', '2024']]

        # Rename '2024' column to 'Trade Value'
        df_cleaned.rename(columns={'2024': 'Trade Value'}, inplace=True)
        
        # Drop rows with missing 'Trade Value'
        df_cleaned.dropna(subset=['Trade Value'], inplace=True)

        # Define cleaned file path
        cleaned_file_path = os.path.join(cleaned_dir, cleaned_name)

        # Ensure the cleaned directory exists
        os.makedirs(cleaned_dir, exist_ok=True)
        
        # Save cleaned data
        df_cleaned.to_csv(cleaned_file_path, index=False)
        
        print(f"Cleaned data saved to {cleaned_file_path}")

    except Exception as e:
        print(f"Error processing {raw_file_path}: {str(e)}")

# Main function to process files
def process_files():
    base_raw_data_dir = "C:/Users/16316/Documents/GitHub/Long-Island-Business-Report/raw_data"
    base_cleaned_data_dir = "C:/Users/16316/Documents/GitHub/Long-Island-Business-Report/cleaned_data"
    
    # List of raw files to rename and process (old name → new name)
    files_to_rename = {
        "raw_us_exports_total.csv": "Raw Total Goods Exported US to World 2024.csv",
    }
    
    for category in ["world"]:  # Extend if needed
        raw_data_dir = os.path.join(base_raw_data_dir, category)
        cleaned_data_dir = os.path.join(base_cleaned_data_dir, category)

        if not os.path.exists(raw_data_dir):
            print(f"Directory {raw_data_dir} does not exist, skipping.")
            continue

        for old_name, new_name in files_to_rename.items():
            old_path = os.path.join(raw_data_dir, old_name)

            if os.path.exists(old_path):
                # Rename raw file in its original directory
                new_raw_path = rename_raw_file(old_path, new_name)

                # Clean data and save in the cleaned_data directory
                cleaned_name = new_name.replace("Raw ", "").replace(".csv", "_cleaned.csv")
                clean_data(new_raw_path, cleaned_data_dir, cleaned_name)
            else:
                print(f"File {old_path} not found, skipping.")

# Run the script
process_files()
