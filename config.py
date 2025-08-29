# config.py
import os
from typing import Dict, Any

class Config:
    """Configuration settings for the prediction market flow"""
    
    # LLM Settings
    OLLAMA_BASE_URL = "http://localhost:11434"
    MODEL_NAME = "ollama/llama3.2"
    
    # Scraping Settings
    SCRAPING_DELAY = 2  # seconds between requests
    MAX_RETRIES = 3
    TIMEOUT = 30
    
    # Target Websites
    WEBSITES = [
        {
            "name": "Polymarket",
            "url": "https://polymarket.com",
            "selectors": {
                "market_name": ".market-title",
                "price": ".price",
                "probability": ".probability"
            }
        },
        {
            "name": "Kalshi", 
            "url": "https://kalshi.com",
            "selectors": {
                "market_name": ".event-title",
                "price": ".contract-price",
                "probability": ".probability-display"
            }
        },
        {
            "name": "PredictIt",
            "url": "https://www.predictit.org",
            "selectors": {
                "market_name": ".market-name",
                "price": ".last-price",
                "probability": ".percentage"
            }
        }
    ]
    
    # Output Settings
    OUTPUT_CSV = "unified_prediction_markets.csv"
    BACKUP_CSV = "prediction_markets_backup.csv"
    
    # Validation Settings
    MIN_CONFIDENCE_THRESHOLD = 50.0
    MIN_PRICE = 0.01
    MAX_PRICE = 0.99
    
    @classmethod
    def get_env_config(cls) -> Dict[str, Any]:
        """Get environment-specific configuration"""
        return {
            "OLLAMA_API_BASE": os.getenv("OLLAMA_API_BASE", cls.OLLAMA_BASE_URL),
            "MODEL_NAME": os.getenv("MODEL_NAME", cls.MODEL_NAME),
            "OUTPUT_DIR": os.getenv("OUTPUT_DIR", "./output"),
            "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO")
        }