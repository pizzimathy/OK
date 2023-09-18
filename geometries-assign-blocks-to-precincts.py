
import json
import geopandas as gpd
from gerrytools.geometry import unitmap

# Retrieve geometries; create a unit map.
blocks = gpd.read_file("data/geometries/block20/")
blocks = blocks[["GEOID20", "TOTPOP20", "geometry"]]
blocks["GEOID20"] = blocks["GEOID20"].astype(str)

precincts = gpd.read_file("data/geometries/precinct20-elec/")
precincts["PRECINCTID20"] = precincts["PCT_CEB"]
precincts = precincts[["PRECINCTID20", "geometry"]]
precincts["PRECINCTID20"] = precincts["PRECINCTID20"].astype(str).str.zfill(6)

correspondence = unitmap((blocks, "GEOID20"), (precincts, "PRECINCTID20"))
with open("data/unitmaps/blocks20-precincts-badtypes.json", "w") as w: json.dump(correspondence, w)
