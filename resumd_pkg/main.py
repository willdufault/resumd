import sys
from pathlib import Path

from rich import print

from .models.config_parser import ConfigParser
from .models.font_fetcher import FontFetcher
from .models.layout_calculator import LayoutCalculator
from .models.resume_pdf import ResumePdf
from .models.resume_pdf_factory import ResumePdfFactory
from .models.resume_renderer import ResumeRenderer


def init() -> None:
    print("Copying templates...", flush=True, end="")
    templates_dir = Path(__file__).parent / ("templates")
    user_cwd = Path.cwd()
    for file_path in templates_dir.iterdir():
        if file_path.is_file():
            target_path = user_cwd / file_path.name
            target_path.write_bytes(file_path.read_bytes())
    print("✅")


def build() -> None:
    if len(sys.argv) < 3:
        print("[red]Missing resume filepath[/red]")
        sys.exit()
    resume_path = sys.argv[2]

    try:
        with open(resume_path) as file:
            resume_lines = file.readlines()
    except Exception:
        print(f"[red]Error reading file {resume_path}[/red]")
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

    try:
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
        stem_path = resume_path.rsplit(".", 1)[0]
        output_path = f"{stem_path}.pdf"
        pdf.output(output_path)
        print("✅")
    except Exception as error:
        print(f"[red]{error}[/red]")
        sys.exit()


# TODO: add MD link support!
# TODO: add build & init commands
# TODO: update readme
# TODO: use testPypi to test page & download
# TODO: create GH actions pipeline to deploy to testPypi & bump version
# TODO: upload to real pypi with cmd, update pipeline
def main() -> None:
    if len(sys.argv) < 2:
        print("[red]Must provide a command[/red]")
        sys.exit()
    command = sys.argv[1]

    match command:
        case "init":
            init()
        case "build":
            build()
        case _:
            print(f"[red]Unknown command {command}[/red]")
            sys.exit()


if __name__ == "__main__":
    main()
