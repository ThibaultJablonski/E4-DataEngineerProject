import scrapy
import re
from datetime import datetime
from snep.items import AlbumItem, ArtisteItem, LabelItem, CertificationItem

class CertificationsSpider(scrapy.Spider):
    name = "certifications"
    start_urls = ["https://snepmusique.com/les-certifications/?categories=Albums"]

    def parse(self, response):
        certifications = response.xpath("//div[contains(@class, 'certification')]")
        count = 0  # Compteur pour limiter à 10

        for cert in certifications:
            if count >= 10:  # Arrêter après 10 éléments
                break
            
            categorie = cert.xpath(".//div[@class='categorie']/text()").get()
            if not categorie or "albums" not in categorie.lower():
                self.logger.info(f"Ignoré (non album) : {categorie if categorie else 'Catégorie non trouvée'}")
                continue  # Ignorer les certifications qui ne sont pas des albums


            date_sortie = self.extract_date(cert, "Date de sortie")
            date_constat = self.extract_date(cert, "Date de constat")

            if not self.is_valid_year(date_sortie) or not self.is_valid_year(date_constat):
                continue

            album_name = cert.xpath(".//div[contains(@class, 'titre')]/text()").get("").strip()
            artiste_name = cert.xpath(".//div[contains(@class, 'artiste')]/text()").get("").strip()
            label_name = cert.xpath(".//div[contains(@class, 'editeur')]/text()").get("").strip()
            certification_type = cert.xpath(".//div[contains(@class, 'certif')]/text()").get("").strip()

            album_id = self.generate_id(album_name)
            artiste_id = self.generate_id(artiste_name)
            label_id = self.generate_id(label_name)
            certification_id = self.generate_id(f"{album_id}_{certification_type}")

            yield AlbumItem(_id=album_id, nom=album_name, artiste_id=artiste_id, label_id=label_id, date_sortie=date_sortie)
            yield ArtisteItem(_id=artiste_id, nom=artiste_name)
            yield LabelItem(_id=label_id, nom=label_name)
            yield CertificationItem(_id=certification_id, album_id=album_id, type=certification_type, date_obtention=date_constat)

            count += 1  # Incrémenter le compteur

    def extract_date(self, cert, date_type):
        date_raw = cert.xpath(f".//div[@class='block_dates']/div[contains(., '{date_type}')]/text()").get()
        return self.format_date(date_raw.strip() if date_raw else None)

    def format_date(self, date_raw):
        try:
            return datetime.strptime(date_raw, "%d/%m/%Y").strftime("%Y-%m-%d")
        except (ValueError, TypeError):
            return None

    def is_valid_year(self, date):
        return date and 2015 <= int(date.split("-")[0]) <= 2025

    def generate_id(self, name):
        return re.sub(r"\W+", "_", name.strip().lower())