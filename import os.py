import os
import shutil
import time
import pandas as pd
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Define paths
REPO_PATH = r"C:\Users\16316\Documents\GitHub\Long-Island-Business-Report"
INPUT_FOLDER = os.path.join(REPO_PATH, "raw_data", "world")
OUTPUT_FOLDER = os.path.join(REPO_PATH, "cleaned_data", "world")

# Folder mapping based on data type
viz_folders = {
    "product": os.path.join(REPO_PATH, "cleaned_data", "product"),
    "sales": os.path.join(REPO_PATH, "cleaned_data", "sales"),
    "revenue": os.path.join(REPO_PATH, "cleaned_data", "revenue"),
}

# Ensure necessary folders exist
def create_cleaned_data_folders():
    """Create necessary folders for cleaned data."""
    for folder in viz_folders.values():
        os.makedirs(folder, exist_ok=True)

# Call this before running the script
create_cleaned_data_folders()

def clean_product_data(df):
    """Cleaning logic specific to product data."""
    # Example cleaning steps for product data
    df.drop(columns=["Product Classification", "Unit"], inplace=True)
    df["Product Name"] = df["Product Name"].str.strip()
    df.fillna(method='ffill', inplace=True)
    return df

def clean_sales_data(df):
    """Cleaning logic specific to sales data."""
    # Example cleaning steps for sales data
    df.drop(columns=["Country", "Region"], inplace=True)
    df["Sales"] = df["Sales"].apply(lambda x: float(x.replace(",", "")))
    df.fillna(method='ffill', inplace=True)
    return df

def clean_revenue_data(df):
    """Cleaning logic specific to revenue data."""
    # Example cleaning steps for revenue data
    df.drop(columns=["Revenue Category"], inplace=True)
    df["Revenue"] = df["Revenue"].apply(lambda x: float(x.replace("$", "").replace(",", "")))
    df.fillna(method='ffill', inplace=True)
    return df

def clean_data(file_path, destination_folder):
    """General cleaning function with specific output folder."""
    try:
        # Read the file
        df = pd.read_excel(file_path, engine="openpyxl")
        
        # Apply the appropriate cleaning logic based on the file name or content
        if "product" in file_path.lower():
            df = clean_product_data(df)
        elif "sales" in file_path.lower():
            df = clean_sales_data(df)
        elif "revenue" in file_path.lower():
            df = clean_revenue_data(df)
        else:
            # Default cleaning if no match is found
            df.fillna(method='ffill', inplace=True)
        
        # Save the cleaned file in the destination folder
        cleaned_file_path = os.path.join(destination_folder, os.path.basename(file_path))
        df.to_excel(cleaned_file_path, index=False, engine="openpyxl")
        print(f"Cleaned file saved to: {cleaned_file_path}")
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

class FileHandler(FileSystemEventHandler):
    """Handles new file events in the monitored folder."""
    def on_created(self, event):
        if event.is_directory:
            return

        file_path = event.src_path
        if file_path.endswith(".xlsx"):  # Process only Excel files
            print(f"New file detected: {file_path}")

            time.sleep(2)  # Delay to ensure file is fully written

            # Determine the appropriate folder for cleaned data
            if "product" in file_path:
                destination_folder = viz_folders["product"]
            elif "sales" in file_path:
                destination_folder = viz_folders["sales"]
            elif "revenue" in file_path:
                destination_folder = viz_folders["revenue"]
            else:
                destination_folder = os.path.join(REPO_PATH, "cleaned_data", "other")

            # Clean and move file
            clean_data(file_path, destination_folder)
            shutil.move(file_path, destination_folder)
            print(f"Moved to: {destination_folder}")

def process_existing_files():
    """Process any Excel files already in the input folder."""
    for file_name in os.listdir(INPUT_FOLDER):
        file_path = os.path.join(INPUT_FOLDER, file_name)
        if file_path.endswith(".xlsx") and os.path.isfile(file_path):
            print(f"Processing existing file: {file_path}")

            # Determine the folder for cleaned data
            if "product" in file_path:
                destination_folder = viz_folders["product"]
            elif "sales" in file_path:
                destination_folder = viz_folders["sales"]
            elif "revenue" in file_path:
                destination_folder = viz_folders["revenue"]
            else:
                destination_folder = os.path.join(REPO_PATH, "cleaned_data", "other")

            # Clean and move file
            clean_data(file_path, destination_folder)
            shutil.move(file_path, destination_folder)

def monitor_folder():
    """Monitor the input folder for new files."""
    process_existing_files()

    event_handler = FileHandler()
    observer = Observer()

    observer.schedule(event_handler, INPUT_FOLDER, recursive=False)
    observer.start()
    print(f"Monitoring {INPUT_FOLDER} for new files...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    monitor_folder()

import subprocess

# Add all files to the staging area
subprocess.run(["git", "add", "."])

# Commit changes
subprocess.run(['git', 'commit', '-m', 'Updated files after running the cleaning script'])

# Push changes to GitHub (replace 'main' with your branch if necessary)
subprocess.run(['git', 'push', 'origin', 'main'])
