import yaml

from models.resume_pdf import ResumePdf

# TODO: read paths from sys.argv
RESUME_PATH = "resume.md"
TEMPLATE_PATH = "templates/default.yaml"

with open(RESUME_PATH) as file:
    resume_lines = file.readlines()

with open(TEMPLATE_PATH) as file:
    template_config = yaml.safe_load(file)


def main() -> None:
    pdf = ResumePdf(template_config)
    for line in resume_lines:
        line = line.strip()
        # TODO: add with unicode font
        # line = line.replace(" - ", " – ")
        line = line.replace(" - ", " -- ")

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

    pdf.output("resume.pdf")


if __name__ == "__main__":
    main()
