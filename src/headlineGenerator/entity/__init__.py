from pathlib import Path
from dataclasses import dataclass


@dataclass(frozen=True)
class Content:
    headline: str
    last_update: str
    writer: str
    editor: str
    summary: str
    main_story: str
    page_url: str


@dataclass(frozen=True)
class DataScraperConfig:
    root_dir: Path
    save_dir: Path
    source_url: str
    categories: list
    max_pages: int


@dataclass(frozen=True)
class DataPreparationConfig:
    root_dir: Path
    data_dir: Path
    save_dir: Path
