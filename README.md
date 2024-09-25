# rest-ensembl-batch-request

A collection of python files to help analyze gene coordinates for regulatory features

Genes can be analyzed for regulatory features using the Ensembl REST API. The files are designed to be used in a batch request, where the user can input a list of gene coordinates and retrieve regulatory features for each gene. The files use the Ensembl REST API to retrieve regulatory features for a given gene coordinate. The regulatory features include transcription factor binding sites, enhancers, promoters, and other regulatory elements.

The files in this repository are meant to analyze the human genome.

# Steps to use the files

## 1. Clone the repository

```bash
git clone https://github.com/your-username/new-repo.git
```

## 1a. Create a virtual environment

Optional: At the root of the repository, create a virtual environment, and select it as the interpreter.

```bash
python -m venv venv
```

## 2. Install the required packages

Still at the root of the repository, install the required packages:

```bash
pip install requirements.txt
```

## 3. Update input files

Place the gene coordinates in a csv file in the `data/input` directory. The csv file should have the column `chromosomal_region`, in the format:

```csv
1:918352:918705
```

where the numbers represent `chromosome_number:start_position:end_position`.

## 4. Run the main file

From the root directory, run

```bash
python -m src.main
```

This will retrieve regulatory features for the gene coordinates that are listed in each csv file in the `data/input` directory. Depending on the size of your input file(s), this may take several minutes or hours.

## 5. Wait for the requests to complete

Depending on the number of gene coordinates, the process may take some time. Print statements are used to indicate which chromosome and which file are currently being read. The output will be saved in the `data/output` directory as a csv file.

## 5a. Flatten the output

Optional: The output csv will have a `regulatory_features` column which may be "flattened" into a more usable format by updating the filenames in the `src/flatten.py` file.

First, open `src/flatten.py` and update the filenames lsited. Then, run the file:

```bash
python -m src.flatten
```

Each file should now be "flattened" and saved in the `data/output` directory.

# Future Improvements

- [ ] Flattening output should happen automatically and shouldn't require an additional step.
