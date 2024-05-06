import folium
import streamlit_folium
from ipyleaflet import basemaps

class Map(folium.Map):
    def __init__(self, center = [20,0], zoom = 2, **kwargs):
        super().__init__(location=center, zoom_start = zoom, **kwargs)



#the whole point is to adapt conventions in case one package doesn't work in a given area. if ipyleaflet doesn't work then you can import the thebeans.foliummap module
# copy in modules for original module and adapt in this module
# can export maps to .html and add to any website server
    
#folium doesn't allow widgets but when you render a html can use widgets outside map

    
    def add_raster(self, data, name="raster", **kwargs):
        """Adds a raster layer to the map.

        Args:
            data (str): The path to the raster file.
            name (str, optional): The name of the layer. Defaults to "raster".
        """

        try:
            from localtileserver import TileClient, get_folium_tile_layer
        except ImportError:
            raise ImportError("Please install the localtileserver package.")

        client = TileClient(data)
        layer = get_folium_tile_layer(client, name=name, **kwargs)
        layer.add_to(self)

    def add_tile_layer(self, url, name, attribution="Custom Tile", **kwargs):
        """
        Adds a tile layer to the current map.

        Args:
            url (str): The URL of the tile layer.
            name (str): The name of the layer.
            attribution (str, optional): The attribution text to be displayed for the layer. Defaults to "Custom Tile".
            **kwargs: Arbitrary keyword arguments for additional layer options.

        Returns:
            None
        """
        layer = folium.TileLayer(tiles=url, name=name, attr=attribution, **kwargs)
        layer.add_to(self)

    def add_basemap(self, name, overlay=True):
        """
        Adds a basemap to the current map.

        Args:
            name (str or object): The name of the basemap as a string, or an object representing the basemap.
            overlay (bool, optional): Whether the basemap is an overlay. Defaults to True.

        Raises:
            TypeError: If the name is neither a string nor an object representing a basemap.

        Returns:
            None
        """

        if isinstance(name, str):
            url = eval(f"basemaps.{name}").build_url()
            self.add_tile_layer(url, name, overlay=overlay)
        else:
            name.add_to(self)

    def to_streamlit(self, width=700, height=500):
        """
        Converts the map to a streamlit component.

        Args:
            width (int, optional): The width of the map. Defaults to 700.
            height (int, optional): The height of the map. Defaults to 500.

        Returns:
            object: The streamlit component representing the map.
        """

        from streamlit_folium import folium_static

        return folium_static(self, width=width, height=height)

    def add_layer_control(self):
        """
        Adds a layer control to the map.

        Returns:
            None
        """
    def add_raster(self, data, name="raster", zoom_to_layer=True, **kwargs):
        """Adds a raster layer to the map.

        Args:
            data (str): The path to the raster file.
            name (str, optional): The name of the layer. Defaults to "raster".
        """
        import localtileserver
        
        try:
            from localtileserver import TileClient, get_folium_tile_layer
        except ImportError:
            raise ImportError("Please install the localtileserver package.")

        client = TileClient(data)
        layer = get_folium_tile_layer(client, name=name, **kwargs)
        self.add(layer)

        if zoom_to_layer:
            self.center = client.center()
            self.zoom = client.default_zoom

        folium.LayerControl().add_to(self)
