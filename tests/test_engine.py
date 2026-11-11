"""Uji unit untuk mesin chatbot (tanpa Flask)."""
from pathlib import Path

import pytest

from chatbot.engine import ChatbotEngine, load_themes, preprocess, similarity

THEMES = load_themes(Path(__file__).resolve().parent.parent / "themes")


def test_preprocess_normalisasi_dan_stopword():
    assert preprocess("Gimana cara commit perubahan, dong?") == ["bagaimana", "cara", "commit", "perubahan"]


def test_similarity_kalimat_sama_bernilai_satu():
    t = ["commit", "perubahan"]
    assert similarity(t, t) == 1.0


def test_similarity_kalimat_berbeda_rendah():
    assert similarity(["gudeg"], ["commit", "perubahan"]) < 0.3


def test_hanya_tema_git_yang_termuat():
    assert set(THEMES) == {"git"}


@pytest.mark.parametrize("pesan, intent", [
    ("halo", "salam"),
    ("kamu siapa", "identitas"),
    ("cara commit perubahan", "git_commit"),
    ("cara membuat branch baru", "git_switch"),
    ("membatalkan commit terakhir", "git_reset"),
    ("perbedaan git pull dan fetch", "perbedaan_pull_fetch"),
    ("kena conflict saat merge", "mengatasi_conflict"),
    ("cara bikin gitignore", "git_ignore"),
    ("pulihkan commit yang kehapus", "git_reflog"),
])
def test_klasifikasi_intent(pesan, intent):
    engine = ChatbotEngine(THEMES["git"])
    tag, _ = engine.classify(pesan)
    assert tag == intent


def test_salah_ketik_masih_dikenali():
    engine = ChatbotEngine(THEMES["git"])
    tag, _ = engine.classify("cara commit perubhan")
    assert tag == "git_commit"


def test_pertanyaan_di_luar_tema_memberi_fallback():
    engine = ChatbotEngine(THEMES["git"])
    hasil = engine.reply("siapa pemenang piala dunia")
    assert hasil["intent"] is None
    assert hasil["reply"] in THEMES["git"]["fallback"]


def test_fallback_git_menyertakan_link_dokumentasi():
    engine = ChatbotEngine(THEMES["git"])
    hasil = engine.reply("cara bikin website dengan react")
    assert hasil["intent"] is None
    assert hasil["reply"] in THEMES["git"]["fallback"]
    assert "docs.github.com" in hasil["reply"]


def test_response_git_menyertakan_contoh_perintah():
    engine = ChatbotEngine(THEMES["git"])
    hasil = engine.reply("cara commit perubahan")
    assert "git commit -m" in hasil["reply"]


def test_placeholder_nama_bot_diganti():
    engine = ChatbotEngine(THEMES["git"])
    hasil = engine.reply("kamu siapa")
    assert "{nama_bot}" not in hasil["reply"]
    assert "GitBot" in hasil["reply"]


def test_explain_mengurutkan_kandidat_dari_skor_tertinggi():
    engine = ChatbotEngine(THEMES["git"])
    kandidat = engine.explain("cara commit perubahan")
    assert kandidat[0]["intent"] == "git_commit"
    assert kandidat[0]["pattern"] == "cara commit perubahan"
    skor = [k["score"] for k in kandidat]
    assert skor == sorted(skor, reverse=True)


def test_validate_theme_menemukan_kesalahan():
    from chatbot.engine import validate_theme
    rusak = {"id": "x", "name": "X", "bot_name": "B", "avatar": "*", "color": "#000",
             "description": "d", "greeting": "g", "suggestions": [], "fallback": ["f"],
             "intents": [{"tag": "a", "patterns": ["halo"], "responses": ["hai"]},
                         {"tag": "b", "patterns": ["halo"], "responses": []}]}
    masalah = validate_theme(rusak)
    assert any("responses kosong" in m for m in masalah)
    assert any("'a' dan 'b'" in m for m in masalah)


def test_semua_tema_bawaan_valid():
    from chatbot.engine import validate_theme
    for theme in THEMES.values():
        assert validate_theme(theme) == []


def test_akurasi_data_uji_git_minimal_90_persen():
    from evaluate import baca_data, evaluasi
    akurasi, _ = evaluasi(THEMES["git"], baca_data("git"), 0.45)
    assert akurasi >= 0.9
