import os
import yaml
import shutil
import pandas as pd
import pyarrow as pa
from typing import Any
from pathlib import Path
import pyarrow.parquet as pq
from .types_check import _path, _str, _array


def get_dirs(path: str | Path) -> list[Path]:
    if not _path(path):
        return []
    return [x for x in Path(path).glob("*") if x.is_dir()]


def get_files(
    path: str | Path, extensions: str | list[str] | tuple[str, ...] | None = None
) -> list[Path]:
    if not _path(path):
        return []
    elif not extensions:
        return [x for x in Path(path).glob("*") if x.is_file()]
    elif _str(extensions):
        if extensions[0] == ".":
            extensions = extensions[1:]
        return [x for x in Path(path).glob(f"*.{extensions}") if x.is_file()]
    elif _array(extensions):
        results = []
        for y in extensions:
            if _str(y):
                results.extend(get_files(path, y))
        return results
    return []


def create_path(path: str | Path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)


def _load_parquet(content: Any):
    if not isinstance(content, dict):
        return content
    return {key: list(value) for key, value in content.items()}


def load_parquet(path: str):
    """Load a Parquet file."""
    table = pq.read_table(path).to_pandas().to_dict(orient="records")
    return [_load_parquet(x) for x in table]


def save_parquet(path: str, data: list | dict) -> None:
    """Save a list to a Parquet file."""
    create_path(path)
    table = pa.Table.from_pandas(pd.DataFrame(data))
    pq.write_table(table, path)


def load_text(
    path: Path | str,
    encoding: str = "utf-8",
) -> str:
    """Load text content from a file. If not exists it returns a empty string."""
    if not _path(path):
        return ""
    with open(path, "r", encoding=encoding) as file:
        return file.read()


def save_text(path: Path | str, content: str, encoding: str = "utf-8") -> None:
    """Save a text file to the provided path."""
    create_path(path)
    with open(path, "w", encoding=encoding) as file:
        file.write(content)


def load_yaml(
    path: Path | str,
    encoding: str = "utf-8",
    unsafe_loader=False,
) -> None | list[Any] | dict[Any, Any]:
    """Load YAML content from a file."""
    if not _path(path):
        return None
    with open(path, "r", encoding=encoding) as file:
        if not unsafe_loader:
            return yaml.safe_load(file, Loader=yaml.FullLoader)
        return yaml.unsafe_load(file, Loader=yaml.FullLoader)


def save_yaml(
    path: Path | str,
    content: list | tuple | dict,
    encoding: str = "utf-8",
    safe_dump: bool = False,
) -> None:
    """Save a YAML file to the provided path."""
    create_path(path)
    with open(path, "w", encoding=encoding) as file:
        if safe_dump:
            yaml.safe_dump(content, file, encoding=encoding)
        else:
            yaml.dump(content, file, encoding=encoding)


def move_to(source_path: str | Path, destination_path: str | Path):
    assert (
        str(source_path).strip() and Path(source_path).exists()
    ), "Source path does not exists!"

    os.makedirs(str(destination_path), exist_ok=True)
    shutil.move(source_path, destination_path)


def delete_path(path: str | Path | list[str | Path] | tuple[str | Path, ...]):
    if _str(path) and Path(path).exists():
        shutil.rmtree(path)
    elif _array(path):
        delete_path(path)
