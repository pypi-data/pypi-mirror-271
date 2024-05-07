import logging
import shutil
import typing
from pathlib import Path

from np_aind_metadata import common, np, storage

logger = logging.getLogger(__name__)


def copy_rig(
    rig_name: common.RigName,
    output_path: Path,
    storage_directory: typing.Optional[Path] = None,
) -> Path:
    """Copies a rig from storage to `output_path`.

    >>> storage_directory = Path("examples") / "rig-directory"
    >>> copy_rig("NP3", Path("rig.json"), storage_directory)
    PosixPath('rig.json')

    Notes
    -----
    - If `storage_directory` is not provided, will attempt to get default from
     np-config.
    """
    if storage_directory is None:
        logger.debug("Getting storage directory from np-config.")
        storage_directory = np.get_rig_storage_directory()

    return Path(
        shutil.copy2(
            storage.get_item(storage_directory, rig_name),
            output_path,
        )
    )
