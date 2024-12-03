import math
from typing import Literal

import pandas as pd
import plotly.graph_objects as go


type AnalyticsColumn = Literal[
    "Participantes",
    "Compradores",
    "PorcentagemCompradores",
    "LivrosVendidos",
    "Total",
]


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

    def __init__(
        self, df: pd.DataFrame, geojson: dict, collection: str, column: AnalyticsColumn
    ) -> None:
        df = df.loc[df["Coletânea"] == collection]

        super().__init__(
            geojson=geojson,
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
def get_state_choropleth(
    df: pd.DataFrame, geojson: dict, collection: str, column: str
) -> go.Choropleth:
    return StateChoropleth(df, geojson, collection, column)


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

    def __init__(
        self, df: pd.DataFrame, collection: str, column: AnalyticsColumn
    ) -> None:
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
def get_city_scattergeo(
    df: pd.DataFrame, collection: str, column: AnalyticsColumn
) -> go.Scattergeo:
    return CityScattergeo(df, collection, column)


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

    def __init__(
        self,
        state_df: pd.DataFrame,
        state_geojson: dict,
        city_df: pd.DataFrame,
        collection: str,
        column: AnalyticsColumn,
    ) -> None:
        super().__init__()
        self.add_trace(
            get_state_choropleth(state_df, state_geojson, collection, column)
        )
        self.add_trace(get_city_scattergeo(city_df, collection, column))
        self.update_geos(fitbounds="locations", visible=False)
        self.update_layout(
            title_text=self.get_title_text(collection, column),
            showlegend=False,
        )
