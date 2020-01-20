# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 13:56:06 2019

@author: Tanguy HODONOU

Test Data Engineer
"""
import os
os.chdir("E:\data_engineer_test")

#Importation des library et module qui vont être utilisé
from requests import get
from time import sleep
from random import randint
from bs4 import BeautifulSoup
import time

#Création d'une liste appelée pages contenant les chaînes de caractère correspondant aux 10 pages.
pages = [str(i) for i in range(1,11)]

# déclaration des listes dans lesquelles stocker les données
Nom_du_film1 = []
Realisateur1 = []
Acteurs_principaux1 = []
Type_de_film1 = []
Duree1 = []
Date_de_sortie1 = []

# Préparer la surveillance de la boucle
start_time = time.time()
requests = 0

# Pour chaque page dans l'intervalle 1-10
for page in pages:
# Faire une demande de get
    response =get('https://www.senscritique.com/liste/Bon_Films/66436#page-'+page)
    
# Mettre la boucle en pause pendant un intervalle de temps compris entre 8 et 15 secondes
    sleep(randint(8,15))

    #Nous allons contrôler le débit de la boucle en utilisant la fonction sleep () du module time de Python. 
    #sleep () suspendra l'exécution de la boucle pendant un nombre de secondes spécifié.
    #Pour imiter le comportement humain, nous allons faire varier le temps d’attente entre les demandes en utilisant 
    #la fonction randint () du module random de Python. 
    #randint () génère de manière aléatoire des entiers dans un intervalle spécifié. ici 8, 15
    #ceci permet de ne pas se faire banir lors du scraping.
    
# Utiliser Beautifulsoup pour avoir le contenu en html
    page_html = BeautifulSoup(response.text, 'html.parser')

# Sélectionnez tous les 30 conteneurs de film sur une seule page
    movie_containers = page_html.find_all('div', class_ = 'elli-content')

# Pour chaque film de ces 30 déterminer : le nom, le réalisateur, les acteurs...
    for container in movie_containers:

# Nom du film
        Nom_du_film = container.h3.a.text
        Nom_du_film1.append(Nom_du_film)
    
# Réalisateur
        Realisateur = container.find('a', attrs={'class':"elco-baseline-a"}).text
        Realisateur1.append(Realisateur)
# Acteurs_principaux
        Acteurs_principaux = container.find_all('p', class_="elco-baseline")[1].text.strip().split("avec")[1:]
        Acteurs_principaux1.append(Acteurs_principaux)
# Type_de_film
        Type_de_film = container.find('p', attrs={'class':"elco-baseline elco-options"}).text.strip().split(".")[-2].strip().split()
        Type_de_film1.append(Type_de_film)
#Durée
        Duree = container.find('p', attrs={'class':"elco-baseline elco-options"}).text.strip().split(".")[0]
        Duree1.append(Duree)
#Date de sortie
        Date_de_sortie = container.find_all('p', class_="elco-baseline")[0].time.text
        Date_de_sortie1.append(Date_de_sortie)

import pandas as pd
film_df = pd.DataFrame({'Nom_du_film': Nom_du_film1,
                        'Realisateur': Realisateur1,
                        'Acteurs_principaux': Acteurs_principaux1,
                        'Type_de_film': Type_de_film1,
                        'Duree': Duree1,
                        'Date_de_sortie': Date_de_sortie1                        
                        })
print(film_df.info())

#Exportation des données en CSV en préservant les characters en français
film_df.to_csv('films.csv', encoding='utf-8-sig', index=False)
