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

| Command | Description |
|---|---|
| `resumd init` | Copies all built-in templates to the current directory |
| `resumd build <resume.md>` | Builds a PDF from the given resume Markdown file |

1. Run `resumd init` to copy the built-in templates to your current directory
2. Edit a template with your content
3. Run:
   ```bash
   resumd build <template.md>
   ```
4. Open the output PDF

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

Templates are Markdown files with a YAML frontmatter. Run `resumd init` to copy the built-in templates to your current directory, then pass any template to `resumd build`.

## Configuration

Each template file has a YAML frontmatter block that controls styling:

```yaml
---
font: Carlito          # Google Font name (e.g. Carlito, Tinos)
margins: compact       # compact | standard | spacious
spacing: compact       # compact | standard | spacious | smart
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
