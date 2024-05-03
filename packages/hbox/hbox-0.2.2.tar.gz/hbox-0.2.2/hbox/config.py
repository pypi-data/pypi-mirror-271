import importlib.metadata
import os
import json
from typing import Dict, Optional, List

from pydantic import BaseModel, Field

from hbox.utils import resolve_path

lib_name = "hbox"
base_dir = resolve_path(os.getenv("HBOX_DIR", os.path.expanduser(f"~/.{lib_name}")))
config_path = resolve_path(os.path.join(base_dir, "config.json"))
versions_path = resolve_path(os.path.join(base_dir, "versions.json"))
shims_path = resolve_path(os.path.join(base_dir, "shims"))


class VolumeConfig(BaseModel):
    source: str
    target: str


class PackageConfig(BaseModel):
    image: str
    volumes: Optional[List[VolumeConfig]] = Field(default_factory=list)


class Config(BaseModel):
    debug: Optional[bool] = False
    packages: Dict[str, PackageConfig] = Field(default_factory=dict)


class Package(BaseModel):
    name: str
    versions: List[str]
    current: Optional[str] = None


class Packages(BaseModel):
    packages: List[Package] = Field(default_factory=list)


def load_config() -> Config:
    if not os.path.isfile(config_path):
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
        default_config = Config()
        with open(config_path, "w") as f:
            f.write(default_config.model_dump_json(indent=2))
        return default_config
    with open(config_path, "r") as f:
        return Config(**json.load(f))


def save_config(data: Config):
    with open(config_path, "w") as f:
        f.write(data.model_dump_json(indent=2))


def load_versions() -> Packages:
    if not os.path.isfile(versions_path):
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
        default_packages = Packages()
        with open(versions_path, "w") as f:
            f.write(default_packages.model_dump_json(indent=2))
        return default_packages
    with open(versions_path, "r") as f:
        return Packages(**json.load(f))


def save_versions(data: Packages):
    with open(versions_path, "w") as f:
        f.write(data.model_dump_json(indent=2))


def get_library_version() -> str:
    try:
        version = importlib.metadata.version(lib_name)
        return version
    except importlib.metadata.PackageNotFoundError:
        return "<unknown>"
