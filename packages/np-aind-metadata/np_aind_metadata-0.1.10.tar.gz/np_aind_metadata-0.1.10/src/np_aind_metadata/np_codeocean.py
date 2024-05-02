import datetime
import logging
import pathlib

from aind_data_schema.core import rig, session

from np_aind_metadata import storage, update

logger = logging.getLogger(__name__)


def scrape_session_model_path(session_directory: pathlib.Path) -> pathlib.Path:
    """Scrapes aind-metadata session json from dynamic routing session
    directory.
    """
    matches = list(session_directory.glob("*session.json"))
    logger.debug("Scraped session model paths: %s" % matches)
    return matches[0]


# def parse_rig_id(rig_id: str) -> tuple[str, str]:
#     """Parses rig id, returning rig name and date.

#     >>> parse_rig_id("323_NP3_210101")
#     ('NP3', '210101')
#     """
#     split = rig_id.split("_")
#     return split[-2], split[-1]


def add_rig_to_dynamic_routing_session_dir(
    session_dir: pathlib.Path,
    rig_model_dir: pathlib.Path,
    modification_date: datetime.date,
) -> pathlib.Path:
    """Direct support for np_codeocean. Adds an aind-metadata rig model
    rig.json to a dynamic routing session directory. If rig_id is updated,
     will update the associated session json.

    Notes
    -----
    - An aind metadata session json must exist and be ending with filename
    session.json (pattern: `*session.json`) in the root directory.
    """
    matches = list(session_dir.glob("*session.json"))
    logger.debug("Scraped session model paths: %s" % matches)
    scraped_session_model_path = matches[0]
    logger.debug("Scraped session model path: %s" % scraped_session_model_path)
    scraped_session = session.Session.model_validate_json(
        scraped_session_model_path.read_text()
    )
    scraped_rig_id = scraped_session.rig_id
    logger.info("Scraped rig id: %s" % scraped_rig_id)
    _, rig_name, _ = scraped_rig_id.split("_")
    logger.info("Parsed rig name: %s" % rig_name)
    current_model_path = storage.get_item(
        rig_model_dir,
        rig_name,
    )
    logger.info("Current model path: %s" % current_model_path)
    settings_sources = list(session_dir.glob("**/settings.xml"))
    logger.info("Scraped open ephys settings: %s" % settings_sources)
    current_model = rig.Rig.model_validate_json(current_model_path.read_text())
    current_model.write_standard_file(session_dir)
    rig_model_path = session_dir / "rig.json"
    updated_model_path = update.update_neuropixels_rig(
        rig_model_path,
        open_ephys_settings_sources=settings_sources,
        output_path=rig_model_path,
    )
    updated_model_path = update.update_rig_modification_date(
        updated_model_path,
        modification_date,
    )
    update.update_session_modification_date(
        scraped_session_model_path,
        modification_date,
    )
    storage.update_item(
        rig_model_dir,
        updated_model_path,
        rig_name,
    )

    return updated_model_path
