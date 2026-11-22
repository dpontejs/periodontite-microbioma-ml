# Classificação periodontal a partir do microbioma oral

Projeto 2 da disciplina **IMD0611 — Aprendizado de Máquina em Bioinformática** (IMD/UFRN, 2026).
Autores: Diego Medeiros e Renato Carvalho.

**Pergunta:** a composição do microbioma oral permite distinguir pessoas com e sem periodontite?

**Dados:** NHANES 2009–2012, do CDC (EUA). São usados o microbioma oral de amostras de enxágue
bucal (16S rRNA, DADA2, SILVA v123) e o exame periodontal completo de cada participante, além de
dados demográficos e de saúde. A condição periodontal segue os critérios de vigilância CDC/AAP.

## Principais resultados

Média ± desvio padrão em 10 divisões treino/teste (`periodontite_v3_conjunta.ipynb`):

| Modelo | Atributos | AUC |
|---|---|---|
| C | só covariáveis (idade, sexo, renda, saúde geral…) | 0,697 ± 0,009 |
| A | só gêneros do microbioma | 0,789 ± 0,012 |
| **B** | **gêneros + covariáveis** | **0,834 ± 0,010** |

O microbioma sozinho já supera as covariáveis, e somar os dois dá o melhor modelo: o microbioma
acrescenta +0,137 de AUC às covariáveis, e as covariáveis acrescentam +0,045 ao microbioma. Os
gêneros mais importantes incluem *Treponema*, *Desulfobulbus*, *Porphyromonas*, *Filifactor* e
*Tannerella*, conhecidos na literatura sobre periodontite.

---

## Sumário

- [Principais resultados](#principais-resultados)
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
| `periodontite_v3_conjunta.ipynb` | **A análise principal (versão conjunta).** É aqui que se trabalha. |
| `periodontite_v2_renato.ipynb` | A versão v2 do Renato, mantida para referência e comparação. |
| `baixar_dados.py` | Baixa os dados do site do CDC para a pasta `datasets/`. O notebook chama ele sozinho. |
| `microbioma.py` | A transformação CLR (mesma da aula de metagenômica), usada pelo notebook e pelo modelo final. |
| `resultados.py` | Funções para salvar o modelo final na pasta `resultados/`. |
| `resultados/` | Modelo, métricas e figuras salvos pelo notebook. É o que a demonstração mostra. |
| `app.py` | A demonstração interativa (uma página web feita com Gradio). |
| `images/` | Imagens usadas no notebook. |
| `pyproject.toml`, `uv.lock` | Lista das bibliotecas e das versões exatas usadas. |
| `requirements.txt` | A mesma lista, num formato que o Colab entende. **Não edite à mão** (veja "Adicionar uma biblioteca"). |
| `tests/` | Testes automáticos dos arquivos `.py`. |

A pasta `datasets/` **não** fica no repositório: ela é recriada baixando os dados do CDC.

---

## Jeito 1: rodar no Google Colab (sem instalar nada)

1. **Abra o notebook no Colab** pelo link direto (precisa estar logado numa conta Google):
   <https://colab.research.google.com/github/dpontejs/periodontite-microbioma-ml/blob/main/periodontite_v3_conjunta.ipynb>
2. **Salve uma cópia sua** (menu **Arquivo → Salvar uma cópia no Drive**). A cópia abre numa
   **aba nova**, com o nome "Cópia de periodontite_v3_conjunta.ipynb": feche a aba antiga e continue na
   nova. Assim suas alterações ficam guardadas no seu Google Drive.
3. **Confira o endereço.** Na primeira célula de código (seção **"0. Preparação do ambiente"**),
   a linha `URL_REPOSITORIO = "..."` já vem com o endereço do repositório. Não precisa mudar nada.
4. **Rode essa célula** (botão ▶ à esquerda dela, ou `Shift + Enter`). Se aparecer o aviso
   *"Este notebook não foi criado pelo Google"*, clique em **Executar mesmo assim**: ele aparece
   para qualquer notebook aberto do GitHub. Na primeira vez a célula:
   - baixa os arquivos do projeto;
   - instala as bibliotecas nas versões certas;
   - **reinicia a sessão sozinha.** Aparece um aviso dizendo que a sessão travou ou foi
     reiniciada. Isso é esperado.
5. **Rode a mesma célula de novo** depois que o Colab reconectar. Agora ela pula a instalação e
   baixa os dados do NHANES (uns 130 MB, cerca de 1 minuto).
6. Depois é só rodar as outras células em ordem. O menu **Ambiente de execução → Executar tudo**
   também funciona.

> **Tempo de execução.** O notebook inteiro leva cerca de 30 a 60 minutos no Colab gratuito. A
> parte mais demorada é a seção 9 (ajuste de hiperparâmetros nas 10 divisões treino/teste). Deixe
> a aba do Colab aberta enquanto roda.

> **Para abrir a v2 do Renato** no Colab, use o mesmo caminho com o nome do outro notebook:
> <https://colab.research.google.com/github/dpontejs/periodontite-microbioma-ml/blob/main/periodontite_v2_renato.ipynb>

> Se você fechar o Colab e voltar outro dia, a máquina dele é nova: abra a sua cópia no Drive e
> repita a partir do passo 4.

> **Suas alterações no Colab ficam só na sua cópia do Drive**, e não chegam ao GitHub sozinhas.
> Para enviá-las ao repositório, use **Arquivo → Salvar uma cópia no GitHub** (sua conta precisa
> ser colaboradora do repositório) ou baixe o `.ipynb` (**Arquivo → Fazer download → .ipynb**),
> coloque-o na pasta do projeto no seu computador e faça o commit como em "Trabalhando com o git".

### Onde fica o repositório

- **Código (GitHub):** <https://github.com/dpontejs/periodontite-microbioma-ml>. É esse
  endereço que se usa no `git clone` e no `URL_REPOSITORIO` do notebook.
- **Demonstração:** não fica hospedada na internet; ela abre no seu computador ou dentro do
  Colab (veja "A demonstração (app)").

---

## Jeito 2: rodar no seu computador

Você só precisa instalar duas ferramentas: o **git**, que baixa o projeto e guarda o histórico, e o
**uv**, que instala o Python e as bibliotecas certas. Não é preciso instalar o Python separado.

Funciona em **Windows, macOS e Linux**, com os mesmos comandos:

- **Windows:** o "terminal" é o **PowerShell**. Para abrir, aperte a tecla Windows, digite
  `PowerShell` e aperte Enter. Todos os comandos deste README funcionam nele do jeito que estão
  escritos (`cd`, `git`, `uv run ...`).
- **macOS:** use o app **Terminal**.
- **Linux:** use o terminal da sua distribuição.

Para entrar numa pasta, use `cd` seguido do caminho. Por exemplo, `cd Documents` entra na pasta
Documentos. O projeto vai ser baixado dentro da pasta onde o terminal estiver quando você rodar
o `git clone` do Passo 2.

### Passo 1: instalar as ferramentas (só na primeira vez)

- **git:** baixe em <https://git-scm.com/downloads> e instale com as opções padrão. No Windows,
  o instalador tem várias telas: pode clicar em **Next** em todas e, no fim, em **Install**.
  Depois de instalar, diga ao git o seu nome e e-mail (só uma vez; use o e-mail da sua conta do
  GitHub), senão o primeiro `git commit` dá erro:
  ```bash
  git config --global user.name "Seu Nome"
  git config --global user.email "seu-email@exemplo.com"
  ```
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

Escolha uma pasta para guardar o projeto e entre nela com `cd`. **No Windows, evite a pasta
Documentos e a Área de Trabalho**, que muitas vezes são sincronizadas pelo OneDrive: o projeto
cria milhares de arquivos (ambiente e dados) que deixam a sincronização lenta e podem travar.
Uma opção simples no Windows:

```powershell
mkdir C:\projetos
cd C:\projetos
```

(No macOS ou Linux, pode usar `cd ~`, que é a sua pasta pessoal.) Depois baixe o projeto e entre
na pasta dele:

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

Abre uma aba no navegador. Clique em `periodontite_v3_conjunta.ipynb` e rode as células em ordem.

Nos outros dias, para voltar a trabalhar: abra o terminal, entre na pasta do projeto usando o
caminho completo (no Windows, `cd C:\projetos\periodontite-microbioma-ml` se seguiu o exemplo
do Passo 2) e rode `uv run jupyter lab` de novo. Atalho no Windows: no Explorador de Arquivos,
clique com o botão direito na pasta `periodontite-microbioma-ml` e escolha **Abrir no Terminal**.

> **Sempre use `uv run` na frente dos comandos.** É ele que garante que o Python usado é o do
> projeto, com as bibliotecas certas. Se usar o VS Code, escolha o interpretador `.venv` como kernel.

---

## A demonstração (app)

A demonstração é uma página com três abas:

- **Predição:** escolhe-se um participante do conjunto de teste e aparecem duas probabilidades de
  periodontite, a do modelo principal (Modelo B, microbioma + covariáveis) e a do modelo só com o
  microbioma (Modelo A), além do diagnóstico real e dos gêneros bacterianos mais abundantes
  daquela pessoa.
- **Desempenho:** métricas e gráficos do modelo.
- **Sobre:** a pergunta, os dados e como usar a página.

O app só lê a pasta `resultados/`, que já vem no repositório: dá para abrir a demonstração logo
depois de baixar o projeto, sem rodar o notebook. Quando o notebook é executado até o fim, a
seção **"12.1 Salvar os resultados para a demonstração"** grava essa pasta de novo; se a análise
mudou, faça commit da pasta `resultados/` junto com o notebook.

Para abrir a demonstração no seu computador:

```bash
uv run python app.py
```

e acesse o endereço que aparecer no terminal (normalmente <http://127.0.0.1:7860>). Para parar,
aperte `Ctrl + C` no terminal. Se a pasta `resultados/` ainda não existir, a página mostra um aviso
em vez da demonstração.

Para abrir a demonstração **no Colab**:

1. rode o notebook até o fim (ou pelo menos a célula 0, já que a pasta `resultados/` vem pronta
   no repositório);
2. na seção **"12.2 Abrir a demonstração"**, troque `ABRIR_DEMO = False` por `ABRIR_DEMO = True`
   e rode a célula;
3. a demonstração aparece dentro do próprio notebook e, logo acima dela, um link público
   terminado em `.gradio.live`. Esse link abre a demonstração em qualquer navegador e funciona
   **por 72 horas** (ou até a sessão do Colab ser encerrada): dá para mandar ao professor ou usar
   na apresentação.

Para parar, clique no botão ■ da célula ou encerre a sessão do Colab.

---

## Trabalhando com o git

### Comandos do dia a dia

```bash
git status                        # o que mudou desde o último commit
git add periodontite_v3_conjunta.ipynb   # marca o arquivo para o próximo commit
git commit -m "feat: descreve o que foi feito"
git push                          # envia para o repositório online
git pull                          # traz o que os outros enviaram
```

Quem baixou o projeto com `git clone` já fica conectado ao GitHub, então `git push` e
`git pull` funcionam direto. Para enviar (`git push`), sua conta do GitHub precisa ter sido
adicionada como colaboradora do repositório. No primeiro `git push`, abre uma janela do
navegador pedindo para entrar na sua conta do GitHub; depois disso, não pede mais.

---

## Adicionar uma biblioteca

```bash
uv add nome-da-biblioteca
uv export --no-hashes --no-dev -o requirements.txt
```

O primeiro comando instala e registra a biblioteca no `pyproject.toml` e no `uv.lock`. O segundo
atualiza o `requirements.txt` usado pelo Colab. Faça commit dos três arquivos.

---

## Problemas comuns

| O que aparece | O que fazer |
|---|---|
| `ModuleNotFoundError: No module named ...` no notebook | O notebook está usando outro Python. Abra com `uv run jupyter lab` ou escolha o kernel `.venv`. No Colab, rode de novo a célula "0. Preparação do ambiente". |
| `Preencha URL_REPOSITORIO...` no Colab | O endereço do repositório foi apagado da primeira célula de código. Restaure a linha: `URL_REPOSITORIO = "https://github.com/dpontejs/periodontite-microbioma-ml.git"`. |
| `Não foi possível baixar ...` | Sem internet ou site do CDC fora do ar. Espere um pouco e rode de novo. Só os arquivos que faltam são baixados. |
| `... não confere com o esperado` | O arquivo no site do CDC mudou ou veio corrompido. Rode de novo. Se persistir, avise no grupo. |
| A página do app diz "Resultados ainda não disponíveis" | A pasta `resultados/` sumiu ou está incompleta. Recupere a versão do repositório com `git checkout resultados/`, ou rode o notebook até a seção "12.1 Salvar os resultados para a demonstração". |
| `uv: command not found` | Feche e abra o terminal depois de instalar o uv. Se continuar, refaça o Passo 1. |
| No Windows: `uv : O termo 'uv' não é reconhecido...` (ou `git` não reconhecido) | Mesmo caso acima: feche e abra o PowerShell depois de instalar. Se continuar, reinicie o computador, que atualiza a lista de programas instalados. |
| No Windows: aviso sobre *política de execução* ao instalar o uv | Use exatamente o comando do Passo 1, que já inclui `-ExecutionPolicy ByPass`. |

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
`38 passed`. O número pode crescer conforme novos testes forem adicionados. O importante é
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

(No Windows, o caminho aparece com barras invertidas, por exemplo
`C:\projetos\periodontite-microbioma-ml\datasets`. Está certo.)

Rodando de novo, todas as linhas devem ser `ok`, sem baixar nada. Isso confirma que os 17
arquivos conferem com a assinatura (SHA-256) dos arquivos originais do CDC.

**Se der erro:** veja a tabela "Problemas comuns" (linhas sobre download).

### Etapa 4: o notebook roda do começo ao fim?

Abra com `uv run jupyter lab`, clique em `periodontite_v3_conjunta.ipynb` e use o menu
**Run → Run All Cells**. Ou rode tudo direto no terminal, sem abrir o navegador:

```bash
uv run jupyter nbconvert --to notebook --execute --inplace periodontite_v3_conjunta.ipynb
```

Esse comando executa todas as células e salva os resultados dentro do próprio notebook. Leva
uns 10 a 30 minutos, dependendo do computador (a parte mais demorada é o ajuste de
hiperparâmetros da seção 9, nas 10 divisões treino/teste).

**Deve aparecer:** nenhuma célula com erro (no Jupyter, erros aparecem em vermelho; no comando
acima, o terminal mostraria `CellExecutionError`). Confira também alguns números-chave, que
devem ser iguais (pelo menos nas duas primeiras casas decimais) em qualquer computador, porque
as sementes aleatórias são fixas:

| Onde | O que conferir | Valor esperado |
|---|---|---|
| Seção 6.1 | participantes sem / com periodontite | 2984 / 2892 |
| Seção 6.3 | gêneros mantidos pelo filtro de prevalência em cada treino | 106 a 112 |
| Seção 6.3 | AUC do Modelo A (XGBoost padrão) | 0,772 ± 0,010 |
| Seção 6.3 | AUC do DummyClassifier | 0,500 |
| Seção 7 | classificador padrão com maior AUC (Modelo A) | Regressão logística (0,777) |
| Seção 10 | AUC do Modelo A ajustado | 0,789 ± 0,012 |
| Seção 10 | AUC do Modelo B ajustado | 0,834 ± 0,010 |
| Seção 10 | AUC do Modelo C (só covariáveis) | 0,697 ± 0,009 |
| Seção 10 | o que o microbioma acrescenta (B − C) | +0,137, positivo em 10 de 10 sementes |
| Seção 10.1 | AUC do Modelo B na semente 42 | 0,838 |

> Esses valores valem para a versão atual de `periodontite_v3_conjunta.ipynb`. Se alguém mudar a análise (filtros,
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

Confira as três abas:
  - **Predição:** ao escolher outro participante na lista, as duas probabilidades, a condição real
    e a tabela de gêneros mudam;
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
uv run jupyter nbconvert --to notebook --execute --inplace periodontite_v3_conjunta.ipynb
uv run python app.py
```
