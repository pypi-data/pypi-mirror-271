import json
from hnt_sap_gui import SapGui

def test_create():
    with open("./devdata/json/fatura_GHN-577.json", "r", encoding="utf-8") as arquivo_json: fatura = json.load(arquivo_json)

    txResult = SapGui().hnt_run_transaction_FV60(fatura)
    assert txResult is not None