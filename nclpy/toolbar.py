import os
import ipywidgets as widgets
from ipyleaflet import WidgetControl, DrawControl
from ipyfilechooser import FileChooser
from IPython.display import display
from .generate_points import random_points
from .common import *


def main_toolbar(m):

    padding = "0px 0px 0px 5px"  # upper, right, bottom, left

    toolbar_button = widgets.ToggleButton(
        value=False,
        tooltip="Toolbar",
        icon="wrench",
        layout=widgets.Layout(width="28px", height="28px", padding=padding),
    )

    close_button = widgets.ToggleButton(
        value=False,
        tooltip="Close the tool",
        icon="times",
        button_style="primary",
        layout=widgets.Layout(height="28px", width="28px", padding=padding),
    )

    toolbar = widgets.HBox([toolbar_button])

    def close_click(change):
        if change["new"]:
            toolbar_button.close()
            close_button.close()
            toolbar.close()

    close_button.observe(close_click, "value")

    rows = 2
    cols = 2
    grid = widgets.GridspecLayout(
        rows, cols, grid_gap="0px", layout=widgets.Layout(width="62px")
    )

    icons = ["folder-open", "map", "gears", "circle"]

    for i in range(rows):
        for j in range(cols):
            grid[i, j] = widgets.Button(
                description="",
                button_style="primary",
                icon=icons[i * rows + j],
                layout=widgets.Layout(width="28px", padding="0px"),
            )

    toolbar = widgets.VBox([toolbar_button])

    def toolbar_click(change):
        if change["new"]:
            toolbar.children = [widgets.HBox([close_button, toolbar_button]), grid]
        else:
            toolbar.children = [toolbar_button]

    toolbar_button.observe(toolbar_click, "value")

    toolbar_ctrl = WidgetControl(widget=toolbar, position="topright")

    m.add_control(toolbar_ctrl)

    output = widgets.Output()
    output_ctrl = WidgetControl(widget=output, position="topright")

    buttons = widgets.ToggleButtons(
        value=None,
        options=["Apply", "Reset", "Close"],
        tooltips=["Apply", "Reset", "Close"],
        button_style="primary",
    )
    buttons.style.button_width = "80px"

    data_dir = os.path.abspath("./data")

    fc = FileChooser(data_dir)
    fc.use_dir_icons = True
    fc.filter_pattern = ["*.shp", "*.geojson"]

    filechooser_widget = widgets.VBox([fc, buttons])

    draw_control = DrawControl()

    def button_click(change):
        if change["new"] == "Apply" and fc.selected is not None:
            if fc.selected.endswith(".shp"):
                m.add_shapefile(fc.selected, layer_name="Shapefile")
            elif fc.selected.endswith(".geojson"):
                m.add_geojson(fc.selected, layer_name="GeoJSON")
        elif change["new"] == "Reset":
            fc.reset()
        elif change["new"] == "Close":
            if m is not None:
                m.toolbar_reset()
                if m.tool_control is not None and m.tool_control in m.controls:
                    m.remove_control(m.tool_control)
                    m.tool_control = None
            toolbar_widget.close()

    buttons.observe(button_click, "value")

    def tool_click(b):
        with output:
            output.clear_output()
            if b.icon == "folder-open":
                dropdown = widgets.Dropdown(
                    options=data_dir,
                    value="csv",
                    layout=widgets.Layout(width="200px")
                )

                close_btn = widgets.Button(
                    icon="times",
                    tooltip="Close the csv widget",
                    button_style="primary",
                    layout=widgets.Layout(width="32px"),
                )

                csv_widget = widgets.HBox([dropdown, close_btn])

                def on_click(change):
                    csv_name = change["new"]

                    if len(m.layers) == 1:
                        old_csv = m.layers[0]
                    else:
                        old_csv = m.layers[1]
                    m.csv_toshapefile(old_csv)
                dropdown.observe(on_click, "value")

                def close_click(change):
                    m.toolbar_reset()
                    if m.csv_ctrl is not None and m.csv_ctrl in m.controls:
                        m.remove_control(m.csv_ctrl)
                    csv_widget.close()

                close_btn.on_click(close_click)

                csv_control = WidgetControl(widget=csv_widget)
                m.add_control(csv_control)
                m.csv_ctrl = csv_control
            elif b.icon == "map":
                change_basemap(m)
            elif b.icon == "gears":
                import whiteboxgui.whiteboxgui as wbt

                if hasattr(m, "whitebox") and m.whitebox is not None:
                    if m.whitebox in m.controls:
                        m.remove_control(m.whitebox)

                tools_dict = wbt.get_wbt_dict()
                wbt_toolbox = wbt.build_toolbox(
                    tools_dict, max_width="800px", max_height="500px"
                )

                wbt_control = WidgetControl(widget=wbt_toolbox, position="bottomright")

                m.whitebox = wbt_control
                m.add_control(wbt_control)
            elif b.icon == "circle":
                if m.user_roi is not None:
                    print(m.user_roi)
                    geom = geojson_to_ee(m.user_roi, False)
                    r_points = random_points(geom)
                    print(r_points)

    def close_btn_click(change):
        if change["new"]:
            toolbar_button.value = False
            if m is not None:
                if m.tool_control is not None and m.tool_control in m.controls:
                    m.remove_control(m.tool_control)
                    m.tool_control = None
                m.toolbar_reset()
            toolbar_widget.close()

    close_button.observe(close_btn_click, "value")

    def change_basemap(m):
        """Widget for change basemaps.
        Args:
            m (object): geemap.Map()
        """
        from .basemaps import _ee_basemaps

        dropdown = widgets.Dropdown(
            options=list(_ee_basemaps.keys()),
            value="ROADMAP",
            layout=widgets.Layout(width="200px")
            # description="Basemaps",
        )

        close_btn = widgets.Button(
            icon="times",
            tooltip="Close the basemap widget",
            button_style="primary",
            layout=widgets.Layout(width="32px"),
        )

        basemap_widget = widgets.HBox([dropdown, close_btn])

        def on_click(change):
            basemap_name = change["new"]

            if len(m.layers) == 1:
                old_basemap = m.layers[0]
            else:
                old_basemap = m.layers[1]
            m.substitute_layer(old_basemap, _ee_basemaps[basemap_name])

        dropdown.observe(on_click, "value")

        def close_click(change):
            m.toolbar_reset()
            if m.basemap_ctrl is not None and m.basemap_ctrl in m.controls:
                m.remove_control(m.basemap_ctrl)
            basemap_widget.close()

        close_btn.on_click(close_click)

        basemap_control = WidgetControl(widget=basemap_widget, position="topright")
        m.add_control(basemap_control)
        m.basemap_ctrl = basemap_control
    
    

    for i in range(rows):
        for j in range(cols):
            tool = grid[i, j]
            tool.on_click(tool_click)
