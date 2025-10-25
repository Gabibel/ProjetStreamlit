import streamlit as st

def run(df):
    st.header("Conclusion")

    st.write("""
L’analyse conduite sur les données de qualité de l’air met en évidence plusieurs constats robustes.
D’abord, la pollution atmosphérique en France ne suit pas une trajectoire uniforme. Si certains
polluants, comme le PM10, montrent par exemple une tendance à la baisse sur plusieurs années,
cette dynamique n’est ni linéaire ni garantie dans le temps : des phases de remontée réapparaissent,
ce qui rappelle que l’amélioration observée reste réversible et dépendante des contextes locaux.

Ensuite, les écarts territoriaux observés sont nets et structurels. Des zones comme Mayotte,
Fort-de-France ou Pointe-à-Pitre présentent des niveaux nettement supérieurs à la moyenne nationale,
alors que d’autres territoires restent durablement plus faibles. Autrement dit, le risque sanitaire
lié à la pollution de l’air dépend autant **du lieu où l’on vit** que **du polluant auquel on est exposé**.

Les analyses par polluant confirment d’ailleurs que la situation n’est pas portée par une seule
substance : certaines zones sont dominées par un polluant particulier, tandis que d’autres cumulent
plusieurs dépassements simultanés. Cette distinction change la nature des réponses à apporter :
un excès chronique d’ozone ne se traite pas comme un épisode particulaire, et une zone qui cumule
plusieurs polluants impose des stratégies de régulation différentes de celles visant un seul agent.

Ce travail montre ainsi que la pollution de l’air en France n’est pas un phénomène abstrait ou uniforme,
mais un ensemble de situations locales hétérogènes qu’il faut analyser au bon niveau de granularité
pour en comprendre les enjeux. Il confirme aussi que des progrès existent, mais qu’ils restent fragiles
et partiels, une amélioration dans le temps ne suffit pas à compenser des inégalités géographiques
marquées ni à garantir une trajectoire durable.

Enfin, cette analyse ouvre plusieurs prolongements possibles. Elle pourrait être enrichie par
des croisements avec des variables socio-démographiques (densité, trafic routier, usage du bois,
métropole vs outre-mer), ou par une étude saisonnière pour distinguer pollution chronique et
pollution événementielle. À plus long terme, le suivi de ces données fournirait un indicateur
précieux pour évaluer l’impact réel des politiques publiques et vérifier si la courbe observée
aujourd’hui, parfois décroissante, parfois instable, se transforme en amélioration durable
et partagée sur l’ensemble du territoire.
""")

    st.subheader("Et maintenant, qu’est-ce qu’on en fait ?")

    st.write("""
Cette analyse n’a pas seulement permis d’identifier les zones et les polluants problématiques,
elle fournit aussi des leviers d’action concrets :

- Les politiques publiques peuvent être **ciblées géographiquement**, plutôt que définies
  de manière uniforme à l’échelle nationale.
- Une analyse plus fine par **saisonnalité ou conditions météorologiques** permettrait
  de distinguer ce qui relève de phénomènes chroniques et de pics ponctuels.
- Le croisement avec d’autres données (santé respiratoire, trafic routier, densité urbaine,
  usage du chauffage au bois, etc.) pourrait éclairer les causes et les conséquences réelles
  des niveaux observés.

Ce tableau de bord constitue ainsi une **première couche de lecture opérationnelle** :
il oriente le regard, identifie des priorités, et ouvre la voie à des analyses plus ciblées
et plus actionnables dans une perspective de décision publique ou d’évaluation d’impact.
""")

    st.success("Merci d’avoir exploré ce tableau de bord sur la qualité de l’air !)")
