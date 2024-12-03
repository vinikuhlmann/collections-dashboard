import json

import pandas as pd
import streamlit as st


@st.cache_data
def get_city_df() -> pd.DataFrame:
    return pd.read_csv("data/collections_summary_city.csv")


@st.cache_data
def get_state_df() -> pd.DataFrame:
    return pd.read_csv("data/collections_summary_state.csv")


@st.cache_data
def get_state_geojson() -> dict:
    with open("data/state_geometries.geojson") as f:
        return json.load(f)
