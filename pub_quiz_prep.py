import glob
import os
import re
from typing import List, Tuple, Dict    

import requests
from bs4 import BeautifulSoup

from services.azure_openai_service import AzureOpenAIService
from services.bing_image_service import BingImageService
from services.spotify_service import create_spotify_playlist
from services.pdf_service import PDFService
from utils.date_utils import check_future_date, get_preceding_7_days_with_year
from utils.html_utils import extract_html_section, extract_news
from utils.image_utils import is_valid_image_format, save_image

class PubQuizPrep:
    def __init__(self, model: str, temperature: float):
        self.azure_service = AzureOpenAIService(model, temperature)
        self.bing_service = BingImageService()
        self.pdf_service = PDFService()
        
    def get_news(self, day: str, month: str) -> str:
        print(f"Beginne Zusammenfassung der Nachrichten der letzten Woche...")

        relevant_dates = get_preceding_7_days_with_year(day, month)
        news_summary = {}
        
        for d, m, y in relevant_dates:
            url = f"https://en.wikipedia.org/wiki/Portal:Current_events/{y}_{m}_{d}"
            try:
                response = requests.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                news_summary[f"{d}. {m} {y}"] = extract_news(soup)
            except requests.RequestException as e:
                print(f"Fehler beim Extrahieren der Nachrichten vom {d}-{m}-{y}: {e}")
                continue
        
        news_summary = ''.join(f"Datum: {title}\nNachrichten: \n'''{content}'''\n\n" for title, content in news_summary.items()).strip()
        
        prompt = f"""
        Erstelle eine Liste der signifkantesten Nachrichten mehrerer Tage. Dazu erhältst du eine Quelle, die sowohl das Datum als auch die 
        bereits zusammengefassten Inhalte der Nachrichten dieses Datums beinhaltet. Die Nachrichten sind hierbei durch ''' am Anfang und am Ende gekennzeichnet.
        Da es sich um die gesamten Nachrichten mehrerer Tage handelt, können Redundanzen und Wiederholungen auftreten. Wiederholungen implizieren keine höhere Wichtigkeit, ignoriere sie einfach.
        Besonders wichtig sind große sportliche Ereignisse, vor allem das Austragungsland und Sieger, sowie Tode bekannter Persönlichkeiten oder Wechsel der politischen Führung eines Landes.
        Achte außerdem auf die globale Relevanz der Nachrichten, lokale Ereignisse sind weniger wichtig. 
        Kriegerische Auseinandersetzungen sind nicht sehr interessant.         
        Hier ist deine Quelle, die du als Kontext nehmen musst:
        ### {news_summary} ###
        Fasse nun die signifkantesten Nachrichten zusammen. Halte dich dabei strikt an den obigen Kontext. 
        Besonders wichtig sind große sportliche Ereignisse (vor allem Austragungsland und Sieger), sowie Tode bekannter Persönlichkeiten oder Wechsel in der politischen Führung eines Landes.
        Beachte, dass die Nachrichten zwar auf Englisch sind, die Liste der signifkantesten Nachrichten aber auf Deutsch sein muss. 
        Erstelle als Ergebnis eine sortierte Liste nach Relevanz ohne weitere Bemerkungen.
        """
        
        response = self.azure_service.create_completion(prompt, "Du bist ein Experte im prägnanten Zusammenfassen der wichtigsten Nachrichten.")
        print(f"Nachrichten zwischen dem {relevant_dates[-1][0]}. und {day}. {month} erfolgreich zusammengefasst!")        
        return response
    
    def day_of_year_summary(self, day: str, month: str) -> str:
        print(f"Beginne Zusammenfassung des Tages...")
        url = f"https://de.wikipedia.org/wiki/{day}._{month}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            print(f"Fehler beim Extrahieren der Daten für den {day}-{month}: {e}")
            return ""

        events = extract_html_section(soup, "Ereignisse", "Geboren")
        births = extract_html_section(soup, "Geboren", "Gestorben")
        deaths = extract_html_section(soup, "Gestorben", "Feier-_und_Gedenktage")
        holidays = extract_html_section(soup, "Feier-_und_Gedenktage", "catlinks")

        data_dict = {
            "Ereignisse": events,
            "Geburten": births,
            "Tode": deaths,
            "Gedenk- und Feiertage": holidays
        }

        res_dict = {}
        for title, content in data_dict.items():
            prompt = f"""
            Fasse die wichtigsten {title} des {day}. {month} im Laufe der Geschichte zusammen.
            Beachte dabei, die Zusammenfassung auf die für die Menschheitsgeschichte signifkantesten Ereignisse und Personen zu beschränken.
            Konzentriere dich außerdem auf die jüngere Geschichte, vor allem des 20. und 21. Jahrhunderts, aber wenn weiter zurückliegende Ereignisse extrem signifikant waren, dürfen sie ebenfalls auftauchen.
            Gib eine Liste mit bis zu 20 {title} zurück. Hier deine Quelle, die du als Kontext nehmen musst:
            ### {title}: {content} ###
            Fasse nun die wichtigsten {title} zusammen. Halte dich dabei strikt an den obigen Kontext. Gib nur die Liste ohne weitere Bemerkungen zurück.
            """
            
            response = self.azure_service.create_completion(prompt, "Du bist ein Experte im prägnanten Zusammenfassen von Informationen. Du hältst dich immer strikt an den dir gegebenen Kontext.")
            res_dict[title] = response
            print(f"Zusammenfassung der {title} fertiggstellt!")

        res_text = ''.join(f"### {key}\n{value}\n\n" for key, value in res_dict.items())
        return res_text

    def image_round(self, topic: str, num: int) -> List[Tuple[str, str]]:
        print(f"Beginne mit Erstellung der Bilderrunde...")
        
        prompt = f"""
        Stelle eine Liste mit den {num} signifkantesten Elementen zum Thema '{topic}' bereit.
        Die Elemente sollten entsprechend ihrer Berühmtheit und Signifkanz für alle Bereiche, zB Kultur, Historik oder Filme, berücksichtigt werden.
        Gib eine Antwort ohne Erklärung und die Liste mit komma-separierten Strings.
        """
        
        response = self.azure_service.create_completion(prompt, "Du bist ein Experte im Erstellen von Listen für alle denkbaren Themen.")
        subjects = response.split(',')

        images = []
        for sub in subjects:
            sub = sub.strip()
            search_results = self.bing_service.search_images(f"{topic}: {sub}")
            for res in search_results:
                img_url = res.get("contentUrl")
                img_data = self.bing_service.download_image(img_url)
                if img_data and is_valid_image_format(img_data):
                    temp_dir = "resources/temp"
                    if not os.path.exists(temp_dir):
                        os.makedirs(temp_dir)
                    
                    img_path = os.path.join(temp_dir, f"{sub}.jpg")
                    save_image(img_data, img_path)
                    images.append((sub, img_path))
                    break

        print(f"Bilderrunde fertiggestellt!")
        return images

    def music_round(self, topic: str, num: int) -> Tuple[str, str, str]:
        print(f"Beginne mit Erstellung der Musikrunde...")
        
        prompt = f"""
        Erstelle eine numerierte Liste der {num} signifkantesten Songs, die das Thema '{topic}' als Kernthema, im Titel oder als Interpreten haben.
        Konzentriere dich auf englische sowie deutsche Songs. Gib eine Antwort ohne Erklärung und benutze keine Anführungszeichen.
        """
        
        response = self.azure_service.create_completion(prompt, "Du bist ein Experte für Musik.")
        songs_dict = {artist.strip(): title.strip('"') for title, artist in re.findall(r'\d+\.\s*([^-\d]+)\s*-\s*([^0-9]+)', response)}
        if not songs_dict: 
            print("Songs waren zur Erstellung einer Playlist nicht extrahierbar.")
            raise SystemExit("Exiting program due to empty dictionary.")
        
        playlist_url, img = create_spotify_playlist(songs_dict, topic)
             
        print(f"Musikrunde fertiggestellt!")
        return response, playlist_url, img

    def prepare_quiz(self, day: str, month: str, image_topic: str, image_num: int, music_theme: str, music_num: int):
        if check_future_date(day, month):
            print(f"Der {day}.{month} liegt in der Zukunft. Die Vorbereitung kann nicht gestartet werden.")
            return
        
        print(f"Vorbereitung für das Pub Quiz am {day}. {month} gestartet!")

        # News
        news = self.get_news(day, month)
        self.pdf_service.add_news(news)

        # Summary
        day_summary = self.day_of_year_summary(day, month)
        self.pdf_service.add_summary(day, month, day_summary)

        # Image round
        images = self.image_round(image_topic, image_num)
        self.pdf_service.add_images(images, image_topic)

        # Music round
        songs, playlist_url, qr_code = self.music_round(music_theme, music_num)
        self.pdf_service.add_music_round(music_theme, songs, playlist_url, qr_code)
        
        # Clean-up
        for file_path in glob.glob('resources/temp/*.[jp][pn]g'):
            os.remove(file_path)

        # Save results
        self.pdf_service.save_pdf(day, month)
        print(f"Vorbereitung für das Pub Quiz am {day}. {month} abgeschlossen!")
