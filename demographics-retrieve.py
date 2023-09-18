
import us
from gerrytools.data import census20

for table in ["P1", "P3", "P4"]:
    # Get block population data from the Census.
    data = census20(us.states.OK, geometry="block", table=table)
    data["GEOID20"] = data["GEOID20"].astype(str)
    data.to_csv(f"data/demographics/blocks20-{table}.csv", index=False)
