import ee
import pandas as pd
from utilities.gee_utils import ee_initialize

# Initialize GEE
ee_initialize()

state = "uttar_pradesh"
district = "jaunpur"
block = "badlapur"

asset_path = f'projects/ee-corestackdev/assets/apps/mws/{state}/{district}/{block}/'

list_of_vector_layer = ['ET_annual_{district}_{block}', 'ET_fortnight_{district}_{block}', 'ET_fortnight_{district}_{block}_2017_2022', 
                        'ET_fortnight_{district}_{block}_2022_2024', 'Prec_annual_{district}_{block}', 'Prec_fortnight_{district}_{block}', 'Prec_fortnight_{district}_{block}', 
                        'Runoff_annual_{district}_{block}', 'Runoff_fortnight_{district}_{block}', 'admin_boundary_{district}_{block}', 'aquifer_vector_{district}_{block}',
                        'change_vector_{district}_{block}_Afforestation', 'change_vector_{district}_{block}_CropIntensity', 'change_vector_{district}_{block}_Deforestation',
                        'change_vector_{district}_{block}_Degradation', 'change_vector_{district}_{block}_Urbanization', 'crop_grid_{district}_{block}_with_uid_16ha',
                        'cropping_intensity_{district}_{block}_2017-23', 'drainage_lines_{district}_{block}', 'drought_{district}_{block}_2017_2022', 'filtered_delta_g_annual_{district}_{block}_uid',
                        'filtered_delta_g_fortnight_{district}_{block}_uid', 'filtered_mws_{district}_{block}_uid', '{district}_{block}_lulcXplains_clusters', '{district}_{block}_terrain_clusters',
                        'lulc_vector_{district}_{block}', 'restoration_{district}_{block}_vector', 'soge_vector_{district}_{block}', 'swb1_{district}_{block}', 'swb2_{district}_{block}',
                        'swb3_jaunpur_badlapur', 'tree_health_ccd_vector_{district}_{block}_2017', 'tree_health_ccd_vector_{district}_{block}_2018', 'tree_health_ccd_vector_{district}_{block}_2019',
                        'tree_health_ccd_vector_{district}_{block}_2020', 'tree_health_ccd_vector_{district}_{block}_2021', 'tree_health_ch_vector_{district}_{block}_2017',
                        'tree_health_ch_vector_{district}_{block}_2018', 'tree_health_ch_vector_{district}_{block}_2019', 'tree_health_ch_vector_{district}_{block}_2020', 'tree_health_ch_vector_{district}_{block}_2021',
                        'tree_health_overall_change_vector_{district}_{block}', 'well_depth_annual_{district}_{block}', 'well_depth_net_value_{district}_{block}'
                        ]

results = []

for each_asset in list_of_vector_layer:
    asset_name = each_asset.format(district=district, block=block)
    full_path = asset_path + asset_name
    
    try:
        print(f"Processing: {asset_name}")
        asset = ee.FeatureCollection(full_path)
        first_feature = asset.first()
        field_names = first_feature.propertyNames().getInfo()
        
        # Add asset name row
        results.append({
            "Asset": asset_name,  # Asset name in first row
            "Field": ""  # Empty for asset row
        })
        
        # Add each field under the asset
        for field in field_names:
            results.append({
                "Asset": "",  # Empty for field rows
                "Field": field
            })
            
        # Add empty row separator
        results.append({
            "Asset": "",
            "Field": ""
        })
        
    except Exception as e:
        print(f" Error processing {asset_name}: {str(e)}")
        results.append({
            "Asset": asset_name,
            "Field": f"ERROR: {str(e)}"
        })

# Create DataFrame and save
df = pd.DataFrame(results)
output_file = f"GEE_Asset_Fields_Grouped_{district}_{block}.xlsx"

# Simple export without formatting
df.to_excel(output_file, index=False)

print(f"\n Saved grouped fields to: {output_file}")
