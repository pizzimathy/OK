
from gerrytools.geometry import dualgraph
import geopandas as gpd

precincts = gpd.read_file("data/geometries/precinct20.json")
G = dualgraph(precincts, index="PRECINCTID20")
G.to_json("data/graphs/precinct20.json")
