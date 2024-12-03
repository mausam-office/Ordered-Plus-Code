import streamlit as st
import json
from utils import count_top_lvl_grids, count_second_lvl_grids

st.set_page_config(page_title="RL-TS", page_icon="💫")
st.title(":rainbow[Order the Plus Code in the ROI]")


def upload_geojson():
    uploaded_file = st.file_uploader("Choose a JSON file", type="json", key="uploader")

    input_data = None
    if uploaded_file is not None:
        # Read the file and convert to JSON
        input_data = json.load(uploaded_file)

        try:
            input_data = input_data["geometry"]["coordinates"][0]
        except:
            st.error("Error in pasrsing. Please follow the template structure.")
            st.stop()

        # # Display the JSON data
        # st.json(input_data)
    return input_data


def main(input_data):
    level1_ordered, plus_codes = count_top_lvl_grids.entry(input_data)
    level2_ordered_imputed = count_second_lvl_grids.entry(level1_ordered, plus_codes)
    st.success(level2_ordered_imputed)


with st.sidebar:
    if st.button("Template"):
        with open("./data/template.json") as geo_file:
            template = json.load(geo_file)
            st.json(template)


input_data = upload_geojson()
main(input_data)
