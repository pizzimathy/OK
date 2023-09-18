
from gerrychain import (
    GeographicPartition, Graph, MarkovChain, updaters, constraints,
    accept, Election
)
from gerrychain.tree import recursive_tree_part as rtp
from gerrychain.proposals import recom
from functools import partial
import jsonlines

# Set up election columns and statistics.
elections = {
    "PRES20": Election("PRES20", {"D": "PRES20D", "R": "PRES20R"}),
    "SEN20": Election("SEN20", {"D": "SEN20D", "R": "SEN20R"})
}

statistics = {
    "TOTPOP20": updaters.Tally("TOTPOP20", alias="TOTPOP20"),
    "CUTEDGES": lambda p: len(updaters.cut_edges(p)),
    "RSEATS": lambda p: p["PRES20"].seats("R"),
    "DSEATS": lambda p: p["PRES20"].seats("D"),
    "RPCTS": lambda p: list(p["PRES20"].percents("R")),
    "DPCTS": lambda p: list(p["PRES20"].percents("D"))
}
statistics.update(elections)

# Import the dual graph and get an initial partition.
G = Graph.from_json("../../data/graphs/precinct20.json")

TOTPOP20 = sum(data["TOTPOP20"] for _, data in G.nodes(data=True))
DISTRICTS = 5
initialAssignment = rtp(G, range(DISTRICTS), TOTPOP20/DISTRICTS, "TOTPOP20", 0.05)
initial = GeographicPartition(G, initialAssignment, updaters=statistics)

# Set the proposal and kick off the chain.
proposal = partial(recom, pop_col="TOTPOP20", pop_target=TOTPOP20/DISTRICTS, epsilon=0.05)
constraints = [constraints.within_percent_of_ideal_population(initial, 0.05, pop_key="TOTPOP20")]
N = 100000

chain = MarkovChain(
    proposal=proposal, constraints=constraints, accept=accept.always_accept,
    initial_state=initial, total_steps=N
)

# Iterate through the chain, collecting information along the way.
desired = ["TOTPOP20", "CUTEDGES", "RSEATS", "DSEATS", "RPCTS", "DPCTS"]

with jsonlines.open("output/statistics/neutral.jsonl", mode="w") as w:
    for partition in chain.with_progress_bar():
        stats = { name: partition[name] for name in desired }
        w.write(stats)
