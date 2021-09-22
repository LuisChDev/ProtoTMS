"""
This module provides two ways of obtaining a locations map for testing the
algorithms in the module.

the first one simply generates a bunch of random coordinates, constrained to
certain parameters (a rectangular box, minimal distance between, etc.). The
second one uses web scrapping to generate real-world locations from several
chain stores and restaurants. The first way provides info on general
performance of the algorithms, while the second one focuses on real-world
cases.
"""

import re
import os
from random import random
from typing import List, Tuple, Dict

from bs4 import BeautifulSoup
from yaml import load, SafeLoader
import matplotlib.pyplot as plt
import matplotlib
import requests as rq

matplotlib.use("Tkagg")


def random_coords(
        num: int = 10, width: int = 100, length: int = 100
) -> List[Tuple[float, float]]:
    """ This method generates a list of random coordinate pairs (floats),
    constrained to a rectangular box. All these parameters can be customized.
    """
    coords: List[Tuple[float, float]] = []
    for _ in range(0, num):
        coords.append((random() * width, random() * length))
    return coords


def plot_coords(coords: List[Tuple[float, float]]):
    """ takes a list of (lat, long) values and plots them through
    pyplot. """
    plt.scatter(list(map(lambda x: x[0], coords)),
                list(map(lambda x: x[1], coords)))
    plt.show()


def site_data(refresh: bool = False) -> List[Dict[str, str]]:
    """ This method scraps the locations off a website
    and returns the data about the sites.
    """

    # only reload the file when needed
    if refresh or not os.path.isfile('assets/ubicaciones.html'):
        with open("config.yaml") as fil:
            conf = load(fil, Loader=SafeLoader)
        with open("assets/ubicaciones.html", "w+") as fil:
            fil.write(str(rq.get(conf["stores_url"]).text))

    with open("assets/ubicaciones.html") as fil:
        ara_raw = BeautifulSoup(fil.read(), features="html.parser")

    # isolate all the store entries
    ara = ara_raw.find_all(class_=re.compile("views-row"))

    # convert each entry into a dict containing the relevant info
    # remove all the whitespace
    entries: List[Dict[str, str]] = []
    entries_ = [x for x in ara if x not in ["\n", "\t", " "]]
    for entry in entries_:
        value: Dict[str, str] = {}
        for y in [y for y in [*entry.children] if y not in ["\n", "\t", " "]]:
            value[
                y.get_attribute_list("class")[1][12:]] = [*[*y.children][1]][0]
            # coordinates are placed in as attributes
            # yes, that is a typo on the website
            if y.get_attribute_list("class")[1][12:] == "field-cordenadas":
                value[y.get_attribute_list("class")[1][12:]] = (
                    [*[*y
                       .children][
                           1].children][0].get_attribute_list("latitud")[0]
                    + ","
                    + [*[*y
                         .children][
                             1].children][0].get_attribute_list("longitud")[0]
                )
        entries.append(value)

    return entries


def site_coords(data: List[Dict[str, str]]) -> List[Tuple[float, float]]:
    """ returns the locations from the list of attributes.
    """
    # return [*map(lambda x: (x["field-coordenadas"].split(",")[0],
    #                         x["field-coordenadas"].split(",")[1]), data)]
    coords: List[Tuple[float, float]] = []
    for x in data:
        [lat, lon] = x["field-cordenadas"].split(",")
        coords.append((float(lat), float(lon)))
    return coords


# Local Variables:
# python-indent: 4
# End:
