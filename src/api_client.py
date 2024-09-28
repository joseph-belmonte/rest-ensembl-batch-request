""" 
This module is responsible for making requests to the Ensembl REST API
"""

import os
import json
import requests
from src.config import SERVER, BASE_DIR


class APIClient:
    """
    This class is responsible for making requests to the Ensembl REST API. It fetches gene
    regulatory features based on coordinates with caching. It also logs errors to a file for
    later review.
    """

    def __init__(self):
        self.error_log = os.path.join(
            BASE_DIR, "..", "data", "error_logs", "unchecked_coordinates.log"
        )
        if not os.path.exists(os.path.dirname(self.error_log)):
            os.makedirs(os.path.dirname(self.error_log))

    def fetch_regulatory_features(self, chromosome, start, end, cache_file):
        """Fetch gene regulatory features from the API based on coordinates with caching."""
        region = f"{chromosome}:{start}-{end}"
        cached_data = self.load_cached_data(cache_file)
        if region in cached_data:
            print(f"Loading cached regulatory features for region {region}")
            return cached_data[region]

        # Fetch from API if not cached
        print(f"Fetching regulatory features for region {region}")
        url = f"{SERVER}/overlap/region/human/{region}?feature=regulatory"
        response = self.make_request(url, region)
        print('api reponse:', response)
        if response:
            cached_data[region] = response
            self.cache_data(cached_data, cache_file)
        if not response:
            print('response is None')
        return response

    def make_request(self, url, identifier):
        """Makes a request to a URL and handles errors by logging them"""
        try:
            print(f"Making request to {url}")
            response = requests.get(
                url, headers={"Content-Type": "application/json"}, timeout=10
            )
            response.raise_for_status()
            print(f"Received response for {identifier}: {response.status_code}")
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed request for {identifier}: {e}")
            self.log_error(identifier, str(e))
            return None

    def cache_data(self, data, file_path):
        """Cache the data in a JSON file."""
        if os.path.exists(file_path):
            # Load the existing cache data to avoid overwriting
            existing_data = self.load_cached_data(file_path)
            existing_data.update(data)
            data = existing_data
        with open(file_path, "w") as file:
            json.dump(data, file)

    def load_cached_data(self, file_path):
        """Load data from a cached JSON file."""
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                return json.load(file)
        return {}  # Return an empty dictionary if no cache exists yet

    def log_error(self, identifier, error_message):
        """Log errors to a file for later review."""
        with open(self.error_log, "a") as file:
            file.write(f"Error for {identifier}: {error_message}\n")
