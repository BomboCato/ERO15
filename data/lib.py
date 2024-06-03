#
# data/data.py
#
# Optimizing loading times

from pathlib import Path

import pickle

data_path = Path(__file__).parent


def get_data(file_name: str) -> dict:
    """
    Return the object contained in the @file_path file.
    Create the file if it does not exist.
    """
    pick = {}

    try:
        with open(data_path / file_name, "rb") as data:
            pick = pickle.load(data)
    except FileNotFoundError:
        Path(file_name).touch()

    return pick


def save_data(file_name: str, data: dict) -> None:
    """
    Save @data in @file_path file.
    """
    with open(data_path / file_name, "wb") as data_file:
        pickle.dump(data, data_file, pickle.HIGHEST_PROTOCOL)
