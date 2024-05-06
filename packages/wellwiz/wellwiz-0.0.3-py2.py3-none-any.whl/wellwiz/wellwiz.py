"""Main module."""

from ipyleaflet import Map, Marker, WidgetControl, LayersControl, TileLayer, basemaps
import pandas as pd
import ipywidgets as widgets
import numpy as np

class MapWithCSV(Map):
    """
    Extends ipyleaflet.Map to handle CSV-based geographic data for mapping and risk evaluation.
    """

    def __init__(self, **kwargs):
        """
        Initializes the map, adds base layers, controls, and preloads CSV data.
        """
        super().__init__(**kwargs)
        self.center = (35.8, -86.0)  # Set the initial center of the map
        self.zoom = 7  # Set the initial zoom level
        self.scroll_wheel_zoom = True  # Enable scroll wheel zoom

        # Adding the OpenStreetMap layer
        osm_layer = TileLayer(name='OpenStreetMap', url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png")
        self.add_layer(osm_layer)
        self.add_control(LayersControl(position='topright'))

        # Output widget for displaying information
        self.output_widget = widgets.Output(layout={'border': '1px solid black', 'width': '100%', 'height': '100px'})
        self.add_control(WidgetControl(widget=self.output_widget, position='bottomleft'))

        self.latlon_display = widgets.Label()  # Create a label to display coordinates
        self.add_control(WidgetControl(widget=self.latlon_display, position='topright'))

        # Preload CSV data from a URL
        self.default_csv_url = "https://raw.githubusercontent.com/OmIImO05/wellwiz/main/csv/Oil%20and%20Gas%20Well%20Permits.csv"
        self.csv_data = self.load_csv_data(self.default_csv_url)
        self.markers = {}
        self.configure_ui()
        self.add_latlong_widget()

    def load_csv_data(self, url):
        """
        Loads CSV data from a specified URL into a DataFrame.
        
        Parameters:
            url (str): URL pointing to a CSV file.

        Returns:
            DataFrame: A DataFrame containing the loaded data.
        """
        try:
            return pd.read_csv(url)
        except Exception as e:
            print(f"Failed to load CSV data: {e}")
            return pd.DataFrame({'Latitude': [], 'Longitude': []})  # Return an empty DataFrame on failure

    def add_csv_layer(self, csv_url):
        """
        Loads new CSV data from a URL and updates the map with markers.

        Parameters:
            csv_url (str): URL to load the CSV data from.
        """
        self.csv_data = self.load_csv_data(csv_url)
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
        Handles click events on markers, displaying detailed information.

        Parameters:
            marker (Marker): The marker that was clicked.
        """
        with self.output_widget:
            self.output_widget.clear_output(wait=True)
            data = self.markers[marker]
            lat, lon = marker.location
            print(f"Latitude: {lat}, Longitude: {lon}")
            print(f"Well Name and Number: {data['Well Name and Number']}")
            print(f"Purpose af Well: {data['Purpose af Well']}")


    def add_latlong_widget(self):
        """
        Sets up an output widget and interaction handler for displaying lat/lon on map clicks.
        """
        output = widgets.Output()
        control = WidgetControl(widget=output, position="bottomleft")
        self.add_control(control)

        def update_latlon(**kwargs):
            if kwargs.get('type') == 'click':
                latlon = kwargs.get('coordinates')
                if latlon:
                    with output:
                        output.clear_output()
                        print(f"Lat: {latlon[0]:.4f}, Long: {latlon[1]:.4f}")
                        self.risk_button(latlon)

        self.on_interaction(update_latlon)

    def risk_button(self, latlon):
        """
        Displays a button for initiating risk evaluation based on clicked coordinates.

        Parameters:
            latlon (tuple): Latitude and Longitude as a tuple.
        """
        if not hasattr(self, 'output_widget'):
            self.output_widget = widgets.Output()

        self.output_widget.clear_output()  # Clear previous widgets and outputs

        button = widgets.Button(description="Calculate your risk ...")
        button.on_click(lambda b: self.evaluate_risk(latlon[0], latlon[1]))
    
        with self.output_widget:
            display(button)
            

    def evaluate_risk(self, lat, lon):
        """
        Evaluates geographic risk based on proximity to CSV data points.

        Parameters:
            lat (float): Latitude for risk evaluation.
            lon (float): Longitude for risk evaluation.
        """
        miles_per_degree = 69.0
        watch_out_buffer_miles = 0.5
        cautious_buffer_miles = 2.5

        closest_distance = float('inf')
        for index, row in self.csv_data.iterrows():
            dist_lat = abs(row['Latitude'] - lat) * miles_per_degree
            dist_lon = abs(row['Longitude'] - lon) * miles_per_degree * np.cos(np.radians(lat))
            distance = np.sqrt(dist_lat**2 + dist_lon**2)
            if distance < closest_distance:
                closest_distance = distance

        if closest_distance <= watch_out_buffer_miles:
            print("Watch out, Bro!")
        elif closest_distance <= cautious_buffer_miles:
            print("Do not panic but be cautious!")
        else:
            print("Take a chill pill.")

    def configure_ui(self):
        """
        Configures the user interface for uploading CSV data and managing risk calculations.
        """
        csv_url_text = widgets.Text(description="CSV URL:", placeholder="Enter CSV URL here", layout=widgets.Layout(width='300px'))
        csv_add_button = widgets.Button(description="Add CSV")
        csv_add_button.on_click(lambda b: self.add_csv_layer(csv_url_text.value))
        control_box = widgets.HBox([csv_url_text, csv_add_button])
        self.add_control(WidgetControl(widget=control_box, position='topright'))


        risk_dropdown = widgets.Dropdown(
            options=['Select Action', 'Calculate your risk of fracking exposure', 'I am good!'],
            value='Select Action',
            disabled=False,
            style={'description_width': 'initial'}
        )
        risk_dropdown.layout.width = '300px'  # Adjust width
        risk_dropdown.layout.height = 'auto'  # Adjust height to auto
        risk_dropdown.observe(self.handle_risk_dropdown, names='value')
        self.add_control(WidgetControl(widget=risk_dropdown, position='topleft'))

    def handle_risk_dropdown(self, change):
        """
        Handles changes in the risk dropdown.

        Args:
        change (dict): The change event.
        """

        if change.new == 'Calculate your risk of fracking exposure':
            self.request_user_coordinates()
        elif change.new == 'I am good!':
            with self.output_widget:
                self.output_widget.clear_output()
                print("No action needed. Enjoy your day!")

    def request_user_coordinates(self):
        """
        Requests user coordinates for risk evaluation.
        """

        lat_text = widgets.Text(placeholder='Enter Latitude', description='Latitude:')
        lon_text = widgets.Text(placeholder='Enter Longitude', description='Longitude:')
        submit_button = widgets.Button(description='Check Risk')
        submit_button.on_click(lambda b: self.evaluate_risk(float(lat_text.value), float(lon_text.value)))
        user_input_ui = widgets.VBox([lat_text, lon_text, submit_button])
        with self.output_widget:
            self.output_widget.clear_output(wait=True)
            display(user_input_ui)

    def evaluate_risk(self, lat, lon):
        """
        Evaluates the risk based on user coordinates.

        Args:
            lat (float): Latitude.
            lon (float): Longitude.
        """

        with self.output_widget:
            self.output_widget.clear_output(wait=True)
            if any(np.isclose(self.csv_data['Latitude'], lat, atol=0.01) & np.isclose(self.csv_data['Longitude'], lon, atol=0.01)):
                print("Watch out, Bro!")
            else:
                print("Take a chill pill.")




