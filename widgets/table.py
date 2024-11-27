import streamlit as st

st.title("Dados crus")
st.dataframe(
    df,
    use_container_width=True,
    column_config={
        "Nome": st.column_config.TextColumn(width="medium"),
        "CPF": st.column_config.TextColumn(width="medium"),
        "Email": st.column_config.TextColumn(width="medium"),
        "Rua/Logradouro": st.column_config.TextColumn(width="medium"),
        "Número": st.column_config.TextColumn(width="small"),
        "Complemento": st.column_config.TextColumn(width="small"),
        "Bairro": st.column_config.TextColumn(width="medium"),
        "Cidade": st.column_config.TextColumn(width="medium"),
        "UF": st.column_config.TextColumn(width="small"),
        "CEP": st.column_config.TextColumn(width="medium"),
        "Quantidade": st.column_config.NumberColumn(width="small"),
        "Total Livro": st.column_config.NumberColumn(format="R$ %.2f", width="small"),
        "Frete": st.column_config.NumberColumn(format="R$ %.2f", width="small"),
        "Total Geral": st.column_config.NumberColumn(format="R$ %.2f", width="small"),
        "Comprou": st.column_config.TextColumn(width="medium"),
        "Coletânea": st.column_config.TextColumn(width="medium"),
    },
    hide_index=True,
)
