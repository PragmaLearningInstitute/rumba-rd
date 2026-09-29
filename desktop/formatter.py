from __future__ import annotations

from dataclasses import dataclass

from Function import FormatResult

ALLOWED_FONTS = ("Avenir Next", "Arial", "OpenDyslexic")
ALLOWED_SIZES = (11, 12, 13, 14, 15)


@dataclass
class OutputStyle:
    font_family: str = "Arial"
    font_size: int = 13
    line_height: float = 1.5

    def normalized(self) -> "OutputStyle":
        font = self.font_family if self.font_family in ALLOWED_FONTS else "Arial"
        size = self.font_size if self.font_size in ALLOWED_SIZES else 13
        return OutputStyle(font_family=font, font_size=size, line_height=1.5)


def render_html_document(result: FormatResult, style: OutputStyle) -> str:
    s = style.normalized()
    return f"""<!doctype html>
<html lang=\"fr\">
  <head>
    <meta charset=\"utf-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
    <title>Rumba Reader Output</title>
    <style>
      body {{
        margin: 24px;
        background: #ffffff;
        color: #171717;
        font-family: '{s.font_family}', Arial, sans-serif;
        font-size: {s.font_size}pt;
        line-height: {s.line_height};
        font-weight: 400;
      }}
      strong {{
        font-weight: 700;
      }}
      .meta {{
        margin-bottom: 16px;
        font-size: 10pt;
        color: #555;
      }}
      .output {{
        font-weight: 400;
      }}
    </style>
  </head>
  <body>
    <div class=\"meta\">FRE: {result.analysis.flesch_score} | Common vocabulary ratio: {result.analysis.zipf_common_ratio:.2%} | Langue: {result.analysis.language}</div>
    <div class=\"output\">{result.html_text}</div>
  </body>
</html>
"""
