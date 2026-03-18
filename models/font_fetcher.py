import re
from pathlib import Path

import requests

NORMAL_FONT_WEIGHT = 400
BOLD_FONT_WEIGHT = 700

_GOOGLE_FONTS_URL_TEMPLATE = "https://fonts.googleapis.com/css2?family={font_name}:ital,wght@0,400;0,700;1,400;1,700"
_CSS_BLOCK_PATTERN = r"@font-face\s+\{.*?\}"
_FONT_STYLE_PATTERN = r"font-style:\s+([a-z]+);"
_FONT_WEIGHT_PATTERN = r"font-weight:\s+(\d+);"
_FONT_URL_PATTERN = r"src:\s+url\((.*?)\)"
_FONT_UNICODE_RANGE_PATTERN = r"unicode-range:\s+([A-Z0-9\-+]+);"
_LATIN_UNICODE_RANGE = "U+0000-00FF"

type FontPaths = dict[tuple[str, int], str]


class FontFetcher:
    @staticmethod
    def get_normalized_font_name(font_name: str) -> str:
        return font_name.replace(" ", "+")

    @classmethod
    def fetch_font(cls, font_name: str) -> FontPaths:
        """Download the font from Google Fonts and return a dict of styles and
        weights to file paths."""
        font_name = cls.get_normalized_font_name(font_name)

        url = _GOOGLE_FONTS_URL_TEMPLATE.format(font_name=font_name)
        css = requests.get(url).text
        blocks = re.findall(_CSS_BLOCK_PATTERN, css, re.DOTALL)

        font_paths = {}
        for block in blocks:
            style_match = re.search(_FONT_STYLE_PATTERN, block)
            if style_match is None:
                continue
            style = style_match.group(1)

            weight_match = re.search(_FONT_WEIGHT_PATTERN, block)
            if weight_match is None:
                continue
            weight = int(weight_match.group(1))

            url_match = re.search(_FONT_URL_PATTERN, block)
            if url_match is None:
                continue
            url = url_match.group(1)
            font_type = url.rsplit(".", 1)[-1]

            # Some fonts don't include a unicode range. If no blocks in the response
            # include a unicode range field, assume they are latin.
            unicode_range_match = re.search(_FONT_UNICODE_RANGE_PATTERN, block)
            is_latin = (
                unicode_range_match is None
                or _LATIN_UNICODE_RANGE in unicode_range_match.group(1)
            )
            if not is_latin:
                continue

            font_path = Path(
                f"fonts/{font_name}/{font_name}-{style}-{weight}.{font_type}"
            )
            font_path.parent.mkdir(parents=True, exist_ok=True)

            response = requests.get(url)
            with open(font_path, "wb") as file:
                file.write(response.content)
            font_paths[(style, weight)] = font_path
        return font_paths
