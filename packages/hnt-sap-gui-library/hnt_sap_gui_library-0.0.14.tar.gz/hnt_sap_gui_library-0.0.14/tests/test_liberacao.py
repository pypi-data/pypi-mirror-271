import json
from hnt_sap_gui import SapGui
from hnt_sap_gui.nota_fiscal.nota_pedido_transaction import NotaPedidoTransaction

def test_create():
    cod_nota_pedido = '4506202888'
    result = SapGui().hnt_run_transaction_liberacao(cod_nota_pedido)
    assert result is not None
