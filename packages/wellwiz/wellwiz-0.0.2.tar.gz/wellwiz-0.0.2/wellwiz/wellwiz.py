"""Main module."""

from ipyleaflet import Map, Marker, WidgetControl, LayersControl, TileLayer, basemaps
import pandas as pd
import ipywidgets as widgets
import numpy as np

class MapWithCSV(Map):
    def __init__(self, **kwargs):
        """
        Initializes the MapWithCSV class.

        Args:
            **kwargs: Additional keyword arguments for initializing the map.
        """
        super().__init__(**kwargs)
        self.center = (35.8, -86.0)  
        self.zoom = 7                
        self.scroll_wheel_zoom = True  

        # Define base layers
        osm_layer = TileLayer(name='OpenStreetMap', url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png")
        esri_layer = TileLayer(name='Esri Satellite', url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}")

        # Add base layers to the map
        self.add_layer(osm_layer)
        self.add_layer(esri_layer)

        # Add controls
        self.add_control(LayersControl(position='topright'))
        self.configure_ui()

        self.markers = {}  
        self.csv_data = None  

    def add_csv_layer(self, csv_url):
        """
        Adds CSV data as markers to the map.

        Args:
            csv_url (str): The URL of the CSV file containing marker data.
        """
        self.csv_data = pd.read_csv(csv_url)  
        for index, row in self.csv_data.iterrows():
            marker = Marker(location=(row['Latitude'], row['Longitude']), draggable=False)
            self.markers[marker] = {
                'Well Name and Number': row['Well Name and Number'],
                'Purpose af Well': row['Purpose af Well']
            }
            marker.on_click(lambda *args, marker=marker, **kwargs: self.on_marker_click(marker, *args, **kwargs))
            self.add_layer(marker)

    def on_marker_click(self, marker, *args, **kwargs):
        """
        Handles click events on markers.

        Args:
            marker (Marker): The marker clicked.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.
        """
        data = self.markers[marker]
        lat, lon = marker.location
        print(f"Latitude: {lat}, Longitude: {lon}, Well Name and Number: {data['Well Name and Number']}, Purpose af Well: {data['Purpose af Well']}")

    def configure_ui(self):
        """
        Configures the user interface elements.
        """
        # Existing UI setup for CSV layer
        csv_url_text = widgets.Text(
            description="CSV URL:",
            placeholder="Enter CSV URL here",
            layout=widgets.Layout(width='300px')
        )
        csv_add_button = widgets.Button(description="Add CSV")
        csv_add_button.on_click(lambda b: self.add_csv_layer(csv_url_text.value))
        control_box = widgets.HBox([csv_url_text, csv_add_button])
        self.add_control(WidgetControl(widget=control_box, position='topright'))
        
        # Dropdown for risk calculation
        risk_dropdown = widgets.Dropdown(
            options=['Select Action', 'Calculate your risk of fracking exposure', 'I am good!'],
            value='Select Action',  
            disabled=False,
        )
        risk_dropdown.observe(self.handle_risk_dropdown, names='value')
        self.add_control(WidgetControl(widget=risk_dropdown, position='bottomleft'))

    def handle_risk_dropdown(self, change):
        """
        Handles changes in the risk dropdown.

        Args:
            change (dict): The change event.
        """
        if change.new == 'Calculate your risk of fracking exposure':
            self.request_user_coordinates()
        elif change.new == 'I am good!':
            print("No action needed. Enjoy your day!")  

    def request_user_coordinates(self):
        """
        Requests user coordinates for risk evaluation.
        """
        lat_text = widgets.Text(placeholder='Enter Latitude', description='Latitude:')
        lon_text = widgets.Text(placeholder='Enter Longitude', description='Longitude:')
        submit_button = widgets.Button(description='Check Risk')
        submit_button.on_click(lambda b: self.evaluate_risk(float(lat_text.value), float(lon_text.value)))
        display(widgets.VBox([lat_text, lon_text, submit_button]))

    def evaluate_risk(self, lat, lon):
        """
        Evaluates the risk based on user coordinates.

        Args:
            lat (float): Latitude.
            lon (float): Longitude.
        """
        # Check if the user coordinates are in the CSV list
        if any(np.isclose(self.csv_data['Latitude'], lat, atol=0.01) & np.isclose(self.csv_data['Longitude'], lon, atol=0.01)):
            print("Watch out, Bro!")
        else:
            print("Take a chill pill.")



