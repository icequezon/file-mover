from src import constants
from src.classifiers.rule_classifier import RuleClassifier
from src.utils.metadata import extract_date_info
from src.logger import logger
from src.exceptions import MissingFileException, IgnoreDotfileException

from pathlib import Path

import shutil


class FileMover:
    def __init__(self, config):
        self.rule_classifier = RuleClassifier(config["rules"])
        self.default_destination = config["settings"]["default_destination"]
        self.ignore_dotfiles = config["settings"]["ignore_dotfiles"]

    def handle_event(self, event):
        logger.info(f"Handling event: {event}")
        path = Path(event[constants.REDIS_EVENT_PATH_KEY].decode("utf-8"))
        event_type = event[constants.REDIS_EVENT_TYPE_KEY].decode("utf-8")

        self.check_dotfiles(path)

        if constants.INOTIFY_CREATE_EVENT in event_type:
            logger.debug("File was just created. Waiting for file copy to finish.")
            return

        if constants.INOTIFY_DELETE_EVENT in event_type:
            logger.debug("File was just deleted. Skipping...")
            return

        if constants.INOTIFY_FINISHED_WRITE_EVENT not in event_type:
            logger.debug(f"Event {event} not supported")
            return

        if not path.exists():
            raise MissingFileException("File not found")

        rule = self.rule_classifier.match(path, event_type)
        if rule:
            logger.debug(f"Applying rule: {rule['name']} to {str(path)}")
            dest_pattern = rule.get("destination_pattern") or rule.get("destination")
            if rule.get("use_metadata_date"):
                date_info = extract_date_info(path)
                dest = Path(dest_pattern.format(**date_info))
            else:
                dest = Path(dest_pattern)
        else:
            logger.debug(
                f"Did not find an applicable rule for {str(path)}. Using default"
            )
            dest = Path(self.default_destination)

        logger.info(f"Moving {path} to {dest}")
        dest.mkdir(parents=True, exist_ok=True)
        shutil.move(str(path), str(dest / path.name))

        logger.info(f"Moved {path} to {dest}")

    def check_dotfiles(self, path):
        starting_char = path.name[0]
        is_dotfile = starting_char == '.'
        if self.ignore_dotfiles and is_dotfile:
            raise IgnoreDotfileException("Ignore dot files.")
