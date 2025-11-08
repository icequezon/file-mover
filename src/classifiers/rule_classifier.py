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

            if exts and contains:
                if path.suffix in exts and contains in str(path):
                    return rule
            elif exts:
                if path.suffix in exts:
                    return rule
            elif contains:
                if contains in str(path):
                    return rule

        return None
