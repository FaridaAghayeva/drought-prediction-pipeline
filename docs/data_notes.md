# Data notes

## Satellite TIFs (data/raw/NDMI_CSOLNOK)

- Files: 158 TIFs, first date ___ to last date ___, typical gap ___ days
- Source: Sentinel-2 (S2A), NDMI, two tiles: T33TYN (95 files) and T34TCT (62 files), plus 1 odd file
- All real files share one CRS: EPSG:23700 (HD72 / EOV, Hungary)

### Tile T33TYN (95 files)
- CRS: EPSG:23700
- Resolution: ~9.9954 m
- Bounds: left=541279.85, bottom=161041.92, right=656577.03, top=276339.10
- Size (pixels): 11535 x 11535
- Bands: 1
- Data type: float32
- Nodata: None (not set; NaN used in practice)
- NaN share / zero share (2021-06-03 file): 21.1% / 9.4%
- Value range (min/max/mean): -0.9995 / 1.0 / 0.198

### Tile T34TCT (62 files)
- CRS: EPSG:23700
- Resolution: ~10.0008 m
- Bounds: left=596122.92, bottom=165931.30, right=708652.07, top=278450.44
- Size (pixels): 11252 x 11251
- Bands: 1
- Data type: float32
- Nodata: None (not set; NaN used in practice)
- NaN share / zero share (2021-07-06 file): 17.6% / 4.8%
- Value range (min/max/mean): -1.0 / 0.915 / 0.137

### What the image shows
NDMI moisture map: farm fields (yellow = drier, blue = wetter), a river on the right, a lake at the bottom left.

### Issues
- Empty swath area (NaN) in each scene, and no nodata value set in the files
- Zero share of 5-9% in the inspected files: likely fill values at the edges, to be treated as missing in later steps
- The two tiles have slightly different resolution and size (11535 x 11535 vs 11252 x 11251)
- 2021-03-08 file (N0209) is a 100x100 float64 raster in EPSG:4326: placeholder, excluded from analysis (ask supervisor)
