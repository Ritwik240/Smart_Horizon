# utils/input_utils.py

import os
import json
import random
import requests
from agents.risk_agent import RiskDetectionAgent

def fetch_from_api(api_url: str):
    """
    Fetches field data from the ingestion API.
    Returns a list of records or empty list if API fails.
    """
    try:
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list):
            print(f"[INFO] Fetched {len(data)} records from API")
            return data
        print("[WARN] API returned non-list data")
        return []
    except Exception as e:
        print(f"[WARN] Failed to fetch from API: {e}")
        return []

def load_from_json(json_path: str):
    """
    Loads input data from a JSON file.
    """
    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            data = json.load(f)
        if isinstance(data, list):
            print(f"[INFO] Loaded {len(data)} records from JSON")
            return data
        print("[WARN] JSON content is not a list")
        return []
    print(f"[WARN] JSON file not found: {json_path}")
    return []

def load_input_data(api_url: str = None, json_path: str = None):
    """
    Attempts to load input data from API first; falls back to JSON file; if both fail, generates a single random input.
    """
    data = []
    if api_url:
        data = fetch_from_api(api_url)
    if not data and json_path:
        data = load_from_json(json_path)
    if not data:
        print("[INFO] Using fallback random input for demo")
        data = [RiskDetectionAgent.generate_random_input()]
    return data

def generate_random_input():
    """
    Generates a random input record compatible with RiskDetectionAgent.
    """
    return {
        "crop": random.choice(["rice", "wheat", "cotton", "sugarcane"]),
        "temperature": random.uniform(5, 45),
        "humidity": random.uniform(30, 90),
        "soil_moisture": random.uniform(20, 80),
        "ndvi": random.uniform(0.2, 0.9)
    }