import sys
sys.path.insert(0, '../')

import pytest

from koala.application.core.utils.date import Date

def describe_date_utils():
    def test_valid_month_replacement():
        assert Date.replace_month_pt_to_numerical("01 JAN 2022") == "2022-01-01"
        assert Date.replace_month_pt_to_numerical("15 FEV 2021") == "2021-02-15"
        assert Date.replace_month_pt_to_numerical("30 DEZ 2020") == "2020-12-30"

    def test_invalid_month_replacement():
        with pytest.raises(Exception) as e_info:
            Date.replace_month_pt_to_numerical("01 XXX 2022")
        assert str(e_info.value) == 'Not a valid month identifier.'

    def test_case_insensitivity():
        assert Date.replace_month_pt_to_numerical("01 jan 2022") == "2022-01-01"
        assert Date.replace_month_pt_to_numerical("15 FeV 2021") == "2021-02-15"

    def test_incorrect_date_format():
        with pytest.raises(Exception, match='Not a valid month identifier.'):
            Date.replace_month_pt_to_numerical("10 NOT 2022")

        with pytest.raises(Exception, match='Wrong date_str format. This function only accepts: dd B YYYY, for example: 20 JUL 1999'):
            Date.replace_month_pt_to_numerical("2022 JAN 01")

        with pytest.raises(Exception, match='Wrong date_str format. This function only accepts: dd B YYYY, for example: 20 JUL 1999'):
            Date.replace_month_pt_to_numerical("01 JAN 23")

        with pytest.raises(Exception, match='Wrong date_str format. This function only accepts: dd B YYYY, for example: 20 JUL 1999'):
            Date.replace_month_pt_to_numerical("01 JANEIRO 2023")

        with pytest.raises(Exception, match='Wrong date_str format. This function only accepts: dd B YYYY, for example: 20 JUL 1999'):
            Date.replace_month_pt_to_numerical("1 JANEIRO 2023")