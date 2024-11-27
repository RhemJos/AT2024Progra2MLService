import json
import logging

from utils.file_utils import extract_filename
from utils.path_utils import normalize_path


class DetectedFrame:
    def __init__(self, path, algorithm, word, percentage, time):
        self.path = extract_filename(normalize_path(path))
        self.algorithm = algorithm
        self.word = word
        self.percentage = percentage
        self.time = self.get_time()

    def to_json(self):
        # Dictionary built with the data
        data = {
            "name": self.path,
            "algorithm": self.algorithm,
            "word": self.word,
            "percentage": self.percentage,
            "second": self.time
        }
        # data Dictionary converted in json
        return json.dumps(data, indent=4)

    def __str__(self):
        return (f"DetectedFrame(path={self.path}, algorithm={self.algorithm}, "
                f"word={self.word}, percentage={self.percentage}%, "
                f"second={self.time})")

    def get_time(self) -> str:
        # Split the path by '/' to obtain the name that will be the time
        parts = self.path.split('/')

        # get the last part (file name) and split the extension
        if parts:
            filename = parts[-1].split('.')[0]

            # If the name is a number it will be the time
            if filename.isdigit():
                return filename
            else:
                logging.warning("No valid time found in the text.")
                return "No valid time found in the text."
        return "No valid time found in the text."
