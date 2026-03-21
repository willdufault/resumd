import sys
from pathlib import Path

from rich import print

from models.config_parser import ConfigParser
from models.font_fetcher import FontFetcher
from models.layout_calculator import LayoutCalculator
from models.resume_pdf import ResumePdf
from models.resume_pdf_factory import ResumePdfFactory
from models.resume_renderer import ResumeRenderer


# TODO: for pypi, think about where to give starter templates. in github?
# in package root dir? command to create them all in curr dir?
# TODO: where to store fonts? can't use local fonts dir
# TODO: update readme
# TODO: create GH actions pipeline to deploy to Pypi
# TODO: add MD link support!
def main() -> None:
    if len(sys.argv) < 2:
        print("[red]Missing resume filepath[/red]")
        sys.exit()
    resume_path = sys.argv[1]

    try:
        with open(resume_path) as file:
            resume_lines = file.readlines()
    except Exception:
        print(f"[red]Error reading {resume_path}[/red]")
        sys.exit()

    try:
        print("Parsing config...", flush=True, end="")
        config, closing_index = ConfigParser.parse(resume_lines)
        resume_data = resume_lines[closing_index + 1 :]
        print("✅")
    except Exception as error:
        print("❌")
        print(f"[red]{error}[/red]")
        sys.exit()

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

    print("Rendering resume...", flush=True, end="")
    pdf = ResumePdf(config, font_paths, spacing_in=spacing_in)
    pdf = ResumeRenderer.render(pdf, resume_data)
    print("✅")

    print("Writing resume...", flush=True, end="")
    resume_name = Path(resume_path).stem
    pdf.output(f"{resume_name}.pdf")
    print("✅")


if __name__ == "__main__":
    main()
