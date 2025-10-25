import pandas as pd
import numpy as np

def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """
    Nettoie et prépare les données de qualité de l'air pour l'analyse.
    Étapes :
      1. Conversion des dates
      2. Création de variables temporelles
      3. Nettoyage des chaînes de caractères
      4. Gestion des valeurs manquantes (NaN)
      5. Création de variables catégorielles
      6. Normalisation des valeurs
      7. Suppression des doublons et colonnes inutiles
      8. Sauvegarde du dataset propre
    """
    df['Date de début'] = pd.to_datetime(df['Date de début'], errors='coerce')
    df['Date de fin']   = pd.to_datetime(df['Date de fin'], errors='coerce')
    df['annee'] = df['Date de début'].dt.year
    df['mois']  = df['Date de début'].dt.month
    df['jour']  = df['Date de début'].dt.date
    df['heure'] = df['Date de début'].dt.hour
    for i in ['Polluant', "type d'implantation", "type d'influence", 'Zas', 'Organisme']:
        if i in df.columns:
            df[i] = df[i].astype(str).str.strip().str.upper()
    df = df.drop(columns=['discriminant', 'taux de saisie',
                          'couverture temporelle', 'couverture de données'], errors='ignore')
    df = df.dropna(subset=['valeur'])
    for col in ["type d'implantation", "type d'influence", 'Zas', 'Organisme']:
        if col in df.columns:
            df[col] = df[col].fillna('INCONNU')
    conditions = [
        df['mois'].isin([12, 1, 2]),
        df['mois'].isin([3, 4, 5]),
        df['mois'].isin([6, 7, 8]),
        df['mois'].isin([9, 10, 11])
    ]
    categories = ['HIVER', 'PRINTEMPS', 'ÉTÉ', 'AUTOMNE']
    df['saison'] = np.select(conditions, categories, default='INCONNU')
    df['valeur_norm'] = (df['valeur'] - df['valeur'].mean()) / df['valeur'].std()
    df = df.drop_duplicates()
    map_region_dept = {
        'AIR BREIZH': 'Finistere',
        'AIR PAYS DE LA LOIRE': 'Loire-Atlantique',
        'AIRPARIF': 'Paris',
        'ATMO AUVERGNE-RHÔNE-ALPES': 'Rhone',
        'ATMO BOURGOGNE-FRANCHE-COMTE': "Cote-d'Or",
        'ATMO GRAND EST': 'Bas-Rhin',
        'ATMO GUYANE': 'Guyane',
        'ATMO HAUTS DE FRANCE': 'Nord',
        'ATMO NORMANDIE': 'Seine-Maritime',
        'ATMO NOUVELLE-AQUITAINE': 'Gironde',
        'ATMO OCCITANIE': 'Haute-Garonne',
        'ATMO REUNION': 'La Reunion',
        'ATMO SUD': 'Bouches-du-Rhone',
        "GWAD'AIR": 'Guadeloupe',
        'HAWA MAYOTTE': 'Mayotte',
        "LIG'AIR": 'Loiret',
        'MADININAIR': 'Martinique',
        'QUALITAIR CORSE': 'Corse-du-Sud'
    }
    zas_to_organisme = {
        'ZR NOUVELLE-AQUITAINE': 'ATMO NOUVELLE-AQUITAINE',
        'ZR GRAND-EST': 'ATMO GRAND EST',
        'ZR BOURGOGNE-FRANCHE-COMTE': 'ATMO BOURGOGNE-FRANCHE-COMTE',
        'ZR OCCITANIE': 'ATMO OCCITANIE',
        'ZR NORMANDIE': 'ATMO NORMANDIE',
        'ZR CENTRE-VAL-DE-LOIRE': "LIG'Air".upper(),
        'ZR BRETAGNE': 'AIR BREIZH',
        'ZAR BASTIA': 'QUALITAIR CORSE',
        'ZAR AJACCIO': 'QUALITAIR CORSE',
        'ZAR CHALON': 'ATMO BOURGOGNE-FRANCHE-COMTE',
        'ZR CENTRE-VAL DE LOIRE': "LIG'Air".upper(),
        'ZR CORSE': 'QUALITAIR CORSE',
        'ZAR FREJUS-DRAGUIGNAN': 'ATMO SUD',
    }
    if 'Zas' in df.columns:
        df['Organisme'] = df['Organisme'].fillna('')
        mask_fill = (df['Organisme'] == '') | (df['Organisme'] == 'INCONNU')
        df.loc[mask_fill, 'Organisme'] = df.loc[mask_fill, 'Zas'].map(zas_to_organisme).fillna(df.loc[mask_fill, 'Organisme'])
    df['Departement'] = df['Organisme'].map(map_region_dept)
    df.to_parquet('data/data_clean.parquet', index=False)
    return df

def make_tables(df: pd.DataFrame) -> dict:
    """
    Crée différentes tables agrégées pour l'affichage dans Streamlit :
    - Moyenne journalière (timeseries)
    - Moyenne par région (by_region)
    - Comptage par polluant (by_pollutant)
    """
    table_timeseries = df.groupby('jour', as_index=False)['valeur'].mean().rename(columns={'valeur': 'valeur_moyenne'})
    if 'Zas' in df.columns:
        table_region = df.groupby('Zas', as_index=False)['valeur'].mean().rename(columns={'valeur': 'valeur_moyenne'})
    else:
        table_region = pd.DataFrame()
    table_polluants = df['Polluant'].value_counts().reset_index().rename(columns={'index': 'Polluant', 'Polluant': 'Nombre_mesures'})
    return {"cleaned": df, "timeseries": table_timeseries, "by_region": table_region, "by_pollutant": table_polluants}
