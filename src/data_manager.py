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
    each gene, processing and exporting data to CSV files.

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
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
        self.client = APIClient()

    def load_csv_data(self, filename):
        """Load data from a CSV file and fetch regulatory features for each gene.

        Args:
          filename (str): The name of the CSV file to load.

        Returns:
          list: A list of dictionaries containing gene data, including regulatory features.
        """
        file_path = os.path.join(self.input_dir, filename)
        gene_data = []
        cache_file = os.path.join(
            self.cache_dir, f"cache_{os.path.basename(filename)}.json"
        )
        with open(file_path, mode="r", encoding="utf-8-sig") as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                gene_identifier = row["external_gene_name"]
                parts = row["chromosomal_region"].split(":")
                if len(parts) == 3:
                    chromosome = parts[0]
                    start, end = parts[1], parts[2]
                    regulatory_features = self.client.fetch_regulatory_features(
                        chromosome, start, end, cache_file
                    )
                    gene_data.append(
                        {
                            "name": gene_identifier,
                            "coordinate": f"{chromosome}:{start}-{end}",
                            "biotype": row["gene_biotype"],
                            "regulatory_data": regulatory_features,
                        }
                    )
        return gene_data

    def process_all_csv_files(self):
        """Process and export data for all CSV files in the input directory."""
        for filename in os.listdir(self.input_dir):
            if filename.endswith(".csv"):
                print(f"Processing data from {filename}")
                gene_data = self.load_csv_data(filename)
                df = pd.DataFrame(gene_data)
                output_csv_filename = f"output_{filename}"
                self.export_to_csv(df, output_csv_filename)

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
