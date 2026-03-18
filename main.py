from enums.special_char import SpecialChar
from models.config_parser import ConfigParser
from models.font_fetcher import FontFetcher
from models.resume_pdf import ResumePdf

# TODO: read paths from sys.argv
RESUME_PATH = "templates/default.md"


def main() -> None:
    with open(RESUME_PATH) as file:
        resume_lines = file.readlines()
    config, closing_index = ConfigParser.parse(resume_lines)
    print("✅ Parsed config")

    font_paths = FontFetcher.fetch_font(config["font"])
    print("✅ Downloaded fonts")

    pdf = ResumePdf(config, font_paths)

    resume_data = resume_lines[closing_index + 1 :]
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

    pdf.output("resumes/resume.pdf")
    print("✅ Output resume")


if __name__ == "__main__":
    main()
