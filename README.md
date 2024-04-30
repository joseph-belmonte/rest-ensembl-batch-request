# rest-ensembl-batch-request

A collection of python files to help analyze gene coordinates for regulatory features

Genes can be analyzed for regulatory features using the Ensembl REST API. This repository contains a collection of python files that can be used to analyze gene coordinates for regulatory features. The files are designed to be used in a batch request, where the user can input a list of gene coordinates and retrieve regulatory features for each gene. The files use the Ensembl REST API to retrieve regulatory features for a given gene coordinate. The regulatory features include transcription factor binding sites, enhancers, promoters, and other regulatory elements.

The files in this repository are meant to analyze the human genome.

# Steps to use the files

## 1. Clone the repository

## 1a. Create a virtual environment

Optional: At the root of the repository, create a virtual environment, and select it as the interpreter.

`python -m venv venv`

## 2. Install the required packages

Run the following commands:

`pip install pandas`
`pip install requests`

## 3. Update input files

Place the gene coordinates in a csv file in the `data/input` directory. The csv file should have the column `chromosomal_region`, in the format: `1:918352:918705`. The `:` separates the chromosome number, start position, and end position of the gene coordinate. The csv file should have a header row. Other columns may be included in the csv file, but the `chromosomal_region` column is required to fetch regulatory features.

## 4. Run the main file

From the root directory, run `python -m src.main` to retrieve regulatory features for the gene coordinates that are listed in each csv file in the `data/input` directory.

## 5. Wait for the requests to complete

Depending on the number of gene coordinates, the process may take some time. Print statements are used to indicate which chromosome and which file are currently being read. The output will be saved in the `data/output` directory as a csv file.

## 5a. Flatten the output

Optional: The output csv will have a `regulatory_features` column which maybe "flattened" into a more usable format by updating the filenames in the `src/flatten.py` file. Run `python -m src.flatten` to flatten the `regulatory_features` column for each csv file in the `data/output` directory.
