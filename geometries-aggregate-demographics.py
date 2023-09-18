
import pandas as pd
import geopandas as gpd
import json


# Create a dataframe mapping block IDs to precinct IDs with appropriate types.
with open("data/unitmaps/blocks20-precincts.json") as r: correspondence = json.load(r)
cdf = pd.DataFrame.from_dict(correspondence, orient="index", columns=["PRECINCTID20"])
cdf = cdf.reset_index().rename(columns={"index": "GEOID20"})
for c in list(cdf): cdf[c] = cdf[c].astype(str) 

# Read in block-level data; get total population and VAP data.
demographics = pd.read_csv("data/demographics/blocks20-P1.csv")
demographicsVAP = pd.read_csv("data/demographics/blocks20-P3.csv")
demographicsNHVAP = pd.read_csv("data/demographics/blocks20-P4.csv").drop("VAP20", axis=1)

demographics = demographics.merge(demographicsVAP, on="GEOID20").merge(demographicsNHVAP, on="GEOID20")
demographics["GEOID20"] = demographics["GEOID20"].astype(str)
demographics = demographics.merge(cdf, on="GEOID20")

# Keep only the things we want.
keep = [
    "GEOID20", "PRECINCTID20", "TOTPOP20", "VAP20", "WHITEVAP20", "NHWHITEVAP20",
    "BLACKVAP20", "NHBLACKVAP20", "AMINVAP20", "NHAMINVAP20"
]
demographics = demographics[keep]

# Group by precinct ID, then sum. Add rows for small, overlooked precincts.
aggregated = demographics.groupby("PRECINCTID20").sum().reset_index()
aggregated["PRECINCTID20"] = aggregated["PRECINCTID20"].str.zfill(6)

# Get geometries, then assign.
precincts = gpd.read_file("data/geometries/precinct20-elec.json")

# Merge demographic data.
precinctsDemo = precincts.merge(aggregated, on="PRECINCTID20")
precinctsDemo["PRECINCTID20"] = precinctsDemo["PRECINCTID20"].astype(str).str.zfill(6)

try:
    print("Checking that we don't lose precincts after adding demographics: ", end="")
    assert(len(precinctsDemo) == len(precincts))
except:
    print("missed something.")
    print("aggregated precincts:", len(aggregated))
    print("geometric precincts:", len(precincts))
    print("missing identifiers: ", set(precincts["PRECINCTID20"]).symmetric_difference(set(aggregated["PRECINCTID20"])))

print("didn't miss anything!")

# Write to file.
precinctsDemo.to_file("data/geometries/precinct20.json")
