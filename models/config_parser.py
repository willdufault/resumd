from typing import Any

import yaml


class ConfigParser:
    @staticmethod
    def parse(resume_lines: list[str]) -> tuple[dict[str, Any], int]:
        """Return the config dict and the index of the frontmatter closing line."""
        if resume_lines[0].strip() != "---":
            raise ValueError("❌ Resume is missing config")

        for closing_index, line in enumerate(resume_lines[1:]):
            if line.strip() == "---":
                break
        else:
            raise ValueError("❌ Resume config is not closed")

        # Add 1 because for loop skipped first row
        config = yaml.safe_load("".join(resume_lines[1 : closing_index + 1]))
        return config, closing_index + 1
