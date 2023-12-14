import folium
from folium.plugins import HeatMap
import geopandas as gpd


#class for map-object

class Map_obj():
    def __init__(self):
        self.map = None
        self.mask = None


    def get_mask_layer(self, city): 
        #sets the city as the mask

        file = gpd.read_file(r'alla_kommuner_correct\alla_kommuner_correct.shp')

        filtered_data = file.loc[file['KOM_NAMN'] == city]

        self.mask = filtered_data['geometry'].values[0]


    def get_norway_road(self):


        # Load the Shapefile into a GeoDataFrame

        gdf = gpd.read_file(r'Rv80_Veistrekning\Rv80_Veistrekning.shp')

        # Set the CRS for the GeoDataFrame (replace 'EPSG:4326' with the appropriate CRS for your data)
        gdf = gdf.to_crs('EPSG:4326')

        # Assuming there's only one row in the GeoDataFrame
        line_geometry = gdf['geometry'].iloc[0]

        # Buffer operation to create a polygon representing a thicker line
        buffer_width = 0.00015  # Adjust this value based on the desired thickness
        self.mask = line_geometry.buffer(buffer_width)

        # Ensure the resulting polygon is valid
        if self.mask.is_valid:
        # Create a GeoDataFrame with the polygon geometry
            thicker_line_gdf = gpd.GeoDataFrame(geometry=[self.mask], crs='EPSG:4326')

        # Create a Folium map
            self.map = folium.Map(location=[line_geometry.centroid.y, line_geometry.centroid.x], zoom_start=10)

        # Plot the thicker line polygon on the map
            folium.GeoJson(thicker_line_gdf).add_to(self.map)
            mask_group = folium.FeatureGroup(name='Mask Layer').add_to(self.map)
            folium.GeoJson(self.mask).add_to(mask_group)

        
        
        


    def get_heatlayer(self, coordinates):
        #adds the coordinates to list. The folium.Heatmap wants list!

        list_coords = []

        for coord in coordinates:
            list_coords.append([coord.latitude, coord.longitude, coord.weight])
        return list_coords
    

    def get_markerslayer(self, list_coords, city):
        #adds the marker to map

        popup = self.print_elements(list_coords, city)
        folium.Marker([self.mask.centroid.y.mean(), self.mask.centroid.x.mean()], icon=folium.Icon(color='lightgray', icon='car-rear', prefix='fa'), popup=popup).add_to(folium.FeatureGroup(name='Antal').add_to(self.map))


    def get_map(self):

     
        if self.mask != None:
            #adds the mask to the layer
            self.map = folium.Map(location=[self.mask.centroid.y.mean(), self.mask.centroid.x.mean()], zoom_start=11)

            # Create a feature group for the mask GeoJSON layer
            mask_group = folium.FeatureGroup(name='Mask Layer').add_to(self.map)

            # Add the GeoJSON layer to the feature group
            folium.GeoJson(self.mask).add_to(mask_group)

        else:
            #else returns a empty map
            self.map = folium.Map(location=(63,15),zoom_start=5)
            
    
    def render_map(self):
        # to display a map, the map must be rendered to a html map
        self.map = self.map.get_root().render()


    def get_heatmap(self, coordinates, city):
        #adds the heatmap to the map
        
        list_coords = self.get_heatlayer(coordinates)
        self.get_markerslayer(list_coords, city)
        HeatMap(list_coords, radius = 15).add_to(folium.FeatureGroup(name='Heat Map').add_to(self.map))
        folium.LayerControl().add_to(self.map)
        
        return list_coords


    def print_elements(self, list_of_coords, city):
        #this string will be displayed in the popup/marker

        html = f"""{city}: {len(list_of_coords)} """
        iframe = folium.IFrame(html=html, width=100, height=100)
        popup = folium.Popup(iframe, max_width=2650)

        return popup

    def add_layer_control(self):
        self.map = folium.LayerControl().add_to(self.map)

       