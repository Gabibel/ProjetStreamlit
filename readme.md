# Tableau de bord – Qualité de l’air (Streamlit)

Application Streamlit qui raconte l’évolution de la qualité de l’air en France à partir de données publiques.

### Contenu

```
app.py                # point d’entrée streamlit
requirements.txt
sections/             # pages : intro, overview, deep_dives, conclusion
utils/                # io, prep (clean), viz (graphiques)
data/                 # jeux de données
```

### Installation

```
python -m venv .venv
source .venv/bin/activate  # ou .venv\Scripts\activate sous Windows
pip install -r requirements.txt
```

### Lancer

```
streamlit run app.py
```

Navigation via la sidebar (Intro → Overview → Deep dives → Conclusion).

### Données

Données publiques issues des portails Atmo France / LCSQA / INERIS. Elles décrivent les niveaux de polluants (NO₂, O₃, PM10, PM2.5…) sur différentes zones de surveillance en France. Ici, l’usage est descriptif et narratif, sans modélisation prédictive.

### Projet

Ce tableau de bord Streamlit transforme des données publiques sur la qualité de l’air en une narration visuelle : on nettoie les données, on calcule des indicateurs, puis on guide l’utilisateur à travers plusieurs pages (intro → overview → deep dives → conclusion) pour raconter comment la qualité de l’air évolue en France et où se situent les écarts.

Lien Répo Github : https://github.com/Gabibel/ProjetStreamlit

### Par qui 

Réalisé par Gabriel Tannous en 2025
