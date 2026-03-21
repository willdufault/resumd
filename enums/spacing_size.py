from enum import Enum


class SpacingSize(Enum):
    COMPACT = 1.23  # 1.0 in Google Docs
    STANDARD = 1.32  # 1.08 in Google Docs
    SPACIOUS = 1.4  # 1.15 in Google Docs
    SMART = 0  # Must be overriden
