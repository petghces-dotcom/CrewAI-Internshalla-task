# test_flow.py
import unittest
import json
import os
from unittest.mock import Mock, patch
from main import PredictionMarketFlow
import pandas as pd

class TestPredictionMarketFlow(unittest.TestCase):
    """Test cases for the prediction market flow"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.flow = PredictionMarketFlow()
        
        # Mock data for testing
        self.sample_data = {
            "website_name": "TestSite",
            "products": [
                {
                    "name": "Test Market 1",
                    "description": "Test description",
                    "price": 0.65,
                    "probability": 65.0,
                    "category": "politics",
                    "source": "TestSite"
                },
                {
                    "name": "Test Market 2", 
                    "description": "Another test",
                    "price": 0.45,
                    "probability": 45.0,
                    "category": "sports",
                    "source": "TestSite"
                }
            ]
        }
    
    @patch('main.ScrapeWebsiteTool')
    def test_data_collection(self, mock_scraper):
        """Test data collection phase"""
        mock_scraper.return_value._run.return_value = json.dumps(self.sample_data)
        
        result = self.flow.collect_data()
        
        self.assertEqual(result["status"], "success")
        self.assertIn("raw_data", result)
    
    def test_csv_processing(self):
        """Test CSV processing functionality"""
        test_products = [
            {
                "unified_name": "Test Unified Market",
                "products": self.sample_data["products"],
                "average_price": 0.55,
                "confidence_level": 85.0,
                "sources": ["TestSite"]
            }
        ]
        
        csv_path = self.flow._process_csv_output(test_products)
        
        self.assertTrue(os.path.exists(csv_path))
        
        # Verify CSV content
        df = pd.read_csv(csv_path, comment='#')
        self.assertGreater(len(df), 0)
        self.assertIn('unified_name', df.columns)
        self.assertIn('confidence_level', df.columns)
    
    def test_price_validation(self):
        """Test price parsing and validation"""
        from tools import PredictionMarketScraper
        
        scraper = PredictionMarketScraper()
        
        # Test various price formats
        test_cases = [
            ("$0.65", 0.65),
            ("65%", 0.65),
            ("65¢", 0.65),
            ("0.45", 0.45),
            ("invalid", 0.5)  # fallback
        ]
        
        for price_text, expected in test_cases:
            result = scraper._parse_price(price_text)
            self.assertAlmostEqual(result, expected, places=2)
    
    def tearDown(self):
        """Clean up test files"""
        test_files = [
            'unified_prediction_markets.csv',
            'unified_prediction_markets_fallback.csv',
            'unified_prediction_markets_error.csv'
        ]
        
        for file in test_files:
            if os.path.exists(file):
                os.remove(file)

if __name__ == '__main__':
    unittest.main()