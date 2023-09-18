
import geopandas as gpd

# Read in electoral VTDs and ones with demographics.
precincts = gpd.read_file("data/geometries/precinct20-elec")

# Reformat columns.
columns = {
    "PCT_CEB": "PRECINCTID20",
    "G20PRERTRU": "PRES20R",
    "G20PREDBID": "PRES20D",
    "G20USSRINH": "SEN20R",
    "G20USSDBRO": "SEN20D"
}
precincts = precincts.rename(columns=columns)
precincts = precincts[["geometry"] + list(columns.values())]
precincts["PRECINCTID20"] = precincts["PRECINCTID20"].astype(str).str.zfill(6)
precincts.to_file("data/geometries/precinct20-elec.json", driver="GeoJSON")
