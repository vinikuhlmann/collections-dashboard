import streamlit as st

from dataclasses import dataclass
from data.getters import get_city_df, get_state_df, get_state_geojson


@dataclass
class Column:
    name: str
    title: str
    relationship_text: str = None


COLUMNS = [
    Column("Participantes", "Quantidade de participantes"),
    Column("Compradores", "Quantidade de compradores"),
    Column("LivrosVendidos", "Quantidade de livros vendidos", "na"),
    Column("Total", "Receita total", "obtida"),
]

column_title_mapping = {column.title: column for column in COLUMNS}


class Sidebar:
    def __init__(self):
        self.city_df = get_city_df()
        self.state_df = get_state_df()
        self.state_geojson = get_state_geojson()

        with st.sidebar:
            st.title("Filtros")

            self.collection_filter = st.selectbox(
                "Coletânea",
                self.city_df["Coletânea"].unique(),
                index=None,
                placeholder="Selecione uma coletânea",
            )

            self.column_filter = st.selectbox(
                "Métrica",
                [column.title for column in COLUMNS],
            )

    @property
    def column(self):
        return column_title_mapping[self.column_filter]

    @property
    def filtered_state_df(self):
        return (
            self.state_df[self.state_df["Coletânea"] == self.collection_filter]
            if self.collection_filter
            else self.state_df
        )

    @property
    def filtered_city_df(self):
        return (
            self.city_df[self.city_df["Coletânea"] == self.collection_filter]
            if self.collection_filter
            else self.city_df
        )

    @property
    def plot_title(self) -> str:
        relationship_text = (
            f" {self.column.relationship_text}" if self.column.relationship_text else ""
        )
        collection_text = (
            f'na coletânea "{self.collection_filter}"'
            if self.collection_filter
            else "em todas as coletâneas"
        )
        return (
            f"Mapa de {self.column.title.lower()}{relationship_text} {collection_text}"
        )
