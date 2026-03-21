from ..enums.special_char import SpecialChar
from .resume_pdf import ResumePdf


class ResumeRenderer:
    @staticmethod
    def render(pdf: ResumePdf, resume_data: list[str]) -> ResumePdf:
        for line in resume_data:
            line = line.strip()
            line = line.replace(" - ", f" {SpecialChar.EN_DASH.value} ")
            line = line.replace(" * ", f" {SpecialChar.BULLET.value} ")

            is_comment = line.startswith("<!--") and line.endswith("-->")
            if is_comment:
                continue

            if line == "":
                pdf.line_break()
            elif line.startswith("# "):
                pdf.h1(line[2:])
            elif line.startswith("## "):
                pdf.h2(line[3:])
            elif line.startswith("- "):
                pdf.bullet(line[2:])
            else:
                pdf.body(line)
        return pdf
