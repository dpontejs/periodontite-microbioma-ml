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
periodontite?

**Dados:** NHANES 2009–2012 (CDC, EUA). Amostras de enxágue bucal sequenciadas
(gene 16S rRNA, região V4, processadas com DADA2 e classificadas com SILVA v123),
cruzadas com o exame periodontal completo de cada participante. A condição
periodontal segue os critérios de vigilância CDC/AAP, agrupados em dois rótulos:
*Sem periodontite* e *Periodontite* (leve, moderada ou grave).

**Como usar esta página**

- **Predição:** escolha um participante do conjunto de teste (dados que o modelo
  não viu no treino). Aparecem a probabilidade estimada de cada classe, o rótulo
  real e os gêneros bacterianos mais abundantes na amostra.
- **Desempenho:** métricas e gráficos do modelo no conjunto de teste.

O código completo da análise está no notebook `projeto_2_colab.ipynb`, no mesmo
repositório desta página.

*IMD0611 — Aprendizado de Máquina em Bioinformática (IMD/UFRN), 2026.
Diego Medeiros e Renato Carvalho.*
"""


def _atributos_do_modelo(res: Resultados) -> list[str]:
    nomes = getattr(res.modelo, "feature_names_in_", None)
    if nomes is not None:
        return list(nomes)
    return [c for c in res.teste.columns if c != "rotulo"]


def prever(res: Resultados, seqn: int) -> tuple[dict[str, float], str, pd.DataFrame]:
    """Probabilidades por classe, rótulo real e os 10 atributos mais abundantes."""
    seqn = int(seqn)
    if seqn not in res.teste.index:
        raise gr.Error(f"O participante {seqn} não está no conjunto de teste.")

    linha = res.teste.loc[[seqn]]
    probabilidades = res.modelo.predict_proba(linha[_atributos_do_modelo(res)])[0]
    por_classe = {CLASSES[int(c)]: float(p) for c, p in zip(res.modelo.classes_, probabilidades)}

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
            with gr.Row():
                probabilidades = gr.Label(label="Probabilidade estimada pelo modelo")
                rotulo_real = gr.Textbox(label="Condição real (exame periodontal)")
            tabela = gr.Dataframe(label="Gêneros mais abundantes nesta amostra")

            def _atualizar(seqn):
                return prever(res, seqn)

            saidas = [probabilidades, rotulo_real, tabela]
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
