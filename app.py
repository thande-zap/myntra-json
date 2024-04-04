import pandas as pd
import streamlit as st
from scrapper import scrapper


def app():

    st.set_page_config(
        page_title="Myntra Gold Products",
        layout="wide",
        page_icon=":money_bag:",
    )
    df = pd.read_csv("db/products.csv")

    if st.button("Refresh"):
        scrapper()
        df = pd.read_csv("db/products.csv")

    st.sidebar.header("Filter")
    weights = st.sidebar.multiselect(
        "Filter by Weight:",
        options=df["Weight"].unique(),
        default=df["Weight"].unique(),
    )
    df_selection = df.query(
        "Weight == @weights",
    )

    st.dataframe(
        df_selection,
        hide_index=True,
        use_container_width=True,
        height=1000,
    )


app()
