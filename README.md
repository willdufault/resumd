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

1. Edit a template in `templates/` with your content
2. Set `RESUME_PATH` in `main.py` to point to your template (CLI argument support is planned)
3. Run:
   ```bash
   uv run main.py
   ```
4. Open `resumes/resume.pdf`

## Resume Format

| Syntax | Result |
|---|---|
| `# Name` | Name heading |
| `## Section` | Section heading with divider |
| `- text` | Bullet point |
| `**text**` | Bold text |
| `*text*` | Italic text |
| `***text***` | Bold italic text |
| `\*` | Escaped literal `*` |
| `<!-- comment -->` | Ignored (HTML comment) |
| `left >> right` | Left + right-aligned pair (e.g. job title and date) |
| `  -  ` | En-dash (–) (inline text replacement) |
| `  *  ` | Bullet (•) (inline text delimiter) |

## Templates

Templates live in `templates/` as Markdown files with YAML frontmatter. Built-in options: `default`, `harvard`, `mit`, `r_engineering_resumes`.

To switch templates, update `RESUME_PATH` in `main.py`.

## Configuration

Each template file has a YAML frontmatter block that controls styling:

```yaml
---
font: Carlito          # Google Font name (e.g. Carlito, Tinos)
margins: compact       # compact | standard | spacious
spacing: compact       # compact | standard | spacious
h1:
  font_size: 20
  center: true
  line: false
h2:
  font_size: 14
  bold: true
  center: false
  line: true
body:
  font_size: 11
bullet:
  indent: compact      # compact | standard | spacious
  space_after: true
line:
  width: standard      # thin | standard | thick
---
```
