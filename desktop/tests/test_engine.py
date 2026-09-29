import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from Function import common_words, gaussReformulator  # noqa: E402


def test_common_words_kept_and_enriched():
    assert isinstance(common_words, set)
    assert 'le' in common_words
    assert 'the' in common_words
    assert 'colour' in common_words
    assert 'color' in common_words


def test_formatter_returns_metrics_and_markup():
    text = "Bonjour, je lis un texte simple pour tester la mise en forme."
    result = gaussReformulator(text, seed=42)

    assert result.analysis.total_words > 0
    assert 0 <= result.analysis.zipf_common_ratio <= 1
    assert '<strong>' in result.html_text
    assert '**' in result.markdown_text


def test_all_input_characters_survive_html_formatting():
    from html import unescape
    import re
    text = "Prix: 123,45 € — 0_1 <script>alert('x')</script> & 漢字 😀\nL’été 2026."
    result = gaussReformulator(text, seed=42)
    rendered = unescape(re.sub(r"<[^>]+>", "", result.html_text.replace("<br>", "\n").replace("<br/>", "\n").replace("<br />", "\n")))
    assert rendered == text
    assert "<script>" not in result.html_text
