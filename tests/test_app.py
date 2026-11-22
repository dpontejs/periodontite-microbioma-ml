import gradio as gr
import pytest

from app import criar_app, criar_app_ou_aviso, prever, prever_taxons, tabela_metricas
from resultados import CLASSES, carregar_resultados


@pytest.fixture
def res(resultados_exemplo):
    return carregar_resultados(resultados_exemplo)


def test_prever_probabilidades(res):
    seqn = int(res.teste.index[0])
    probabilidades, _, _ = prever(res, seqn)

    assert set(probabilidades) == set(CLASSES)
    assert sum(probabilidades.values()) == pytest.approx(1.0)


def test_prever_rotulo_real(res):
    seqn = int(res.teste.index[0])
    _, rotulo_real, _ = prever(res, seqn)

    assert rotulo_real == CLASSES[res.teste.loc[seqn, "rotulo"]]


def test_prever_top_atributos(res):
    seqn = int(res.teste.index[0])
    _, _, tabela = prever(res, seqn)

    assert list(tabela.columns) == ["atributo", "abundancia"]
    assert len(tabela) <= 10
    assert tabela["abundancia"].is_monotonic_decreasing
    assert set(tabela["atributo"]) <= set(res.rotulos_atributos.values())


def test_prever_colunas_embaralhadas(res):
    seqn = int(res.teste.index[0])
    esperado, _, _ = prever(res, seqn)

    res.teste = res.teste[list(reversed(res.teste.columns))]
    obtido, _, _ = prever(res, seqn)

    assert obtido == pytest.approx(esperado)


def test_prever_seqn_inexistente(res):
    with pytest.raises(gr.Error):
        prever(res, 999_999)


def test_tabela_metricas(res):
    tabela = tabela_metricas(res)

    assert list(tabela.columns) == ["metrica", "valor"]
    assert dict(zip(tabela["metrica"], tabela["valor"])) == res.metricas


def test_criar_app(res):
    assert isinstance(criar_app(res), gr.Blocks)


def test_app_sem_resultados(tmp_path, monkeypatch):
    monkeypatch.setenv("RESULTADOS_DIR", str(tmp_path))

    assert isinstance(criar_app_ou_aviso(), gr.Blocks)


def test_prever_taxons(resultados_com_taxons):
    res = carregar_resultados(resultados_com_taxons)
    seqn = int(res.teste.index[0])

    probabilidades = prever_taxons(res, seqn)

    assert set(probabilidades) == set(CLASSES)
    assert sum(probabilidades.values()) == pytest.approx(1.0)


def test_prever_taxons_sem_modelo(res):
    assert prever_taxons(res, int(res.teste.index[0])) is None


def test_app_com_modelo_taxons(resultados_com_taxons):
    assert isinstance(criar_app(carregar_resultados(resultados_com_taxons)), gr.Blocks)
