import streamlit as st
from utils.prep import make_tables
from utils.viz import line_chart, bar_chart

def run(df,metric=None):
    st.header("Overview — premières tendances globales")

    if metric:
        st.info(f"Polluant sélectionné : {metric}")

    st.write("""
    Maintenant qu’on a vu où les mesures sont faites, on peut regarder **ce que disent
    les données à un niveau global**. L’idée ici n’est pas encore d’entrer dans le détail,
    mais d’avoir une première intuition : est-ce que les niveaux de pollution baissent ?
    Est-ce que c’est homogène en France ?
    """)

    st.write("""
    Il est possible de choisir **un polluant spécifique** à analyser à l’aide du menu de gauche ainsi que les zones géographiques (ZAS) (si existante avec le polluant) et la période.""")

    c1, c2, c3 = st.columns(3)
    c1.metric("Période couverte", f"{df['annee'].min()} — {df['annee'].max()}")
    c2.metric("Polluant mesuré", df['Polluant'].nunique())
    c3.metric("Zones (ZAS)", df['Zas'].nunique())

    st.write("""
    La période des données couvre plusieurs années (2021 - 2025), on y trouve 5 jours de données différentes""")

    tables = make_tables(df)

    st.subheader("Évolution temporelle des niveaux de pollution")
    st.write("Ce graphique représente l’évolution dans le temps de la valeur moyenne mesurée pour le polluant sélectionné. Chaque point correspond à la moyenne quotidienne des mesures disponibles pour ce polluant sur la période affichée.")
    line_chart(tables["timeseries"], polluant=metric)
    st.write("""
    Par exemple, on peut prendre le cas du polluant PM10. On observe, sur la période entre ocotbre 2021 et septembre 2025, une baisse progressive, avec une chute drastique entre 14 avril 2025
             et 14 septembre 2025 des concentrations moyennes avant
    une augmentation. Ce type de profil n’est pas propre à une seule zone : il traduit un comportement global qui peut ensuite varier localement.""")

    st.subheader("Comparaison entre zones géographiques")
    st.write("Ce graphique permet de repérer les zones ZAS présentant des niveaux moyens plus élevés que les autres.")
    bar_chart(tables["by_region"], polluant=metric)
    st.write("""
        Dans la continuité de notre exemple des PM10. Dans ce cas précis, les zones ultramarines (comme Mayotte, 
             Pointe-à-Pitre ou encore Fort-de-France)montrent des niveaux moyens nettement plus élevées que la plupart des zones métropolitaines. """)

    st.caption("Cette vue d’ensemble sert de point d’entrée avant d’examiner plus finement les écarts dans la section suivante.")
