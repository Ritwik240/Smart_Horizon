# storage/json_storage.py

import os
import json
from typing import List, Dict, Any

class JSONStorage:
    """
    Handles saving and loading of JSON files for RiskDetectionAgent outputs.
    """

    def __init__(self, file_path: str = "data/risk_results.json"):
        self.file_path = file_path
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def save(self, data: List[Dict[str, Any]]) -> None:
        """
        Saves a list of dictionaries to the JSON file.
        """
        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=4)

    def load(self) -> List[Dict[str, Any]]:
        """
        Loads data from the JSON file. Returns empty list if file does not exist.
        """
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                return json.load(f)
        return []

    def append(self, records: List[Dict[str, Any]]) -> None:
        """
        Appends new records to the JSON file.
        """
        existing_data = self.load()
        existing_data.extend(records)
        self.save(existing_data)