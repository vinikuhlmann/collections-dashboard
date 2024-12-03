import math

import pandas as pd
import plotly.graph_objects as go

from data.getters import get_state_geojson


class StateChoropleth(go.Choropleth):
    def __init__(
        self,
        state_df: pd.DataFrame,
        column_name: str,
        column_title: str,
    ) -> None:
        super().__init__(
            geojson=get_state_geojson(),
            locations=state_df["UF"],
            z=state_df[column_name],
            colorscale="Greens",
            hovertemplate="%{location}<br>%{z}<extra></extra>",
            colorbar=dict(title=column_title),
        )


class CityScattergeo(go.Scattergeo):
    def _get_text(self, df: pd.DataFrame) -> pd.Series:
        return (
            "Coletânea: "
            + df["Coletânea"]
            + "<br>Cidade: "
            + df["Cidade"]
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

    def _calc_size(self, df: pd.Series) -> pd.Series:
        return df.apply(lambda x: 5 + math.log(x + 1) * 5)

    def __init__(self, city_df: pd.DataFrame, column_name: str) -> None:
        city_df["size"] = self._calc_size(city_df[column_name])

        super().__init__(
            lon=city_df["Longitude"],
            lat=city_df["Latitude"],
            text=self._get_text(city_df),
            hovertemplate="%{text}<extra></extra>",
            marker=dict(
                size=city_df["size"],
            ),
        )


class CollectionMap(go.Figure):
    def __init__(
        self,
        state_df: pd.DataFrame,
        city_df: pd.DataFrame,
        column_name: str,
        column_title: str,
        plot_title: str,
    ) -> None:
        super().__init__()
        self.add_trace(StateChoropleth(state_df, column_name, column_title))
        self.add_trace(CityScattergeo(city_df, column_name))
        self.update_geos(fitbounds="locations", visible=False)
        self.update_layout(
            title_text=plot_title,
            showlegend=False,
        )
