import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt

geojson_path = 'Parki_Narodowe.geojson'
parks_gdf = gpd.read_file(geojson_path)

poland_shapefile_path = 'polska.shp'
poland_gdf = gpd.read_file(poland_shapefile_path)

if parks_gdf.crs != "EPSG:4326":
    parks_gdf = parks_gdf.to_crs("EPSG:4326")
if poland_gdf.crs != "EPSG:4326":
    poland_gdf = poland_gdf.to_crs("EPSG:4326")

cities = {
    'Warszawa': (21.0122, 52.2297),
    'Kraków': (19.9445, 50.0647),
    'Wrocław': (17.0385, 51.1079),
    'Gdańsk': (18.6466, 54.3520)
}

cities_gdf = gpd.GeoDataFrame(
    list(cities.keys()),
    geometry=[Point(coords) for coords in cities.values()],
    crs="EPSG:4326"
)

nearest_parks = []
distances_km = []
for city in cities_gdf.geometry:
    distances = parks_gdf.geometry.distance(city)
    nearest_park = parks_gdf.iloc[distances.idxmin()]
    nearest_parks.append(nearest_park)
    distance_km = distances.min() * 111 
    distances_km.append(distance_km)

cities_gdf['nearest_park'] = [park['name'] for park in nearest_parks]
cities_gdf['distance_km'] = distances_km

fig, ax = plt.subplots(1, 1, figsize=(12, 12))
poland_gdf.plot(ax=ax, color='none', edgecolor='black')
parks_gdf.plot(ax=ax, color='green', edgecolor='black', alpha=0.5, label='National Parks')
cities_gdf.plot(ax=ax, color='red', markersize=50, label='Cities')

for i, (city, park) in enumerate(zip(cities_gdf.geometry, nearest_parks)):
    park_centroid = park.geometry.centroid
    city_coords = city.coords[0]
    plt.plot([city_coords[0], park_centroid.x], [city_coords[1], park_centroid.y], 'k--')
    mid_x = (city_coords[0] + park_centroid.x) / 2
    mid_y = (city_coords[1] + park_centroid.y) / 2
    plt.text(mid_x, mid_y, f"{distances_km[i]:.1f} km", fontsize=9, ha='center')

for city, coords in cities.items():
    plt.text(coords[0], coords[1], city, fontsize=12, ha='right')

plt.legend()
plt.title('Nearest National Park for Selected Cities in Poland')
plt.show()
