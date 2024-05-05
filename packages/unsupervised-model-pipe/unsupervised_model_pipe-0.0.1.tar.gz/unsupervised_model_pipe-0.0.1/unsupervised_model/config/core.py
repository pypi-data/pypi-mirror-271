from pathlib import Path
from typing import Optional

from pydantic import BaseModel
from strictyaml import YAML, load

import unsupervised_model

# Project directories
PACKAGE_ROOT = Path(unsupervised_model.__file__).resolve().parent
ROOT = PACKAGE_ROOT.parent
CONFIG_FILE_PATH = PACKAGE_ROOT / "config.yml"
DATASET_DIR = PACKAGE_ROOT / "datasets"
PIPE_SAVE_DIR = PACKAGE_ROOT / "trained_models"


class AppConfig(BaseModel):
    """
    Application-level config.
    """

    package_name: str
    pipeline_save_file: str
    training_data_file: str


class ModelConfig(BaseModel):
    """
    All configurations relevant to unsupervised
    learning pipeline and feature engineering
    """

    random_state: int
    pca_components: int
    kpca_components: int
    kpca_kernel: str
    kmeans_init: str
    n_init: int
    max_iter: int


class Config(BaseModel):
    """Master config object"""
    app_config: AppConfig
    model_config: ModelConfig


def find_config_file() -> Path:
    """Locate configuration file"""
    if CONFIG_FILE_PATH.is_file():
        return CONFIG_FILE_PATH
    raise Exception(f"Config not found at {CONFIG_FILE_PATH!r}")


def fetch_config_from_yaml(cfg_path: Optional[Path] = None) -> YAML:
    """Parse YAML containing the package configurations."""

    if not cfg_path:
        cfg_path = find_config_file()

    if cfg_path:
        with open(cfg_path, "r") as conf_file:
            parsed_config = load(conf_file.read())
            return parsed_config
    raise OSError(f"Did not find config file at path: {cfg_path}")


def create_and_validate_config(parsed_config: YAML = None) -> Config:
    """Run validation on config values."""
    if parsed_config is None:
        parsed_config = fetch_config_from_yaml()

    # specify the data attribute from the strictyaml YAML type
    _config = Config(
        app_config=AppConfig(**parsed_config.data),
        model_config=ModelConfig(**parsed_config.data),
    )

    return _config


config = create_and_validate_config()
