
import numpy as np


def metropolis(column, threshold=0.40):
    """
    Prefers plans with one or more opportunity districts.
    """
    def _(partition):
        # If we don't have a parent, just accept.
        if not partition.parent: return True

        # Compare the number of "electoral opportunity" districts.
        proposed = sum(int(p > threshold) for p in partition[column])
        current = sum(int(p > threshold) for p in partition.parent[column])

        # Metropolis-Hastings.
        P = proposed/current
        q = np.random.uniform()
        return q < min(1, P)
    
    return _
