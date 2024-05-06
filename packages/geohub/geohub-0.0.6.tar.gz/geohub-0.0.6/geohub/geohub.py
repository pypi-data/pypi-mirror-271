"""Main module."""
import ipyleaflet
# import os
from PIL import Image
# import imageio
from ipyleaflet import basemaps, WidgetControl
import ipywidgets as widgets
from ipywidgets import Layout
from ipywidgets import IntSlider, Play, jslink, HBox
from ipyleaflet import TileLayer
from rasterio import open as rio_open


class Map(ipyleaflet.Map):
    """This is the map class that inherits from ipyleaflet.Map.

    Args:
        ipyleaflet (Map): The ipyleaflet.Map class.
    """

    def __init__(self, center=[40, -100], zoom=4, **kwargs):
        """Initialize the map.

        Args:
            center (list, optional): Set the center of the map. Defaults to [20, 0].
            zoom (int, optional): Set the zoom level of the map. Defaults to 2.
        """

        if "scroll_wheel_zoom" not in kwargs:
            kwargs["scroll_wheel_zoom"] = True

        if "add_layer_control" not in kwargs:
            layer_control_flag = True
        else:
            layer_control_flag = kwargs["add_layer_control"]
        kwargs.pop("add_layer_control", None)

        super().__init__(center=center, zoom=zoom, **kwargs)
        if layer_control_flag:
            self.add_layers_control()

        self.add_toolbar()

    def add_tile_layer(self, url, name, **kwargs):
        layer = ipyleaflet.TileLayer(url=url, name=name, **kwargs)
        self.add(layer)

    def add_basemap(self, name):
        """
        Adds a basemap to the current map.

        Args:
            name (str or object): The name of the basemap as a string, or an object representing the basemap.

        Raises:
            TypeError: If the name is neither a string nor an object representing a basemap.

        Returns:
            None
        """

        if isinstance(name, str):
            url = eval(f"basemaps.{name}").build_url()
            self.add_tile_layer(url, name)
        else:
            self.add(name)

    def add_layers_control(self, position="topright"):
        """Adds a layers control to the map.

        Args:
            position (str, optional): The position of the layers control. Defaults to "topright".
        """
        self.add_control(ipyleaflet.LayersControl(position=position))

    def add_geojson(self, data, name="geojson", **kwargs):
        """Adds a GeoJSON layer to the map.

        Args:
            data (str | dict): The GeoJSON data as a string or a dictionary.
            name (str, optional): The name of the layer. Defaults to "geojson".
        """
        import json

        if isinstance(data, str):
            with open(data) as f:
                data = json.load(f)

        if "style" not in kwargs:
            kwargs["style"] = {"color": "blue", "weight": 1, "fillOpacity": 0}

        if "hover_style" not in kwargs:
            kwargs["hover_style"] = {"fillColor": "#ff0000", "fillOpacity": 0.5}

        layer = ipyleaflet.GeoJSON(data=data, name=name, **kwargs)
        self.add(layer)

    def add_shp(self, data, name="shp", **kwargs):
        """
        Adds a shapefile to the current map.

        Args:
            data (str or dict): The path to the shapefile as a string, or a dictionary representing the shapefile.
            name (str, optional): The name of the layer. Defaults to "shp".
            **kwargs: Arbitrary keyword arguments.

        Raises:
            TypeError: If the data is neither a string nor a dictionary representing a shapefile.

        Returns:
            None
        """
        import shapefile
        import json

        if isinstance(data, str):
            with shapefile.Reader(data) as shp:
                data = shp.__geo_interface__

        self.add_geojson(data, name, **kwargs)

    def add_image(self, url, bounds, name="image", **kwargs):
        """Adds an image overlay to the map.

        Args:
            url (str): The URL of the image.
            bounds (list): The bounds of the image.
            name (str, optional): The name of the layer. Defaults to "image".
        """
        layer = ipyleaflet.ImageOverlay(url=url, bounds=bounds, name=name, **kwargs)
        self.add(layer)

    def add_raster(self, data, name="raster", zoom_to_layer=True, **kwargs):
        """Adds a raster layer to the map.

        Args:
            data (str): The path to the raster file.
            name (str, optional): The name of the layer. Defaults to "raster".
        """

        try:
            from localtileserver import TileClient, get_leaflet_tile_layer
        except ImportError:
            raise ImportError("Please install the localtileserver package.")

        client = TileClient(data)
        layer = get_leaflet_tile_layer(client, name=name, **kwargs)
        self.add(layer)

        if zoom_to_layer:
            self.center = client.center()
            self.zoom = client.default_zoom
            
    def add_vector(self, data):
        """
        Add vector data to the map.

        Args:
            data (str or geopandas.GeoDataFrame): The vector data to add. This can be a file path or a GeoDataFrame.
        """
        import geopandas as gpd
        from ipyleaflet import GeoData
        
        if isinstance(data, gpd.GeoDataFrame):
            geo_json_data = data.to_json()
        elif isinstance(data, str):
            data = gpd.read_file(data)
            geo_json_data = data.to_json()
        else:
            raise ValueError("Unsupported data format. Please provide a GeoDataFrame or a file path.")

        vector_layer = GeoData(geo_dataframe = gpd.read_file(geo_json_data))
        self.add_layer(vector_layer)

    def add_zoom_slider(
        self, description="Zoom level", min=0, max=24, value=10, position="topright"
    ):
        """Adds a zoom slider to the map.

        Args:
            position (str, optional): The position of the zoom slider. Defaults to "topright".
        """
        zoom_slider = widgets.IntSlider(
            description=description, min=min, max=max, value=value
        )

        control = ipyleaflet.WidgetControl(widget=zoom_slider, position=position)
        self.add(control)
        widgets.jslink((zoom_slider, "value"), (self, "zoom"))

    def add_widget(self, widget, position="topright"):
        """Adds a widget to the map.

        Args:
            widget (object): The widget to be added.
            position (str, optional): The position of the widget. Defaults to "topright".
        """
        control = ipyleaflet.WidgetControl(widget=widget, position=position)
        self.add(control)

    def add_opacity_slider(
        self, layer_index=-1, description="Opacity", position="topright"
    ):
        """Adds an opacity slider to the map.

        Args:
            layer (object): The layer to which the opacity slider is added.
            description (str, optional): The description of the opacity slider. Defaults to "Opacity".
            position (str, optional): The position of the opacity slider. Defaults to "topright".
        """
        layer = self.layers[layer_index]
        opacity_slider = widgets.FloatSlider(
            description=description,
            min=0,
            max=1,
            value=layer.opacity,
            style={"description_width": "initial"},
        )

        def update_opacity(change):
            layer.opacity = change["new"]

        opacity_slider.observe(update_opacity, "value")

        control = ipyleaflet.WidgetControl(widget=opacity_slider, position=position)
        self.add(control)

    #basemap dropdown menu widget and behavior
    def add_basemap_gui(self, basemaps=None, position="topright"):
        """Adds a basemap GUI to the map.

        Args:
            position (str, optional): The position of the basemap GUI. Defaults to "topright".
        """
        basemap_selector = widgets.Dropdown( 
            options= [
                "OpenStreetMap",
                "OpenTopoMap",
                "Esri.WorldImagery",
                "Esri.NatGeoWorldMap",
                "NASAGIBS.ModisTerraTrueColorCR",
                "NASAGIBS.ModisTerraBands367CR",
                "NASAGIBS.ModisTerraBands721CR",
                "NASAGIBS.ModisAquaTrueColorCR",
                "NASAGIBS.ModisAquaBands721CR",
                "NASAGIBS.ViirsEarthAtNight2012",
            ],
            value = "OpenStreetMap",
            description="Basemap",
        )

        #close button for dropdown menu
        close_button = widgets.Button(
            description= "",
            button_style = "primary",
            tooltip = "Dropdown Toggle",
            icon = "times",
            layout = Layout(width ="35px") #less than 35 add noise
        )
        
        basebox = widgets.HBox([basemap_selector, close_button]) #widget box

        #actions for buttons and button control
        def on_click(change):
            self.add_basemap(change["new"])
        basemap_selector.observe(on_click, "value")

        def close_click(change):
            basemap_selector.close()
            close_button.close()
    

        close_button.on_click(close_click)


        control = ipyleaflet.WidgetControl(widget=basebox, position=position)
        self.add(control)





    def add_toolbar(self, position="topright"): #add toolbar functionality, basemap gui button, how keep toolbar from disappearing, remove basemap widget
        """Adds a toolbar to the map.

        Args:
            position (str, optional): The position of the toolbar. Defaults to "topright".
        """

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

        open_button = widgets.ToggleButton(
            value=False,
            tooltip='Open a file',
            icon='folder-open',
            layout=widgets.Layout(height='28px', width='28px')
        )


        toolbar = widgets.VBox([toolbar_button])


        def close_click(change):
            if change["new"]:
                toolbar_button.close()
                close_button.close()
                toolbar.close()

        close_button.observe(close_click, "value")

        rows = 2
        cols = 2
        grid = widgets.GridspecLayout(
            rows, cols, grid_gap="0px", layout=widgets.Layout(width="65px")
        )

        icons = ["folder-open", "map", "info", "question"]

        for i in range(rows):
            for j in range(cols):
                grid[i, j] = widgets.Button(
                    description="",
                    button_style="primary",
                    icon=icons[i * rows + j],
                    layout=widgets.Layout(width="28px", padding="0px"),
                )


        #click signal to backend/frontend
        def on_click(change):
            if change["new"]:
                toolbar.children = [widgets.HBox([close_button, toolbar_button]), grid]
            else:
                toolbar.children = [toolbar_button]

        toolbar_button.observe(on_click, "value")
        toolbar_ctrl = WidgetControl(widget=toolbar, position="topright")
        self.add(toolbar_ctrl)

        #output widget confirming button click
        output = widgets.Output()
        output_control = WidgetControl(widget=output, position="bottomright")
        self.add(output_control)



        def toolbar_callback(change): #links to actions to buttons

            if change.icon == "map":
                self.add_basemap_gui() #call basemap selector
                with output:
                    output.clear_output()
                    print("change the basemap")
            elif change.icon == "info":
                with output:
                    output.clear_output()
                    print("There is no info here.")
            elif change.icon == "question":
                with output:
                    output.clear_output()
                    print("There is no help here.")
            else:
                with output:
                    output.clear_output()
                    print(f"Icon: {change.icon}")

        for tool in grid.children:
            tool.on_click(toolbar_callback)


    def add_heatmap(
        self,
        data,
        latitude="latitude",
        longitude="longitude",
        value="value",
        name="Heat map",
        radius=25,
        **kwargs,
    ):
        """Adds a heat map to the map. Reference: https://ipyleaflet.readthedocs.io/en/latest/api_reference/heatmap.html

        Args:
            data (str | list | pd.DataFrame): File path or HTTP URL to the input file or a list of data points in the format of [[x1, y1, z1], [x2, y2, z2]]. For example, https://raw.githubusercontent.com/opengeos/leafmap/master/examples/data/world_cities.csv
            latitude (str, optional): The column name of latitude. Defaults to "latitude".
            longitude (str, optional): The column name of longitude. Defaults to "longitude".
            value (str, optional): The column name of values. Defaults to "value".
            name (str, optional): Layer name to use. Defaults to "Heat map".
            radius (int, optional): Radius of each “point” of the heatmap. Defaults to 25.

        Raises:
            ValueError: If data is not a list.
        """
        import pandas as pd
        from ipyleaflet import Heatmap

        try:
            if isinstance(data, str):
                df = pd.read_csv(data)
                data = df[[latitude, longitude, value]].values.tolist()
            elif isinstance(data, pd.DataFrame):
                data = data[[latitude, longitude, value]].values.tolist()
            elif isinstance(data, list):
                pass
            else:
                raise ValueError("data must be a list, a DataFrame, or a file path.")

            heatmap = Heatmap(locations=data, radius=radius, name=name, **kwargs)
            self.add(heatmap)

        except Exception as e:
            raise Exception(e)

    def add_legend(self, legend_title="Legend", legend_dict=None, position="topright"):
        """Adds a legend to the map.

        Args:
            legend_title (str, optional): The title of the legend. Defaults to "Legend".
            legend_dict (dict, optional): The legend dictionary. Defaults to None.
            position (str, optional): The position of the legend. Defaults to "topright".
        """
        from ipyleaflet import LegendControl

        legend = LegendControl(
            {
                legend_title: legend_dict
            },
            name="Legend",
            position=position,
        )
        self.add_control(legend)
    def add_marker_from_csv(self, in_csv, latitude="latitude", longitude="longitude", **kwargs):
        """Adds markers to the map based on a CSV file.

        Args:
            in_csv (str): The input CSV file containing the marker information.
            latitude (str, optional): The column name of latitudes. Defaults to "latitude".
            longitude (str, optional): The column name of longitudes. Defaults to "longitude".
        """
        import pandas as pd
        from ipyleaflet import Marker

        df = pd.read_csv(in_csv)
        for i, row in df.iterrows():
            marker = Marker(location=(row[latitude], row[longitude]), **kwargs)
            self.add_layer(marker)

    def add_time_slider(self, layers, time_intervals, position="bottomleft"):
        from ipywidgets import IntSlider, Play, jslink, HBox
        from ipyleaflet import WidgetControl

        start_year = time_intervals[0]
        end_year = time_intervals[-1]
        slider = IntSlider(value=start_year, min=start_year, max=end_year, description='Year')
        play = Play(value=start_year, min=start_year, max=end_year, step=1, interval=1000, description="Press play", disabled=False)
        jslink((play, 'value'), (slider, 'value'))
        widget_control = WidgetControl(widget=HBox([play, slider]), position=position)
        self.add_control(widget_control)

        def update_map(change):
            year = change['new']
            self.layers = [layer for layer in self.layers if layer.name != str(year)]
            if str(year) in layers:
                self.add_raster(layers[str(year)], name=str(year), colormap='terrain')

        slider.observe(update_map, 'value')

    # def create_gif(image_paths, output_path, duration=200):
    #     """
    #     Creates a GIF from a list of image paths.

    #     Args:
    #         image_paths (list): A list of paths to the images.
    #         output_path (str): The path where the GIF should be saved.
    #         duration (float, optional): The display time for each frame in seconds. Defaults to 0.2.
    #     """
    #     # Create a list to hold the images
    #     images = []

    #     # Iterate over the image paths
    #     for image_path in image_paths:
    #         # Read the image file
    #         img = imageio.imread(image_path)
            
    #         # Append the image to the list
    #         images.append(img)

    #     # Save the images as a GIF
    #     imageio.mimsave(output_path, images, duration=duration)
    # def create_gif(image_paths, output_path, duration=200):
    #     """
    #     Creates a GIF from a list of image paths.

    #     Args:
    #         image_paths (list): A list of paths to the images.
    #         output_path (str): The path where the GIF should be saved.
    #         duration (int, optional): The display time for each frame in milliseconds. Defaults to 200.
    #     """
    #     # Create a list to hold the images
    #     images = []

    #     # Iterate over the image paths
    #     for image_path in image_paths:
    #         # Open the image file
    #         img = Image.open(image_path)
            
    #         # Append the image to the list
    #         images.append(img)

    #     # Save the images as a GIF
    #     images[0].save(output_path, save_all=True, append_images=images[1:], loop=0, duration=duration)