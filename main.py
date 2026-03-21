from models.config_parser import ConfigParser
from models.font_fetcher import FontFetcher
from models.layout_calculator import LayoutCalculator
from models.resume_renderer import ResumeRenderer
from models.resume_pdf import ResumePdf
from models.resume_pdf_factory import ResumePdfFactory

# TODO: read paths from sys.argv
RESUME_PATH = "templates/default.md"


def main() -> None:
    print("Parsing config...", flush=True, end="")
    with open(RESUME_PATH) as file:
        resume_lines = file.readlines()
    config, closing_index = ConfigParser.parse(resume_lines)
    resume_data = resume_lines[closing_index + 1 :]
    print("✅")

    print("Downloading fonts...", flush=True, end="")
    font_paths = FontFetcher.fetch_font(config["font"])
    print("✅")

    spacing_in = None
    if config["spacing"] == "smart":
        print("Calculating smart spacing...", flush=True, end="")
        pdf_factory = ResumePdfFactory(config, font_paths)
        spacing_in = LayoutCalculator._calculate_smart_spacing_in(
            pdf_factory, resume_data
        )
        print("✅")

    print("Building resume...", flush=True, end="")
    pdf = ResumePdf(config, font_paths, spacing_in=spacing_in)
    pdf = ResumeRenderer.render(pdf, resume_data)
    print("✅")

    print("Saving file...", flush=True, end="")
    pdf.output("resumes/resume.pdf")
    print("✅")


if __name__ == "__main__":
    main()
