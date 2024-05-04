from datetime import datetime
from .constants import DATE_FORMATS


class DateTime:
    def __init__(self, dt):
        self._date = None
        self._style = None
        self._parse_date(dt)

    def _parse_date(self, date):
        for style in DATE_FORMATS:
            try:
                self._date = datetime.strptime(date, style)
                self._style = style
                return  # 解析成功后立即返回
            except ValueError:
                pass
