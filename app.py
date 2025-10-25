import streamlit as st
import pandas as pd

from utils.io import load_data
from utils.prep import preprocess, make_tables
from utils.viz import line_chart, bar_chart, heatmap_polluant_zone, show_summary, map_zones_pollution, map_interactive_zas

import sections.intro as intro
import sections.overview as overview
import sections.deep_dives as deep
import sections.conclusion as conclu

st.set_page_config(page_title="La qualité de l'air en France", layout="wide")

@st.cache_data(show_spinner=False)
def get_data():
    df_raw = load_data()
    df_clean = preprocess(df_raw)
    tables = make_tables(df_clean)
    return df_clean, tables

st.title("La qualité de l’air en France : une histoire de données")
st.caption("Source : LCSQA / INERIS / Atmo France — data.gouv.fr — Licence Ouverte Etalab 2.0")

df, _ = get_data()

with st.sidebar:
    st.header("Navigation")
    page = st.radio("Aller vers", ["Introduction", "Overview", "Deep dives", "Conclusion"])

df_filtered = df

if page in ["Overview", "Deep dives"]:
    with st.sidebar:
        st.markdown("---")
        st.header("Filtres")
        polluant_options = sorted(df['Polluant'].dropna().unique())
        metric = st.selectbox("Polluant", polluant_options)
        zas_filtered = df[df["Polluant"] == metric]["Zas"].dropna().unique()
        zas_options = sorted(zas_filtered)
        regions = st.multiselect("Zone (ZAS)", zas_options, default=zas_options)
        df_temp = df[(df["Polluant"] == metric) & (df["Zas"].isin(regions))]
        available_days = sorted(df_temp['jour'].dropna().unique())
        if available_days:
            date_range = st.select_slider(
                "Plage de dates",
                options=available_days,
                value=(available_days[0], available_days[-1])
            )
        else:
            date_range = None

    df_filtered = df.copy()
    df_filtered = df_filtered[df_filtered['Polluant'] == metric]
    df_filtered = df_filtered[df_filtered['Zas'].isin(regions)]
    if date_range:
        start, end = date_range
        df_filtered = df_filtered[(df_filtered['jour'] >= start) & (df_filtered['jour'] <= end)]

if page == "Introduction":
    intro.run(df)
elif page == "Overview":
    overview.run(df_filtered, metric=metric)
elif page == "Deep dives":
    deep.run(df_filtered, metric=metric)
else:
    conclu.run(df)
