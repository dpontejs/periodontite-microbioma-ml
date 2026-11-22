"""Transformações dos dados de microbioma usadas no notebook e no modelo final.

A função fica num arquivo próprio (e não só no notebook) para que o modelo salvo
em ``resultados/modelo.joblib`` consiga usá-la quando for carregado pelo app.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import _check_feature_names_in, check_is_fitted, validate_data


def clr(X: pd.DataFrame) -> pd.DataFrame:
    """Transformação CLR (centered log-ratio), amostras nas linhas.

    Mesma função da aula de Machine Learning e Metagenômica: valores menores que
    1e-6 viram 1e-6 (para evitar log(0)); depois, cada valor é dividido pela média
    geométrica da sua linha e passa pelo logaritmo.
    """
    X = pd.DataFrame(X).clip(lower=1e-6)
    gm = np.exp(np.mean(np.log(X), axis=1))
    return np.log(X.div(gm, axis=0))


class RemoverCorrelacionados(TransformerMixin, BaseEstimator):
    """Remove atributos muito correlacionados entre si (método de filtro da aula 04).

    Percorre os atributos em ordem; quando dois têm |correlação| >= ``limiar``,
    mantém o primeiro e descarta o outro. As correlações são calculadas só nos
    dados passados ao ``fit`` (o treino), e o ``transform`` apenas aplica a escolha.
    """

    def __init__(self, limiar: float = 0.8):
        self.limiar = limiar

    def fit(self, X, y=None):
        X = validate_data(self, X, reset=True)
        with np.errstate(invalid="ignore", divide="ignore"):
            corr = np.abs(np.corrcoef(X, rowvar=False))
        corr = np.nan_to_num(np.atleast_2d(corr))
        manter = np.ones(X.shape[1], dtype=bool)
        for i in range(X.shape[1]):
            if manter[i]:
                manter[i + 1:] &= corr[i, i + 1:] < self.limiar
        self.manter_ = manter
        return self

    def transform(self, X):
        check_is_fitted(self, "manter_")
        X_validado = validate_data(self, X, reset=False)
        if isinstance(X, pd.DataFrame):
            return X.iloc[:, self.manter_]
        return X_validado[:, self.manter_]

    def get_feature_names_out(self, input_features=None):
        check_is_fitted(self, "manter_")
        nomes = _check_feature_names_in(self, input_features)
        return np.asarray(nomes)[self.manter_]


class FiltroPrevalencia(TransformerMixin, BaseEstimator):
    """Remove gêneros raros e pouco abundantes (critério de Zhuang et al., usado na v2).

    Um gênero é removido quando atende **aos dois** critérios ao mesmo tempo:
    abundância relativa média < ``limiar_abundancia`` (0,0002 = 0,02%) e
    prevalência (fração de participantes com valor > 0) < ``limiar_prevalencia``
    (0,20 = 20%). Os critérios são calculados só nos dados do ``fit`` (o treino).
    Recebe abundâncias relativas (antes da CLR).
    """

    def __init__(self, limiar_abundancia: float = 0.0002, limiar_prevalencia: float = 0.20):
        self.limiar_abundancia = limiar_abundancia
        self.limiar_prevalencia = limiar_prevalencia

    def fit(self, X, y=None):
        X = validate_data(self, X, reset=True)
        media = X.mean(axis=0)
        prevalencia = (X > 0).mean(axis=0)
        remover = (media < self.limiar_abundancia) & (prevalencia < self.limiar_prevalencia)
        self.manter_ = ~remover
        return self

    def transform(self, X):
        check_is_fitted(self, "manter_")
        X_validado = validate_data(self, X, reset=False)
        if isinstance(X, pd.DataFrame):
            return X.iloc[:, self.manter_]
        return X_validado[:, self.manter_]

    def get_feature_names_out(self, input_features=None):
        check_is_fitted(self, "manter_")
        nomes = _check_feature_names_in(self, input_features)
        return np.asarray(nomes)[self.manter_]
