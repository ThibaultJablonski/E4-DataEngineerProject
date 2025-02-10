# Projet SNEP Dashboard

## Description du projet

Le projet **SNEP Dashboard** est une application web permettant d'explorer les certifications d'albums musicaux en France. Il repose sur un scraping des données du **SNEP** (Syndicat National de l'Édition Phonographique) et offre une interface interactive via **Dash** pour rechercher des albums, artistes et labels.

L'application utilise **Elasticsearch** comme base de données pour stocker et rechercher efficacement les données collectées.

## Choix effectués

Durant notre projet, nous avons eu quelques soucis concernant le scraping. En effet, le site Web de la SNEP est extrêmement mal fait. Car lorsque l'on navigue avec un filtre, le changement de page enlève le filtre. 
Nous avons donc dû malheureusement prendre sans filtres et changer dans notre spider.
 Nous avons enlevé tout ce qui était des singles et vidéos et ne pas stocker dans la base de données si la date de sortie était avant 2016.
Ce code n'est actuellement pas présent dans la spider actuelle car le scraping mettant plus de 3 heures à se faire, nous avons stockés les données dans des fichiers JSON pour pouvoir les réutiliser par la suite via ElasticSearch. Alors pour la démonstration de scraping, nous avons fait un scraping de 10 données. Pour le constater, aller sur ce lien : http://localhost:8081/
Le mot de passe et le nom d'utilisateur sont : admin


Pour la suite du projet, nous avons donc décidé d'utiliser ElasticSearch et Dash pour l'application.
Dans le code actuel de la spider, il y a une fonction is_valid_year(). Cette fonction permet de ne pas aller trop loin dans la date.
Cette fonction a été utilisé pour le scraping des données stockées dans les fichiers JSON et elle a été gardée ici, bien qu'elle ne sert à rien car le scraping se fait en commençant par le plus jeune.


---

## Architecture du projet

### 1. Scraping avec Scrapy
L'application repose sur **Scrapy** pour extraire les informations depuis le site web du SNEP. Les données récupérées ont été stockées sous forme de fichiers **JSON** via une base de données Mongo avant d'être insérées dans Elasticsearch.

### 2. Base de données Elasticsearch
Les données sont indexées dans Elasticsearch pour permettre une recherche rapide et efficace sur les artistes, albums et labels.

### 3. Interface utilisateur avec Dash
L'application web est développée en **Dash** avec une interface permettant de :
- Rechercher un **artiste** et afficher ses albums et certifications.
- Rechercher un **album** et afficher ses détails.
- Rechercher un **label** et voir les albums associés.

---

## Technologies utilisées

| Technologie | Description |
|------------|------------|
| Scrapy | Scraping web pour collecter les données |
| Elasticsearch | Base de données pour indexer les données et faciliter la recherche |
| Flask | Serveur backend pour l'application Dash |
| Dash | Framework Python pour la création de tableaux de bord interactifs |
| Docker | Conteneurisation du projet |
| Docker Compose | Orchestration des différents services |

---

## Installation et exécution

### 1. Prérequis
Assurez-vous d'avoir installé **Docker** et **Docker Compose** sur votre machine.

### 2. Cloner le projet
```sh
$ git clone https://github.com/ThibaultJablonski/E4-DataEngineerProject
```

Se rendre sur le dossier que tu as cloné

```sh
$ cd E4-DataEngineerProjet
```

### 3. Lancer les services Docker

Assurez-vous d'avoir lancer Docker Desktop 

```sh
$ docker-compose up --build
```
Cela démarre Elasticsearch, Kibana, Scrapy et l'application web.

### 4. Accéder à l'application
- **Dashboard** : [http://localhost:8000](http://localhost:8000)
- **Elasticsearch** : [http://localhost:9200](http://localhost:9200)
- **Kibana** : [http://localhost:5601](http://localhost:5601)
- **MongoDB** : [http://localhost:8081](http://localhost:8081)

---

## Fonctionnalités détaillées

### 🎵 Recherche d'un artiste
- Permet d'afficher les albums d'un artiste.
- Montre les certifications obtenues par chaque album.

### 💿 Recherche d'un album
- Donne des détails sur un album spécifique.
- Affiche l'artiste, le label et les certifications obtenues.

### 🏷️ Recherche d'un label
- Permet de voir tous les albums produits par un label spécifique.
- Affiche les certifications des albums du label.

---

## Structure du projet
```
C:.
│   docker-compose.yml
│   README.md
│   requirements.txt
│
├───data
│       albums.json
│       artistes.json
│       certifications.json
│       labels.json
│
├───scrapy
│   │   Dockerfile
│   │   scrapy.cfg
│   └───snep
│       │   items.py
│       │   middlewares.py
│       │   pipelines.py
│       │   settings.py
│       │   __init__.py
│       └───spiders
│           │   snep_spider.py
│
└───webapp
    │   Dockerfile
    │   import_to_elastic.py
    │   main.py
    │
    ├───assets
    │       style.css
    │       images...
    │
    └───layout_tabs
            about.py
            layout.py
            search_album.py
            search_artist.py
            search_label.py
            utils.py
```

---

## Fichiers importants

### Scrapy
- **items.py** : Définit les modèles de données (albums, artistes, labels, certifications).
- **pipelines.py** : Envoie les données scrappées vers Elasticsearch.
- **settings.py** : Configuration de Scrapy.

### Elasticsearch
- **import_to_elastic.py** : Insère les données JSON dans Elasticsearch.

### Application Web
- **main.py** : Initialise le serveur Dash.
- **layout.py** : Définition du layout général de l'application.
- **search_album.py / search_artist.py / search_label.py** : Gère la recherche et l'affichage des résultats.

### Docker
- **docker-compose.yml** : Configure les services nécessaires (Elasticsearch, Kibana, Scrapy, WebApp).

---

## Auteurs
**Thibault Jablonski & Thibault Le Guidevais**
