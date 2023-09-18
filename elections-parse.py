
import pandas as pd

for year in ["20", "22"]:
    elections = pd.read_csv(
        f"data/elections/raw20{year}.csv",
        usecols=range(16),
        lineterminator="\n",
        header=None
    )

    # Align columns and types.
    elections = elections[[1,3,10,14]].drop([0])
    elections = elections.rename(columns={1: "PRECINCTID20", 3: "RACEID", 10: "PARTY", 14: f"TOTVOT"})
    for c in list(elections): elections[c] = elections[c].astype(str)
    
    # Get a dictionary for things.
    data = elections.to_dict("records")

    # Rewrite dataset.
    races = {
        "20": {
            "10001": "PRES20",
            "10003": "SEN20",
            "10005": "CONG20",
            "10010": "STSEN20"
        },
        "22": {
            "10001": "GOV22",
            "10002": "LTGOV22",
            "10010": "SEN22",
            "10013": "CONG22"
        }
    }

    # Reconstruct the dataframe so we have all races per identifier.
    rewired = { identifier: {} for identifier in elections["PRECINCTID20"]}

    for row in data:
        # Get the correct race codes per year; ignore rows without a race code in
        # our list of desired codes.
        subrace = races[year]
        if not any(race == row["RACEID"] for race in subrace.keys()): continue

        # Get the necessary info from the row.
        identifier = row["PRECINCTID20"]
        party = row["PARTY"][0]
        race = subrace[row["RACEID"]]

        # Continue if we hit an independent candidate.
        if party == "I": continue

        # Construct the new row.
        rewired[identifier]["PRECINCTID20"] = identifier
        rewired[identifier][race+party] = row["TOTVOT"]

    # Convert the dictionary into a dataframe.
    records = list(rewired.values())
    elections = pd.DataFrame.from_records(records).fillna(0)

    elections.to_csv(f"data/elections/20{year}.csv", index=False)
