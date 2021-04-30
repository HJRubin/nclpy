"""This module lets you draw shapes and generate random points inside."""
import ee
import ipywidgets as widgets
from .common import ee_initialize

ee_initialize()


def random_points(region, color="00FFFF", points=100, seed=0):
    """Generates a specified number of random points inside a given area.
    Args: region(feature): region to generate points
          color(color code): default is red, I think
          points(numeric): how many points do you want? Default is 100
          seed:(numeric): default is 0
    Returns: a feature collection of locations
    """

    if not isinstance(region, ee.Geometry):
        err_str = "\n\nThe region of interest must be an ee.Geometry."
        raise AttributeError(err_str)

    color = "000000"

    if color is None:
        color = "00FFFF"
    if points is None:
        points = 100

    points_rand = ee.FeatureCollection.randomPoints(
        region=region, points=points, seed=seed
    )
    return points_rand
