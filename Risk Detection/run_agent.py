# run_agent.py
import os
import json
from utils.logger import get_logger
from agents.risk_agent import RiskDetectionAgent
from config.crop_rules import CROP_RULES
from utils.input_utils import load_input_data, generate_random_input  # helper functions

logger = get_logger(__name__)

def main():
    # Initialize the agent
    agent = RiskDetectionAgent()  # optionally pass image_dataset_path if needed

    # Load input data from ingestion output or fallback
    # Adjust path relative to this script
    ingestion_json_path = os.path.join(
        os.path.dirname(__file__),
        "..",  # Go up to Smart_Horizon
        "Data Ingestion",
        "data",
        "processed_data.json"
    )

    input_data = load_input_data(json_path=ingestion_json_path)

    results = []
    for record in input_data:
        # Select a random image from the dataset for disease detection
        image_path = agent.get_random_image()
        result = agent.detect_risk(record, image_path)
        results.append(result)

    # Save results to JSON
    output_path = os.path.join(os.path.dirname(__file__), "data", "risk_results.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(results, f, indent=4)

    logger.info(f"Processed {len(results)} records. Results saved to {output_path}")

    # Print results to console
    for r in results:
        print(json.dumps(r, indent=4))

if __name__ == "__main__":
    main()