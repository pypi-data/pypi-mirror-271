import datetime
from .constants import *


class Currency(dict):
    def __init__(self):
        super().__init__()

    def fetch(self):
        import requests
        import xml.etree.ElementTree as ET
        response = requests.get(FETCH_URL_PBC)
        xml_content = response.text
        root = ET.fromstring(xml_content)
        for child in root.findall(PBC_ITEM):
            self[child.find(PBC_ITEM_DATE).text] = float(child.find(PBC_ITEM_VALUE).text)

    def get(self, date=None) -> float | None:
        today = datetime.date.today().strftime(DATE_FORMAT)
        now = datetime.datetime.now()
        if (now.hour == 9 and now.minute > 30) or now.hour > 9:
            print("当前时间已经超过 9:30 了")
        else:
            print("还没到 9:30")
        if
        self.fetch()
        return super().get(date)

