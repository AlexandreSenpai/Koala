from datetime import datetime
import re
from typing import Union


class Transformer:
    @staticmethod
    def string_to_datetime(date: Union[str, datetime]) -> datetime:
        if isinstance(date, datetime): return date

        matched = re.fullmatch(r'\d{4}-\d{2}-\d{2}', date)
        if matched: return datetime.strptime(date, '%Y-%m-%d')
        raise Exception('Invalid input date. You must input a valid YYYY-MM-DD date.')