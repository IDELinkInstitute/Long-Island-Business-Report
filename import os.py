import os
import pandas as pd

# Function to rename raw file
def rename_raw_file(file_path, new_name):
    new_file_path = os.path.join(os.path.dirname(file_path), new_name)
    
    # Rename only if the names are different
    if file_path != new_file_path:
        os.rename(file_path, new_file_path)
        print(f"Renamed raw file to: {new_file_path}")
    
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
    
    category = "world"
    raw_data_dir = os.path.join(base_raw_data_dir, category)
    cleaned_data_dir = os.path.join(base_cleaned_data_dir, category)

    # Old and new raw file names
    old_raw_name = "Total Goods Exported US to World 2024.csv"
    new_raw_name = "raw_data_Total Goods Exported US to World 2024.csv"

    old_raw_path = os.path.join(raw_data_dir, old_raw_name)

    if os.path.exists(old_raw_path):
        # Rename the raw file
        new_raw_path = rename_raw_file(old_raw_path, new_raw_name)

        # Create cleaned file name
        cleaned_name = new_raw_name.replace("raw_data_", "").replace(".csv", "_cleaned.csv")

        # Clean data and save in cleaned_data directory
        clean_data(new_raw_path, cleaned_data_dir, cleaned_name)
    else:
        print(f"File {old_raw_path} not found, skipping.")

# Run the script
process_files()
