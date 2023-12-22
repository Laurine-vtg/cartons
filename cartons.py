import streamlit as st 
import pandas as pd 

#titre de l'app
st.header('Les cartons en L2 pour la saison 23/24')

# Sélection du fichier CSV
uploaded_file = st.file_uploader("Choisissez un fichier CSV", type=["csv"])

# Vérification si un fichier a été téléchargé
if uploaded_file is not None:
    # Lecture du fichier CSV
    data = pd.read_csv(uploaded_file)

else:
    st.info("Veuillez télécharger un fichier CSV.")



#montrer le tableau
#st.dataframe(data)

# Remplacer "Quevilly-Rouen Métropole" par "Quevilly Rouen"
data['club'] = data['club'].replace('Quevilly-Rouen Métropole', 'Quevilly Rouen')

#selection des clubs à garder
club_filtré = ['St Etienne', "Bordeaux", "Caen", "Pau", "Auxerre", "Ajaccio", "Bastia", "Valenciennes", "Paris FC", "Amiens", "Dunkerque", "Grenoble", "Quevilly Rouen", "Concarneau", "Rodez", "Angers", "Annecy", "Guingamp", "Troyes", "Laval"]



#filtrer en fonction de la saison sélectionnée et des clubs de L2
data_filtré = data[(data['saison'] == 'Season 2023/2024') & (data['club'].isin(club_filtré))]

# Sélectionner un club à partir de la boîte de sélection
club_selectionné = st.selectbox("Sélectionnez un club", club_filtré)
# Filtrer le DataFrame pour le club sélectionné
club_data = data_filtré[data_filtré['club'] == club_selectionné]

# Afficher les lignes uniques pour le club sélectionné
colonne_a_afficher = ['club', 'type_cartons','type-faute','arbitre','player']
#st.dataframe(club_data.drop_duplicates()[colonne_a_afficher])


#compter le nombre de cartons jaunes et rouges par joueur
st.write("Nombre de cartons jaunes et rouges par joueur:")
cartons_par_joueur = club_data.groupby(['player', 'type_cartons']).size().unstack(fill_value=0)
#st.dataframe(cartons_par_joueur)

#boutons radio pour le classement
classement = st.radio("Trier", ['Cartons Jaunes', 'Cartons Rouges'])

#classement en fonction des cartons jaunes ou rouges
if classement == 'Cartons Jaunes':
    cartons_par_joueur = cartons_par_joueur.sort_values(by='Yellow', ascending=False)
else:
    cartons_par_joueur = cartons_par_joueur.sort_values(by='Red', ascending=False)

#afficher le tableau classé
#st.write(f"Classement par {classement}:")
st.dataframe(cartons_par_joueur)

# Calculer le nombre total de cartons par équipe
total_cartons_par_equipe = data_filtré.groupby('club')['type_cartons'].count().reset_index(name='total_cartons')

# Trier le DataFrame en fonction du nombre total de cartons
total_cartons_par_equipe = total_cartons_par_equipe.sort_values(by='total_cartons', ascending=True)

# Ajouter une colonne numérotée de 1 à 20
total_cartons_par_equipe['Classement'] = range(1, 21)

# Afficher le DataFrame pour déboguer
#st.write(total_cartons_par_equipe)

# Utiliser la colonne "Classement" comme index
total_cartons_par_equipe.set_index('Classement', inplace=True)

# Afficher le tableau classé des équipes en fonction du nombre total de cartons
st.write("Classement des équipes par nombre total de cartons:")
st.dataframe(total_cartons_par_equipe[[ 'club', 'total_cartons']])

#faire un classement de toutes les équipes de ligue 2 pour les cartons

#mettre chiffre dans mon classement de 1 à 20 et masquer la première colonne de valeur chiffré

