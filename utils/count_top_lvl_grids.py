import streamlit as st
from kataho import KatahoSDK
from utils import utils


def entry(coordinates):
    if not coordinates:
        st.stop()

    plus_codes = list(
        set([KatahoSDK.lat_lng_to_plus(f"{lat},{long}") for long, lat in coordinates])
    )
    level1_plus_codes = [kode[:2] for kode in plus_codes]

    level1_matrix = utils.create_level1_matrix()

    level1_ordered, numbered_order = utils.order_level1_selected(
        level1_plus_codes, level1_matrix
    )
    return level1_ordered, plus_codes
