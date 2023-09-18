from datetime import datetime
import sys

from koala.application.core.utils.date import Date

sys.path.insert(0, '../')

from unittest.mock import MagicMock, patch, Mock, call

import pytest

from koala.application.parsers.pdf.nubank import NubankParser
from koala.application.core.interfaces.extract_expenses_from_pdf import MonetaryValues

sut = NubankParser()

page_example = """NOME DO USUARIO
FATURA 17 AGO 2023  EMISSÃO E ENVIO 10 AGO 2023
 6 de 8
TRANSAÇÕES
DE 10 JUL A 10 AGO 
VALORES EM R$ 
31 JUL 
 
Pagamento em 31 JUL 
1.727,00 
31 JUL 
 
Pag*Posto
130,00 
31 JUL 
 
Pag*Loreleyedith 
12,00 
31 JUL 
 
Autoban 
12,20 
31 JUL 
 
Autoban 
12,40 
31 JUL 
 
Autoban 
12,20 
31 JUL 
 
Renovias Fpay 
15,80 
31 JUL 
 
Antecipada - Mercadolivre*Mercadol - 7/7 
296,55 
01 AGO 
 
Ifood *Ifd*Habibs It 
85,70 
02 AGO 
 
Dl*Google Cloud 
70,63 
02 AGO 
 
Pag*Mrgcomercioe 
27,00 
02 AGO 
 
Top 
8,80 
03 AGO 
 
Vindi *Caniballssport 
89,90 
03 AGO 
 
Pag*Smartshop 
26,84 
04 AGO 
 
Pag*Riotgame - 1/3 
41,64 
04 AGO 
 
Auto Posto Carlu 
50,00 
04 AGO 
 
Pag*Zig 
10,00 
04 AGO 
 
IOF de "Paypal *Crunchyroll" 
1,12 
04 AGO 
 
Paypal *Crunchyroll 
20,80 
04 AGO 
 
Pag*Zig 
15,00 
04 AGO 
 
Starbucks Brasil Comer 
64,00 
04 AGO 
 
Restaurante Xanntony 
35,00 
05 AGO 
 
Paypal *Medium.Com
25,28 
05 AGO 
 
Pag*Smartshop 
31,74 
05 AGO 
 
IOF de "Paypal *Medium.Com" 
1,36 
05 AGO 
 
Lanchonete da Cidade L 
69,16 
06 AGO 
 
Peg Pese Morumbi 
103,74 
06 AGO 
 
Parker Estacionamentos 
14,00
"""

minor_example = """NOME DO USUARIO
FATURA 17 AGO 2023  EMISSÃO E ENVIO 10 AGO 2023
 6 de 8
TRANSAÇÕES
DE 10 JUL A 10 AGO 
VALORES EM R$ 
31 JUL 
 
Pagamento em 31 JUL 
1.727,00 
"""

def describe_get_monetary_values():
    def check_get_monetary_values_returned_type() -> None:
        monetary_values = sut.get_monetary_values(page=page_example)
        assert isinstance(monetary_values, list)
        for expense in monetary_values:
            assert isinstance(expense, MonetaryValues)

    def check_get_all_monetary_values_from_bill_page() -> None:
        monetary_values = sut.get_monetary_values(page=page_example)
        assert len(monetary_values) == 28

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
        sut.get_monetary_values(page=minor_example)
        date_mock.assert_called_once_with(date_str="31 JUL 2023")

