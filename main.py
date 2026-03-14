import sys

# TODO: read paths from sys.argv
RESUME_PATH = "test_resume.md"
TEMPLATE_PATH = "templates/will.yaml"

with open(RESUME_PATH) as file:
    resume_lines = file.readlines()


def main() -> None:
    for line in resume_lines:
        line = line.strip()
        line = line.replace(" - ", " – ")
        if line.startswith("# "):
            print("h1:", line[2:])
        elif line.startswith("## "):
            print("h2:", line[3:])
        elif line.startswith("- "):
            print("bull:", line[2:])
        elif line == "":
            print("(empty)")
        elif line == "---":
            print("----- line -----")
        else:
            print("body: ", end="")

            if "**" in line:
                new_line = ""
                parts = line.split("**")
                for idx, part in enumerate(parts):
                    if idx % 2 == 1:
                        new_line += f"<b>{part}</b>"
                    else:
                        new_line += part
                line = new_line

            if " >> " in line:
                left, right = line.split(" >> ", 1)
                line = f"<l>{left}</l><r>{right}</r>"

            print(line)


if __name__ == "__main__":
    main()
