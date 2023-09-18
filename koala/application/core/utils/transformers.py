from datetime import datetime
import re
from typing import Union


class Transformer:
    @staticmethod
    def string_to_datetime(date: Union[str, datetime]) -> datetime:
        if isinstance(date, datetime): return date
        if not isinstance(date, str):
            raise Exception('This method only accepts datetime or string parameters.')

        matched = re.fullmatch(r'\d{4}-\d{2}-\d{2}', date)
        if matched: return datetime.strptime(date, '%Y-%m-%d')
        raise Exception('Invalid input date. You must input a valid YYYY-MM-DD date.')
    
    @staticmethod
    def string_to_float(value: Union[str, float]) -> float:
        if isinstance(value, str):
            return float(value.replace(',', '.'))
        return float(value)