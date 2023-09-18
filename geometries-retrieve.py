
from us import states
from zipfile import ZipFile
from gerrytools.data import geometries20
from gerrytools.utilities import rename

# Retrieve geometries, unzip, and rename.
for geometry in ["block"]:
    geometries = geometries20(states.OK, f"data/geometries/{geometry}20.zip", geometry=geometry)
    with ZipFile(f"data/geometries/{geometry}20.zip", "r") as z: z.extractall(path=f"data/geometries/{geometry}20/")
    rename(f"data/geometries/{geometry}20", f"{geometry}20")
