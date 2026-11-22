import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import pytest  # noqa: E402
from sklearn.linear_model import LogisticRegression  # noqa: E402

from resultados import salvar_resultados  # noqa: E402

ATRIBUTOS = [f"RSV_genus{i}" for i in range(1, 6)]
METRICAS_EXEMPLO = {"acuracia_balanceada": 0.61, "auc_roc": 0.67}


@pytest.fixture
def resultados_exemplo(tmp_path):
    """Pasta resultados/ com um modelo pequeno, no mesmo formato do notebook."""
    rng = np.random.default_rng(0)
    abundancias = rng.dirichlet(np.ones(len(ATRIBUTOS)), size=40)
    X = pd.DataFrame(abundancias, columns=ATRIBUTOS, index=pd.Index(range(1000, 1040), name="SEQN"))
    y = pd.Series(np.tile([0, 1], 20), index=X.index, name="rotulo")
    modelo = LogisticRegression().fit(X.iloc[:30], y.iloc[:30])

    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 1])

    pasta = tmp_path / "resultados"
    salvar_resultados(
        modelo,
        X.iloc[30:],
        y.iloc[30:],
        METRICAS_EXEMPLO,
        {"curva_roc": fig},
        {c: f"Gênero {i}" for i, c in enumerate(ATRIBUTOS, 1)},
        pasta=pasta,
    )
    plt.close(fig)
    return pasta


@pytest.fixture
def resultados_com_taxons(tmp_path):
    """Como resultados_exemplo, mas com um segundo modelo que usa só parte das colunas."""
    rng = np.random.default_rng(1)
    abundancias = rng.dirichlet(np.ones(len(ATRIBUTOS)), size=40)
    X = pd.DataFrame(abundancias, columns=ATRIBUTOS, index=pd.Index(range(2000, 2040), name="SEQN"))
    y = pd.Series(np.tile([0, 1], 20), index=X.index, name="rotulo")
    modelo = LogisticRegression().fit(X.iloc[:30], y.iloc[:30])
    modelo_taxons = LogisticRegression().fit(X.iloc[:30, :3], y.iloc[:30])

    pasta = tmp_path / "resultados_ab"
    salvar_resultados(
        modelo, X.iloc[30:], y.iloc[30:], METRICAS_EXEMPLO, {},
        {c: f"Gênero {i}" for i, c in enumerate(ATRIBUTOS, 1)},
        pasta=pasta, modelo_taxons=modelo_taxons,
    )
    return pasta
