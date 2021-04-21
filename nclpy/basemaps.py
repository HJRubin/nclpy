"""Module for basemaps. Each basemap is defined as item in the ee_basemaps dictionary. For example, to access Google basemaps, use the following:
ee_basemaps['ROADMAP'], ee_basemaps['SATELLITE'], ee_basemaps['HYBRID'].
More WMS basemaps can be found at the following websites:
1. USGS National Map: https://viewer.nationalmap.gov/services/
2. MRLC NLCD Land Cover data: https://viewer.nationalmap.gov/services/
3. FWS NWI Wetlands data: https://www.fws.gov/wetlands/Data/Web-Map-Services.html
"""

from box import Box
from ipyleaflet import TileLayer, WMSLayer, basemap_to_tiles
import ipyleaflet.basemaps as ipybasemaps


_ee_basemaps = {
    "ROADMAP": TileLayer(
        url="https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}",
        attribution="Google",
        name="Google Maps",
    ),
    "SATELLITE": TileLayer(
        url="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
        attribution="Google",
        name="Google Satellite",
    ),
    "TERRAIN": TileLayer(
        url="https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={z}",
        attribution="Google",
        name="Google Terrain",
    ),
    "HYBRID": TileLayer(
        url="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",
        attribution="Google",
        name="Google Satellite",
    ),
    "ESRI": TileLayer(
        url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attribution="Esri",
        name="Esri Satellite",
    ),
    "Esri Ocean": TileLayer(
        url="https://services.arcgisonline.com/ArcGIS/rest/services/Ocean/World_Ocean_Base/MapServer/tile/{z}/{y}/{x}",
        attribution="Esri",
        name="Esri Ocean",
    ),
    "Esri Satellite": TileLayer(
        url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attribution="Esri",
        name="Esri Satellite",
    ),
    "Esri Standard": TileLayer(
        url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}",
        attribution="Esri",
        name="Esri Standard",
    ),
    "Esri Terrain": TileLayer(
        url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Terrain_Base/MapServer/tile/{z}/{y}/{x}",
        attribution="Esri",
        name="Esri Terrain",
    ),
    "Esri Transportation": TileLayer(
        url="https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Transportation/MapServer/tile/{z}/{y}/{x}",
        attribution="Esri",
        name="Esri Transportation",
    ),
    "Esri Topo World": TileLayer(
        url="https://services.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}",
        attribution="Esri",
        name="Esri Topo World",
    ),
    "Esri National Geographic": TileLayer(
        url="http://services.arcgisonline.com/ArcGIS/rest/services/NatGeo_World_Map/MapServer/tile/{z}/{y}/{x}",
        attribution="Esri",
        name="Esri National Geographic",
    ),
    "Esri Shaded Relief": TileLayer(
        url="https://services.arcgisonline.com/arcgis/rest/services/World_Shaded_Relief/MapServer/tile/{z}/{y}/{x}",
        attribution="Esri",
        name="Esri Shaded Relief",
    ),
    "Esri Physical Map": TileLayer(
        url="https://services.arcgisonline.com/arcgis/rest/services/World_Physical_Map/MapServer/tile/{z}/{y}/{x}",
        attribution="Esri",
        name="Esri Physical Map",
    ),
    
}

# Adds ipyleaflet basemaps
for item in ipybasemaps.values():
    try:
        name = item["name"]
        basemap = "ipybasemaps.{}".format(name)
        _ee_basemaps[name] = basemap_to_tiles(eval(basemap))
    except Exception:
        for sub_item in item:
            name = item[sub_item]["name"]
            basemap = "ipybasemaps.{}".format(name)
            basemap = basemap.replace("Mids", "Modis")
            _ee_basemaps[name] = basemap_to_tiles(eval(basemap))

basemap_tiles = Box(_ee_basemaps, frozen_box=True)
basemaps = Box(
    dict(zip(list(_ee_basemaps.keys()), list(_ee_basemaps.keys()))), frozen_box=True)