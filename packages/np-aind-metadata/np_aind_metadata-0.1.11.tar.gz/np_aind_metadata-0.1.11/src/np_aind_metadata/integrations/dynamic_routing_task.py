import datetime
import logging
import pathlib
import typing

from aind_data_schema.core import rig, session

from np_aind_metadata import common, np, rigs, storage, update, utils

logger = logging.getLogger(__name__)


SESSION_MODEL_GLOB_PATTERN = "*session.json"


def scrape_session_model_path(session_directory: pathlib.Path) -> pathlib.Path:
    """Scrapes aind-metadata session json from dynamic routing session
    directory.

    >>> session_directory = pathlib.Path("examples") / \
        "example-session-directory"
    >>> scrape_session_model_path(session_directory)
    PosixPath('examples/example-session-directory/\
702131_2024-02-26_session.json')
    """
    matches = list(session_directory.glob(SESSION_MODEL_GLOB_PATTERN))
    logger.debug("Scraped session model paths: %s" % matches)
    return matches[0]


def update_session_from_rig(
    session_source: pathlib.Path,
    rig_source: pathlib.Path,
    output_path: pathlib.Path,
) -> pathlib.Path:
    """Convenience function that updates the `rig_id` of a session model at
     `session_source`. Uses the `rig_id` of `rig_source`.

    >>> update_session_from_rig(
    ...     pathlib.Path(
    ...         ".",
    ...         "examples",
    ...         "example-session-directory",
    ...         "702131_2024-02-26_session.json"
    ...     ),
    ...     pathlib.Path(
    ...         ".",
    ...         "examples",
    ...         "rig.json"
    ...     ),
    ...     pathlib.Path("session.json"),
    ... )
    PosixPath('session.json')

    Notes
    -----
    - Overwrites the session model at `output_path`.
    """
    session_model = session.Session.model_validate_json(session_source.read_text())
    rig_model = rig.Rig.model_validate_json(rig_source.read_text())
    session_model.rig_id = rig_model.rig_id
    return utils.save_aind_model(session_model, output_path)


def add_rig_to_session_dir(
    session_dir: pathlib.Path,
    modification_date: datetime.date,
    rig_model_dir: typing.Optional[pathlib.Path] = None,
) -> None:
    """Direct support for the dynamic routing task. Adds an `aind-data-schema`
     `rig.json` to a dynamic routing session directory. The `aind-data-schema`
     `session.json` in `session_dir` will be updated with the `rig_id` of the
      added `rig.json`.

    >>> add_rig_to_session_dir(
    ...     pathlib.Path("examples") / "example-session-directory",
    ...     datetime.date(2024, 4, 1),
    ...     pathlib.Path("examples") / "rig-directory",
    ... )

    Notes
    -----
    - An aind metadata session json must exist and be ending with filename
    session.json (pattern: `*session.json`) in `session_dir`.
    - If `rig_model_dir` is not provided, will attempt to get default from
     np-config. You will need to be onprem for `np-config` to work.
    """
    scraped_session_model_path = scrape_session_model_path(session_dir)
    logger.debug("Scraped session model path: %s" % scraped_session_model_path)
    scraped_session = session.Session.model_validate_json(
        scraped_session_model_path.read_text()
    )
    scraped_rig_id = scraped_session.rig_id
    logger.info("Scraped rig id: %s" % scraped_rig_id)
    _, rig_name, _ = scraped_rig_id.split("_")
    logger.info("Parsed rig name: %s" % rig_name)
    rig_model_path = session_dir / "rig.json"

    if not rig_model_dir:
        logger.debug("Getting storage directory from np-config.")
        rig_model_dir = np.get_rig_storage_directory()

    current_model_path = rigs.copy_rig(
        rig_name,
        rig_model_path,
        rig_model_dir,
    )

    logger.info("Current model path: %s" % current_model_path)
    settings_sources = list(session_dir.glob("**/settings.xml"))
    logger.info("Scraped open ephys settings: %s" % settings_sources)

    updated_model_path = update.update_rig(
        rig_model_path,
        modification_date=modification_date,
        open_ephys_settings_sources=settings_sources,
        output_path=rig_model_path,
    )

    update_session_from_rig(
        scraped_session_model_path,
        updated_model_path,
        scraped_session_model_path,
    )

    storage.update_item(
        rig_model_dir,
        updated_model_path,
        rig_name,
    )


def update_neuropixels_rig_from_dynamic_routing_session_dir(
    rig_source: pathlib.Path,
    session_dir: pathlib.Path,
    output_path: pathlib.Path = pathlib.Path("rig.json"),
    modification_date: typing.Optional[datetime.date] = None,
    mvr_mapping: dict[str, str] = common.DEFAULT_MVR_MAPPING,
) -> pathlib.Path:
    """Scrapes dynamic routing session directory for various rig
    configuration/settings and updates `rig_source`.

    Notes
    -----
    - Will likely be depreciated in the future.
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

    return update.update_rig(
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
