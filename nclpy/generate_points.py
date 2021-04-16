"""This module lets you draw shapes and generate random points inside."""
import ee
import ipywidgets as widgets

def ee_initialize(token_name="EARTHENGINE_TOKEN"):
    """Authenticates Earth Engine and initialize an Earth Engine session"""
    if ee.data._credentials is None:
        try:
            ee_token = os.environ.get(token_name)
            if ee_token is not None:
                credential_file_path = os.path.expanduser("~/.config/earthengine/")
                if not os.path.exists(credential_file_path):
                    credential = '{"refresh_token":"%s"}' % ee_token
                    os.makedirs(credential_file_path, exist_ok=True)
                    with open(credential_file_path + "credentials", "w") as file:
                        file.write(credential)

            ee.Initialize()
        except Exception:
            ee.Authenticate()
            ee.Initialize()

def random_points(region, color="00FFFF", points=100, seed=0):
    """Generates a specified number of random points inside a given area.
    Args: region(feature): region to generate points
          color(color code): default is red, I think
          points(numeric): how many points do you want? Default is 100
          seed:(numeric): default is 0
    Returns: a feature collection of locations
    """
    if (
        not isinstance(region, ee.Geometry)
    ):
        err_str = "\n\nThe region of interest must be an ee.Feature."
        raise AttributeError(err_str)
    color = "000000"

    if color is None:
        color = "00FFFF"
    if points is None:
        points = 100
     
    points = ee.FeatureCollection.randomPoints(region = region, points = points, seed = seed)
    return points

