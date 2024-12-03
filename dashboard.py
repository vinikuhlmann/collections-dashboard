import plotly.express as px
import streamlit as st

from data.getters import get_city_df, get_state_df, get_state_geojson
from widgets.map import CollectionMap

st.set_page_config(
    page_title="Dashboard Coletâneas",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Dashboard Coletâneas")

col1, col2 = st.columns(2)

with col1:
    collection_selectbox = st.selectbox(
        "Coletânea",
        get_city_df()["Coletânea"].unique(),
    )

with col2:
    column_selectbox = st.selectbox(
        "Métrica",
        [
            "Participantes",
            "Compradores",
            "PorcentagemCompradores",
            "LivrosVendidos",
            "Total",
        ],
    )

st.plotly_chart(
    CollectionMap(
        state_df=get_state_df(),
        state_geojson=get_state_geojson(),
        city_df=get_city_df(),
        collection=collection_selectbox,
        column=column_selectbox,
    ),
    use_container_width=True,
)
