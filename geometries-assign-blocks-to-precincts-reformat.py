
import json
import numpy as np
from gerrytools.geometry import invert

# Correct and convert types.
with open("data/unitmaps/blocks20-precincts-badtypes.json") as r: correspondence = json.load(r)

updated = {}

for block, precinct in correspondence.items():
    try: int(precinct)
    except: continue

    updated[block] = str(int(precinct)).zfill(6)

with open("data/unitmaps/blocks20-precincts.json", "w") as w: json.dump(updated, w)
with open("data/unitmaps/precincts-blocks20.json", "w") as w: json.dump(invert(updated), w)
