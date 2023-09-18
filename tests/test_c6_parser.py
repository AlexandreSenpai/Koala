import sys

sys.path.insert(0, '../')

import io
from unittest.mock import MagicMock, patch, call

import requests
import pytest

from koala.application.core.utils.date import Date
from koala.application.parsers.pdf.c6 import C6Parser
from koala.application.core.interfaces.extract_expenses_from_pdf import MonetaryValues

sut = C6Parser(initial_costs_page=1)

page_example = """NOME DO USUARIO
FATURA 17 AGO 2023  EMISSÃO E ENVIO 10 AGO 2023
 6 de 8
TRANSAÇÕES
DE 10 JUL A 10 AGO 
VALORES EM R$

31 JUL Pagamento em 31 JUL 1.727,00 
31 JUL Pag*Posto 130,00 
31 JUL Pag*Loreleyedith 12,00 
31 JUL Autoban 12,20 
31 JUL Autoban 12,40 
31 JUL Autoban 12,20 
31 JUL Renovias Fpay 15,80 
31 JUL Mercadolivre*Mercadol - Parcela 7/7 296,55 
01 AGO Ifood *Ifd*Habibs It 85,70

"""

minor_example = """NOME DO USUARIO
FATURA 17 AGO 2023  EMISSÃO E ENVIO 10 AGO 2023
 6 de 8
TRANSAÇÕES
DE 10 JUL A 10 AGO 
VALORES EM R$ 

31 JUL Mercadolivre*Mercadol - Parcela 7/7 296,55

"""

def describe_get_monetary_values():
    def check_get_monetary_values_returned_type() -> None:
        monetary_values = sut.get_monetary_values(page=page_example)
        assert isinstance(monetary_values, list)
        for expense in monetary_values:
            assert isinstance(expense, MonetaryValues)

    def check_get_all_monetary_values_from_bill_page() -> None:
        monetary_values = sut.get_monetary_values(page=page_example)
        assert len(monetary_values) == 8

    def check_all_amount_values_type() -> None:
        monetary_values = sut.get_monetary_values(page=page_example)
        for value in monetary_values:
            assert isinstance(value.amount, float) or isinstance(value.amount, int)

    def check_all_installment_values_type() -> None:
        monetary_values = sut.get_monetary_values(page=page_example)
        for value in list(filter(lambda x: x.installment_to is not None, monetary_values)):
            assert isinstance(value.installment_of, int)
            assert isinstance(value.installment_to, int)

    def check_name_values_type() -> None:
        monetary_values = sut.get_monetary_values(page=page_example)
        for value in monetary_values:
            assert isinstance(value.name, str)

    def it_should_return_empty_list_in_case_that_it_finds_nothing():
        monetary_values = sut.get_monetary_values(page="lorem ipsum lijasidjsid asidisd")
        assert isinstance(monetary_values, list)
        assert len(monetary_values) == 0

    @patch(f'koala.application.core.utils.date.Date.replace_month_pt_to_numerical', 
           wraps=Date.replace_month_pt_to_numerical)
    def it_should_call_data_parse_method(date_mock: MagicMock):
        expenses = sut.get_monetary_values(page=minor_example)
        print(expenses)
        date_mock.assert_called_once_with(date_str="31 JUL 2023")

def describe_get_pages():
    dummy_pdf_req = requests.get('https://www.africau.edu/images/default/sample.pdf')
    dummy_pdf = io.BytesIO(dummy_pdf_req.content)

    def it_should_return_two_str_pages():
        pages = sut.get_pages(buffered_pdf=dummy_pdf, 
                              initial_page=0)
        assert isinstance(pages, list)
        assert len(pages) == 2
        for page in pages:
            assert isinstance(page, str)
    
    def it_should_use_initial_page_from_class_if_user_do_not_pass_any():
        pages = sut.get_pages(buffered_pdf=dummy_pdf)
        assert isinstance(pages, list)
        assert len(pages) == 1

    def it_should_raise_and_error_if_initial_page_is_greater_than_max_pdf_pages():
        with pytest.raises(Exception, 
                           match='Initial page is over the maximum pages of the pdf.'):
            sut.get_pages(buffered_pdf=dummy_pdf,
                          initial_page=10)

def describe_extract_expenses():
    @patch('koala.application.parsers.pdf.c6.C6Parser.get_pages', 
           wraps='C6Parser.get_pages')
    @patch('koala.application.parsers.pdf.c6.C6Parser.get_monetary_values', 
           wraps='C6Parser.get_monetary_values')
    def test_extract_expenses(mock_get_monetary_values: MagicMock, 
                              mock_get_pages: MagicMock):
        # Mock the return values of the dependencies
        mock_get_pages.return_value = ["page1_content", 
                                       "page2_content"]
        mock_get_monetary_values.side_effect = [
            [MonetaryValues(purchased_at="2023-08-01", 
                            name="expense1",
                            amount= 100.0)],
            [MonetaryValues(purchased_at="2023-08-02", 
                            name="expense2", 
                            amount=200.0)]
        ]

        # Call the method
        expenses = sut.extract_expenses(buffered_pdf=MagicMock())

        # Assertions
        assert len(expenses) == 2
        assert expenses[0].name == "expense1"
        assert expenses[1].name == "expense2"

        # Check if the mocked methods were called correctly
        mock_get_pages.assert_called_once()
        mock_get_monetary_values.assert_has_calls([
            call("page1_content"),
            call("page2_content")
        ])
