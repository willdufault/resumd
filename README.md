# resumd

resumd is a CLI tool that converts a plain Markdown file into a professionally formatted PDF resume. Style your resume with YAML templates — no design tools required.

> ⚠️ **Work in progress** — features and APIs may change.

## Demo

<!-- TODO: add demo video/gif -->
To be added.

## Installation

**Requirements:** Python 3.13+, [uv](https://docs.astral.sh/uv/)

```bash
git clone https://github.com/yourusername/resumd.git
cd resumd
uv sync
```

## Usage

1. Edit `resume.md` with your content
2. Run:
   ```bash
   uv run main.py
   ```
3. Open `resume.pdf`

## Resume Format

| Syntax | Result |
|---|---|
| `# Name` | Name heading |
| `## Section` | Section heading with divider |
| `- text` | Bullet point |
| `**text**` | Bold text |
| `left >> right` | Left + right-aligned pair (e.g. job title and date) |

## Templates

Templates live in `templates/` as YAML files. Built-in options: `default`, `harvard`.

To switch templates, update the template path in `main.py`.
