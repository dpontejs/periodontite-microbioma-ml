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

## Sumário

- [O que tem nesta pasta](#o-que-tem-nesta-pasta)
- [Jeito 1: rodar no Google Colab](#jeito-1-rodar-no-google-colab-sem-instalar-nada)
- [Jeito 2: rodar no seu computador](#jeito-2-rodar-no-seu-computador)
- [A demonstração (app)](#a-demonstração-app)
- [Trabalhando com o git](#trabalhando-com-o-git)
- [Adicionar uma biblioteca](#adicionar-uma-biblioteca)
- [Problemas comuns](#problemas-comuns)
- [Como conferir que tudo funciona](#como-conferir-que-tudo-funciona)

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

1. **Abra o notebook no Colab.** Entre em <https://colab.research.google.com>, menu
   **Arquivo → Abrir notebook → aba GitHub**, cole `dpontejs/periodontite-microbioma-ml` na
   busca e clique em `projeto_2_colab.ipynb`.
2. **Salve uma cópia sua** (menu **Arquivo → Salvar uma cópia no Drive**). Assim suas alterações
   ficam guardadas no seu Google Drive.
3. **Confira o endereço.** Na primeira célula de código (seção **"0. Preparação do ambiente"**),
   a linha `URL_REPOSITORIO = "..."` já vem com o endereço do repositório. Não precisa mudar nada.
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

- **Código (GitHub):** <https://github.com/dpontejs/periodontite-microbioma-ml>. É esse
  endereço que se usa no `git clone` e no `URL_REPOSITORIO` do notebook.
- **Demonstração (Hugging Face Spaces):** vai ser publicada quando o modelo final estiver pronto;
  o link vai aparecer aqui.

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
git clone https://github.com/dpontejs/periodontite-microbioma-ml.git
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

A versão publicada vai ficar no Hugging Face Spaces, que recebe uma cópia deste repositório: o
Hugging Face lê o cabeçalho no topo deste README e roda o `app.py`.

---

## Trabalhando com o git

### Comandos do dia a dia

```bash
git status                        # o que mudou desde o último commit
git add projeto_2_colab.ipynb     # marca o arquivo para o próximo commit
git commit -m "feat: descreve o que foi feito"
git push                          # envia para o repositório online
git pull                          # traz o que os outros enviaram
```

Quem baixou o projeto com `git clone` já fica conectado ao GitHub, então `git push` e
`git pull` funcionam direto. Para enviar (`git push`), sua conta do GitHub precisa ter sido
adicionada como colaboradora do repositório.

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

## Como conferir que tudo funciona

Use este roteiro depois de baixar o projeto pela primeira vez, ao trocar de computador, ou antes
de uma apresentação. Cada etapa diz **o comando**, **o que deve aparecer** e **o que fazer se
não aparecer**. Todos os comandos são rodados no terminal, **dentro da pasta do projeto**
(`cd periodontite-microbioma-ml`).

### Etapa 1: o ambiente está instalado?

```bash
uv sync
```

**Deve aparecer:** algumas linhas terminando sem a palavra `error`. Na primeira vez, ele baixa
as bibliotecas e pode levar alguns minutos; nas próximas, termina em segundos.

**Se der erro:** confira se o uv está instalado (`uv --version` deve mostrar um número de
versão). Se não estiver, volte ao "Passo 1" do Jeito 2.

### Etapa 2: os testes automáticos passam?

Os testes conferem, sozinhos, as partes do projeto que não são o notebook: o download dos
dados, o formato de `resultados/` e a demonstração. Eles não usam a internet nem os dados reais,
então rodam em poucos segundos.

```bash
uv run pytest
```

**Deve aparecer:** uma linha de pontos (cada ponto é um teste que passou) e, no final, algo como
`20 passed`. O número pode crescer conforme novos testes forem adicionados. O importante é
**não aparecer `failed` nem `error`**.

**Se aparecer `failed`:** a saída mostra o nome do teste e o motivo. Normalmente é algo que foi
alterado em `baixar_dados.py`, `resultados.py` ou `app.py`. Desfaça a última mudança nesses
arquivos (`git diff` mostra o que mudou) ou peça ajuda no grupo.

### Etapa 3: os dados baixam e estão íntegros?

```bash
uv run python baixar_dados.py
```

**Deve aparecer:** uma linha por arquivo, `baixando ...` na primeira vez ou `ok` quando o
arquivo já existe e está íntegro, e no final:

```
Pronto: 17 arquivos em .../periodontite-microbioma-ml/datasets
```

Rodando de novo, todas as linhas devem ser `ok`, sem baixar nada. Isso confirma que os 17
arquivos conferem com a assinatura (SHA-256) dos arquivos originais do CDC.

**Se der erro:** veja a tabela "Problemas comuns" (linhas sobre download).

### Etapa 4: o notebook roda do começo ao fim?

Abra com `uv run jupyter lab`, clique em `projeto_2_colab.ipynb` e use o menu
**Run → Run All Cells**. Ou rode tudo direto no terminal, sem abrir o navegador:

```bash
uv run jupyter nbconvert --to notebook --execute --inplace projeto_2_colab.ipynb
```

Esse comando executa todas as células e salva os resultados dentro do próprio notebook. Leva
alguns minutos (a parte mais demorada é o treino dos modelos nas 10 divisões treino/teste).

**Deve aparecer:** nenhuma célula com erro (no Jupyter, erros aparecem em vermelho; no comando
acima, o terminal mostraria `CellExecutionError`). Confira também alguns números-chave, que
devem ser iguais (pelo menos nas duas primeiras casas decimais) em qualquer computador, porque
as sementes aleatórias são fixas:

| Onde | O que conferir | Valor esperado |
|---|---|---|
| Seção 4.3 | participantes sem / com periodontite | 2985 / 2892 |
| Seção 5.1 | dimensões da matriz CLR | (5877, 1349) |
| Seção 5.2 | AUC média do XGBoost | 0,777 ± 0,011 |
| Seção 5.2 | AUC do DummyClassifier | 0,500 |
| Seção 6 | modelo com maior AUC média | XGBoost |

> Esses valores valem para a versão atual do notebook. Se alguém mudar a análise (filtros,
> modelos, parâmetros), os números mudam junto; atualize esta tabela no mesmo commit.

**Se der erro:** leia a última linha da mensagem em vermelho. `ModuleNotFoundError` quase
sempre é o notebook usando o Python errado (veja "Problemas comuns"). `FileNotFoundError` com
nome de arquivo `.xpt` ou `.txt` indica que a Etapa 3 não foi feita.

### Etapa 5: a demonstração abre?

```bash
uv run python app.py
```

**Deve aparecer:** uma linha parecida com `* Running on local URL:  http://127.0.0.1:7860`. Abra esse endereço
no navegador.

- **Se o notebook ainda não salvou resultados** (a célula `salvar_resultados(...)` ainda está
  comentada), a página mostra só o aviso *"Resultados ainda não disponíveis"*. Isso é o esperado
  nesse momento, e já confirma que o app funciona.
- **Depois que existir a pasta `resultados/`**, confira as três abas:
  - **Predição:** ao escolher outro participante na lista, a probabilidade, a condição real e a
    tabela de gêneros mudam;
  - **Desempenho:** aparece a tabela de métricas e as figuras salvas;
  - **Sobre:** aparece o texto explicando o projeto.

Para fechar o app, volte ao terminal e aperte `Ctrl + C`.

### Etapa 6 (opcional): o fluxo do Colab funciona?

Siga o "Jeito 1" do começo deste README numa sessão nova do Colab. Deve acontecer exatamente
isto:

1. 1ª execução da célula "0. Preparação do ambiente": instala as bibliotecas e a sessão
   reinicia sozinha (aviso de sessão travada/reiniciada);
2. 2ª execução da mesma célula: aparecem as linhas `baixando ...` e `Pronto: 17 arquivos`;
3. **Ambiente de execução → Executar tudo**: o notebook roda até o fim sem erro, com os mesmos
   números da tabela da Etapa 4.

### Resumo rápido

Para quem já fez tudo uma vez e só quer conferir rapidamente:

```bash
cd periodontite-microbioma-ml
uv sync
uv run pytest
uv run python baixar_dados.py
uv run jupyter nbconvert --to notebook --execute --inplace projeto_2_colab.ipynb
uv run python app.py
```
