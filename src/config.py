"""
This file contains the configuration settings for the project.
"""

# Base directory of the project (directory containing this config file)
import os

SERVER = "https://rest.ensembl.org"

# File paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(BASE_DIR, "..", "data", "input")
OUTPUT_DIR = os.path.join(BASE_DIR, "..", "data", "output")
CACHE_DIR = os.path.join(BASE_DIR, "..", "data", "cached_responses")
ERROR_LOG_DIR = os.path.join(BASE_DIR, "..", "data", "error_logs")

# Ensure directories exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(ERROR_LOG_DIR, exist_ok=True)
