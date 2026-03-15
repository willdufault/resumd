from copy import deepcopy
from typing import Any

import fpdf
import yaml

from enums.bullet_indent_size import BulletIndentSize
from enums.line_width import LineWidth
from enums.margin_size import MarginSize
from enums.spacing_size import SpacingSize

# TODO: finalize these values, test w diff spacing
_SPACE_AFTER_BULLET_MULTIPLIER = 0.4
_SPACE_AFTER_LINE_MULTIPLIER = 0.15


with open("templates/default.yaml") as file:
    default_config = yaml.safe_load(file)


class ResumePdf(fpdf.FPDF):
    def __init__(self, template_config: dict[str, Any]) -> None:
        super().__init__(format="letter", unit="in")

        template_config = self._deep_merge(default_config, template_config)
        self._margins_in = MarginSize[template_config["margins"].upper()].value
        self._spacing_in = SpacingSize[template_config["spacing"].upper()].value
        self._h1_font_size = template_config["h1"]["font_size"]
        self._h1_centered = template_config["h1"]["center"]
        self._h1_line_after = template_config["h1"]["line"]
        self._h2_font_size = template_config["h2"]["font_size"]
        self._h2_centered = template_config["h2"]["center"]
        self._h2_line_after = template_config["h2"]["line"]
        self._body_font_size = template_config["body"]["font_size"]
        self._bullet_char = template_config["bullet"]["char"]
        self._bullet_indent_in = BulletIndentSize[
            template_config["bullet"]["indent"].upper()
        ].value
        # self._bullet_space_after_in = (
        #     _BULLET_SPACE_AFTER_MULTIPLIER * self._spacing_in
        #     if template_config["bullet"]["space_after"]
        #     else 0
        # )
        self._line_width_in = LineWidth[template_config["line"]["width"].upper()].value

        # TODO: better way to do this?
        self._after_h1 = False
        self._after_bullet = False

        self._set_up_page()

    def _deep_merge(
        self, left: dict[str, Any], right: dict[str, Any]
    ) -> dict[str, Any]:
        """Merge the right dict onto the left one."""
        merged = deepcopy(left)
        for key, value in right.items():
            merged[key] = (
                self._deep_merge(merged[key], value)
                if isinstance(value, dict)
                else value
            )
        return merged

    def _set_up_page(self) -> None:
        self.add_page()

        self.c_margin = 0
        self.set_margin(self._margins_in)
        self.set_auto_page_break(True, self._margins_in)
        self.set_line_width(self._line_width_in)
        self.set_text_shaping(True)

        # TODO: add google fonts
        # self.add_font("Carlito", style="", fname="fonts/Carlito-Regular.ttf")
        # self.add_font("Carlito", style="B", fname="fonts/Carlito-Bold.ttf")
        self.set_font("Helvetica")

    def write(self, *args, **kwargs):
        return super().write(*args, **kwargs, h=self._spacing_in * self.font_size)

    def cell(self, *args, **kwargs):
        return super().cell(*args, **kwargs, h=self._spacing_in * self.font_size)

    def multi_cell(self, *args, **kwargs):
        return super().multi_cell(
            *args,
            **kwargs,
            h=self._spacing_in * self.font_size,
            align=fpdf.Align.L,
        )

    def line_break(self, multiplier: float | None = None) -> None:
        if multiplier is None:
            multiplier = 1
        self.ln(multiplier * self._spacing_in * self.font_size)

    def line(self, *args, **kwargs) -> None:
        super().rect(
            *args,
            **kwargs,
            x=self.get_x(),
            y=self.get_y(),
            w=self.w - 2 * self.l_margin,
            h=self._line_width_in,
        )
        self.line_break(_SPACE_AFTER_LINE_MULTIPLIER)

    def h1(self, text: str) -> None:
        self.set_font(style="B", size=self._h1_font_size)
        self.cell(text=text, center=self._h1_centered)
        self.line_break()
        if self._h1_line_after:
            self.line()
        self._after_h1 = True
        self._after_bullet = False

    def h2(self, text: str) -> None:
        self.set_font(style="B", size=self._h2_font_size)
        self.cell(text=text, center=self._h2_centered)
        self.line_break()
        if self._h2_line_after:
            self.line()
        self._after_h1 = False
        self._after_bullet = False

    def bullet(self, text: str) -> None:
        # TODO: handle bold in bullets
        self.set_font(style="", size=self._body_font_size)
        self.cell(
            self._bullet_indent_in,
            text=self._bullet_char,
            align=fpdf.Align.C,
        )
        self.multi_cell(0, text=text, new_x=fpdf.XPos.LMARGIN)
        self._after_h1 = False
        self._after_bullet = True

    def body(self, text: str) -> None:
        if self._after_h1:
            self.set_font(style="", size=self._body_font_size)
            self.cell(text=text, center=self._h1_centered)
            self.line_break()
            return

        if self._after_bullet:
            self.line_break(_SPACE_AFTER_BULLET_MULTIPLIER * self.font_size)

        if " >> " in text:
            left, right = text.split(" >> ", 1)
        else:
            left, right = text, ""

        # TODO: extract into helper, do same for italics
        # left side
        if "**" in left:
            parts = left.split("**")
            for idx, part in enumerate(parts):
                if len(part) > 0:
                    self.set_font(
                        style="B" if idx % 2 == 1 else "",
                        size=self._body_font_size,
                    )
                    self.write(text=part)
        elif len(left) > 0:
            self.set_font(style="", size=self._body_font_size)
            self.write(text=left)

        # right side
        if len(right) > 0:
            # TODO: worth handling bold parsing on right?
            if right.startswith("**"):
                right = right.strip("*")
                self.set_font(style="B", size=self._body_font_size)
                self.cell(0, text=right, align=fpdf.Align.R)
            else:
                self.set_font(style="", size=self._body_font_size)
                self.cell(0, text=right, align=fpdf.Align.R)

        self.line_break()
