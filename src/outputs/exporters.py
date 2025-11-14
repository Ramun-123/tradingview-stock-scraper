import json
import csv
import logging
import pandas as pd

class Exporter:
    @staticmethod
    def export_json(data, filename):
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        logging.info(f"JSON exported: {filename}")

    @staticmethod
    def export_csv(data, filename):
        if not data:
            return
        keys = data[0].keys()
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=keys)
            writer.writeheader()
            for row in data:
                writer.writerow(row)
        logging.info(f"CSV exported: {filename}")

    @staticmethod
    def export_excel(data, filename):
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)
        logging.info(f"Excel exported: {filename}")