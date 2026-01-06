This is the development repo for the implementation of STAC specification (https://stacspec.org/en) for CoRE Stack Datasets (https://core-stack.org/). 

The STAC specs generated are live at : https://stac.core-stack.org/

Code Structure: 

| Code    | Description |
| ----------- | ----------- |
| notebooks/generate_stac_refactored.ipynb     | generate a raster and a vector item and create corresponding catalogs       |
| notebooks/final_flow.ipynb   | complete flow of STAC into 2 main flows : raster and vector, and updating files (STAC jsons for the catalogs/collections) and uploading data to s3        |
| scripts/generate_STAC_layerwise.py   | python script generated from final_flow.ipynb notebook     |