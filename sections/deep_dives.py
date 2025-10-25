import streamlit as st
from utils.viz import heatmap_polluant_zone, map_zones_pollution, dominant_pollutant_table
from utils.io import load_data
from utils.prep import preprocess

def run(df, metric=None):
    st.header("Deep dives")

    st.write("""
    Le Deep Dives approfondit les données pour identifier
    des motifs plus nets : **quelles zones ressortent comme les plus exposées** et
    **quels polluants dominent réellement selon les territoires**. L’enjeu n’est plus
    seulement de constater qu’il existe des écarts, mais de comprendre **où** et **sous
    quelle forme** ils apparaissent.

    Les résultats confirment que la pollution atmosphérique n’est pas répartie de manière
    uniforme. Certaines zones présentent des niveaux nettement supérieurs à la moyenne
    nationale, tandis que d’autres restent structurellement plus faibles. Ce contraste
    se maintient quel que soit le polluant, même si l’intensité des écarts varie.

    Enfin, la comparaison par organisme de surveillance montre que ces écarts ne proviennent pas d’un 
    différent de mesure mais de différences réelles entre territoires. Certaines zones sont surtout affectées par un seul polluant dominant, 
    alors que d’autres cumulent plusieurs sources de pollution, ce qui n’implique pas les mêmes priorités d’action.

    """)

    st.subheader("Quelles zones sont les plus touchées ?")
    st.write("""
    La carte ci-dessous permet de visualiser les zones de surveillance (ZAS) avec
    leur niveau moyen et le volume de mesures associé. Elle met en évidence les
    territoires où la concentration dépasse clairement la moyenne observée ailleurs.
    """)
    map_zones_pollution(df)
    
    st.subheader("Quels polluants dominent selon les zones ?")
    st.write("""
    La carte thermique ci-dessous montre si certains polluants sont problématiques
    de manière locale (zones spécifiques) ou globale (présents partout à des niveaux élevés).
    """)
    heatmap_polluant_zone(df, polluant=metric, key="deep_heatmap")

    df_full = preprocess(load_data())
    dominant_pollutant_table(df_full)
