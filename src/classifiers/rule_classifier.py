from pathlib import Path

from src.logger import logger


class RuleClassifier:
    def __init__(self, rules):
        self.rules = rules

    def match(self, file_path, event_type):
        path = Path(str(file_path))
        for rule in self.rules:
            match = rule.get("match", {})
            logger.info((path.suffix, match.get("extensions")))
            if match.get("extensions") and path.suffix in match["extensions"]:
                return rule
            if match.get("contains") and match["contains"] in str(path):
                return rule
        return None
