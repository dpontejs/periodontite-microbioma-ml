import joblib
import numpy as np
import pandas as pd
import pytest
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer

from microbioma import clr


def test_clr_linhas_somam_zero():
    X = pd.DataFrame({"a": [0.5, 0.2], "b": [0.3, 0.3], "c": [0.2, 0.5]})

    resultado = clr(X)

    assert resultado.sum(axis=1).to_numpy() == pytest.approx([0.0, 0.0])


def test_clr_substitui_zeros_por_1e_6():
    X = pd.DataFrame({"a": [0.0], "b": [1.0]})

    resultado = clr(X)

    esperado_a = np.log(1e-6) - (np.log(1e-6) + np.log(1.0)) / 2
    assert resultado.loc[0, "a"] == pytest.approx(esperado_a)


def test_clr_preserva_colunas_e_indice():
    X = pd.DataFrame({"RSV_genus1": [0.4], "RSV_genus2": [0.6]}, index=pd.Index([77], name="SEQN"))

    resultado = clr(X)

    assert list(resultado.columns) == ["RSV_genus1", "RSV_genus2"]
    assert list(resultado.index) == [77]


def test_clr_em_pipeline_salvo_e_recarregado(tmp_path):
    rng = np.random.default_rng(0)
    X = pd.DataFrame(rng.dirichlet(np.ones(4), size=30), columns=[f"RSV_genus{i}" for i in range(4)])
    y = np.tile([0, 1], 15)
    modelo = make_pipeline(FunctionTransformer(clr), LogisticRegression()).fit(X, y)

    joblib.dump(modelo, tmp_path / "m.joblib")
    recarregado = joblib.load(tmp_path / "m.joblib")

    assert list(recarregado.feature_names_in_) == list(X.columns)
    assert recarregado.predict_proba(X) == pytest.approx(modelo.predict_proba(X))


from microbioma import RemoverCorrelacionados  # noqa: E402


def _dados_com_copia():
    rng = np.random.default_rng(1)
    a = rng.normal(size=50)
    return pd.DataFrame({
        "a": a,
        "copia_de_a": 2 * a + 1,               # correlação 1 com "a"
        "inverso_de_a": -a,                     # correlação -1 com "a"
        "b": rng.normal(size=50),
    })


def test_remove_atributo_correlacionado_mantendo_o_primeiro():
    X = _dados_com_copia()

    filtro = RemoverCorrelacionados(limiar=0.8).fit(X)

    assert list(filtro.get_feature_names_out()) == ["a", "b"]
    assert list(filtro.transform(X).columns) == ["a", "b"]


def test_limiar_alto_mantem_tudo():
    X = _dados_com_copia()[["a", "b"]]

    filtro = RemoverCorrelacionados(limiar=0.8).fit(X)

    assert list(filtro.get_feature_names_out()) == ["a", "b"]


def test_usa_apenas_os_dados_do_fit():
    X = _dados_com_copia()
    filtro = RemoverCorrelacionados(limiar=0.8).fit(X)

    novo = X.copy()
    novo["copia_de_a"] = np.random.default_rng(2).normal(size=50)  # no "teste" não é mais cópia

    assert list(filtro.transform(novo).columns) == ["a", "b"]


def test_funciona_com_numpy_e_no_pipeline_salvo(tmp_path):
    X = _dados_com_copia()
    y = (X["a"] + X["b"] > 0).astype(int)
    modelo = make_pipeline(RemoverCorrelacionados(0.8), LogisticRegression()).fit(X, y)
    joblib.dump(modelo, tmp_path / "m.joblib")

    recarregado = joblib.load(tmp_path / "m.joblib")

    assert recarregado.predict_proba(X) == pytest.approx(modelo.predict_proba(X))
    assert RemoverCorrelacionados(0.8).fit(X.to_numpy()).transform(X.to_numpy()).shape == (50, 2)
