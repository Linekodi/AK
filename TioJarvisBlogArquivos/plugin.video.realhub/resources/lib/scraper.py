import requests
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self):
        self.base_url = "https://vizer.tv/"

    def get_categories(self):
        categories = []
        url = self.base_url
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        for category_link in soup.find_all("a", class_="card-header"):
            category_url = self.base_url + category_link["href"]
            category_name = category_link.text.strip()
            categories.append({"name": category_name, "url": category_url})
        return categories

    def get_videos(self, category_url):
        videos = []
        response = requests.get(category_url)
        soup = BeautifulSoup(response.content, "html.parser")
        for video_link in soup.find_all("a", class_="card-link"):
            video_url = self.base_url + video_link["href"]
            video_title = video_link.find("h5").text.strip()
            video_description = video_link.find("p", class_="card-text").text.strip()
            videos.append({"title": video_title, "url": video_url, "description": video_description})
        return videos
