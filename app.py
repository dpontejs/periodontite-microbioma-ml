"""Demonstração interativa do modelo de classificação periodontal.

Rodar localmente, a partir da pasta do projeto:

    uv run python app.py

e abrir o endereço que aparecer no terminal (normalmente http://127.0.0.1:7860).
O app só lê a pasta ``resultados/``, gerada pelo notebook.
"""

from __future__ import annotations

import os
from pathlib import Path

import gradio as gr
import pandas as pd

from resultados import CLASSES, Resultados, carregar_resultados

SOBRE = """
## Microbioma oral e periodontite

**Pergunta:** a composição do microbioma oral permite distinguir pessoas com e sem
periodontite? E quanto as características do participante acrescentam a essa informação?

**Dados:** NHANES 2009–2012 (CDC, EUA). Amostras de enxágue bucal sequenciadas
(gene 16S rRNA, região V4, processadas com DADA2 e classificadas com SILVA v123),
cruzadas com o exame periodontal completo de cada participante e com dados
demográficos e de saúde. A condição periodontal segue os critérios de vigilância
CDC/AAP, agrupados em dois rótulos: *Sem periodontite* e *Periodontite* (leve,
moderada ou grave).

**Modelos**

- **Modelo principal:** gêneros do microbioma + características do participante
  (idade, sexo, raça/etnia, escolaridade, estado civil, renda, álcool, atividade
  física, hipertensão, diabetes, doença cardiovascular e câncer).
- **Só microbioma:** apenas os gêneros. Comparar as duas probabilidades mostra quanto
  da previsão vem do microbioma.

**Como usar esta página**

- **Predição:** escolha um participante do conjunto de teste (dados que os modelos
  não viram no treino). Aparecem as probabilidades estimadas pelos dois modelos, a
  condição real e os gêneros bacterianos mais abundantes na amostra.
- **Desempenho:** métricas (média de 10 divisões treino/teste) e gráficos.

O código completo da análise está no notebook `periodontite_v3_conjunta.ipynb`, no
repositório https://github.com/dpontejs/periodontite-microbioma-ml.

*IMD0611 — Aprendizado de Máquina em Bioinformática (IMD/UFRN), 2026.
Diego Medeiros e Renato Carvalho.*
"""


def _atributos_do_modelo(modelo, res: Resultados) -> list[str]:
    nomes = getattr(modelo, "feature_names_in_", None)
    if nomes is not None:
        return list(nomes)
    return [c for c in res.teste.columns if c != "rotulo"]


def _probabilidades(modelo, res: Resultados, linha: pd.DataFrame) -> dict[str, float]:
    probabilidades = modelo.predict_proba(linha[_atributos_do_modelo(modelo, res)])[0]
    return {CLASSES[int(c)]: float(p) for c, p in zip(modelo.classes_, probabilidades)}


def _linha(res: Resultados, seqn: int) -> pd.DataFrame:
    seqn = int(seqn)
    if seqn not in res.teste.index:
        raise gr.Error(f"O participante {seqn} não está no conjunto de teste.")
    return res.teste.loc[[seqn]]


def prever(res: Resultados, seqn: int) -> tuple[dict[str, float], str, pd.DataFrame]:
    """Probabilidades por classe, rótulo real e os 10 atributos mais abundantes."""
    linha = _linha(res, seqn)
    por_classe = _probabilidades(res.modelo, res, linha)

    rotulo_real = CLASSES[int(linha["rotulo"].iloc[0])]

    taxons = [c for c in linha.columns if c in res.rotulos_atributos]
    abundancias = linha[taxons].iloc[0].sort_values(ascending=False).head(10)
    tabela = pd.DataFrame(
        {
            "atributo": [res.rotulos_atributos[c] for c in abundancias.index],
            "abundancia": abundancias.to_numpy(),
        }
    )
    return por_classe, rotulo_real, tabela


def prever_taxons(res: Resultados, seqn: int) -> dict[str, float] | None:
    """Probabilidades do modelo só com o microbioma, se ele existir."""
    if res.modelo_taxons is None:
        return None
    return _probabilidades(res.modelo_taxons, res, _linha(res, seqn))


def tabela_metricas(res: Resultados) -> pd.DataFrame:
    return pd.DataFrame({"metrica": list(res.metricas), "valor": list(res.metricas.values())})


def criar_app(res: Resultados) -> gr.Blocks:
    participantes = [int(s) for s in res.teste.index]

    with gr.Blocks(title="Microbioma oral e periodontite") as demo:
        gr.Markdown("# Classificação periodontal a partir do microbioma oral")
        with gr.Tab("Predição"):
            escolha = gr.Dropdown(
                participantes, value=participantes[0], label="Participante (SEQN)"
            )
            tem_taxons = res.modelo_taxons is not None
            with gr.Row():
                probabilidades = gr.Label(
                    label="Probabilidade — microbioma + dados do participante (modelo principal)"
                    if tem_taxons else "Probabilidade estimada pelo modelo"
                )
                probabilidades_taxons = gr.Label(
                    label="Probabilidade — só microbioma", visible=tem_taxons
                )
            rotulo_real = gr.Textbox(label="Condição real (exame periodontal)")
            tabela = gr.Dataframe(label="Gêneros mais abundantes nesta amostra")

            def _atualizar(seqn):
                por_classe, real, generos = prever(res, seqn)
                return por_classe, prever_taxons(res, seqn), real, generos

            saidas = [probabilidades, probabilidades_taxons, rotulo_real, tabela]
            escolha.change(_atualizar, escolha, saidas)
            demo.load(_atualizar, escolha, saidas)
        with gr.Tab("Desempenho"):
            gr.Dataframe(tabela_metricas(res), label="Métricas no conjunto de teste")
            gr.Gallery([str(p) for p in res.figuras], label="Figuras", columns=2)
        with gr.Tab("Sobre"):
            gr.Markdown(SOBRE)
    return demo


def criar_app_ou_aviso() -> gr.Blocks:
    """Cria o app; se ainda não houver resultados, mostra só um aviso."""
    pasta = Path(os.environ.get("RESULTADOS_DIR", "resultados"))
    try:
        res = carregar_resultados(pasta)
    except FileNotFoundError as erro:
        with gr.Blocks(title="Microbioma oral e periodontite") as aviso:
            gr.Markdown(f"## Resultados ainda não disponíveis\n\n{erro}")
        return aviso
    return criar_app(res)


if __name__ == "__main__":
    criar_app_ou_aviso().launch()
