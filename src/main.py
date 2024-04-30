""" 
This is the main file for the project. 
"""

from src.data_manager import DataManager


def main():
    """
    Entry point of the program.

    This function initializes a DataManager object and calls its `process_all_csv_files` method.
    """
    manager = DataManager()
    manager.process_all_csv_files()


if __name__ == "__main__":
    main()
