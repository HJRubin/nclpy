"""Main module for the nclpy package."""
import os
import ipyleaflet
import ee
from .common import ee_initialize, geojson_to_ee
from ipyleaflet import FullScreenControl, LayersControl, DrawControl, MeasureControl, ScaleControl, TileLayer
from .utils import random_string
from .generate_points import random_points
from .toolbar import main_toolbar
from .basemaps import basemaps, basemap_tiles


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

ee_initialize()

class Map(ipyleaflet.Map):
    """This Map class inherits the ipyleaflet Map class.
    Args:
        ipyleaflet (ipyleaflet.Map): An ipyleaflet map.
    """    

    def __init__(self, **kwargs):

        if "center" not in kwargs:
            kwargs["center"] = [40, -100]

        if "zoom" not in kwargs:
            kwargs["zoom"] = 4

        if "scroll_wheel_zoom" not in kwargs:
            kwargs["scroll_wheel_zoom"] = True

        super().__init__(**kwargs)

        if "height" not in kwargs:
            self.layout.height = "600px"
        else:
            self.layout.height = kwargs["height"]

        self.draw_count = 0
        self.draw_features = []
        self.draw_last_feature = None
        self.draw_layer = None
        self.draw_last_json = None
        self.draw_last_bounds = None
        self.user_roi = None
        self.user_rois = None

        main_toolbar(self)
        self.toolbar = None
        self.toolbar_button = None
        train_props = {}

        def find_layer_index(self, name):
            """Finds layer index by name
            Args:
                name (str): Name of the layer to find.
            Returns:
                int: Index of the layer with the specified name
            """
            layers = self.layers

            for index, layer in enumerate(layers):
                if layer.name == name:
                    return index

            return -1

        def handle_draw(target, action, geo_json):
            try:
                print(target, action, geo_json, type(geo_json))
                # geom = geojson_to_ee(geo_json, False)
                self.user_roi = geo_json
                if len(train_props) > 0:
                    feature = ee.Feature(geo_json, train_props)
                else:
                    feature = ee.Feature(geo_json) #geom
                self.draw_last_json = geo_json
                self.draw_last_feature = feature
                if action == "deleted" and len(self.draw_features) > 0:
                    self.draw_features.remove(feature)
                    self.draw_count -= 1
                else:
                    self.draw_features.append(feature)
                    self.draw_count += 1
                collection = ee.FeatureCollection(self.draw_features)
                self.user_rois = collection
                ee_draw_layer = ee_tile_layer(
                    collection, {"color": "blue"}, "Drawn Features", False, 0.5
                )
                draw_layer_index = find_layer_index(self,"Drawn Features")

                if draw_layer_index == -1:
                    self.add_layer(ee_draw_layer)
                    self.draw_layer = ee_draw_layer
                else:
                    self.substitute_layer(self.draw_layer, ee_draw_layer)
                    self.draw_layer = ee_draw_layer

            except Exception as e:
                self.draw_count = 0
                self.draw_features = []
                self.draw_last_feature = None
                self.draw_layer = None
                self.user_roi = None
                self.roi_start = False
                self.roi_end = False
                print("There was an error creating Earth Engine Feature.")
                raise Exception(e)


        self.add_control(FullScreenControl())
        self.add_control(LayersControl(position="topright"))
        draw_control = DrawControl(position="topleft")
        draw_control.on_draw(handle_draw)
        # self.draw_control = draw_control
        self.add_control(draw_control)
        self.add_control(MeasureControl())
        self.add_control(ScaleControl(position="bottomleft"))

        ###
        ###


        if "toolbar_ctrl" not in kwargs.keys():
            kwargs["toolbar_ctrl"] = True

        if "google_map" not in kwargs:
            layer = TileLayer(
                url="https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}",
                attribution="Google",
                name="Google Maps",
            )
            self.add_layer(layer)
        else:
            if kwargs["google_map"] == "ROADMAP":
                layer = TileLayer(
                    url="https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}",
                    attribution="Google",
                    name="Google Maps",
                )
                self.add_layer(layer)
            elif kwargs["google_map"] == "HYBRID":
                layer = TileLayer(
                    url="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",
                    attribution="Google",
                    name="Google Satellite"
                )
                self.add_layer(layer)
    

    def add_geojson(self, in_geojson, style=None, layer_name="Untitled"):
        """Adds a GeoJSON file to the map.
        Args:
            in_geojson (str): The file path to the input GeoJSON.
            style (dict, optional): The style for the GeoJSON layer. Defaults to None.
            layer_name (str, optional): The layer name for the GeoJSON layer. Defaults to "Untitled".
        Raises:
            FileNotFoundError: If the provided file path does not exist.
            TypeError: If the input geojson is not a str or dict.
        """        

        import json

        if layer_name == "Untitled":
            layer_name = "Untitled " + random_string()

        if isinstance(in_geojson, str):

            if not os.path.exists(in_geojson):
                raise FileNotFoundError("The provided GeoJSON file could not be found.")

            with open(in_geojson) as f:
                data = json.load(f)
        
        elif isinstance(in_geojson, dict):
            data = in_geojson
        
        else:
            raise TypeError("The input geojson must be a type of str or dict.")

        if style is None:
            style = {
                "stroke": True,
                "color": "#000000",
                "weight": 2,
                "opacity": 1,
                "fill": True,
                "fillColor": "#0000ff",
                "fillOpacity": 0.4,
            }

        geo_json = ipyleaflet.GeoJSON(data=data, style=style, name=layer_name)
        self.add_layer(geo_json) 

    def add_shapefile(self, in_shp, style=None, layer_name="Untitled"):
        """Adds a shapefile layer to the map.
        Args:
            in_shp (str): The file path to the input shapefile.
            style (dict, optional): The style dictionary. Defaults to None.
            layer_name (str, optional): The layer name for the shapefile layer. Defaults to "Untitled".
        """
        geojson = shp_to_geojson(in_shp)
        self.add_geojson(geojson, style=style, layer_name=layer_name)

    def add_ee_layer(
        self, ee_object, vis_params={}, name=None, shown=True, opacity=1.0
    ):
        """Adds a given EE object to the map as a layer.
        Args:
            ee_object (Collection|Feature|Image|MapId): The object to add to the map.
            vis_params (dict, optional): The visualization parameters. Defaults to {}.
            name (str, optional): The name of the layer. Defaults to 'Layer N'.
            shown (bool, optional): A flag indicating whether the layer should be on by default. Defaults to True.
            opacity (float, optional): The layer's opacity represented as a number between 0 and 1. Defaults to 1.
        """

        ee_layer = ee_tile_layer(ee_object, vis_params, name, shown, opacity)
        self.add_layer(ee_layer)

    addLayer = add_ee_layer

    def toolbar_reset(self):
        """Reset the toolbar so that no tool is selected."""
        toolbar_grid = self.toolbar
        for tool in toolbar_grid:
            tool.value = False

# Handles draw events
    # def handle_draw(target, action, geo_json):
    #     try:
    #         self.roi_start = True
    #         geom = geojson_to_ee(geo_json, False)
    #         self.user_roi = geom
    #         feature = ee.Feature(geom)
    #         self.draw_last_json = geo_json
    #         self.draw_last_feature = feature
    #         if action == "deleted" and len(self.draw_features) > 0:
    #             self.draw_features.remove(feature)
    #             self.draw_count -= 1
    #         else:
    #             self.draw_features.append(feature)
    #             self.draw_count += 1
    #         collection = ee.FeatureCollection(self.draw_features)
    #         self.user_rois = collection
    #         ee_draw_layer = ee_tile_layer(
    #             collection, {"color": "blue"}, "Drawn Features", False, 0.5
    #         )
    #         draw_layer_index = self.find_layer_index("Drawn Features")

    #         if draw_layer_index == -1:
    #             self.add_layer(ee_draw_layer)
    #             self.draw_layer = ee_draw_layer
    #         else:
    #             self.substitute_layer(self.draw_layer, ee_draw_layer)
    #             self.draw_layer = ee_draw_layer
    #         self.roi_end = True
    #         self.roi_start = False
    #     except Exception as e:
    #         self.draw_count = 0
    #         self.draw_features = []
    #         self.draw_last_feature = None
    #         self.draw_layer = None
    #         self.user_roi = None
    #         self.roi_start = False
    #         self.roi_end = False
    #         print("There was an error creating Earth Engine Feature.")
    #         raise Exception(e)


# if kwargs.get("draw_ctrl"):
#     self.add_control(draw_control)
        
def shp_to_geojson(in_shp, out_geojson=None):
    """Converts a shapefile to GeoJSON.
    Args:
        in_shp (str): The file path to the input shapefile.
        out_geojson (str, optional): The file path to the output GeoJSON. Defaults to None.
    Raises:
        FileNotFoundError: If the input shapefile does not exist.
    Returns:
        dict: The dictionary of the GeoJSON.
    """
    import json
    import shapefile

    in_shp = os.path.abspath(in_shp)

    if not os.path.exists(in_shp):
        raise FileNotFoundError("The provided shapefile could not be found.")

    sf = shapefile.Reader(in_shp)
    geojson = sf.__geo_interface__

    if out_geojson is None:
        return geojson
    else:
        out_geojson = os.path.abspath(out_geojson)
        out_dir = os.path.dirname(out_geojson)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        with open(out_geojson, "w") as f:
            f.write(json.dumps(geojson))   

def ee_tile_layer(ee_object, vis_params={}, name="Layer untitled", shown=True, opacity=1.0):
    """Converts and Earth Engine layer to ipyleaflet TileLayer.
    Args:
        ee_object (Collection|Feature|Image|MapId): The object to add to the map.
        vis_params (dict, optional): The visualization parameters. Defaults to {}.
        name (str, optional): The name of the layer. Defaults to 'Layer untitled'.
        shown (bool, optional): A flag indicating whether the layer should be on by default. Defaults to True.
        opacity (float, optional): The layer's opacity represented as a number between 0 and 1. Defaults to 1.
    """

    image = None

    if (
        not isinstance(ee_object, ee.Image)
        and not isinstance(ee_object, ee.ImageCollection)
        and not isinstance(ee_object, ee.FeatureCollection)
        and not isinstance(ee_object, ee.Feature)
        and not isinstance(ee_object, ee.Geometry)
    ):
        err_str = "\n\nThe image argument in 'addLayer' function must be an instace of one of ee.Image, ee.Geometry, ee.Feature or ee.FeatureCollection."
        raise AttributeError(err_str)

    if (
        isinstance(ee_object, ee.geometry.Geometry)
        or isinstance(ee_object, ee.feature.Feature)
        or isinstance(ee_object, ee.featurecollection.FeatureCollection)
    ):
        features = ee.FeatureCollection(ee_object)

        width = 2

        if "width" in vis_params:
            width = vis_params["width"]

        color = "000000"

        if "color" in vis_params:
            color = vis_params["color"]

        image_fill = features.style(**{"fillColor": color}).updateMask(
            ee.Image.constant(0.5)
        )
        image_outline = features.style(
            **{"color": color, "fillColor": "00000000", "width": width}
        )

        image = image_fill.blend(image_outline)
    elif isinstance(ee_object, ee.image.Image):
        image = ee_object
    elif isinstance(ee_object, ee.imagecollection.ImageCollection):
        image = ee_object.mosaic()

    map_id_dict = ee.Image(image).getMapId(vis_params)
    tile_layer = TileLayer(
        url=map_id_dict["tile_fetcher"].url_format,
        attribution="Google Earth Engine",
        name=name,
        opacity=opacity,
        visible=shown,
    )
    return tile_layer

