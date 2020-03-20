from yaml import safe_load  # , dump
from typing import Dict, List

with open('../secrets.yaml', 'r') as f:
    keys: Dict = safe_load(f)


def dist_matr(locations: List[str]) -> List[List[float]]:
    """
    Generate the distance matrix using a Google Maps API call.
    Args:
        locations: list of strings with the addresses of the locations. These
        can be of any type that Google Maps accepts.
    Returns:
        list of lists (matrix) with the (float) distances between the
        locations.
    """
    return [[]]
