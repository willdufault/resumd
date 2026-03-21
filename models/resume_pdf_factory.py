from typing import Any

from models.font_fetcher import FontPaths
from models.resume_pdf import ResumePdf


class ResumePdfFactory:
    def __init__(self, config: dict[str, Any], font_paths: FontPaths) -> None:
        self._config = config
        self._font_paths = font_paths

    def create(self, spacing_in: float | None = None) -> ResumePdf:
        return ResumePdf(self._config, self._font_paths, spacing_in=spacing_in)
