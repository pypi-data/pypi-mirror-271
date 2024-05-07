import logging
import shutil
import tempfile
from pathlib import Path
from typing import Any, Union

from aind_data_schema import base
from h5py import Dataset, File

logger = logging.getLogger(__name__)


def load_hdf5(h5_path: Path) -> File:
    """Load hdf5 file from path."""
    return File(h5_path, "r")


def extract_hdf5_value(h5_file: File, path: list[str]) -> Union[Any, None]:
    """Extract value from hdf5 file using a path. Path is a list of property
    names that are used to traverse the hdf5 file. A path of length greater
    than 1 is expected to point to a nested property.
    """
    try:
        value = None
        for part in path:
            value = h5_file[part]
    except KeyError as e:
        logger.warning(f"Key not found: {e}")
        return None

    if isinstance(value, Dataset):
        return value[()]
    else:
        return value


def find_replace_or_append(
    iterable: list[Any],
    filters: list[tuple[str, Any]],
    update: Any,
) -> None:
    """Find an item in a list of items that matches the filters and replace it.
    If no item is found, append.
    """
    for idx, obj in enumerate(iterable):
        if all(
            getattr(obj, prop_name, None) == prop_value
            for prop_name, prop_value in filters
        ):
            iterable[idx] = update
            break
    else:
        iterable.append(update)


def save_aind_model(
    model: base.AindCoreModel,
    output_path: Path,
) -> Path:
    """Save aind models to a specified output path.

    Notes
    -----
    - Gets around awkward `write_standard_file` method. to write to a determined
    output path.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        model.write_standard_file(temp_dir)
        return Path(
            shutil.copy2(Path(temp_dir) / model.default_filename(), output_path)
        )
