""" 
This file contains the DataManager class which is responsible for reading
and writing data to the disk. It also contains a method to load data from a CSV file. 
"""

import os
import csv
import pandas as pd
from src.api_client import APIClient
from src.config import BASE_DIR


class DataManager:
    """A class for managing data operations.

    This class provides methods for loading data from CSV files, fetching regulatory features for
    each gene, processing, and exporting data to CSV files.

    Attributes:
      input_dir (str): The directory path where input CSV files are located.
      output_dir (str): The directory path where output CSV files will be saved.
      cache_dir (str): The directory path where cached responses will be stored.
      client (APIClient): An instance of the APIClient class for fetching regulatory features.

    Methods:
    load_csv_data(filename): Load data from a CSV file and fetch regulatory features for each gene.
    process_all_csv_files(): Process and export data for all CSV files in the input directory.
    export_to_csv(df, filename): Export DataFrame to a CSV file in the specified output directory.
    """

    def __init__(self):
        self.input_dir = os.path.join(BASE_DIR, "..", "data", "input")
        self.output_dir = os.path.join(BASE_DIR, "..", "data", "output")
        self.cache_dir = os.path.join(BASE_DIR, "..", "data", "cached_responses")
        os.makedirs(self.cache_dir, exist_ok=True)
        self.client = APIClient()

    def load_csv_data(self, filename):
        """Load data from a CSV file and fetch regulatory features for each gene.

        Args:
          filename (str): The name of the CSV file to load.

        Returns:
          list: A list of dictionaries containing gene data, including regulatory features.
        """
        print(f"Loading data from {filename}")
        file_path = os.path.join(self.input_dir, filename)
        gene_data = []
        cache_file = os.path.join(
            self.cache_dir, f"cache_{os.path.basename(filename)}.json"
        )
        with open(file_path, mode="r", encoding="utf-8-sig") as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                gene_identifier = row.get("external_gene_name", "").strip()
                chromosomal_region = row.get("chromosomal_region", "").strip()
                gene_biotype = row.get("gene_biotype", "").strip()

                print(f"\nFetching data for gene: {gene_identifier}")
                print(f"Chromosomal region: {chromosomal_region}")

                # Parse the chromosomal_region
                if ":" in chromosomal_region:
                    chromosome_part, coordinates_part = chromosomal_region.split(":")
                    chromosome = chromosome_part.strip()

                    # Handle coordinates with or without '-'
                    if "-" in coordinates_part:
                        start_str, end_str = coordinates_part.split("-")
                    else:
                        start_str = end_str = coordinates_part

                    start = start_str.strip()
                    end = end_str.strip()

                    print(f"Parsed region - Chromosome: {chromosome}, Start: {start}, End: {end}")

                    # Fetch regulatory features
                    regulatory_features = self.client.fetch_regulatory_features(
                        chromosome, start, end, cache_file
                    )

                    if regulatory_features:  # Only append if response is valid
                        gene_data.append(
                            {
                                "name": gene_identifier,
                                "coordinate": f"{chromosome}:{start}-{end}",
                                "biotype": gene_biotype,
                                "regulatory_data": regulatory_features,
                            }
                        )
                        print(f"Added data for gene {gene_identifier}")
                    else:
                        print(f"No regulatory features found for gene {gene_identifier}")
                else:
                    print(f"Invalid chromosomal region format for gene {gene_identifier}: {chromosomal_region}")

        return gene_data

    def process_all_csv_files(self):
        """Process and export data for all CSV files in the input directory."""
        for filename in os.listdir(self.input_dir):
            if filename.endswith(".csv"):
                print(f"\nProcessing data from {filename}")
                gene_data = self.load_csv_data(filename)
                if gene_data:
                    df = pd.DataFrame(gene_data)
                    output_csv_filename = f"output_{filename}"
                    self.export_to_csv(df, output_csv_filename)
                else:
                    print(f"No valid data to export for {filename}")

    def export_to_csv(self, df, filename):
        """Export DataFrame to a CSV file in the specified output directory.

        Args:
          df (pandas.DataFrame): The DataFrame to export.
          filename (str): The name of the output CSV file.

        Returns:
          None
        """
        output_path = os.path.join(self.output_dir, filename)
        df.to_csv(output_path, index=False)
        print(f"Data exported to {output_path}")
