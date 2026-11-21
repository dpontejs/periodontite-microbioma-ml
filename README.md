---
title: Microbioma oral e periodontite
emoji: 🦷
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 6.32.0
python_version: "3.12"
app_file: app.py
pinned: false
---

# Classificação periodontal a partir do microbioma oral

Projeto 2 da disciplina **IMD0611 — Aprendizado de Máquina em Bioinformática** (IMD/UFRN, 2026).
Autores: Diego Medeiros e Renato Carvalho.

**Pergunta:** a composição do microbioma oral permite distinguir pessoas com e sem periodontite?

**Dados:** NHANES 2009–2012, do CDC (EUA). São usados o microbioma oral de amostras de enxágue
bucal (16S rRNA, DADA2, SILVA v123) e o exame periodontal completo de cada participante, além de
dados demográficos e de saúde. A condição periodontal segue os critérios de vigilância CDC/AAP.

---

## O que tem nesta pasta

| Arquivo / pasta | Para que serve |
|---|---|
| `projeto_2_colab.ipynb` | **O notebook com toda a análise.** É aqui que se trabalha. |
| `baixar_dados.py` | Baixa os dados do site do CDC para a pasta `datasets/`. O notebook chama ele sozinho. |
| `resultados.py` | Funções para salvar o modelo final na pasta `resultados/`. |
| `resultados/` | Modelo, métricas e figuras salvos pelo notebook. É o que a demonstração mostra. |
| `app.py` | A demonstração interativa (uma página web feita com Gradio). |
| `images/` | Imagens usadas no notebook. |
| `pyproject.toml`, `uv.lock` | Lista das bibliotecas e das versões exatas usadas. |
| `requirements.txt` | A mesma lista, num formato que o Colab e o Hugging Face entendem. **Não edite à mão** (veja "Adicionar uma biblioteca"). |
| `tests/` | Testes automáticos dos arquivos `.py`. |

A pasta `datasets/` **não** fica no repositório: ela é recriada baixando os dados do CDC.

---

## Jeito 1: rodar no Google Colab (sem instalar nada)

1. **Pegue o notebook.** Baixe o arquivo `projeto_2_colab.ipynb` da página do repositório
   (link na seção "Onde fica o repositório", logo abaixo).
2. **Abra no Colab.** Entre em <https://colab.research.google.com>, menu
   **Arquivo → Fazer upload de notebook**, e escolha o arquivo baixado.
3. **Confira o endereço.** Na primeira célula de código (seção **"0. Preparação do ambiente"**),
   a linha `URL_REPOSITORIO = "..."` deve ter o endereço do repositório entre as aspas. Se estiver
   vazia (`""`), cole o endereço.
4. **Rode essa célula** (botão ▶ à esquerda dela, ou `Shift + Enter`). Na primeira vez ela:
   - baixa os arquivos do projeto;
   - instala as bibliotecas nas versões certas;
   - **reinicia a sessão sozinha.** Aparece um aviso dizendo que a sessão travou ou foi
     reiniciada. Isso é esperado.
5. **Rode a mesma célula de novo** depois que o Colab reconectar. Agora ela pula a instalação e
   baixa os dados do NHANES (uns 130 MB, cerca de 1 minuto).
6. Depois é só rodar as outras células em ordem. O menu **Ambiente de execução → Executar tudo**
   também funciona.

> Se você fechar o Colab e voltar outro dia, a máquina dele é nova: repita a partir do passo 4.

### Onde fica o repositório

O repositório ainda vai ser publicado no Hugging Face. Quando estiver no ar, o endereço será
algo como `https://huggingface.co/spaces/<usuario>/<nome>` e vai aparecer aqui. Esse mesmo
endereço serve para o `git clone`, para o `URL_REPOSITORIO` do notebook e para abrir a
demonstração no navegador.

---

## Jeito 2: rodar no seu computador

Você só precisa instalar duas ferramentas: o **git**, que baixa o projeto e guarda o histórico, e o
**uv**, que instala o Python e as bibliotecas certas. Não é preciso instalar o Python separado.

### Passo 1: instalar as ferramentas (só na primeira vez)

- **git:** baixe em <https://git-scm.com/downloads> e instale com as opções padrão.
- **uv:**
  - Windows (no PowerShell):
    ```powershell
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```
  - Linux ou macOS (no terminal):
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
  Feche e abra o terminal de novo depois de instalar.

### Passo 2: baixar o projeto (só na primeira vez)

```bash
git clone <URL-DO-REPOSITORIO> periodontite-microbioma-ml
cd periodontite-microbioma-ml
```

### Passo 3: criar o ambiente (só na primeira vez, ou quando a lista de bibliotecas mudar)

```bash
uv sync
```

Isso cria uma pasta `.venv/` com o Python e todas as bibliotecas, nas mesmas versões para todo mundo.

### Passo 4: baixar os dados

```bash
uv run python baixar_dados.py
```

Os arquivos vão para `datasets/`. Pode rodar de novo quando quiser, porque arquivos já baixados e
íntegros são pulados. (A célula "0. Preparação do ambiente" do notebook faz a mesma coisa.)

### Passo 5: abrir o notebook

```bash
uv run jupyter lab
```

Abre uma aba no navegador. Clique em `projeto_2_colab.ipynb` e rode as células em ordem.

Nos outros dias, para voltar a trabalhar: abra o terminal, entre na pasta do projeto com
`cd periodontite-microbioma-ml` (ou o caminho onde você a clonou) e rode `uv run jupyter lab` de novo.

> **Sempre use `uv run` na frente dos comandos.** É ele que garante que o Python usado é o do
> projeto, com as bibliotecas certas. Se usar o VS Code, escolha o interpretador `.venv` como kernel.

---

## A demonstração (app)

A demonstração é uma página com três abas:

- **Predição:** escolhe-se um participante do conjunto de teste e o modelo mostra a probabilidade
  de periodontite, o diagnóstico real e os gêneros bacterianos mais abundantes daquela pessoa.
- **Desempenho:** métricas e gráficos do modelo.
- **Sobre:** a pergunta, os dados e como usar a página.

O app só lê a pasta `resultados/`. Para gerar essa pasta, rode o notebook até o final: a última
seção, **"Salvar os resultados para a demonstração"**, chama `salvar_resultados(...)`.

Para abrir a demonstração no seu computador:

```bash
uv run python app.py
```

e acesse o endereço que aparecer no terminal (normalmente <http://127.0.0.1:7860>). Para parar,
aperte `Ctrl + C` no terminal. Se a pasta `resultados/` ainda não existir, a página mostra um aviso
em vez da demonstração.

A versão publicada fica no Hugging Face Spaces. É este mesmo repositório: o Hugging Face lê o
cabeçalho no topo deste README e roda o `app.py`.

---

## Trabalhando com o git

### As duas linhas do projeto

Combinamos de seguir caminhos separados a partir da versão do notebook de **11/nov** e juntar
depois. No git isso vira duas "linhas" (branches):

| Branch | O que tem |
|---|---|
| `main` | Linha do Diego, que parte da versão de 11/nov. |
| `v2-colega` | Linha do Renato (a versão v2, editada no Colab/Drive). |

As duas começam do mesmo commit, então na hora de juntar o git consegue mostrar exatamente o que
cada um mudou desde 11/nov.

**Para registrar uma versão nova do notebook do Renato** (baixada do Drive):

```bash
git switch v2-colega
# copie o arquivo baixado por cima de projeto_2_colab.ipynb (mesmo nome)
git add projeto_2_colab.ipynb
git commit -m "chore: atualiza versão do colega"
git switch main
```

### Comandos do dia a dia

```bash
git status                        # o que mudou desde o último commit
git add projeto_2_colab.ipynb     # marca o arquivo para o próximo commit
git commit -m "feat: descreve o que foi feito"
git push                          # envia para o repositório online
git pull                          # traz o que os outros enviaram
```

`git push` e `git pull` só funcionam depois que o repositório estiver publicado (veja "Onde fica
o repositório"). Quem clonou com `git clone` já fica conectado automaticamente.

---

## Adicionar uma biblioteca

```bash
uv add nome-da-biblioteca
uv export --no-hashes --no-dev -o requirements.txt
```

O primeiro comando instala e registra a biblioteca no `pyproject.toml` e no `uv.lock`. O segundo
atualiza o `requirements.txt` usado pelo Colab e pelo Hugging Face. Faça commit dos três arquivos.

---

## Problemas comuns

| O que aparece | O que fazer |
|---|---|
| `ModuleNotFoundError: No module named ...` no notebook | O notebook está usando outro Python. Abra com `uv run jupyter lab` ou escolha o kernel `.venv`. No Colab, rode de novo a célula "0. Preparação do ambiente". |
| `Preencha URL_REPOSITORIO...` no Colab | Coloque o endereço do repositório na linha `URL_REPOSITORIO = ""` da primeira célula de código. |
| `Não foi possível baixar ...` | Sem internet ou site do CDC fora do ar. Espere um pouco e rode de novo. Só os arquivos que faltam são baixados. |
| `... não confere com o esperado` | O arquivo no site do CDC mudou ou veio corrompido. Rode de novo. Se persistir, avise no grupo. |
| A página do app diz "Resultados ainda não disponíveis" | Falta gerar a pasta `resultados/`: rode o notebook até a seção "Salvar os resultados para a demonstração". |
| `uv: command not found` | Feche e abra o terminal depois de instalar o uv. Se continuar, refaça o Passo 1. |

---

## Testes automáticos

Para conferir que os arquivos `.py` continuam funcionando depois de uma mudança:

```bash
uv run pytest
```

Todos devem aparecer como `passed`.
