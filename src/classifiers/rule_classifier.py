from pathlib import Path


class RuleClassifier:
    def __init__(self, rules):
        self.rules = rules

    def match(self, file_path):
        path = Path(file_path)
        for rule in self.rules:
            match = rule.get("match", {})
            exts = match.get("extensions")
            contains = match.get("contains")
            path_suffix = path.suffix.lower()

            if exts and contains:
                if path_suffix in exts and contains in str(path):
                    return rule
            elif exts and path_suffix in exts:
                return rule
            elif contains and contains in str(path):
                return rule

        return None
