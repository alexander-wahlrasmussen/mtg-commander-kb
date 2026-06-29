"""REGRESSION (2026-06-29 audit): update_scryfall_data overwrote the destination
bulk file in place and verified only afterward, so an interrupted/truncated
download corrupted the only good copy (these files are gitignored — no checkout to
recover from). Fix streams to a .part sibling, verifies, then atomically replaces.
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import update_scryfall_data as u  # noqa: E402


class FakeResp:
    """Minimal stand-in for urlopen()'s response context manager."""
    def __init__(self, chunks, content_length):
        self._chunks = list(chunks)
        self.headers = {"Content-Length": str(content_length)}

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def read(self, _n):
        if self._chunks:
            c = self._chunks.pop(0)
            if isinstance(c, Exception):
                raise c
            return c
        return b""


def _patch_urlopen(monkeypatch, resp):
    monkeypatch.setattr(u.urllib.request, "urlopen", lambda req: resp)


def test_truncated_download_preserves_existing(tmp_path, monkeypatch):
    dest = tmp_path / "oracle-cards.json"
    dest.write_text('["GOOD"]', encoding="utf-8")
    # Content-Length promises 100 bytes but only 10 arrive, then EOF.
    _patch_urlopen(monkeypatch, FakeResp([b"0123456789"], content_length=100))
    with pytest.raises(SystemExit):
        u.download_with_progress("http://x", dest)
    assert dest.read_text(encoding="utf-8") == '["GOOD"]'           # untouched
    assert not dest.with_name(dest.name + ".part").exists()         # no partial left


def test_midstream_error_preserves_existing(tmp_path, monkeypatch):
    dest = tmp_path / "rulings.json"
    dest.write_text('["GOOD"]', encoding="utf-8")
    _patch_urlopen(monkeypatch,
                   FakeResp([b"partial", ConnectionResetError("boom")], content_length=0))
    with pytest.raises(ConnectionResetError):
        u.download_with_progress("http://x", dest)
    assert dest.read_text(encoding="utf-8") == '["GOOD"]'
    assert not dest.with_name(dest.name + ".part").exists()


def test_successful_download_writes_part_not_dest(tmp_path, monkeypatch):
    # download alone must NOT swap dest — main() does that only after json-verify.
    dest = tmp_path / "oracle-cards.json"
    dest.write_text('["OLD"]', encoding="utf-8")
    payload = b'["NEW"]'
    _patch_urlopen(monkeypatch, FakeResp([payload], content_length=len(payload)))
    tmp = u.download_with_progress("http://x", dest)
    assert tmp.read_bytes() == payload
    assert dest.read_text(encoding="utf-8") == '["OLD"]'
    tmp.unlink()
