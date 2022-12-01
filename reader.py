import sys
import logging
import os

from bs4 import BeautifulSoup
from urllib.request import urlopen
from gtts import gTTS
from playsound import playsound

class MNMReader:
    def __init__(self, site_url: str) -> None:
        self.__site_url = site_url
        self.__titles = []

    def extract_titles(self):
        logging.debug("Extracting titles from: %s", self.__site_url)
        page = urlopen(self.__site_url)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        full_news = soup.find_all("h2")

        for news in full_news:
            title = "".join(news.get_text())
            logging.info("New title found: %s", title)
            self.__titles.append(title[0:])
    
    def generate_tts(self):
        title_count=1
        for title in self.__titles:
            myobj = gTTS(text=title, lang="es", slow=False)
            sound_filename = "title"+str(title_count)+".mp3"
            myobj.save(sound_filename)
            title_count+=1
            logging.info("Playing new title: %s...", title)
            playsound(sound_filename)
            os.remove(sound_filename)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    logging.info("Running mnmreader...")
    reader = MNMReader("http://www.meneame.net")
    reader.extract_titles()
    reader.generate_tts()