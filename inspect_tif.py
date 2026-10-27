import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import rasterio

path = Path(sys.argv[1])

with rasterio.open(path) as src:
    print("File:       ", path.name)
    print("CRS:        ", src.crs)
    print("Resolution: ", src.res)
    print("Bounds:     ", src.bounds)
    print("Size:       ", src.width, "x", src.height, "pixels")
    print("Bands:      ", src.count)
    print("Data type:  ", src.dtypes)
    print("Nodata:     ", src.nodata)
    band = np.ma.masked_invalid(src.read(1))

print("\nValue range:", float(band.min()), "to", float(band.max()))
print("Mean:       ", float(band.mean()))
print("Masked pixels: %.1f%%" % (100 * np.ma.getmaskarray(band).mean()))

fig, ax = plt.subplots(figsize=(8, 7))
im = ax.imshow(band, cmap="RdYlBu", vmin=-1, vmax=1)
fig.colorbar(im, ax=ax, shrink=0.8, label="NDMI")
ax.set_title(path.name, fontsize=8)
Path("docs").mkdir(exist_ok=True)
fig.savefig(f"docs/{path.stem[:40]}.png", dpi=150, bbox_inches="tight")
plt.show()
