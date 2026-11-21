import hashlib
import io
import re
import urllib.error

import pytest

from baixar_dados import ARQUIVOS, baixar


def _sha(dados: bytes) -> str:
    return hashlib.sha256(dados).hexdigest()


MANIFESTO = {
    "a.xpt": ("https://exemplo/a.xpt", _sha(b"abc")),
    "b.txt": ("https://exemplo/b.txt", _sha(b"xyz")),
}


class ServidorFalso:
    """Substitui urllib.request.urlopen; registra as URLs pedidas."""

    def __init__(self, conteudos: dict[str, bytes]):
        self.conteudos = conteudos
        self.pedidas: list[str] = []

    def __call__(self, requisicao, *args, **kwargs):
        url = requisicao.full_url
        self.pedidas.append(url)
        return io.BytesIO(self.conteudos[url])


def test_baixa_arquivos_ausentes(tmp_path):
    servidor = ServidorFalso({"https://exemplo/a.xpt": b"abc", "https://exemplo/b.txt": b"xyz"})

    baixados = baixar(tmp_path, MANIFESTO, abrir_url=servidor)

    assert sorted(p.name for p in baixados) == ["a.xpt", "b.txt"]
    assert (tmp_path / "a.xpt").read_bytes() == b"abc"
    assert (tmp_path / "b.txt").read_bytes() == b"xyz"


def test_pula_arquivo_valido(tmp_path):
    (tmp_path / "a.xpt").write_bytes(b"abc")
    servidor = ServidorFalso({"https://exemplo/b.txt": b"xyz"})

    baixados = baixar(tmp_path, MANIFESTO, abrir_url=servidor)

    assert servidor.pedidas == ["https://exemplo/b.txt"]
    assert [p.name for p in baixados] == ["b.txt"]


def test_rebaixa_arquivo_corrompido(tmp_path):
    (tmp_path / "a.xpt").write_bytes(b"corrompido")
    (tmp_path / "b.txt").write_bytes(b"xyz")
    servidor = ServidorFalso({"https://exemplo/a.xpt": b"abc"})

    baixar(tmp_path, MANIFESTO, abrir_url=servidor)

    assert (tmp_path / "a.xpt").read_bytes() == b"abc"


def test_hash_divergente_falha(tmp_path):
    servidor = ServidorFalso({"https://exemplo/a.xpt": b"outra coisa"})

    with pytest.raises(ValueError, match="a.xpt"):
        baixar(tmp_path, {"a.xpt": MANIFESTO["a.xpt"]}, abrir_url=servidor)

    assert list(tmp_path.iterdir()) == []


class RespostaQueCai(io.BytesIO):
    def read(self, *args):
        if self.tell() > 0:
            raise ConnectionError("conexão caiu")
        return super().read(1)


def test_falha_no_meio_nao_deixa_arquivo(tmp_path):
    def abrir(requisicao, *args, **kwargs):
        return RespostaQueCai(b"abc")

    with pytest.raises(RuntimeError, match="a.xpt"):
        baixar(tmp_path, {"a.xpt": MANIFESTO["a.xpt"]}, abrir_url=abrir)

    assert list(tmp_path.iterdir()) == []


def test_usa_timeout(tmp_path):
    chamadas = []

    def abrir(requisicao, *args, **kwargs):
        chamadas.append(kwargs.get("timeout"))
        return io.BytesIO(b"abc")

    baixar(tmp_path, {"a.xpt": MANIFESTO["a.xpt"]}, abrir_url=abrir)

    assert chamadas == [60]


def test_erro_http_cita_arquivo(tmp_path):
    def abrir(requisicao, *args, **kwargs):
        raise urllib.error.HTTPError(requisicao.full_url, 404, "Not Found", {}, None)

    with pytest.raises(RuntimeError) as erro:
        baixar(tmp_path, {"a.xpt": MANIFESTO["a.xpt"]}, abrir_url=abrir)

    assert "a.xpt" in str(erro.value)
    assert "https://exemplo/a.xpt" in str(erro.value)


def test_manifesto_completo():
    tabelas = ["ALQ", "BPQ", "DEMO", "DIQ", "MCQ", "OHXPER", "PAQ"]
    esperados = {f"{t}_{c}.xpt" for t in tabelas for c in "FG"} | {
        "dada2rsv-genus-count.txt",
        "dada2rsv-genus-relative.txt",
        "dada2rsv-taxonomy-annotate.txt",
    }
    assert set(ARQUIVOS) == esperados
    for url, sha in ARQUIVOS.values():
        assert url.startswith("https://wwwn.cdc.gov/")
        assert re.fullmatch(r"[0-9a-f]{64}", sha)
