import streamlit as st

st.set_page_config(
    page_title="Dashboard Coletâneas",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
)

from widgets.map import CollectionMap  # noqa: E402
from widgets.sidebar import Sidebar  # noqa: E402

st.title("Dashboard Coletâneas")

sidebar = Sidebar()

st.plotly_chart(
    CollectionMap(
        sidebar.filtered_state_df,
        sidebar.filtered_city_df,
        sidebar.column.name,
        sidebar.column.title,
        sidebar.plot_title,
    ),
    use_container_width=True,
)
