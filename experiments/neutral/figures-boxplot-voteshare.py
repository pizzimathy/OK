
import matplotlib.pyplot as plt
import jsonlines

# Read in data and order appropriately.
ordered = []

with jsonlines.open("output/statistics/neutral.jsonl") as reader:
    for partition in reader:
        ordered.append(partition["RPCTS"])

