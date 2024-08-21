import requests
from requests.exceptions import SSLError
from config import BING_SEARCH_KEY, BING_SEARCH_ENDPOINT

class BingImageService:
    def __init__(self):
        self.headers = {"Ocp-Apim-Subscription-Key": BING_SEARCH_KEY}
        self.endpoint = BING_SEARCH_ENDPOINT

    def search_images(self, query):
        params = {"q": query, "count": 3, "imageType": "photo"}
        try:
            response = requests.get(self.endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json().get("value", [])
        except requests.exceptions.RequestException as e:
            print(f"Error during Bing search request: {e}")
            return []

    def download_image(self, img_url):
        try:
            img_response = requests.get(img_url)
            img_response.raise_for_status()
            return img_response.content
        except SSLError as e:
            print(f"SSL error when downloading image from {img_url}: {e}")
        except requests.exceptions.RequestException as e:
            print(f"Request error when downloading image from {img_url}: {e}")
        return None