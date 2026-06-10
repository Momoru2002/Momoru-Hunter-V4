import json
from momoru.logger import CyberpunkLogger

class JsonExporter:
    @staticmethod
    def export(data: dict, output_path: str):
        with open(output_path, "w") as f:
            json.dump(data, f, indent=4)
        CyberpunkLogger.success(f"Metrics saved into data stream: {output_path}")