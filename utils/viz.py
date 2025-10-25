import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def line_chart(df_timeseries: pd.DataFrame, polluant=None):
    if df_timeseries.empty:
        st.warning("Aucune donnée disponible pour la série temporelle.")
        return
    if polluant:
        st.caption(f"Polluant affiché : **{polluant}**")
    fig = px.line(df_timeseries,x='jour',y='valeur_moyenne',markers=True,template='plotly_white')
    fig.update_traces(line=dict(color="#0072B2", width=2.5))
    fig.update_layout(xaxis_title="Date",yaxis_title="Valeur moyenne",showlegend=False,margin=dict(l=40, r=40, t=60, b=40))
    st.plotly_chart(fig, use_container_width=True, key="line_chart_fig")

def bar_chart(df_region: pd.DataFrame, polluant=None):
    if df_region.empty:
        st.warning("Aucune donnée disponible pour la comparaison par région.")
        return
    if polluant:
        st.caption(f"Polluant affiché : **{polluant}**")
    df_sorted = df_region.sort_values('valeur_moyenne', ascending=False)
    fig = px.bar(df_sorted,x='Zas',y='valeur_moyenne',color='valeur_moyenne',color_continuous_scale='Tealgrn',template='plotly_white')
    fig.update_layout(xaxis_title="Zone géographique (ZAS)",yaxis_title="Valeur moyenne",margin=dict(l=40, r=40, t=60, b=40))
    st.plotly_chart(fig, use_container_width=True, key="bar_chart_fig")

def heatmap_polluant_zone(df: pd.DataFrame, key=None, polluant=None):
    st.markdown("#### Carte thermique : moyenne des polluants par zone (ZAS)")
    if df is None or len(df) == 0:
        st.warning("Pas de données dans le DataFrame fourni à la heatmap.")
        return
    value_col = None
    if 'valeur' in df.columns:
        value_col = 'valeur'
    elif 'valeur_moyenne' in df.columns:
        value_col = 'valeur_moyenne'
    else:
        st.warning("Les colonnes nécessaires ('valeur' ou 'valeur_moyenne') sont manquantes. Vérifiez le prétraitement.")
        return
    if not all(col in df.columns for col in ['Zas', 'Polluant']):
        st.warning("Les colonnes nécessaires ('Zas', 'Polluant') sont manquantes.")
        return
    df_used = df.copy()
    if polluant:
        df_used = df_used[df_used['Polluant'] == polluant]
        if df_used.empty:
            st.warning(f"Aucune donnée pour le polluant demandé : '{polluant}'.")
            return
        st.caption(f"Polluant affiché : **{polluant}** (après filtration : {len(df_used):,} lignes)")
    df_used[value_col] = pd.to_numeric(df_used[value_col], errors='coerce')
    df_pivot = (
        df_used.groupby(['Zas', 'Polluant'], as_index=False)[value_col]
        .mean()
        .pivot(index='Zas', columns='Polluant', values=value_col)
    )
    if df_pivot.empty:
        st.warning("Aucun point à afficher après agrégation / pivot. Vérifiez les valeurs de 'Zas' et 'Polluant'.")
        return
    fig = px.imshow(df_pivot, aspect='auto', color_continuous_scale='YlOrRd',
                    labels=dict(x="Polluant", y="Zone de surveillance (ZAS)", color="Valeur moyenne"),
                    title="Concentration moyenne des polluants selon les zones")
    fig.update_layout(xaxis_side='top', xaxis_title=None, yaxis_title=None, template='plotly_white',
                      margin=dict(l=50, r=50, t=80, b=50))
    chart_key = f"heatmap_zone_fig_{key}" if key is not None else "heatmap_zone_fig"
    st.plotly_chart(fig, use_container_width=True, key=chart_key)
    st.caption("Cette carte thermique met en évidence les différences de concentrations entre les zones de surveillance et les différents polluants. Plus la couleur est chaude, plus la concentration est élevée.")

def show_summary(df: pd.DataFrame):
    st.markdown("#### Résumé des données")
    col1, col2, col3 = st.columns(3)
    col1.metric("Nombre total de mesures", f"{len(df):,}")
    col2.metric("Nombre de polluants", df['Polluant'].nunique())
    col3.metric("Nombre de zones (ZAS)", df['Zas'].nunique())
    st.caption("Ces chiffres donnent un aperçu global de la taille du dataset et de la diversité des mesures.")

def map_zones_pollution(df):
    st.markdown("#### Analyse par Zones de Surveillance Atmosphérique (ZAS)")
    if 'Zas' not in df.columns or df['Zas'].isna().all():
        st.warning("Aucune donnée de ZAS disponible")
        return
    df_zas = (
        df.groupby('Zas', as_index=False)
        .agg({
            'valeur': ['mean', 'median', 'std', 'min', 'max', 'count'],
            'Polluant': 'nunique',
            'Organisme': 'first'
        })
    )
    df_zas.columns = ['Zas', 'valeur_moyenne', 'valeur_mediane', 'ecart_type',
                       'valeur_min', 'valeur_max', 'nb_mesures', 'nb_polluants', 'Organisme']
    df_zas = df_zas.sort_values('valeur_moyenne', ascending=False)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Zones totales", f"{len(df_zas)}")
    col2.metric("Mesures totales", f"{df_zas['nb_mesures'].sum():,}")
    col3.metric("Zone la plus polluée", df_zas.iloc[0]['Zas'] if len(df_zas) > 0 else "N/A")
    col4.metric("Moyenne générale", f"{df_zas['valeur_moyenne'].mean():.2f} µg/m³")
    tab1, tab2, tab3 = st.tabs(["Top zones", "Tableau détaillé", "Comparaisons"])
    with tab1:
        st.markdown("##### Top 20 des zones avec les plus fortes concentrations moyennes")
        top_20 = df_zas.head(20)
        fig = px.bar(
            top_20,
            y='Zas',
            x='valeur_moyenne',
            color='valeur_moyenne',
            color_continuous_scale='YlOrRd',
            orientation='h',
            title="Concentration moyenne par zone (µg/m³)",
            hover_data={
                'valeur_moyenne': ':.2f',
                'nb_mesures': ':,',
                'nb_polluants': True,
                'Organisme': True
            },
            labels={
                'valeur_moyenne': 'Concentration moyenne (µg/m³)',
                'Zas': 'Zone',
                'nb_mesures': 'Nombre de mesures',
                'nb_polluants': 'Polluants',
                'Organisme': 'Organisme'
            }
        )
        fig.update_layout(
            showlegend=False,
            height=600,
            yaxis={'categoryorder': 'total ascending'},
            margin=dict(l=200, r=40, t=60, b=40)
        )
        st.plotly_chart(fig, use_container_width=True, key="top_zones_bar_fig")
        fig2 = px.scatter(
            df_zas,
            x='nb_mesures',
            y='valeur_moyenne',
            size='nb_polluants',
            color='valeur_moyenne',
            color_continuous_scale='YlOrRd',
            hover_name='Zas',
            hover_data={'nb_mesures': ':,', 'valeur_moyenne': ':.2f'},
            labels={
                'nb_mesures': 'Nombre de mesures',
                'valeur_moyenne': 'Concentration moyenne (µg/m³)',
                'nb_polluants': 'Nombre de polluants'
            },
        )
        fig2.update_layout(height=500)
        st.plotly_chart(fig2, use_container_width=True, key="zones_scatter_fig")
    with tab2:
        st.markdown("##### Tableau détaillé de toutes les zones")
        df_display = df_zas.copy()
        df_display['valeur_moyenne'] = df_display['valeur_moyenne'].round(2)
        df_display['valeur_mediane'] = df_display['valeur_mediane'].round(2)
        df_display['ecart_type'] = df_display['ecart_type'].round(2)
        st.dataframe(
            df_display.style.background_gradient(
                subset=['valeur_moyenne'],
                cmap='YlOrRd'
            ).format({
                'valeur_moyenne': '{:.2f}',
                'valeur_mediane': '{:.2f}',
                'ecart_type': '{:.2f}',
                'valeur_min': '{:.2f}',
                'valeur_max': '{:.2f}',
                'nb_mesures': '{:,.0f}'
            }),
            use_container_width=True,
            height=500
        )
        csv = df_display.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Télécharger les données (CSV)",
            data=csv,
            file_name="zones_pollution.csv",
            mime="text/csv"
        )
    with tab3:
        st.markdown("##### Comparaisons par organisme")
        fig3 = px.box(
            df_zas,
            x='Organisme',
            y='valeur_moyenne',
            color='Organisme',
            title="Distribution des concentrations moyennes par organisme",
            labels={
                'valeur_moyenne': 'Concentration moyenne (µg/m³)',
                'Organisme': 'Organisme de surveillance'
            }
        )
        fig3.update_layout(
            showlegend=False,
            height=500,
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig3, use_container_width=True, key="organisme_box_fig")
        st.markdown("##### Statistiques par organisme")
        df_org = (
            df_zas.groupby('Organisme', as_index=False)
            .agg({
                'Zas': 'count',
                'valeur_moyenne': ['mean', 'max'],
                'nb_mesures': 'sum'
            })
        )
        df_org.columns = ['Organisme', 'Nb_zones', 'Moyenne', 'Maximum', 'Total_mesures']
        df_org = df_org.sort_values('Moyenne', ascending=False)
        st.dataframe(
            df_org.style.background_gradient(subset=['Moyenne'], cmap='YlOrRd').format({
                'Moyenne': '{:.2f}',
                'Maximum': '{:.2f}',
                'Total_mesures': '{:,.0f}'
            }),
            use_container_width=True
        )
    st.caption("Chaque point correspond à une zone de surveillance atmosphérique (ZAS) avec sa concentration moyenne. Passer la souris sur un point affiche plus de détails.")

def map_interactive_zas(df):
    import re
    st.markdown("#### Carte interactive des Zones de Surveillance Atmosphérique")
    df_zas = (
        df.groupby(['Zas', 'Organisme'], as_index=False)
        .agg({
            'valeur': ['mean', 'count'],
            'Polluant': 'nunique'
        })
    )
    df_zas.columns = ['Zas', 'Organisme', 'valeur_moyenne', 'nb_mesures', 'nb_polluants']
    coords_dict = {
        'PARIS': (48.8566, 2.3522),
        'LYON': (45.7640, 4.8357),
        'MARSEILLE': (43.2965, 5.3698),
        'TOULOUSE': (43.6047, 1.4442),
        'NICE': (43.7102, 7.2620),
        'NANTES': (47.2184, -1.5536),
        'STRASBOURG': (48.5734, 7.7521),
        'MONTPELLIER': (43.6108, 3.8767),
        'BORDEAUX': (44.8378, -0.5792),
        'LILLE': (50.6292, 3.0573),
        'RENNES': (48.1173, -1.6778),
        'REIMS': (49.2583, 4.0317),
        'SAINT-ETIENNE': (45.4397, 4.3872),
        'TOULON': (43.1242, 5.9280),
        'GRENOBLE': (45.1885, 5.7245),
        'DIJON': (47.3220, 5.0415),
        'ANGERS': (47.4784, -0.5632),
        'NIMES': (43.8367, 4.3601),
        'CLERMONT': (45.7772, 3.0870),
        'HAVRE': (49.4944, 0.1079),
        'AIX': (43.5297, 5.4474),
        'BREST': (48.3904, -4.4861),
        'TOURS': (47.3941, 0.6848),
        'AMIENS': (49.8941, 2.2958),
        'LIMOGES': (45.8336, 1.2611),
        'ANNECY': (45.8992, 6.1294),
        'PERPIGNAN': (42.6886, 2.8948),
        'BESANCON': (47.2380, 6.0243),
        'ORLEANS': (47.9029, 1.9093),
        'ROUEN': (49.4432, 1.0993),
        'MULHOUSE': (47.7508, 7.3359),
        'CAEN': (49.1829, -0.3707),
        'NANCY': (48.6921, 6.1844),
        'METZ': (49.1193, 6.1757),
        'AVIGNON': (43.9493, 4.8055),
        'VALENCE': (44.9334, 4.8924),
        'CHAMBERY': (45.5646, 5.9178),
        'TROYES': (48.2973, 4.0744),
        'LORIENT': (47.7482, -3.3703),
        'POITIERS': (46.5802, 0.3404),
        'ROCHELLE': (46.1591, -1.1520),
        'BAYONNE': (43.4933, -1.4748),
        'PAU': (43.2951, -0.3708),
        'CALAIS': (50.9513, 1.8587),
        'VALENCIENNES': (50.3587, 3.5233),
        'DUNKERQUE': (51.0343, 2.3768),
        'ARRAS': (50.2919, 2.7772),
        'DOUAI': (50.3714, 3.0799),
        'LENS': (50.4281, 2.8317),
        'COLMAR': (48.0778, 7.3584),
        'CHARLEVILLE': (49.7628, 4.7194),
        'CHERBOURG': (49.6337, -1.6220),
        'EVREUX': (49.0246, 1.1510),
        'NIORT': (46.3236, -0.4646),
        'ANGOULEME': (45.6484, 0.1561),
        'BEAUVAIS': (49.4295, 2.0807),
        'NEVERS': (46.9896, 3.1615),
        'BELFORT': (47.6380, 6.8629),
        'BOURG': (46.2054, 5.2259),
        'MACON': (46.3067, 4.8306),
        'VIENNE': (45.5256, 4.8776),
        'GAP': (44.5597, 6.0794),
        'DIGNE': (44.0927, 6.2361),
        'MARTIGUES': (43.4054, 5.0539),
        'CANNES': (43.5528, 7.0174),
        'ANTIBES': (43.5808, 7.1239),
        'VILLEURBANNE': (45.7640, 4.8357),
        'COTE D OPALE': (50.7264, 1.6147),
        'COTE-D-OPALE': (50.7264, 1.6147),
        'BLDV': (50.6292, 3.0573),
        'CREIL': (49.2606, 2.4750),
        'SAINT-DENIS': (-20.8823, 55.4504),
        'REUNION': (-21.1151, 55.5364),
        'VOLCAN': (-21.2444, 55.7142),
        'FORT-DE-FRANCE': (14.6160, -61.0595),
        'MARTINIQUE': (14.6415, -61.0242),
        'POINTE-A-PITRE': (16.2415, -61.5331),
        'GUADELOUPE': (16.2650, -61.5510),
        'ILE-DE-CAYENNE': (4.9227, -52.3269),
        'CAYENNE': (4.9227, -52.3269),
        'GUYANE': (4.0, -53.0),
        'MAYOTTE': (-12.8275, 45.1662),
        'PAYS-DE-LA-LOIRE': (47.7632, -0.3299),
        'PAYS DE LA LOIRE': (47.7632, -0.3299),
        'BLOIS': (47.5868, 1.3350),
        'LE-MANS': (48.0061, 0.1996),
        'LE MANS': (48.0061, 0.1996),
        'MANS': (48.0061, 0.1996),
        'LAVAL': (48.0698, -0.7700),
        'CHARTRES': (48.4469, 1.4850),
        'DREUX': (48.7372, 1.3658),
        'PAYS-DE-SAVOIE': (45.6980, 6.1263),
        'PAYS DE SAVOIE': (45.6980, 6.1263),
        'VALLEE-DU-RHONE': (45.0583, 5.0528),
        'VALLEE DU RHONE': (45.0583, 5.0528),
        'RHONE': (45.7640, 4.8357),
        'VALLEE-DE-L-ARVE': (46.0654, 6.7093),
        'VALLEE DE L ARVE': (46.0654, 6.7093),
        'ARVE': (46.0654, 6.7093),
        'VALLEE-DE-LA-TARENTAISE': (45.5189, 6.6510),
        'TARENTAISE': (45.5189, 6.6510),
        'MOULINS': (46.5667, 3.3333),
        'PROVENCE-ALPES-COTE-D-AZUR': (43.9352, 6.0679),
        'PROVENCE-ALPES-COTE D AZUR': (43.9352, 6.0679),
        'PROVENCE ALPES COTE D AZUR': (43.9352, 6.0679),
        'PACA': (43.9352, 6.0679),

        'DIEPPE': (49.9246, 1.0787),
        'CHARTRES-DREUX': (48.5920, 1.4252),
        'URBAIN': (48.8566, 2.3522),
        'RURAL': (46.5, 2.5),
        'INDUSTRIEL': (50.6292, 3.0573),
        'PERIURBAIN': (48.8566, 2.3522),
        "ZR NOUVELLE-AQUITAINE": (45.75, -0.75),
        "ZR GRAND-EST": (48.70, 6.20),
        "ZR BOURGOGNE-FRANCHE-COMTE": (47.28, 5.09),
        "ZR OCCITANIE": (43.60, 2.30),
        "ZR NORMANDIE": (49.10, -0.40),
        "ZR CENTRE-VAL-DE-LOIRE": (47.75, 1.60),
        "ZR BRETAGNE": (48.10, -2.90),
        "ZR CORSE": (42.15, 9.00),
        "ZAR BASTIA": (42.70, 9.45),
        "ZAR AJACCIO": (41.92, 8.74),
        "ZAR CHALON": (46.78, 4.85),
        "ZAR FREJUS-DRAGUIGNAN": (43.43, 6.74)
    }
    def get_coords_from_zas(zas_name):
        if pd.isna(zas_name):
            return None
        zas_upper = str(zas_name).upper()
        zas_clean = re.sub(r'[^\w\s]', ' ', zas_upper)
        zas_clean = ' '.join(zas_clean.split())
        for ville, coords in coords_dict.items():
            ville_clean = re.sub(r'[^\w\s]', ' ', ville.upper())
            ville_clean = ' '.join(ville_clean.split())
            if ville_clean == zas_clean:
                return coords
        for ville, coords in coords_dict.items():
            ville_clean = re.sub(r'[^\w\s]', ' ', ville.upper())
            ville_clean = ' '.join(ville_clean.split())
            pattern = r'\b' + re.escape(ville_clean) + r'\b'
            if re.search(pattern, zas_clean):
                return coords
        zas_words = set(zas_clean.split())
        for ville, coords in coords_dict.items():
            ville_words = set(re.sub(r'[^\w\s]', ' ', ville.upper()).split())
            common_words = zas_words & ville_words
            if common_words:
                for word in common_words:
                    if len(word) > 5:
                        return coords
        return None
    df_zas['coords'] = df_zas['Zas'].apply(get_coords_from_zas)
    df_zas_mapped = df_zas[df_zas['coords'].notna()].copy()
    df_zas_mapped['latitude'] = df_zas_mapped['coords'].apply(lambda x: x[0])
    df_zas_mapped['longitude'] = df_zas_mapped['coords'].apply(lambda x: x[1])
    zones_non_mappees = df_zas[df_zas['coords'].isna()]
    taux_mapping = (len(df_zas_mapped)/len(df_zas)*100) if len(df_zas) > 0 else 0
    st.info(f"{len(df_zas_mapped)} zones localisées sur {len(df_zas)} zones totales ({taux_mapping:.1f}% )")
    if len(zones_non_mappees) > 0:
        with st.expander(f"{len(zones_non_mappees)} zones non localisées"):
            st.dataframe(
                zones_non_mappees[['Zas', 'Organisme', 'valeur_moyenne', 'nb_mesures']].sort_values('nb_mesures', ascending=False),
                use_container_width=True
            )
    if len(df_zas_mapped) == 0:
        st.warning("Impossible de localiser les zones automatiquement")
        return
    fig = px.scatter_mapbox(
        df_zas_mapped,
        lat='latitude',
        lon='longitude',
        color='valeur_moyenne',
        size='nb_mesures',
        hover_name='Zas',
        hover_data={
            'valeur_moyenne': ':.2f',
            'nb_mesures': ':,',
            'nb_polluants': True,
            'Organisme': True,
            'latitude': False,
            'longitude': False
        },
        color_continuous_scale='YlOrRd',
        size_max=30,
        zoom=5.2,
        center={'lat': 46.5, 'lon': 2.5},
        labels={
            'valeur_moyenne': 'Concentration (µg/m³)',
            'nb_mesures': 'Mesures',
            'nb_polluants': 'Polluants',
            'Organisme': 'Organisme'
        },
        title="Zones de surveillance atmosphérique en France"
    )
    fig.update_layout(
        mapbox_style="carto-positron",
        height=700,
        margin=dict(l=0, r=0, t=40, b=0)
    )
    st.plotly_chart(fig, use_container_width=True, key="map_zas_fig")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Zones localisées", f"{len(df_zas_mapped)}/{len(df_zas)}")
    col2.metric("Mesures totales", f"{df_zas_mapped['nb_mesures'].sum():,}")
    col3.metric("Pollution moyenne", f"{df_zas_mapped['valeur_moyenne'].mean():.2f} µg/m³")
    col4.metric("Maximum", f"{df_zas_mapped['valeur_moyenne'].max():.2f} µg/m³")
    st.caption("Chaque marqueur représente une zone de surveillance atmosphérique (ZAS). La taille du point est proportionnelle au nombre de mesures enregistrées, tandis que la couleur indique le niveau moyen de pollution observé sur la période : plus la couleur tend vers le rouge, plus la concentration mesurée est élevée. Survolez les marqueurs pour voir les détails.")

def dominant_pollutant_table(df: pd.DataFrame, max_cols_display=20):
    if df is None or df.empty:
        st.warning("Pas de données pour calculer le polluant dominant.")
        return
    if 'valeur' in df.columns:
        value_col = 'valeur'
    elif 'valeur_moyenne' in df.columns:
        value_col = 'valeur_moyenne'
    else:
        st.warning("Colonne de valeurs introuvable.")
        return
    gp = df.groupby(['Zas', 'Polluant'], as_index=False)[value_col].mean()
    pivot = gp.pivot(index='Zas', columns='Polluant', values=value_col)
    if pivot.empty:
        st.warning("Aucun résultat après pivot — vérifie Zas / Polluant.")
        return
    dominant = pivot.idxmax(axis=1)
    dominant_val = pivot.max(axis=1)
    result = pivot.reset_index()
    result['dominant_pollutant'] = dominant.values
    result['dominant_valeur'] = dominant_val.values.round(4)
    st.markdown("#### Tableau complet : moyennes par polluant et polluant dominant par ZAS")
    if result.shape[1] > max_cols_display:
        st.caption(f"Le tableau contient {result.shape[1]} colonnes ; certaines colonnes peuvent être masquées pour lisibilité.")
    st.dataframe(result.sort_values('dominant_valeur', ascending=False), use_container_width=True, height=500)
