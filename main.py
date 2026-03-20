from enums.spacing_size import SpacingSize
from enums.special_char import SpecialChar
from models.config_parser import ConfigParser
from models.font_fetcher import FontFetcher
from models.resume_pdf import ResumePdf

# TODO: read paths from sys.argv
RESUME_PATH = "templates/default.md"


def build_resume(pdf: ResumePdf, resume_data: list[str]) -> None:
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


def main() -> None:
    with open(RESUME_PATH) as file:
        resume_lines = file.readlines()
    print("Parsing config...", flush=True, end="")
    config, closing_index = ConfigParser.parse(resume_lines)
    print("✅")

    print("Downloading fonts...", flush=True, end="")
    font_paths = FontFetcher.fetch_font(config["font"])
    print("✅")

    # Smart spacing requires building the resume twice, first with compact spacing.
    # This is because fpdf2 writes directly to the pdf output stream so you can't
    # go back to edit the height of previous elements.
    smart_spacing_enabled = config["spacing"] == "smart"
    if smart_spacing_enabled:
        config["spacing"] = "compact"

    print("Building resume...", flush=True, end="")
    resume_data = resume_lines[closing_index + 1 :]
    pdf = ResumePdf(config, font_paths)
    build_resume(pdf, resume_data)
    print("✅")

    # After building the resume once to calculate the content height, calculate
    # the smart spacing value, then rebuild the resume with that spacing.
    if smart_spacing_enabled:
        print("Applying smart spacing...", flush=True, end="")
        page_height_in = pdf.h - pdf.t_margin - pdf.b_margin
        cumulative_height_in = (
            (pdf.pages_count - 1) * page_height_in + pdf.get_y() - pdf.t_margin
        )
        total_height_in = pdf.pages_count * page_height_in

        # Truncate to 2 decimal places to prevent leaking onto the next page.
        smart_spacing_in = (
            SpacingSize.COMPACT.value * total_height_in / cumulative_height_in
        )
        smart_spacing_in = int(smart_spacing_in * 100) / 100
        smart_spacing_in = max(smart_spacing_in, SpacingSize.COMPACT.value)
        smart_spacing_in = min(smart_spacing_in, SpacingSize.SPACIOUS.value)

        pdf = ResumePdf(config, font_paths)
        pdf._spacing_in = smart_spacing_in
        build_resume(pdf, resume_data)

        # BUG: if >1 page and just right, increasing spacing so that line goes to
        # next page can cause single line on new page
        print("✅")

    print("Saving file...", flush=True, end="")
    pdf.output("resumes/resume.pdf")
    print("✅")


if __name__ == "__main__":
    main()
