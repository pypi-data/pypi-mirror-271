from scgraph.geographs.marnet import marnet_geograph

from cave_utils import GeoUtils

count = 100
print("Creating 100 shortest paths geojson...")
out = GeoUtils.create_shortest_paths_geojson(
    geoGraph=marnet_geograph,
    ids=[str(i) for i in range(count)],
    origin_latitudes=[0 + i / 4 for i in range(count)],
    origin_longitudes=[0 + i / 4 for i in range(count)],
    destination_latitudes=[0 - i / 4 for i in range(count)],
    destination_longitudes=[0 - i / 4 for i in range(count)],
    show_progress=True,
    # filename="test.geojson"
)
print("Done!")
