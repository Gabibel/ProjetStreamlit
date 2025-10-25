import streamlit as st
from utils.viz import map_interactive_zas

def run(df):
    st.header("Introduction, Peut-on vraiment respirer l'air en France ?")

    st.write("""
     Chaque année en France, près de **40 000 décès** sont attribués à la pollution de l’air,
    en particulier à l’exposition prolongée aux particules fines (PM2,5). La qualité de l’air
    n’est donc pas un indicateur environnemental parmi d’autres : c’est un déterminant de santé
    publique dont les effets sont mesurables dès aujourd’hui.

    Ce tableau de bord s’appuie sur des données ouvertes produites par le LCSQA / INERIS / Atmo France,
    qui surveillent en continu différents polluants réglementés (NO₂, O₃, PM10, PM2,5, SO₂…)
    au sein de **81 zones de surveillance atmosphérique (ZAS)** réparties sur le territoire français.
    Ces mesures constituent une base empirique suffisamment riche pour analyser l’évolution et
    la répartition de la pollution dans l’espace et dans le temps.

    L’ambition de ce travail n’est pas seulement descriptive : il s’agit d’interroger ces données
    pour éclairer des écarts potentiels entre territoires, détecter des tendances, et identifier les
    polluants qui contribuent le plus aux dépassements observés. L’enjeu est de savoir si l’amélioration
    perçue en matière de qualité de l’air est homogène, progressive, ou au contraire localisée et fragile.

    L’analyse qui suit cherche à répondre à trois questions essentielles :
    1) observe-t-on une amélioration ou une dégradation au fil des années ?
    2) les niveaux de pollution sont-ils homogènes entre les zones ou fortement contrastés ?
    3) certains polluants dominent-ils selon les régions ou les périodes ?

    Avant d’entrer dans ces dimensions analytiques, la carte ci-dessous situe les zones ZAS
    qui servent de points de collecte aux mesures utilisées dans ce projet.
    """)

    map_interactive_zas(df)

    st.caption("Carte des zones de surveillance atmosphérique (ZAS) présentes dans le dataset.")
