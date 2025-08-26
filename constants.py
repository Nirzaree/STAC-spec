# constants.py
from datetime import datetime

DEFAULT_START_DATE = datetime(2017, 7, 1)
DEFAULT_END_DATE = datetime(2024, 6, 30)

SRTM_DEM_START_DATE = datetime(2020,2,11) #used for terrain raster as it 
#uses SRTMGL1_003 product 
# https://www.earthdata.nasa.gov/data/catalog/lpcloud-srtmgl1-003
SRTM_DEM_END_DATE = datetime(2020,2,21)

no_data_classnames_list = ['clear','background']

base_url="https://raw.githubusercontent.com/Nirzaree/STAC-spec/stac-spec-common/"
data_url="https://raw.githubusercontent.com/Nirzaree/STAC-spec/stac-spec-common/data/"
raster_lulc_id="lulc_raster"
raster_lulc_description="Land Use Land Cover raster map"
raster_lulc_title="Raster layer"
swb_vector_id="swb_vector"
swb_vector_title="SWB Vector"
swb_vector_description="SWB vector layer"
stac_version="1.0.0"
