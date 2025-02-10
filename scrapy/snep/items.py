import scrapy

# Modèle de données pour un album
class AlbumItem(scrapy.Item):
    _id = scrapy.Field() # Identifiant unique
    nom = scrapy.Field() # Nom de l'album
    artiste_id = scrapy.Field() # Référence à l'artiste
    label_id = scrapy.Field() # Référence au label
    date_sortie = scrapy.Field() # Date au format ISO

# Modèle de données pour un artiste
class ArtisteItem(scrapy.Item):
    _id = scrapy.Field()
    nom = scrapy.Field()

# Modèle de données pour un label
class LabelItem(scrapy.Item):
    _id = scrapy.Field()
    nom = scrapy.Field()

# Modèle de données pour une certification
class CertificationItem(scrapy.Item):
    _id = scrapy.Field()
    album_id = scrapy.Field()
    type = scrapy.Field()
    date_obtention = scrapy.Field()
