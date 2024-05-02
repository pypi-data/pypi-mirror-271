import json
from hnt_sap_gui import SapGui

def test_create():
    with open("./devdata/json/miro_GHN-557.json", "r", encoding="utf-8") as miro_arquivo_json: miro = json.load(miro_arquivo_json)
    numero_pedido = '4506202889'
    result = SapGui().hnt_run_transaction_miro(numero_pedido, miro)
    assert result is not None