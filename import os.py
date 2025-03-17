import os
import pandas as pd

# Function to rename raw files
def rename_raw_file(file_path, new_name):
    new_file_path = os.path.join(os.path.dirname(file_path), new_name)
    os.rename(file_path, new_file_path)
    print(f"Renamed raw file to: {new_file_path}")
    return new_file_path  # Return new file path for processing

# Function to clean the data
def clean_data(file_path, cleaned_name):
    try:
        # Load the CSV file
        df = pd.read_csv(file_path)
        
        # Clean the column names (remove leading/trailing spaces)
        df.columns = df.columns.str.strip()

        # Check if 'Country' and '2024' columns exist
        if 'Country' not in df.columns or '2024' not in df.columns:
            raise ValueError(f"'Country' or '2024' column not found in {file_path}")
        
        # Create a cleaned DataFrame with just 'Country' and '2024' columns
        df_cleaned = df[['Country', '2024']]

        # Rename '2024' column to 'Trade Value' for clarity
        df_cleaned.rename(columns={'2024': 'Trade Value'}, inplace=True)
        
        # Remove rows where 'Trade Value' is missing
        df_cleaned = df_cleaned.dropna(subset=['Trade Value'])

        # Define the cleaned file path
        cleaned_dir = file_path.replace("raw_data", "cleaned_data")
        cleaned_file_path = os.path.join(os.path.dirname(cleaned_dir), cleaned_name)

        # Ensure cleaned data directory exists
        os.makedirs(os.path.dirname(cleaned_file_path), exist_ok=True)
        
        # Save the cleaned DataFrame
        df_cleaned.to_csv(cleaned_file_path, index=False)
        
        print(f"Data cleaned and saved to {cleaned_file_path}")

    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")

# Main function to rename, clean, and update files
def process_files():
    base_raw_data_dir = "C:/Users/16316/Documents/GitHub/Long-Island-Business-Report/raw_data"
    
    # List of files to rename and process (old name → new name)
    files_to_rename = {
        "raw_us_exports_total.csv": "Raw Total Goods Exported US to World 2024.csv",
    }
    
    for category in ["world"]:  # Add more categories if needed
        raw_data_dir = os.path.join(base_raw_data_dir, category)

        if not os.path.exists(raw_data_dir):
            print(f"Directory {raw_data_dir} does not exist, skipping.")
            continue

        for old_name, new_name in files_to_rename.items():
            old_path = os.path.join(raw_data_dir, old_name)
            
            if os.path.exists(old_path):
                # Rename raw file
                new_path = rename_raw_file(old_path, new_name)

                # Clean data and save under cleaned_data directory
                cleaned_name = new_name.replace("Raw ", "").replace(".csv", "_cleaned.csv")
                clean_data(new_path, cleaned_name)
            else:
                print(f"File {old_path} not found, skipping.")

# Run the script
process_files()
