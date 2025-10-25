import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    fichiers = ['data/FR_E2_2021-10-14.csv','data/FR_E2_2024-10-14.csv','data/FR_E2_2025-04-14.csv','data/FR_E2_2025-09-14.csv','data/FR_E2_2025-10-14.csv']
    df_list = []
    for f in fichiers:
        temp = pd.read_csv(f, sep=';', encoding='utf-8')
        temp['source_fichier'] = f
        df_list.append(temp)
    df = pd.concat(df_list, ignore_index=True)
    return df

def license_text():
    """Ou les données ont-elles étaient prises ?"""
    import streamlit as st
    st.markdown("""
    ---
    ### Informations sur les données

    **Source :**  
    Données publiques issues du LCSQA, INERIS, Atmo France : https://object.infra.data.gouv.fr/browser/ineris-prod/lcsqa/concentrations-de-polluants-atmospheriques-reglementes/temps-reel/

    **Description :**  
    Mesures en temps réel des concentrations de polluants atmosphériques réglementés (NO₂, O₃, PM10, PM2.5, SO₂, etc.) sur différents sites français.

    **Licence :**  
    Données ouvertes sous Licence Ouverte / Etalab 2.0 : https://www.etalab.gouv.fr/licence-ouverte-open-licence/

    **Producteurs :**  
    - LCSQA (Laboratoire Central de Surveillance de la Qualité de l’Air)  
    - INERIS (Institut National de l’Environnement Industriel et des Risques)  
    - Réseau Atmo France
    """)
