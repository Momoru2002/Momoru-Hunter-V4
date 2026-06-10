import csv
from momoru.logger import CyberpunkLogger

class CsvExporter:
    @staticmethod
    def export(data: dict, output_path: str):
        with open(output_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(data.keys())
            writer.writerow(data.values())
        CyberpunkLogger.success(f"Metrics flattened into tabular state: {output_path}")