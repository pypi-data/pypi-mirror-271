from __future__ import annotations

import os
from pathlib import Path

import jsonpickle
from pydantic import BaseModel


def get_config_filename(filename: Path) -> Path:
    if 'SLURM_VIEW_CONFIG' in os.environ:
        filename = Path(os.environ['SLURM_VIEW_CONFIG'])
        if filename.exists():
            return filename

    if filename.exists():
        return filename

    filename = Path.home() / '.config/slurm_viewer/settings.json'
    if filename.exists():
        return filename

    raise RuntimeError('Settings file could not be found. ')


class Config(BaseModel):
    debug: bool = False
    server: str | None = None
    node_list: list[str] = []
    node_columns: list[str] = []
    queue_columns: list[str] = []

    @classmethod
    def init(cls) -> Config:
        return Config.load(get_config_filename(Path('settings.json')))

    @classmethod
    def load(cls, _filename: Path | str) -> Config:
        if not Path(_filename).exists():
            raise RuntimeError(f'Settings file "{Path(_filename).absolute().resolve()}" does not exist.')

        with Path(_filename).open('r', encoding='utf-8') as settings_file:
            setting = Config(**jsonpickle.decode(settings_file.read()))

        return setting
