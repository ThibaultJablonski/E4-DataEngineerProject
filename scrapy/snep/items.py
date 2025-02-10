import scrapy

class AlbumItem(scrapy.Item):
    _id = scrapy.Field()
    nom = scrapy.Field()
    artiste_id = scrapy.Field()
    label_id = scrapy.Field()
    date_sortie = scrapy.Field()

class ArtisteItem(scrapy.Item):
    _id = scrapy.Field()
    nom = scrapy.Field()

class LabelItem(scrapy.Item):
    _id = scrapy.Field()
    nom = scrapy.Field()

class CertificationItem(scrapy.Item):
    _id = scrapy.Field()
    album_id = scrapy.Field()
    type = scrapy.Field()
    date_obtention = scrapy.Field()
