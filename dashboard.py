import plotly.express as px
import streamlit as st

from widgets.map import render_widget

st.set_page_config(
    page_title="Dashboard Coletâneas",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Dashboard Coletâneas")

render_widget()
