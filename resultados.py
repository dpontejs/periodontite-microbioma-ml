"""Formato padronizado da pasta ``resultados/``.

O notebook grava o modelo final com :func:`salvar_resultados`; o app de
demonstração (``app.py``) lê com :func:`carregar_resultados`. Conteúdo da pasta:

- ``modelo.joblib``: modelo treinado (ex.: um ``Pipeline`` do scikit-learn);
- ``teste.csv.gz``: conjunto de teste (SEQN, atributos e coluna ``rotulo``);
- ``metricas.json``: métricas de desempenho no teste;
- ``rotulos_atributos.json``: código do atributo -> nome legível (ex.: gênero);
- ``figuras/*.png``: figuras para a aba "Desempenho";
- ``modelo_taxons.joblib`` (opcional): um segundo modelo, só com o microbioma, cuja
  probabilidade o app mostra ao lado da do modelo principal.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import joblib
import pandas as pd

CLASSES = ("Sem periodontite", "Periodontite")  # rótulo 0 e rótulo 1


@dataclass
class Resultados:
    modelo: object
    teste: pd.DataFrame  # índice SEQN; atributos + coluna "rotulo" (0/1)
    metricas: dict
    rotulos_atributos: dict
    figuras: list[Path]
    modelo_taxons: object | None = None  # modelo só com o microbioma (opcional)


def salvar_resultados(
    modelo,
    X_teste: pd.DataFrame,
    y_teste: pd.Series,
    metricas: dict[str, float],
    figuras: dict,
    rotulos_atributos: dict[str, str],
    pasta: Path = Path("resultados"),
    modelo_taxons=None,
) -> None:
    """Grava tudo o que o app precisa. ``X_teste`` deve ter SEQN como índice."""
    rotulos = pd.Series(y_teste).astype(int)
    if not rotulos.isin([0, 1]).all():
        raise ValueError("y_teste deve conter apenas 0 ou 1 (0 = sem periodontite, 1 = periodontite).")

    pasta = Path(pasta)
    (pasta / "figuras").mkdir(parents=True, exist_ok=True)

    joblib.dump(modelo, pasta / "modelo.joblib")
    if modelo_taxons is not None:
        joblib.dump(modelo_taxons, pasta / "modelo_taxons.joblib")
    teste = X_teste.copy()
    teste.index.name = "SEQN"
    teste["rotulo"] = rotulos.to_numpy()
    teste.to_csv(pasta / "teste.csv.gz")
    (pasta / "metricas.json").write_text(
        json.dumps(metricas, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (pasta / "rotulos_atributos.json").write_text(
        json.dumps(rotulos_atributos, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    for nome, figura in figuras.items():
        figura.savefig(pasta / "figuras" / f"{nome}.png", dpi=150, bbox_inches="tight")


def carregar_resultados(pasta: Path = Path("resultados")) -> Resultados:
    pasta = Path(pasta)
    if not (pasta / "modelo.joblib").exists():
        raise FileNotFoundError(
            f"Não encontrei resultados em '{pasta}'. Primeiro execute o notebook até a "
            "célula que chama salvar_resultados(...)."
        )
    return Resultados(
        modelo=joblib.load(pasta / "modelo.joblib"),
        teste=pd.read_csv(pasta / "teste.csv.gz", index_col="SEQN"),
        metricas=json.loads((pasta / "metricas.json").read_text(encoding="utf-8")),
        rotulos_atributos=json.loads((pasta / "rotulos_atributos.json").read_text(encoding="utf-8")),
        figuras=sorted((pasta / "figuras").glob("*.png")),
        modelo_taxons=(
            joblib.load(pasta / "modelo_taxons.joblib")
            if (pasta / "modelo_taxons.joblib").exists() else None
        ),
    )
