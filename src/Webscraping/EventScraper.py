import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass


@dataclass
class EventData:
    name: str
    link: str
    date: str
    time: str
    passed: bool


class EventScraper:
    def __init__(
        self,
        events_base_url: str,
        future_events_page_url: str,
        past_events_page_url: str,
    ) -> None:
        self.events_base_url = events_base_url
        self.future_events_page_url = future_events_page_url
        self.past_events_page_url = past_events_page_url

    def get_event_data(self, event_name: str) -> EventData:
        passed = False
        event_page_url = self.get_event_page_url(
            event_name, self.future_events_page_url
        )
        if event_page_url is None:
            passed = True
            event_page_url = self.get_event_page_url(
                event_name, self.past_events_page_url
            )

        if event_page_url is None:
            return None

        event_page = requests.get(event_page_url)
        soup = BeautifulSoup(event_page.text, "html.parser")
        event_date = soup.find(
            "strong", string=lambda s: "дата" in s.lower()
        ).next_sibling.text.strip()
        event_time = soup.find(
            "strong", string=lambda s: "время" in s.lower()
        ).next_sibling.text.strip()
        return EventData(event_name, event_page_url, event_date, event_time, passed)

    def get_event_page_url(self, event_name: str, events_page_url: str) -> str:
        events_page = requests.get(events_page_url)
        soup = BeautifulSoup(events_page.text, "html.parser")
        event_elements = soup.find_all("div", class_="event-item")
        for event_element in event_elements:
            current_event_name = event_element.find("div", class_="event-title").text
            if current_event_name == event_name:
                relative_link = event_element.find("a")["href"]
                return f"{self.events_base_url}{relative_link}"
        return None
