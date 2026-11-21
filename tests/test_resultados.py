import pandas as pd
import pytest
from sklearn.dummy import DummyClassifier

from conftest import METRICAS_EXEMPLO
from resultados import carregar_resultados, salvar_resultados


def test_ida_e_volta(resultados_exemplo):
    res = carregar_resultados(resultados_exemplo)

    assert res.teste.shape[0] == 10
    assert res.teste.index.name == "SEQN"
    assert "rotulo" in res.teste
    assert res.metricas == METRICAS_EXEMPLO
    assert res.rotulos_atributos["RSV_genus1"] == "Gênero 1"
    assert [p.name for p in res.figuras] == ["curva_roc.png"]
    probabilidades = res.modelo.predict_proba(res.teste.drop(columns="rotulo"))
    assert probabilidades.shape == (10, 2)


def test_carregar_sem_pasta(tmp_path):
    with pytest.raises(FileNotFoundError, match="execute o notebook"):
        carregar_resultados(tmp_path / "nao_existe")


def test_salvar_recusa_rotulo_invalido(tmp_path):
    X = pd.DataFrame({"RSV_genus1": [0.1, 0.2]}, index=pd.Index([1, 2], name="SEQN"))
    y = pd.Series([0, 2], index=X.index)
    modelo = DummyClassifier().fit(X, [0, 1])

    with pytest.raises(ValueError, match="0 ou 1"):
        salvar_resultados(modelo, X, y, {}, {}, {}, pasta=tmp_path / "r")


def test_salvar_e_carregar_sem_depender_da_codificacao_do_sistema(tmp_path):
    # No Windows, abrir arquivo sem encoding= usa cp1252 e corrompe acentos.
    # Com -X warn_default_encoding, qualquer abertura sem encoding vira erro.
    import subprocess
    import sys
    from pathlib import Path

    codigo = f"""
import warnings
warnings.simplefilter("error", EncodingWarning)
import pandas as pd
from sklearn.dummy import DummyClassifier
from resultados import salvar_resultados, carregar_resultados
X = pd.DataFrame({{"RSV_genus1": [0.1, 0.2]}}, index=pd.Index([1, 2], name="SEQN"))
y = pd.Series([0, 1], index=X.index)
salvar_resultados(DummyClassifier().fit(X, y), X, y, {{"Acurácia — média": 0.7}},
                  {{}}, {{"RSV_genus1": "Gênero"}}, pasta=r"{tmp_path / 'r'}")
res = carregar_resultados(r"{tmp_path / 'r'}")
assert res.rotulos_atributos == {{"RSV_genus1": "Gênero"}}
assert res.metricas == {{"Acurácia — média": 0.7}}
"""
    raiz = Path(__file__).resolve().parents[1]
    proc = subprocess.run(
        [sys.executable, "-X", "warn_default_encoding", "-c", codigo],
        cwd=raiz, capture_output=True, text=True, encoding="utf-8",
    )
    assert proc.returncode == 0, proc.stderr[-800:]
