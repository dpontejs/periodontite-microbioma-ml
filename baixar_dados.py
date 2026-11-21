"""Baixa os dados do projeto (NHANES 2009–2012) direto do site do CDC.

Uso, a partir da pasta do projeto:

    uv run python baixar_dados.py

Os arquivos vão para a pasta ``datasets/``. Arquivos que já existem e estão
íntegros (conferidos pelo SHA-256) não são baixados de novo, então pode rodar
quantas vezes quiser.
"""

from __future__ import annotations

import hashlib
import http.client
import urllib.error
import urllib.request
from pathlib import Path

_BASE_XPT = "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/{ano}/DataFiles/{nome}"
_BASE_MICROBIOMA = "https://wwwn.cdc.gov/Nchs/Data/Nhanes/omp/{nome}"
_ANO_DO_CICLO = {"F": 2009, "G": 2011}  # F = 2009–2010, G = 2011–2012

_SHA256 = {
    "ALQ_F.xpt": "15a46b2310d5ba90e1488df5f84846d97468247b0aae6608407fa9bf2405d0d1",
    "ALQ_G.xpt": "5f06ba3506f9d69cedffa0380ad0cecbc15df2d6d9b7a3644ac3e2678aaac5e5",
    "BPQ_F.xpt": "e592c987f07002eb309a63dc7ebf6a7eaa83d740a4fd6ae69af15da40c65a21a",
    "BPQ_G.xpt": "39c5a0ee1d76e6f3df867c0057986a21f4a028038002c43214c5af8bdec83cae",
    "DEMO_F.xpt": "78c4d4a6e5eafa9da3bbb24a90d140fef5d8c0cda932a7ff8ee609288d4fae07",
    "DEMO_G.xpt": "eaf0525d1952626885af3e935415a1f66ad62c18698080e7354789c125af252d",
    "DIQ_F.xpt": "7e90371cbc98e77a9684eff32ffa0e4ee3e8fc04d97581a8773e19cb9fe901fa",
    "DIQ_G.xpt": "a9d5475e0cd66d6a7bc30230345ed0172a9abcbc0a7a4145a35025c827a52a87",
    "MCQ_F.xpt": "c2f0f9223c6a9e38e5bf6d26501c4b11d3cfd97b82db46e1c9c266f24761c457",
    "MCQ_G.xpt": "7538eb86c72b81fd5e76b56120fcb068ed38149d44650e9e750670ad58658d52",
    "OHXPER_F.xpt": "248cb45277b546ecb2a1625146674c020f4db14d809d6ec9c2ea4367e5b29daa",
    "OHXPER_G.xpt": "128c369eb836d8b651ea1422566890b410d9dc56019f7b49668755bdb0338310",
    "PAQ_F.xpt": "02d25e8312a36103ff6ed416dfd597fb109f5a299cc951477337ff8fe694aa84",
    "PAQ_G.xpt": "6b56874f6c3af191aebcb10316c028bc1ae1d4f89d0aafc00cc080c9f533b32a",
    "dada2rsv-genus-count.txt": "333fd8628740d52f80e5ef9fc0d4cd3f921ffe6c9bc785f608da6a48a07a6bb3",
    "dada2rsv-genus-relative.txt": "b0df48a44e9dd8a53663f500c94aa8bab0bc14d16306f28f76a700bf4c68cb4b",
    "dada2rsv-taxonomy-annotate.txt": "18971dd0d69c0a0a4a1d99ee516216de777644c9b9c53ea030d52175ebbf70cd",
}


def _url(nome: str) -> str:
    if nome.endswith(".xpt"):
        ciclo = nome.removesuffix(".xpt").rsplit("_", 1)[1]
        return _BASE_XPT.format(ano=_ANO_DO_CICLO[ciclo], nome=nome)
    return _BASE_MICROBIOMA.format(nome=nome)


# nome do arquivo -> (url, sha256 esperado)
ARQUIVOS: dict[str, tuple[str, str]] = {nome: (_url(nome), sha) for nome, sha in _SHA256.items()}

_TAMANHO_BLOCO = 1024 * 1024
_TIMEOUT_SEGUNDOS = 60


def _sha256_do_arquivo(caminho: Path) -> str:
    h = hashlib.sha256()
    with caminho.open("rb") as f:
        for bloco in iter(lambda: f.read(_TAMANHO_BLOCO), b""):
            h.update(bloco)
    return h.hexdigest()


def _baixar_um(nome: str, url: str, sha_esperado: str, destino: Path, abrir_url) -> None:
    parcial = destino / f"{nome}.part"
    requisicao = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        h = hashlib.sha256()
        try:
            resposta = abrir_url(requisicao, timeout=_TIMEOUT_SEGUNDOS)
            with resposta, parcial.open("wb") as saida:
                for bloco in iter(lambda: resposta.read(_TAMANHO_BLOCO), b""):
                    h.update(bloco)
                    saida.write(bloco)
        except (OSError, http.client.HTTPException) as erro:
            # URLError, HTTPError, timeout e conexão caindo no meio são OSError.
            raise RuntimeError(f"Não foi possível baixar {nome} de {url}: {erro}") from erro
        if h.hexdigest() != sha_esperado:
            raise ValueError(
                f"{nome}: o conteúdo baixado de {url} não confere com o esperado "
                "(o arquivo pode ter mudado no site do CDC)."
            )
        parcial.replace(destino / nome)
    finally:
        parcial.unlink(missing_ok=True)


def baixar(
    destino: Path = Path("datasets"),
    arquivos: dict[str, tuple[str, str]] = ARQUIVOS,
    abrir_url=urllib.request.urlopen,
) -> list[Path]:
    """Baixa para ``destino`` os arquivos ausentes ou corrompidos.

    Devolve a lista dos arquivos baixados nesta execução.
    """
    destino = Path(destino)
    destino.mkdir(parents=True, exist_ok=True)
    baixados = []
    for nome, (url, sha) in arquivos.items():
        caminho = destino / nome
        if caminho.exists() and _sha256_do_arquivo(caminho) == sha:
            print(f"ok       {nome}")
            continue
        print(f"baixando {nome} ...", flush=True)
        _baixar_um(nome, url, sha, destino, abrir_url)
        baixados.append(caminho)
    print(f"Pronto: {len(arquivos)} arquivos em {destino.resolve()}")
    return baixados


if __name__ == "__main__":
    baixar()
