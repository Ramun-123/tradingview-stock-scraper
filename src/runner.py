import json
import logging
from pathlib import Path
from extractors.tradingview_parser import TradingViewParser
from outputs.exporters import Exporter

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def load_inputs(path: str):
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file.readlines() if line.strip()]

def main():
    inputs_path = "data/inputs.sample.txt"
    symbols = load_inputs(inputs_path)

    parser = TradingViewParser()
    results = []

    for symbol_url in symbols:
        try:
            logging.info(f"Processing {symbol_url} ...")
            data = parser.parse(symbol_url)
            results.append(data)
        except Exception as e:
            logging.error(f"Error parsing {symbol_url}: {e}")

    Exporter.export_json(results, "output.json")
    Exporter.export_csv(results, "output.csv")
    Exporter.export_excel(results, "output.xlsx")
    logging.info("Export completed successfully.")

if __name__ == "__main__":
    main()