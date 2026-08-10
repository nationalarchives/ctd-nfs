import json
from importlib.resources import as_file, files
from pathlib import Path
from typing import Any, Union

import yaml

from src._tools.xlreader import read_file


def get_data_from_file(_data_file: Union[str, Path], _csv_fieldnames=None) -> Any:
    if _data_file.suffix in [".xls", ".xlsx"]:
        return read_file(_data_file)

    if _data_file.suffix in [".log", ".txt", ".html"]:
        return _data_file.read_text(encoding="utf-8")

    with _data_file.open(mode="r", encoding="utf-8") as _stream:
        if _data_file.suffix == ".yaml":
            return yaml.safe_load(_stream)

        if _data_file.suffix == ".json":
            return json.load(_stream)


def get_data_file_from_package(package: str, file_path_relative_to_package: str) -> Any:
    data_file = files(package).joinpath(file_path_relative_to_package)
    with as_file(data_file) as file_object:
        return get_data_from_file(file_object)


