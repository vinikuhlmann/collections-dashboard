import json
import math
from typing import Literal

import pandas as pd
import plotly.graph_objects as go
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


type AnalyticsColumn = Literal[
    "Participantes",
    "Compradores",
    "PorcentagemCompradores",
    "LivrosVendidos",
    "Total",
]


class CityScattergeo(go.Scattergeo):
    def get_text(self, df: pd.DataFrame) -> pd.Series:
        return (
            df["Cidade"]
            + "<br>Participantes: "
            + df["Participantes"].astype(str)
            + "<br>Compradores: "
            + df["Compradores"].astype(str)
            + "<br>Porcentagem de compradores: "
            + (df["PorcentagemCompradores"] * 100).round(2).astype(str)
            + "%<br>Livros vendidos: "
            + df["LivrosVendidos"].astype(str)
            + "<br>Total: R$"
            + df["Total"].round(2).astype(str)
        )

    def __init__(self, collection: str, column: AnalyticsColumn) -> None:
        df = get_city_df()
        df = df.loc[df["Coletânea"] == collection]
        df["size"] = df.loc[:, column].apply(lambda x: 5 + math.log(x + 1) * 5)

        super().__init__(
            lon=df["Longitude"],
            lat=df["Latitude"],
            text=self.get_text(df),
            hovertemplate="%{text}<extra></extra>",
            marker=dict(
                size=df["size"],
            ),
        )


# @st.cache_resource
def get_city_scattergeo(collection: str, column: AnalyticsColumn) -> go.Scattergeo:
    return CityScattergeo(collection, column)


class StateChoropleth(go.Choropleth):
    def get_title_text(self, column: AnalyticsColumn) -> str:
        mapping: dict[AnalyticsColumn, str] = {
            "Participantes": "Participantes",
            "Compradores": "Compradores",
            "PorcentagemCompradores": "Porcentagem de compradores",
            "LivrosVendidos": "Livros vendidos",
            "Total": "Total",
        }
        return mapping[column]

    def __init__(self, collection: str, column: AnalyticsColumn) -> None:
        df = get_state_df()
        df = df.loc[df["Coletânea"] == collection]

        super().__init__(
            geojson=get_state_geojson(),
            locations=df["UF"],
            z=df[column],
            colorscale="Greens",
            hovertemplate="%{location}<br>%{z}<extra></extra>",
            colorbar=dict(
                title=dict(
                    text=self.get_title_text(column),
                ),
            ),
        )


# @st.cache_resource
def get_state_choropleth(collection: str, column: str) -> go.Choropleth:
    return StateChoropleth(collection, column)


class CollectionMap(go.Figure):
    def get_title_text(self, collection: str, column: AnalyticsColumn) -> str:
        mapping: dict[AnalyticsColumn, str] = {
            "Participantes": "Quantidade de participantes da",
            "Compradores": "Quantidade de compradores",
            "PorcentagemCompradores": "Porcentagem de compradores da",
            "LivrosVendidos": "Quantidade de livros vendidos na",
            "Total": "Receita total obtida na",
        }
        return f'{mapping[column]} coletânea "{collection}"'

    def __init__(self, collection: str, column: AnalyticsColumn) -> None:
        super().__init__()
        self.add_trace(get_state_choropleth(collection, column))
        self.add_trace(get_city_scattergeo(collection, column))
        self.update_geos(fitbounds="locations", visible=False)
        self.update_layout(
            title_text=self.get_title_text(collection, column),
            showlegend=False,
        )


def render_widget():
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
        CollectionMap(collection_selectbox, column_selectbox),
        use_container_width=True,
    )
