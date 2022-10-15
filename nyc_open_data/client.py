"""
Client code for connecting to New York Open Data API
"""
import json
from functools import lru_cache
from typing import List, Optional

from sodapy import Socrata

from nyc_open_data.dataset import Dataset


@lru_cache()
def _client():
    return Socrata("data.cityofnewyork.us", None)


def _datasets() -> List:
    with open("datasets.json", "r") as f:
        return json.load(f)


def datasets() -> List[Dataset]:
    """
    Return all available datasets
    """
    return [Dataset(**d) for d in _datasets()]


def get(dataset_id: str):
    """
    Get the data for a given dataset
    """
    from nyc_open_data import models

    return models.get(_client(), dataset_id)


if __name__ == "__main__":
    print(datasets())
