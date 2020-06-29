from yaml import safe_load  # , dump
from typing import Dict, List, Tuple, Union
from math import sqrt
import googlemaps  # type: ignore

with open('../secrets.yaml', 'r') as f:
    keys: Dict = safe_load(f)

# create the google maps API object
gmaps = googlemaps.Client(key=keys["API_key"])

# utils
Coord = Union[str, Tuple[float, float]]


def pyth_dist(locations: List[Tuple[float, float]]) -> List[List[float]]:
    """
    generates a simple distance matrix based on the Pythagorean distance
    between the points.
    """
    result: List[List[float]] = []
    for (x0, y0) in locations:
        row: List[float] = []
        for (x, y) in locations:
            row.append(sqrt((x0 - x)**2 + (y0 - y)**2))
        result.append(row)
    return result


def dist_matr(locations: List[Coord]) -> Tuple[List[List[float]],
                                               List[List[float]]]:
    """
    Generate the distance matrix using a Google Maps API call.
    Args:
      locations: list of strings with the addresses of the locations. These
      can be of any type that Google Maps accepts.
      alternatively, a tuple with longitude and latitude.
    Returns:
      Tuple containing two lists of lists (matrices), the first one contains
      the distances between the points, the second one the estimated times
      of displacement as calculated by Google.
    """

    # split the list of locations in groups of 10 or less
    batches: List[List[Coord]] = []
    i: int = 0
    while (i < len(locations)):
        batch = []
        if i + 10 < len(locations):
            batch = locations[i:i + 10]
            i += 10
        else:
            batch = locations[i:len(locations)]
            i = len(locations)
        batches.append(batch)

    # build the matrix in 10*10 increments
    pre_matrix: List[List[Dict]] = []
    for batch in batches:
        pre_row: List[Dict] = []
        for batch_ in batches:
            pre_row.append(gmaps.distance_matrix(batch, batch_))
        pre_matrix.append(pre_row)

    # extract the distance and time values of the result
    matrix_t: List[List[float]] = [[] for _ in range(len(locations))]
    matrix_d: List[List[float]] = [[] for _ in range(len(locations))]

    # flatten the responses into one single object
    # for each row of responses:
    for i in range(len(pre_matrix)):
        # for each response:
        for j in range(len(pre_matrix[i])):
            # for each row in the response:
            for k in range(len(pre_matrix[i][j]["rows"])):
                # the row in question
                row = pre_matrix[i][j]["rows"][k]

                # calculate the position in the matrix where the values should
                # be appended, based on the number of rows per response
                # each row in the pre_matrix is one-response-thick, so we take
                # the first element on each row, and compute its length. We
                # add them all together.
                index = sum([len(x[0]["rows"])
                             for x in pre_matrix[:i]] + [len(
                                     pre_matrix[i][j]["rows"][:k])])
                # append the time and distance values to the matrices
                matrix_t[index] += [
                    x["duration"]["value"] for x in row["elements"]]
                matrix_d[index] += [
                    x["distance"]["value"] for x in row["elements"]]

    return (matrix_d, matrix_t)
