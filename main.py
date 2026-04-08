# main.py

from collectors.sensor_collector import SensorCollector
from collectors.weather_collector import WeatherCollector
from collectors.image_collector import ImageCollector
from collectors.market_collector import MarketCollector

from processors.cleaning import DataCleaner
from processors.standardization import DataStandardizer
from processors.synchronization import DataSynchronizer
from processors.reliability import ReliabilityScorer

from storage.json_storage import JSONStorage
from storage.buffer import Buffer

from utils.logger import get_logger
from utils.ollama_integration import OllamaValidator

# Optional API
from api.routes import DataAPI

import uvicorn
from fastapi import FastAPI
from datetime import datetime

# -----------------------------------
# INITIALIZATION
# -----------------------------------

logger = get_logger(__name__)

# Collectors
sensor_collector = SensorCollector()
weather_collector = WeatherCollector()
image_collector = ImageCollector()
market_collector = MarketCollector()

# Processors
cleaner = DataCleaner()
standardizer = DataStandardizer()
synchronizer = DataSynchronizer()
scorer = ReliabilityScorer()

# Storage
DATA_FILE_PATH = "data/processed_data.json"
storage = JSONStorage(file_path=DATA_FILE_PATH)
buffer = Buffer(max_size=10)

# Optional AI Validator
validator = OllamaValidator()

# -----------------------------------
# PIPELINE FUNCTION
# -----------------------------------

def run_pipeline():
    """
    Runs one cycle of the data ingestion pipeline.
    """
    try:
        logger.info("Starting data collection...")

        # Step 1: Collect data
        sensor_data = sensor_collector.collect()
        weather_data = weather_collector.collect()
        image_data = image_collector.collect()
        market_data = market_collector.collect()

        logger.info("Data collected successfully.")

        # Step 2: Standardize data
        timestamp = datetime.utcnow().isoformat()
        standardized_data = standardizer.standardize_data(
            timestamp=timestamp,
            sensor_data=sensor_data,
            weather_data=weather_data,
            image_data=image_data,
            market_data=market_data
        )

        # Step 3: Synchronize
        synced_data = synchronizer.synchronize(standardized_data)

        # Step 4: Compute reliability and optional AI validation
        processed_records = []
        for record in synced_data:
            try:
                # Compute reliability score
                record["reliability_score"] = scorer.compute(record)

                # AI validation via Ollama
                record["validation"] = validator.validate(record)

            except Exception as e:
                logger.warning(
                    f"Validator or scorer failed for record {record.get('field_id', '')}: {e}"
                )
                # Assign default values if processing fails
                record.setdefault("reliability_score", 0)
                record.setdefault("validation", {"status": "failed", "error": str(e)})

            processed_records.append(record)

        logger.info(f"Data processed successfully. Total records: {len(processed_records)}")

        # Step 5: Store or buffer (append whole batch)
        try:
            storage.append(processed_records)
        except Exception:
            logger.warning("Storage failed, buffering data...")
            buffer.add(processed_records)

        # Step 6: Flush buffer if possible
        if buffer.get_all():
            logger.info("Attempting buffer flush...")
            buffer.flush(storage.append)

        logger.info("Pipeline cycle completed successfully.")

    except Exception as e:
        logger.error(f"Pipeline error: {e}")


# -----------------------------------
# MAIN ENTRY POINT
# -----------------------------------

if __name__ == "__main__":

    # Run one pipeline cycle
    run_pipeline()

    # Start API server
    logger.info("Starting API server...")

    app = FastAPI()
    api = DataAPI(data_file_path=DATA_FILE_PATH)  # ensure API uses same storage
    app.include_router(api.router)

    uvicorn.run(app, host="0.0.0.0", port=8000)


#http://127.0.0.1:8000/docs