import os
import pandas as pd

# Function to clean the data
def clean_data(file_path):
    try:
        # Load the CSV file
        df = pd.read_csv(file_path)
        
        # Clean the column names (remove leading/trailing spaces)
        df.columns = df.columns.str.strip()

        # Select only the necessary columns: Country and 2024 trade values
        if 'Country' not in df.columns or '2024' not in df.columns:
            raise ValueError(f"'Country' or '2024' column not found in {file_path}")
        
        # Create a cleaned DataFrame with just 'Country' and '2024' columns
        df_cleaned = df[['Country', '2024']]

        # Rename '2024' column to 'Trade Value' for clarity
        df_cleaned.rename(columns={'2024': 'Trade Value'}, inplace=True)
        
        # Remove rows where the 'Trade Value' is missing
        df_cleaned = df_cleaned.dropna(subset=['Trade Value'])

        # Save the cleaned data to the cleaned data folder
        cleaned_file_path = file_path.replace("raw_data", "cleaned_data")
        cleaned_file_path = cleaned_file_path.replace(".csv", "_cleaned.csv")
        
        # Make sure the cleaned data directory exists
        os.makedirs(os.path.dirname(cleaned_file_path), exist_ok=True)
        
        # Save the cleaned DataFrame to a new CSV
        df_cleaned.to_csv(cleaned_file_path, index=False)
        
        print(f"Data cleaned and saved to {cleaned_file_path}")
    
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")

# Main function to check for files in the specified directory and trigger cleaning
def process_files():
    raw_data_dir = "C:/Users/16316/Documents/GitHub/Long-Island-Business-Report/raw_data/world"
    
    # Check files in the raw_data directory
    for filename in os.listdir(raw_data_dir):
        file_path = os.path.join(raw_data_dir, filename)
        
        # Check if the file is a CSV
        if filename.endswith(".csv"):
            print(f"Found file: {filename}")
            print(f"Starting to process: {file_path}")
            clean_data(file_path)
        else:
            print(f"Skipping unsupported file: {filename}")

# Trigger the processing function
process_files()
