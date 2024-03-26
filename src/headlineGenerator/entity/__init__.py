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


@dataclass(frozen=True)
class DataTransformationConfig:
    root_dir: Path
    data_dir: Path
    save_dir: Path
    checkpoint: Path


@dataclass(frozen=True)
class ModelTrainerConfig:
    root_dir: Path
    data_dir: Path
    checkpoint: Path
    num_train_epochs: int
    warmup_steps: int
    per_device_train_batch_size: int
    weight_decay: float
    logging_steps: int
    evaluation_strategy: str
    eval_steps: int
    save_steps: float
    gradient_accumulation_steps: int


@dataclass(frozen=True)
class ModelEvaluationConfig:
    root_dir: Path
    data_path: Path
    model_path: Path
    tokenizer_path: Path
    metrics_file: Path
