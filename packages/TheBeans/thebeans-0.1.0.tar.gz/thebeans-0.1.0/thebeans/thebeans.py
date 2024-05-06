"""Main module."""
#creating a new ipyleaflet class for deploymnet
#This doc shows you how the package was built. This is where you build code 
#make sure the packages are installed in your environment

#For Ipyleaflet and Ipywidgets
import ipyleaflet
import ipywidgets as widgets
import shutil
import geopandas as gpd
import json
import zipfile
import io
import os
import atexit
import tempfile



from ipyleaflet import Map, basemaps, Marker, WidgetControl, GeoJSON, ImageOverlay
from pyproj import CRS
from ipywidgets import Layout
from zipfile import ZipFile




class Map(ipyleaflet.Map):
    """Map class that inherits from ipyleaflet.Map.

    Args:
        ipyleaflet (Map): The ipyleaflet.Map class.
    """    
    def __init__(self, basemap = "OpenStreetMap", center = (0,0), zoom = 1, **kwargs):
        """Initialize the map.

        Args:
            center (list, optional): Set the center of the map. Defaults to WA [47.7511, -120.7401].
            zoom (int, optional): Set the zoom level of the map. Defaults to 6.
        """
        if "scroll_wheel_zoom" not in kwargs:
            kwargs["scroll_wheel_zoom"] = True

        #add layer control not as straight forward. Need to pass to an object and consider it as a parameter that you can pass. Ipyleaflet doesn't support.
        
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
            # self.grid = Grid()

        #self.add_toolbar()

        

    def add_tile_layer(self, url, name, **kwargs):
        layer = ipyleaflet.TileLayer(url=url, name=name, **kwargs)
        self.add_layer(layer)
    


    #This block means you can call up a basemap based on a string.
    #You can call up the basemap without knowing the url
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
        



    def add_layers_control(self, position='topright'):
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


    def add_vector(self, data, name="vector", extension=None, **kwargs):
        """
        Adds a vector layer to the current map.

        Args:
            data (str, GeoDataFrame, dict): The vector data as a string (path to file), GeoDataFrame, or a dictionary.
            name (str, optional): The name of the layer. Defaults to "vector".
            **kwargs: Arbitrary keyword arguments.

        Raises:
            TypeError: If the data is not in a supported format.

        Returns:
            None
        """
        if isinstance(data, str):
            if data.lower().endswith(('.geojson', '.json')):
                # Load GeoJSON directly
                with open(data) as f:
                    data = json.load(f)
                self.add_geojson(data, name, **kwargs)
            elif data.lower().endswith(('.shp')):
                # Read shapefile using GeoPandas and convert to GeoJSON
                gdf = gpd.read_file(data)
                self.addlayer(gdf)
                # self.add_geojson(gdf.__geo_interface__, name, **kwargs)
            elif extension == '.zip':
                # Extract shapefile from zip, read it using GeoPandas and convert to GeoJSON
                with tempfile.TemporaryDirectory() as tmp_dir:
                    with zipfile.ZipFile(data, 'r') as zip_ref:
                        zip_ref.extractall(tmp_dir)
                    shapefile_name = [file for file in os.listdir(tmp_dir) if file.endswith('.shp')][0]
                    gdf = gpd.read_file(os.path.join(tmp_dir, shapefile_name))
                    self.add_layer(gdf)
            else:
                raise TypeError("Unsupported vector data format.")
        elif isinstance(data, gpd.GeoDataFrame):
            self.add_geojson(data.__geo_interface__, name, **kwargs)
        elif isinstance(data, dict):
            self.add_geojson(data, name, **kwargs)
        else:
            raise TypeError("Unsupported vector data format.")
    


    def add_image(self, url, bounds, name="image", **kwargs):
        """
        Adds an image to the current map.

        Args:
            url (str): The URL of the image.
            bounds (list): The bounds of the image.
            name (str, optional): The name of the image. Defaults to "image".
            **kwargs: Arbitrary keyword arguments.

        Returns:
            None
        """
        import ipyleaflet

        image = ipyleaflet.ImageOverlay(url=url, bounds=bounds, name="image", **kwargs)
        self.add_layer(image)



    def add_raster(self, data, name="raster", zoom_to_layer=True, **kwargs):
        """Adds a raster layer to the map.

        Args:
            data (str): The path to the raster file.
            name (str, optional): The name of the layer. Defaults to "raster".
        """
        import localtileserver
        
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

        #return client to use in other functions
        return client


    def add_zoom_slider(self):
        """
        Adds a zoom slider to the map.
        """
        from ipyleaflet import WidgetControl

        zoom_slider = ipyleaflet.ZoomControl(position='topright')
        self.add_control(zoom_slider)
        




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
        return control






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



        def toolbar_callback(change): #links to actions to buttons,
            if change.icon == "folder-open": #file chooser callback
                self.open_fileupload()
                with output:
                    output.clear_output()

            elif change.icon == "map":
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


    temp_files = [] #store temp files and delete on kernel restart
    def open_fileupload(self, position="bottomright"):
        """Handles file upload from toolbar
        
        Args:
            position (str, optional): The position of the file upload control. Defaults to "bottomright".
            """
        fileupload = widgets.FileUpload(
            accept='',  
            multiple=True  # True to accept multiple files upload else False
        )

        close_button = widgets.Button(
            description= "",
            button_style = "primary",
            tooltip = "Dropdown Toggle",
            icon = "times",
            layout = Layout(width ="35px") #less than 35 add noise
        )

        basebox = widgets.HBox([fileupload, close_button])

        # Define a function to handle file upload
        def on_file_upload(change):
            
            uploaded_file = change['new'][0]
            content = uploaded_file['content'].tobytes() 
            name = uploaded_file['name']
            extension = os.path.splitext(name)[1]
            
            if extension == ".json" or extension == ".geojson":
                data = json.loads(content.decode("utf-8"))
                self.add_vector(data)
            elif extension == ".tif":
                with tempfile.NamedTemporaryFile(delete=False, suffix=".tif") as tmp:
                    tmp.write(content)
                    self.temp_files.append(tmp.name)
                    self.add_raster(tmp.name)
            elif extension == ".shp" or extension == ".zip":
                with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as tmp:
                    tmp.write(content)
                    self.add_vector(tmp.name, name, extension)
                #reads zipped shapefile, pulls crs from .prj, converts to geodataframe, converts to geojson, adds to map
                # ...grab code from add_vector...
                #     self.add_vector(gdf)

        
        # Set the function to be called when a file is uploaded
        fileupload.observe(on_file_upload, 'value')

        def close_click(change):
            fileupload.close()
            close_button.close()
        close_button.on_click(close_click)

        control = ipyleaflet.WidgetControl(widget=basebox, position=position)
        self.add(control)

        def cleanup(self):
            """Clean up the map by removing all layers and controls."""
            for temp_file in temp_files:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
        atexit.register(cleanup)   

    def add_latlong_widget(self, position = "bottomleft"):
        #can change min, max, height of box

        #add output widget to bottom of the map
        output = widgets.Output()
        control = WidgetControl(widget=output, position=position)
        self.add(control)  

        
        #define function to update lat long on mouse click. Can print(kwargs) to see all info
        #can define on double click, hover, move off map, etc
        def update_latlon(**kwargs):
            if kwargs.get('type') == 'mousedown':
                latlon = kwargs.get('coordinates')
                with output:
                    output.clear_output()
                    print(f"Lat: {latlon[0]:.4f}, Long: {latlon[1]:.4f}")

        self.on_interaction(update_latlon)

    # def array_to_overlay(self, array, name, **kwargs):
    #     from PIL import Image
    #     from io import BytesIO
    #     import base64
    #     import numpy as np
    
    #     """Convert a NumPy array to an ImageOverlay and add it to the map.
         
    #      """
    #     # Convert the array to an image
    #     im = Image.fromarray(np.uint8(array))

    #     # Save the image to a BytesIO object
    #     data = BytesIO()
    #     im.save(data, 'PNG')
    #     data.seek(0)

    #     # Encode the BytesIO object as a base64 string
    #     base64_str = "data:image/png;base64," + base64.b64encode(data.read()).decode()

    #     # Create an ImageOverlay with the base64 string as the URL
    #     overlay = ImageOverlay(url=base64_str, name=name)

    #     # Add the overlay to the map
    #     self.add_layer(overlay)
    
    def add_casual_hydrologic_network(self, url, **kwargs):
        from pysheds.grid import Grid
        import requests
        import matplotlib.pyplot as plt
        import matplotlib.colors as colors
        from matplotlib import cm
        from PIL import Image
        from io import BytesIO
        import base64
        import numpy as np

        """Delineate a full hydrologic network in one click. Processing times and ease of use not guaranteed.

        Args:
            data (_type_): Grid data input.
        """
        # def normalize(array):
        #     """Normalize a NumPy array to the range [0, 1]."""
        #     array = array.astype(int)  # Convert boolean arrays to integer
        #     array_min, array_max = array.min(), array.max()
        #     return (array - array_min) / (array_max - array_min)
        
        # #handle array to overlay visualization
        def array_to_image_overlay(array, name):
                """Convert a NumPy array to an ImageOverlay and add it to the map."""
                # Convert the array to an image
                im = Image.fromarray(np.uint8(array))

                # Save the image to a BytesIO object
                data = BytesIO()
                im.save(data, 'PNG')
                data.seek(0)

                # Encode the BytesIO object as a base64 string
                base64_str = "data:image/png;base64," + base64.b64encode(data.read()).decode()

                # Create an ImageOverlay with the base64 string as the URL
                overlay = ImageOverlay(url=base64_str, name=name)

                # Add the overlay to the map
                self.add_layer(overlay)


        #Download raster file from localtileserver
        # tile_client = self.add_raster(url)
        rasname = os.path.basename(url)
        response = requests.get(url)
        with open(rasname, 'wb') as f:
            f.write(response.content)

        grid = Grid.from_raster(rasname, data_name="dem", set_nodata = -999999)
        dem = grid.read_raster(rasname)

        # response = requests.get(data_url)
        # with tempfile.NamedTemporaryFile(delete=False, suffix=".tif") as tmp:
        #     tmp.write(response.content)
        #     data = tmp.name
        #     grid = self.Grid.from_raster(data)
        #     dem = self.read_raster(data) 

        #Surface Conditioning
        fillpits = grid.fill_pits(dem)
        filldepp = grid.fill_depressions(fillpits)
        inflate = grid.resolve_flats(filldepp, eps=1e-12, max_iter=1e9)#default parameters too narrow for most large areas

        #D8 Flow Direction
        dirmap = (64, 128, 1, 2, 4, 8, 16, 32)

        fdir = grid.flowdir(inflate, dirmap=dirmap) #fdir must be fdir
        acc = grid.accumulation(fdir)

        #pour point Methow River/Columbia River. DEFINE BY MARKER?
        x, y = -119.912764, 48.049753

        # Snap pour point to high accumulation cell
        x_snap, y_snap = grid.snap_to_mask(acc > 10000, (x, y))

        catch = grid.catchment(x=x_snap, y=y_snap, fdir=fdir, dirmap=dirmap)
        catch_view = grid.view(catch)

        #assign colormap
        # fdir = cm.viridis(normalize(fdir))
        # acc = cm.viridis(normalize(acc))
        # catch = cm.viridis(normalize(catch))

        # Save the data as image files
        array_to_image_overlay(fdir, 'Flow Direction')
        array_to_image_overlay(acc, 'Accumulation')
        array_to_image_overlay(catch, 'Catchment')

        # Add each dataset as a layer to the map
        # self.array_to_overlay(fdir, 'Flow Direction')
        # self.array_to_overlay(acc, 'Accumulation')
        # self.array_to_overlay(catch, 'Catchment')

        #plot fdir
        fig = plt.figure(figsize=(8,6))
        fig.patch.set_alpha(0)

        plt.imshow(fdir, extent=grid.extent, cmap='viridis', zorder=2)
        boundaries = ([0] + sorted(list(dirmap)))
        plt.colorbar(boundaries= boundaries,
                    values=sorted(dirmap))
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title('Flow direction grid', size=14)
        plt.grid(zorder=-1)
        plt.tight_layout()

        # Plot acc
        fig, ax = plt.subplots(figsize=(8,6))
        fig.patch.set_alpha(0)
        im = ax.imshow(acc, zorder=2,
                    cmap='cubehelix',
                    norm=colors.LogNorm(1, acc.max()),
                    interpolation='bilinear')
        plt.colorbar(im, ax=ax, label='Upstream Cells')
        plt.title('Flow Accumulation', size=14)
        plt.tight_layout()

        # Plot catch
        fig, ax = plt.subplots(figsize=(8,6))
        fig.patch.set_alpha(0)

        plt.grid('on', zorder=0)
        im = ax.imshow(np.where(catch_view, catch_view, np.nan), extent=grid.extent,
                    zorder=1, cmap='Greys_r')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title('Delineated Catchment', size=14)