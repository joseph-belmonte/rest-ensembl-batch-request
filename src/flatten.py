""" 
This file contains a function that takes a CSV file with a column containing
JSON data and expands it into multiple columns.
"""

import os
import json
import pandas as pd
from src.config import OUTPUT_DIR


def parse_json(data):
    """
    Parse a JSON string and return it as a dictionary.

    Args:
      data (str): The JSON string to parse.

    Returns:
      dict: The parsed JSON string as a dictionary. If the input is not a string or if the JSON is invalid, an empty dictionary is returned.
    """
    if not isinstance(data, str):  # Check if data is not a string
        return {}  # Return empty dict if not a string (e.g., NaN or float)
    try:
        # Load the JSON string as a dictionary
        return json.loads(data.replace("'", '"'))
    except json.JSONDecodeError:
        return {}  # Return empty dict if JSON is invalid


def flatten_regulatory_data(input_filename, output_filename):
    """Flatten the regulatory_data column in a CSV file and save the result to a new CSV file."""

    input_csv = os.path.join(OUTPUT_DIR, input_filename)
    output_csv = os.path.join(OUTPUT_DIR, output_filename)

    # Check if the input file exists
    if not os.path.exists(input_csv):
        print(f"Error: File not found - {input_csv}")
        return
    
    # Check if the input file has the expected column
    try:
        df = pd.read_csv(input_csv)
        if "regulatory_data" not in df.columns:
            print(f"Error: Column 'regulatory_data' not found in {input_csv}")
            return
    except pd.errors.EmptyDataError:
        print(f"Error: Empty file - {input_csv}")
        return



    # Apply parse_json to convert JSON strings in 'regulatory_data' to lists of dictionaries
    df["regulatory_data"] = df["regulatory_data"].apply(parse_json)

    # Normalize each item in the list and concatenate them into a single DataFrame
    all_rows = []
    print("Flattening regulatory_data column...")
    for index, row in df.iterrows():
        if row["regulatory_data"]:
            norm_df = pd.json_normalize(row["regulatory_data"])
            for col in norm_df.columns:
                row[col] = norm_df.at[0, col]
        all_rows.append(row)

    print("Completed flattening.")
    # Create a new DataFrame with the expanded data
    full_df = pd.DataFrame(all_rows)

    # Drop the original 'regulatory_data' column as it's now redundant
    full_df = full_df.drop(columns=["regulatory_data"])

    # Save the cleaned and expanded CSV
    full_df.to_csv(output_csv, index=False)
    print(f"Processed file saved to {output_csv}")


# Example usage - run this function to flatten the regulatory_data column in the output CSV file
# Flatten the regulatory_data column in the output CSV file by running the following command:
# flatten_regulatory_data("YOUR_FILENAME_HERE.csv", "flat_YOUR_FILENAME_HERE.csv")
