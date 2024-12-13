import numpy as np
import streamlit as st
import json
from utils import count_top_lvl_grids, count_second_lvl_grids
from utils import utils

st.set_page_config(page_title="RL-TS", page_icon="💫")
st.title(":rainbow[Order the Plus Code in the ROI]")

if st.session_state.get("polygon_type") is None:
    st.session_state["polygon_type"] = "Polygon"


def upload_geojson():
    uploaded_file = st.file_uploader(
        "Choose a JSON file", type=["json", "geojson"], key="uploader"
    )

    input_data = None
    if uploaded_file is not None:
        # Read the file and convert to JSON
        input_data = json.load(uploaded_file)

        type = (
            st.session_state["polygon_type"]
            if st.session_state["manual config"]
            else input_data["features"][0]["geometry"]["type"]
        )
        if (
            st.session_state["polygon_type"]
            != input_data["features"][0]["geometry"]["type"]
        ):
            st.toast("Polygon type mismatch. Manual Configuration required.")
            st.stop()

        try:
            msg = ""
            if type == "Polygon":
                input_data = input_data["features"][0]["geometry"]["coordinates"]
                msg = "single polygon feature "
            elif type == "MultiPolygon":
                if st.session_state["which_polygon"] == "Larger Polygon":
                    larger_polygon_idx = utils.get_larger_polygon_index(input_data)
                    input_data = input_data["features"][0]["geometry"]["coordinates"][
                        larger_polygon_idx
                    ]
                    msg = "MultiPolygon feature -> Larger Polygon "
                elif st.session_state["which_polygon"] == "All Polygons":
                    input_data = utils.include_all_coordinates(input_data)
                    msg = "MultiPolygon feature -> All polygons"

            # if not st.session_state["manual config"]:
            #     input_data = input_data
            # else:
            #     input_data = input_data[0]
            input_data = input_data[0]

            shape = np.array(input_data).shape
            st.toast(f"{msg} {shape}")
        except:
            st.error(
                "Error in pasrsing. Please configure manually or follow the template structure."
            )
            st.stop()

        # # Display the JSON data
        # st.json(input_data)
    return input_data


def main(input_data):
    level1_ordered, plus_codes = count_top_lvl_grids.entry(input_data)
    level2_ordered_imputed = count_second_lvl_grids.entry(level1_ordered, plus_codes)
    st.success(level2_ordered_imputed)


with st.sidebar:
    st.session_state["manual config"] = st.toggle("Manual Configuration")
    if st.session_state["manual config"]:
        st.session_state["polygon_type"] = st.radio(
            "**Select feature type**", ["Polygon", "MultiPolygon"]
        )

        if st.session_state["polygon_type"] == "MultiPolygon":
            st.write("-" * 10)
            st.session_state["which_polygon"] = st.radio(
                "What to include?", ["All Polygons", "Larger Polygon"]
            )
    else:
        st.session_state["polygon_type"] = "Polygon"
        st.session_state["which_polygon"] = None

    st.write("-" * 10)

    if st.button("Template"):
        if st.session_state["polygon_type"] == "Polygon":
            filepath = "./data/template_polygon.geojson"
        elif st.session_state["polygon_type"] == "MultiPolygon":
            filepath = "./data/template_multipolygon.geojson"
        else:
            filepath = ""

        if not filepath:
            st.toast("Filepath is empty")
            st.stop()

        with open(filepath) as geo_file:
            template = json.load(geo_file)
            st.json(template)

    st.write("-" * 10)

input_data = upload_geojson()
main(input_data)
