import datetime
import logging
import pathlib
import shutil
import tempfile
import typing

from aind_data_schema.core import rig, session
from aind_metadata_mapper.neuropixels import (
    mvr_rig,
    neuropixels_rig,
    open_ephys_rig,
    sync_rig,
)

from np_aind_metadata import common, utils
from np_aind_metadata.dynamic_routing_task_etl import DynamicRoutingTaskRigEtl

logger = logging.getLogger(__name__)


def _run_neuropixels_rig_etl(
    etl_class: neuropixels_rig.NeuropixelsRigEtl,
    input_source: pathlib.Path,
    output_dir: pathlib.Path,
    *etl_args,
    **etl_kwargs,
) -> pathlib.Path:
    """Utility for running a neuropixels rig ETL and continuing on error."""
    try:
        etl = etl_class(input_source, output_dir, *etl_args, **etl_kwargs)
        etl.run_job()
        return output_dir / "rig.json"
    except Exception:
        logger.error("Error calling: %s" % etl_class, exc_info=True)
        return input_source


def fix_modification_date(prev: pathlib.Path, new: pathlib.Path) -> None:
    """Fixes an unintentional side effect introduced with open ephys etl.
    Reverts the rig_id if probe serial numbers have not changed.

    Notes
    -----
    - This may be removed in the future if we keep generating a new
     modification date for each upload.
    """
    prev_rig = rig.Rig.model_validate_json(prev.read_text())
    new_rig = rig.Rig.model_validate_json(new.read_text())
    prev_probe_serial_numbers = [
        ephys_assembly.probes[0].serial_number
        for ephys_assembly in prev_rig.ephys_assemblies
    ]
    new_probe_serial_numbers = [
        ephys_assembly.probes[0].serial_number
        for ephys_assembly in new_rig.ephys_assemblies
    ]
    if prev_probe_serial_numbers != new_probe_serial_numbers:
        logger.debug(
            "Probe serial numbers changed. Not reverting modification date."
            f"previous: {prev_probe_serial_numbers},"
            f"new: {new_probe_serial_numbers}"
        )
        return

    logger.debug("Probe serial numbers match. Reverting modification date.")
    with tempfile.TemporaryDirectory() as temp_dir:
        new_rig.rig_id = prev_rig.rig_id
        new_rig.modification_date = prev_rig.modification_date
        new_rig.write_standard_file(temp_dir)
        shutil.copy2(pathlib.Path(temp_dir) / "rig.json", new)


def update_rig_id(rig_id: str, modification_date: datetime.date) -> str:
    """Updates the modification date of a rig id."""
    id_parts = rig_id.split("_")
    id_parts[-1] = modification_date.strftime(common.MODIFICATION_DATE_FORMAT)
    return "_".join(id_parts)


def update_session_modification_date(
    current_model_path: pathlib.Path, modification_date: datetime.date
) -> pathlib.Path:
    model = session.Session.model_validate_json(current_model_path.read_text())
    model.rig_id = update_rig_id(model.rig_id, modification_date)
    return utils.save_aind_model(model, current_model_path)


def update_rig_modification_date(
    current_model_path: pathlib.Path,
    modification_date: datetime.date,
) -> pathlib.Path:
    """Updates the modification date of a rig model and saves it over current
    path.
    """
    model = rig.Rig.model_validate_json(current_model_path.read_text())
    model.rig_id = update_rig_id(model.rig_id, modification_date)
    model.modification_date = modification_date
    return utils.save_aind_model(model, current_model_path)


# class RigUpdateContext:

#     """Context handler for updating rig source files. Edits are made in a temporary directory.

#     Notes
#     -----
#     - Gets a rig model from local storage, updates local storage with the new model when exiting the context.
#     """

#     def __init__(
#         self,
#         rig_name: common.RigName,
#         storage_dir: pathlib.Path,
#         modification_date: typing.Optional[datetime.date] = None,
#         update_rig_storage: bool = True,
#     ) -> None:
#         self.storage_dir = storage_dir
#         self.rig_name = rig_name
#         self.update_rig_storage = update_rig_storage
#         self.modification_date = modification_date
#         self.rig_source_path = storage.get_item(
#             self.storage_dir,
#             self.rig_name,
#         )
#         logger.debug("Rig source path: %s" % self.rig_source_path)
#         self.build_dir = pathlib.Path(tempfile.mkdtemp())
#         self.build_source = pathlib.Path(shutil.copy2(self.rig_source_path, self.build_dir))

#     def __enter__(self) -> pathlib.Path:
#         return self.build_source

#     def __exit__(self, exc_type, exc_value, traceback) -> None:
#         if exc_type is not None:
#             return False

#         if self.update_rig_storage:
#             logger.debug("Updating rig storage. update_rig_storage: %s" % self.update_rig_storage)
#             storage.update_item(
#                 self.storage_dir,
#                 self.build_source,
#             )
#         shutil.rmtree(self.build_dir)

#         return True


def update_neuropixels_rig(
    rig_source: pathlib.Path,
    modification_date: typing.Optional[datetime.date] = None,
    task_source: typing.Optional[pathlib.Path] = None,
    reward_calibration_date: typing.Optional[datetime.date] = None,
    sound_calibration_date: typing.Optional[datetime.date] = None,
    open_ephys_settings_sources: typing.Optional[list[pathlib.Path]] = None,
    sync_source: typing.Optional[pathlib.Path] = None,
    mvr_source: typing.Optional[pathlib.Path] = None,
    mvr_mapping: dict[str, str] = common.DEFAULT_MVR_MAPPING,
    output_path: pathlib.Path = pathlib.Path("rig.json"),
) -> pathlib.Path:
    """Generates a new rig json file with the metadata from the given sources.

    >>> updated_model_path = update_neuropixels_rig(
    ...  pathlib.Path(".", "examples", "rig.json"),
    ...  open_ephys_settings_sources=[
    ...     pathlib.Path(".", "examples", "settings.xml"),
    ...  ],
    ... )

    Notes
    -----
    - If rig_source is None, the rig will be initialized with the default
     values.
    - *_source, if present will update various values in the rig model.
    """
    # build model in a temporary directory
    build_dir = pathlib.Path(tempfile.mkdtemp())

    build_source = pathlib.Path(shutil.copy2(rig_source, build_dir))
    logger.debug("Rig build source: %s" % build_source)
    if task_source:
        logger.debug("Updating rig model with dynamic routing task context.")
        _run_neuropixels_rig_etl(
            DynamicRoutingTaskRigEtl,
            build_source,
            build_dir,
            task_source=task_source,
            sound_calibration_date=sound_calibration_date,
            reward_calibration_date=reward_calibration_date,
        )

    if open_ephys_settings_sources:
        logger.debug("Updating rig model with open ephys context.")
        _run_neuropixels_rig_etl(
            open_ephys_rig.OpenEphysRigEtl,
            build_source,
            build_dir,
            open_ephys_settings_sources=open_ephys_settings_sources,
        )

    if sync_source:
        logger.debug("Updating rig model with sync context.")
        _run_neuropixels_rig_etl(
            sync_rig.SyncRigEtl,
            build_source,
            build_dir,
            config_source=sync_source,
        )

    if mvr_source and mvr_mapping:
        logger.debug("Updating rig model with mvr context.")
        _run_neuropixels_rig_etl(
            mvr_rig.MvrRigEtl,
            build_source,
            build_dir,
            mvr_config_source=mvr_source,
            mvr_mapping=mvr_mapping,
        )

    if modification_date:
        update_rig_modification_date(build_source, modification_date)
    else:
        update_rig_modification_date(build_source, datetime.date.today())

    shutil.copy2(build_source, output_path)
    return output_path


def update_neuropixels_rig_from_dynamic_routing_session_dir(
    rig_source: pathlib.Path,
    session_dir: pathlib.Path,
    output_path: pathlib.Path = pathlib.Path("rig.json"),
    modification_date: typing.Optional[datetime.date] = None,
    mvr_mapping: dict[str, str] = common.DEFAULT_MVR_MAPPING,
) -> pathlib.Path:
    """Scrapes dynamic routing session directory for various rig
    configuration/settings and updates `rig_source`.
    """
    try:
        task_source = next(session_dir.glob("**/Dynamic*.hdf5"))
        logger.debug("Scraped task source: %s" % task_source)
    except StopIteration:
        task_source = None

    # sync
    try:
        sync_source = next(session_dir.glob("**/sync.yml"))
        logger.debug("Scraped sync source: %s" % sync_source)
    except StopIteration:
        sync_source = None

    # mvr
    try:
        mvr_source = next(session_dir.glob("**/mvr.ini"))
        logger.debug("Scraped mvr source: %s" % mvr_source)
    except StopIteration:
        mvr_source = None

    # open ephys
    settings_sources = list(session_dir.glob("**/settings.xml"))
    logger.debug("Scraped open ephys settings: %s" % settings_sources)

    return update_neuropixels_rig(
        rig_source,
        task_source=task_source,
        sync_source=sync_source,
        mvr_source=mvr_source,
        mvr_mapping=mvr_mapping,
        open_ephys_settings_sources=settings_sources,
        output_path=output_path,
        modification_date=modification_date,
        reward_calibration_date=modification_date,
        sound_calibration_date=modification_date,
    )


if __name__ == "__main__":
    from np_aind_metadata import testmod

    testmod()
