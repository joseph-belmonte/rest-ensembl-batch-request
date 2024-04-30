""" 
This file contains a function that takes a CSV file with a column containing
JSON data and expands it into multiple columns.
It can be used to flatten the 'regulatory_data' column in the output CSV file
"""

import os
import json
import pandas as pd
from src.config import BASE_DIR


def parse_json(data):
    """
    Parse a JSON string and return it as a dictionary.

    Args:
      data (str): The JSON string to parse.

    Returns:
      dict: The parsed JSON string as a dictionary. If the input is not a string or
      if the JSON is invalid, an empty dictionary is returned.
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

    input_dir = os.path.join(BASE_DIR, "..", "data", "output")
    output_dir = os.path.join(BASE_DIR, "..", "data", "output")

    input_csv = os.path.join(input_dir, input_filename)
    output_csv = os.path.join(output_dir, output_filename)

    # Load the CSV file
    df = pd.read_csv(input_csv)

    # Apply parse_json to convert JSON strings in 'regulatory_data' to lists of dictionaries
    df["regulatory_data"] = df["regulatory_data"].apply(parse_json)

    # Normalize each item in the list and concatenate them into a single DataFrame
    all_rows = []
    print("Flattening regulatory_data column...")
    for _, row in df.iterrows():
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
flatten_regulatory_data("YOUR_FILENAME_HERE.csv", "flat_YOUR_FILENAME_HERE.csv")
