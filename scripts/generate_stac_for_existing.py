import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add Django project base dir to path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Set Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nrm_app.settings")

import django

django.setup()

import requests
import ee
from geoadmin.models import TehsilSOI
from computing.STAC_specs import generate_STAC_layerwise
from computing.models import Layer

import pandas as pd
layer_mapping_df = pd.read_csv('data/input/metadata/layer_mapping.csv')

def generate_stac_spec():
    layer_names_to_generate_rasters = [
        "change_tree_cover_gain_raster",
        "change_tree_cover_loss_raster",
        "change_cropping_reduction_raster",
        "change_urbanization_raster",
        "change_cropping_intensity_raster",
        "land_use_land_cover_raster",
        "terrain_raster",
        "clart_raster",
        # "tree_canopy_cover_density_raster",
        # "tree_cover_change_raster",
        # "tree_canopy_height_raster",
        "wri_restoration_raster",
    ]

    layer_names_to_generate_vectors = [
        "admin_boundaries_vector",
        "aquifer_vector",
        "drainage_lines_vector",
        "surface_water_bodies_vector",
        "nrega_vector",
        # "terrain_vector",
        "cropping_intensity_vector",
        "stage_of_groundwater_extraction_vector",
        "drought_frequency_vector",
        # "change_in_well_depth_vector",
    ]

    active_tehsils = TehsilSOI.objects.filter(
        active_status=True,
        district__active_status=True,
        district__state__active_status=True,
    ).select_related("district", "district__state")
    for tehsil in active_tehsils:
        state = tehsil.district.state
        district = tehsil.district
        print(state.state_name, district.district_name, tehsil.tehsil_name)
        # for layer_name_to_generate_raster in layer_names_to_generate_rasters:
        #     if layer_name_to_generate_raster == "land_use_land_cover_raster":
        #         lulc_year_range = [2017, 2018, 2019, 2020, 2021, 2022, 2023]
        #         for year in lulc_year_range:
        #             try:
        #                     is_rater_stac_generated = (
        #                         generate_STAC_layerwise.generate_raster_stac(
        #                             state=state.state_name,
        #                             district=district.district_name,
        #                             block=tehsil.tehsil_name,
        #                             layer_name=layer_name_to_generate_raster,
        #                             start_year=year,
        #                         )
        #                     )
        #                     if is_rater_stac_generated:
        #                         print(
        #                             f"stac spec {layer_name_to_generate_raster} generated for {state.state_name}_{district.district_name}_{tehsil.tehsil_name}"
        #                         )
        #                     else:
        #                         print(
        #                             f"ISSUE IN GENERATING {layer_name_to_generate_raster} for {state.state_name}_{district.district_name}_{tehsil.tehsil_name}"
        #                         )
        #                 pass
        #             except Exception as e:
        #                 print(
        #                     f"EXCEPTION IN GENERATING {layer_name_to_generate_raster} for {state.state_name}_{district.district_name}_{tehsil.tehsil_name} and error is:- {e}"
        #                 )
        #
        #     if layer_name_to_generate_raster in [
        #         "tree_canopy_cover_density_raster",
        #         "tree_canopy_height_raster",
        #     ]:
        #         tree_year_range = [2017, 2018, 2019, 2020, 2021, 2022]
        #         for year in tree_year_range:
        #             try:
        #                 is_rater_stac_generated = (
        #                     generate_STAC_layerwise.generate_raster_stac(
        #                         state=state.state_name,
        #                         district=district.district_name,
        #                         block=tehsil.tehsil_name,
        #                         layer_name=layer_name_to_generate_raster,
        #                         start_year=year,
        #                     )
        #                 )
        #                 if is_rater_stac_generated:
        #                     print(
        #                         f"stac spec {layer_name_to_generate_raster} generated for {state.state_name}_{district.district_name}_{tehsil.tehsil_name}"
        #                     )
        #                 else:
        #                     print(
        #                         f"ISSUE IN GENERATING {layer_name_to_generate_raster} for {state.state_name}_{district.district_name}_{tehsil.tehsil_name}"
        #                     )
        #                 pass
        #             except Exception as e:
        #                 print(
        #                     f"EXCEPTION IN GENERATING {layer_name_to_generate_raster} for {state.state_name}_{district.district_name}_{tehsil.tehsil_name} and error is:- {e}"
        #                 )
        #
        #     try:
        #         is_rater_stac_generated = generate_STAC_layerwise.generate_raster_stac(
        #             state=state.state_name,
        #             district=district.district_name,
        #             block=tehsil.tehsil_name,
        #             layer_name=layer_name_to_generate_raster,
        #         )
        #         if is_rater_stac_generated:
        #             print(
        #                 f"stac spec {layer_name_to_generate_raster} generated for {state.state_name}_{district.district_name}_{tehsil.tehsil_name}"
        #             )
        #         else:
        #             print(
        #                 f"ISSUE IN GENERATING {layer_name_to_generate_raster} for {state.state_name}_{district.district_name}_{tehsil.tehsil_name}"
        #             )
        #         pass
        #     except Exception as e:
        #         print(
        #             f"EXCEPTION IN GENERATING {layer_name_to_generate_raster} for {state.state_name}_{district.district_name}_{tehsil.tehsil_name} and error is:- {e}"
        #         )
        for layer_name_to_generate_vector in layer_names_to_generate_vectors:
            layer_df = layer_mapping_df[layer_mapping_df['layer_name'] == layer_name_to_generate_vector]
            db_dataset_name = layer_df['db_dataset_name'].iloc[0]
            geoserver_layer_name = layer_df['geoserver_layer_name'].iloc[0]
            geoserver_layer_name = geoserver_layer_name.replace("district", district.district_name.lower())
            geoserver_layer_name = geoserver_layer_name.replace("block", tehsil.tehsil_name.lower())        

            try:
                is_vector_stac_generated = generate_STAC_layerwise.generate_vector_stac(
                    state=state.state_name,
                    district=district.district_name,
                    block=tehsil.tehsil_name,
                    layer_name=layer_name_to_generate_vector,
                )

                layer_obj = (
                    Layer.objects.filter(
                        dataset__name=db_dataset_name,
                        layer_name=geoserver_layer_name,
                    )
                    .order_by("-layer_version")
                    .first()
                )
                if is_vector_stac_generated:
                    if layer_obj:
                        layer_obj.is_stac_specs_generated = True
                        layer_obj.save()
                        print("db flag updated.....")
                    print(
                        f"stac spec {layer_name_to_generate_vector} generated for {state.state_name}_{district.district_name}_{tehsil.tehsil_name}"
                    )
                else:
                    print(
                        f"ISSUE IN GENERATING {layer_name_to_generate_vector} for {state.state_name}_{district.district_name}_{tehsil.tehsil_name}"
                    )
                pass
            except Exception as e:
                print(
                    f"EXCEPTION IN GENERATING {layer_name_to_generate_vector} for {state.state_name}_{district.district_name}_{tehsil.tehsil_name} and error is:- {e}"
                )
    print("========== ALL STAC GENERATED FOR EXISTING LOCATION ==========")


generate_stac_spec()