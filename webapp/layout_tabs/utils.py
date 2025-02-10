from elasticsearch import Elasticsearch

# Connexion à Elasticsearch
ELASTIC_HOST = "http://elasticsearch:9200"
es = Elasticsearch([ELASTIC_HOST])

def search_elasticsearch(query, index):
    body = {
        "_source": ["nom", "album_id", "artiste_id", "label_id", "type", "date_sortie"],  # ✅ Ajout de "date_sortie"
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["nom", "album_id", "artiste_id", "label_id", "type"]
            }
        }
    }

    results = []
    try:
        res = es.search(index=index, body=body)

        for hit in res["hits"]["hits"]:
            hit["_source"]["_id"] = hit["_id"]  # 🔥 Ajout manuel de _id
            results.append(hit["_source"])

    except Exception as e:
        print(f"❌ Erreur Elasticsearch : {e}")

    return results  # 🔥 Toujours retourner une liste




def get_certification_data(label):
    body = {
        "query": {
            "match": {"label_id": label}
        }
    }

    res = es.search(index="certifications", body=body)
    return [hit["_source"] for hit in res["hits"]["hits"]]

def get_artist_details(artist_name):
    """ Récupère les albums et certifications associés à un artiste """
    artist_results = search_elasticsearch(artist_name, "artistes")

    if not artist_results or not isinstance(artist_results, list) or len(artist_results) == 0:
        return "Aucun artiste trouvé."

    first_artist = artist_results[0]
    artist_id = first_artist.get("_id")  # 🔥 On utilise .get() pour éviter KeyError


    artist_nom = first_artist.get("nom", "Nom Inconnu")

    # 🔎 Étape 2 : Trouver tous les albums de cet artiste
    albums = get_albums_by_artist(artist_id)

    # 🔎 Étape 3 : Récupérer les certifications de ces albums
    final_data = []
    for album in albums:
        album_id = album.get("_id", "ID Album Inconnu")
        label_id = album.get("label_id", "Label Inconnu")
        date_sortie = album.get("date_sortie", "Date Inconnue")

        # Trouver le nom du label
        label_results = search_elasticsearch(label_id, "labels")

        if isinstance(label_results, list) and len(label_results) > 0:
            first_label = label_results[0]["nom"]

            label_nom = first_label.get("nom", f"ID {label_id}")
        else:
            label_nom = f"{label_id}"


        # Trouver les certifications
        certifications = get_certifications_by_album(album_id)

        for cert in certifications:
            final_data.append({
                "artiste": artist_nom,
                "album": album.get("nom", "Nom Album Inconnu"),
                "label": label_nom,
                "date_sortie": date_sortie,
                "certification": cert.get("type", "Non Certifié"),
                "date_certification": cert.get("date_obtention", "Date Inconnue")
            })

    return final_data if final_data else "Aucune certification trouvée."



def get_album_details(album_name):
    """ Récupère l'artiste, le label et la certification d'un album donné """
    
    # 🔎 Étape 1 : Trouver l'album
    album_results = search_elasticsearch(album_name, "albums")

    if not album_results:
        return "Aucun album trouvé."

    first_album = album_results[0]  # On prend le premier album trouvé

    # 🔥 Définition sécurisée des valeurs
    album_nom = first_album.get("nom", "Nom Album Inconnu")
    album_id = first_album.get("_id", "ID Album Inconnu")
    artiste_id = first_album.get("artiste_id", "ID Artiste Inconnu")
    label_id = first_album.get("label_id", "Label Inconnu")
    date_sortie = first_album.get("date_sortie", "Date Inconnue")

    # 🔎 Trouver l'artiste
    artist_results = search_elasticsearch(artiste_id, "artistes")
    artiste_nom = next(
        (artist["nom"] for artist in artist_results),
        f"ID {artiste_id}"
    )

    # 🔎 Trouver le label
    label_results = search_elasticsearch(label_id, "labels")
    label_nom = next(
        (label["nom"] for label in label_results),
        f"{label_id}"
    )

    # 🔎 Trouver les certifications
    certifications = get_certifications_by_album(album_id)

    final_data = []
    for cert in certifications:
        final_data.append({
            "album": album_nom,
            "artiste": artiste_nom,
            "label": label_nom,
            "date_sortie": date_sortie,
            "certification": cert.get("type", "Non Certifié"),
            "date_certification": cert.get("date_obtention", "Date Inconnue")
        })

    return final_data if final_data else "Aucune certification trouvée."


def get_certifications_by_label(label_name):
    """ Récupère tous les albums d'un label et leurs certifications """

    # 🔎 Étape 1 : Trouver le label
    
    label_results = search_elasticsearch(label_name, "labels")

    if not label_results:
        return "Aucun label trouvé."

    first_label = label_results[0]
    label_id = first_label.get("_id", "ID Label Inconnu")
    label_nom = first_label.get("nom", "Nom Label Inconnu")

    # 🔎 Étape 2 : Trouver tous les albums de ce label

    albums = search_elasticsearch(label_id, "albums")

    if not albums:
        return "Aucun album trouvé pour ce label."

    # 🔎 Étape 3 : Trouver les certifications des albums
    final_data = []
    for album in albums:
        album_id = album.get("_id", "ID Album Inconnu")
        date_sortie = album.get("date_sortie", "Date Inconnue")
        album_nom = album.get("nom", "Nom Album Inconnu")
        artiste_id = album.get("artiste_id", "Artiste Inconnu")
        
        artist_results = search_elasticsearch(artiste_id, "artistes")

        artiste_nom = next(
            (artist["nom"] for artist in artist_results),
            f"ID {artiste_id}"
        )

        certifications = get_certifications_by_album(album_id)

        for cert in certifications:
            final_data.append({
                "label": label_nom,
                "album": album_nom,
                "artiste": artiste_nom,
                "date_sortie": date_sortie,
                "certification": cert.get("type", "Non Certifié"),
                "date_certification": cert.get("date_obtention", "Date Inconnue")
            })


    return final_data if final_data else "Aucune certification trouvée."


def get_albums_by_artist(artist_id):
    """ Récupère tous les albums d'un artiste donné """
    body = {
        "query": {
            "match": {
                "artiste_id": artist_id
            }
        }
    }

    try:
        res = es.search(index="albums", body=body)

        albums = []
        for hit in res["hits"]["hits"]:
            hit["_source"]["_id"] = hit["_id"]  # 🔥 Ajout manuel de _id
            albums.append(hit["_source"])

        return albums
    except Exception as e:
        print(f"❌ Erreur Elasticsearch (get_albums_by_artist) : {e}")
        return []


def get_certifications_by_album(album_id):
    """ Récupère toutes les certifications d'un album donné """
    body = {
        "query": {
            "match": {
                "album_id": album_id
            }
        }
    }

    try:
        res = es.search(index="certifications", body=body)
        return [hit["_source"] for hit in res["hits"]["hits"]]
    except Exception as e:
        print(f"Erreur Elasticsearch (get_certifications_by_album) : {e}")
        return []
