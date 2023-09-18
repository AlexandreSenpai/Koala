from datetime import datetime
import sys

sys.path.insert(0, '../')

import pytest
from koala.application.core.utils.transformers import Transformer


def test_datetime_object():
    dt = datetime(2022, 1, 1)
    assert Transformer.string_to_datetime(dt) == dt

def test_valid_string_to_datetime():
    dt = datetime(2022, 1, 1)
    assert Transformer.string_to_datetime("2022-01-01") == dt

def test_invalid_string_to_datetime():
    with pytest.raises(Exception) as e_info:
        Transformer.string_to_datetime("01-01-2022")
    assert str(e_info.value) == 'Invalid input date. You must input a valid YYYY-MM-DD date.'

    with pytest.raises(Exception) as e_info:
        Transformer.string_to_datetime("2022/01/01")
    assert str(e_info.value) == 'Invalid input date. You must input a valid YYYY-MM-DD date.'

def test_invalid_type_to_datetime():
    with pytest.raises(Exception) as e_info:
        Transformer.string_to_datetime(123) # type: ignore
    assert str(e_info.value) == 'This method only accepts datetime or string parameters.'