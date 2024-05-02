import pathlib
import shutil
import datetime

# import pytest
from aind_data_schema.core import rig, session

from np_aind_metadata import np_codeocean, storage, update


def _copy_resource_files(
    source: pathlib.Path,
    dest: pathlib.Path,
) -> pathlib.Path:
    """Test utility. Copies all files from source to dest. Recursively
     traverses directories and copies their files.
    """
    for file in source.iterdir():
        if file.is_dir():
            dest_dir = dest / file.name
            (dest_dir).mkdir()
            _copy_resource_files(file, dest_dir)
        else:
            shutil.copy2(file, dest / file.name)
    return dest


RESOURCES_DIRECTORY = pathlib.Path("tests") / "resources"


def test_add_rig_to_dynamic_routing_session_dir(
    tmp_path: pathlib.Path,
) -> None:
    np_codeocean.logger.setLevel("DEBUG")
    storage.logger.setLevel("DEBUG")
    update.logger.setLevel("DEBUG")
    # setup temporary test directories
    rig_directory_temp = tmp_path / "rig"
    rig_directory_temp.mkdir()
    rig_directory = _copy_resource_files(
        RESOURCES_DIRECTORY / "rig-directory",
        rig_directory_temp,
    )
    session_directory_0_temp = tmp_path / "session-0"
    session_directory_0_temp.mkdir()
    session_directory_0 = _copy_resource_files(
        RESOURCES_DIRECTORY / "session-directory-0",
        session_directory_0_temp,
    )

    def get_current_rig_model() -> rig.Rig:
        return rig.Rig.model_validate_json(
            storage.get_item(
                rig_directory,
                "NP3",
            ).read_text()
        )

    initial_rig_model = get_current_rig_model()

    np_codeocean.add_rig_to_dynamic_routing_session_dir(
        session_directory_0,
        rig_directory,
        datetime.date(2024, 4, 1),
    )
    updated_session_0 = session.Session.model_validate_json(
        next(session_directory_0.glob("*session.json")).read_text()
    )

    updated_rig_model = get_current_rig_model()
    assert initial_rig_model != updated_rig_model
    assert updated_session_0.rig_id == updated_rig_model.rig_id
