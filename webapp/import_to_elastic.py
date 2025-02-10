import json
import os
from elasticsearch import Elasticsearch, helpers
import time

# Connexion à Elasticsearch avec un retry
ELASTIC_HOST = "elasticsearch"
ELASTIC_PORT = 9200
RETRY_DELAY = 5  # secondes
MAX_RETRIES = 12  # Attente max de 60 secondes

# Attendre que Elasticsearch soit prêt
for i in range(MAX_RETRIES):
    try:
        es = Elasticsearch([{"host": ELASTIC_HOST, "port": ELASTIC_PORT, "scheme": "http"}])
        if es.ping():
            print(" Elasticsearch est prêt !")
            break
    except Exception:
        print(f" Elasticsearch n'est pas encore prêt, tentative {i + 1}/{MAX_RETRIES}...")
        time.sleep(RETRY_DELAY)
else:
    print(" Impossible de se connecter à Elasticsearch après plusieurs tentatives.")
    exit(1)

# Liste des fichiers JSON à importer
collections = {
    "certifications": "/data/certifications.json",
    "labels": "/data/labels.json",
    "artistes": "/data/artistes.json",
    "albums": "/data/albums.json"
}

# Vérifier et créer les index s'ils n'existent pas
for index_name in collections.keys():
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name)
        print(f" Index '{index_name}' créé.")

# Importer les fichiers JSON
for index_name, file_path in collections.items():
    if os.path.exists(file_path):  # Vérifie si le fichier existe
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

                if isinstance(data, list) and len(data) > 0:
                    actions = []
                    for item in data:
                        doc_id = item.pop("_id")  # Récupérer l'ID et l'enlever du document
                        actions.append({"_index": index_name, "_id": doc_id, "_source": item})

                    helpers.bulk(es, actions)  # Bulk insert pour plus d'efficacité
                    print(f" {len(data)} documents insérés dans l'index '{index_name}'.")
                else:
                    print(f" Le fichier {file_path} est vide ou mal formaté.")

        except Exception as e:
            print(f" Erreur lors de l'importation de {file_path} dans '{index_name}': {e}")
    else:
        print(f" Fichier {file_path} non trouvé, import ignoré.")

print(" Importation terminée avec succès !")


#✔ Création automatique des index si jamais ils n'existent pas dans Elasticsearch.