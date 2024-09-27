import os
from src.data_manager import DataManager
from src.flatten import flatten_regulatory_data
from src.config import BASE_DIR

def main():
    # Initialize the data manager
    data_manager = DataManager()

    # Process all CSV files in the input directory
    print("Starting CSV processing...")
    data_manager.process_all_csv_files()

    # After processing, flatten the output data
    output_dir = os.path.join(BASE_DIR, "..", "data", "output")
    for filename in os.listdir(output_dir):
        if filename.startswith("output_") and filename.endswith(".csv"):
            print(f"Flattening regulatory data for {filename}...")
            flat_output_filename = f"flat_{filename}"
            flatten_regulatory_data(filename, flat_output_filename)
    
    print("Processing complete.")

if __name__ == "__main__":
    main()
