import requests
from bs4 import BeautifulSoup


class FBGroupScraper:

    def __init__(self, group_id):
        self.group_id = group_id
        self.page_url = "https://mobile.facebook.com/groups/" + self.group_id
        self.page_content = ""

    def get_page_content(self):
        self.page_content = requests.get(self.page_url).text

    def parse(self):
        soup = BeautifulSoup(self.page_content, "html.parser")
        feed_container = soup.find(id="m_group_stories_container").find_all("p")
        for i in feed_container:
            print(i.text)

group_id = "2459047080785676"
d = FBGroupScraper(group_id)
d.get_page_content()
mensaje = d.parse()
print(mensaje)
