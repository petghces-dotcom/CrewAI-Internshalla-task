# tools.py
import time
import requests
from typing import List, Dict, Any, Optional
from crewai_tools import BaseTool
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import logging

logger = logging.getLogger(__name__)

class PredictionMarketScraper(BaseTool):
    """Custom tool for scraping prediction market data"""
    
    name: str = "Prediction Market Scraper"
    description: str = "Scrapes prediction market data from various betting platforms"
    
    def __init__(self):
        super().__init__()
        self.setup_selenium()
    
    def setup_selenium(self):
        """Setup Selenium WebDriver with proper configuration"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            logger.info("Selenium WebDriver initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize WebDriver: {str(e)}")
            self.driver = None
    
    def _run(self, website_url: str, selectors: Dict[str, str] = None) -> str:
        """Execute the scraping operation"""
        try:
            if not self.driver:
                return "Error: WebDriver not initialized"
            
            logger.info(f"Scraping data from: {website_url}")
            
            # Navigate to website
            self.driver.get(website_url)
            time.sleep(3)  # Wait for page load
            
            # Wait for content to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Extract data based on website
            if "polymarket" in website_url.lower():
                return self._scrape_polymarket()
            elif "kalshi" in website_url.lower():
                return self._scrape_kalshi()
            elif "predictit" in website_url.lower():
                return self._scrape_predictit()
            else:
                return self._generic_scrape()
                
        except Exception as e:
            logger.error(f"Scraping failed for {website_url}: {str(e)}")
            return f"Error scraping {website_url}: {str(e)}"
    
    def _scrape_polymarket(self) -> str:
        """Scrape Polymarket data"""
        try:
            markets = []
            
            # Look for market elements (adjust selectors based on actual site structure)
            market_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid*='market'], .market-card, .event-card")
            
            for element in market_elements[:10]:  # Limit to first 10 markets
                try:
                    # Extract market name
                    name_elem = element.find_element(By.CSS_SELECTOR, "h3, .title, .market-title")
                    name = name_elem.text.strip()
                    
                    # Extract price/probability
                    price_elem = element.find_element(By.CSS_SELECTOR, ".price, .probability, [data-testid*='price']")
                    price_text = price_elem.text.strip()
                    
                    # Parse price
                    price = self._parse_price(price_text)
                    
                    if name and price > 0:
                        markets.append({
                            "name": name,
                            "description": name,
                            "price": price,
                            "probability": price * 100,
                            "category": "politics",  # Default category
                            "source": "Polymarket"
                        })
                        
                except Exception as e:
                    logger.debug(f"Error parsing market element: {str(e)}")
                    continue
            
            return json.dumps({"website_name": "Polymarket", "products": markets})
            
        except Exception as e:
            logger.error(f"Polymarket scraping error: {str(e)}")
            return json.dumps({"website_name": "Polymarket", "products": [], "error": str(e)})
    
    def _scrape_kalshi(self) -> str:
        """Scrape Kalshi data"""
        try:
            markets = []
            
            # Look for event elements
            event_elements = self.driver.find_elements(By.CSS_SELECTOR, ".event, .market, [data-testid*='event']")
            
            for element in event_elements[:10]:
                try:
                    # Extract event name
                    name_elem = element.find_element(By.CSS_SELECTOR, ".event-title, .title, h3")
                    name = name_elem.text.strip()
                    
                    # Extract price
                    price_elem = element.find_element(By.CSS_SELECTOR, ".price, .last-price, [data-testid*='price']")
                    price_text = price_elem.text.strip()
                    
                    price = self._parse_price(price_text)
                    
                    if name and price > 0:
                        markets.append({
                            "name": name,
                            "description": name,
                            "price": price,
                            "probability": price * 100,
                            "category": "events",
                            "source": "Kalshi"
                        })
                        
                except Exception as e:
                    continue
            
            return json.dumps({"website_name": "Kalshi", "products": markets})
            
        except Exception as e:
            return json.dumps({"website_name": "Kalshi", "products": [], "error": str(e)})
    
    def _scrape_predictit(self) -> str:
        """Scrape PredictIt data"""
        try:
            markets = []
            
            # Look for market elements
            market_elements = self.driver.find_elements(By.CSS_SELECTOR, ".market, .contract, [data-testid*='market']")
            
            for element in market_elements[:10]:
                try:
                    # Extract market name
                    name_elem = element.find_element(By.CSS_SELECTOR, ".market-name, .title, h3")
                    name = name_elem.text.strip()
                    
                    # Extract price
                    price_elem = element.find_element(By.CSS_SELECTOR, ".last-price, .price, .buy-price")
                    price_text = price_elem.text.strip()
                    
                    price = self._parse_price(price_text)
                    
                    if name and price > 0:
                        markets.append({
                            "name": name,
                            "description": name,
                            "price": price,
                            "probability": price * 100,
                            "category": "politics",
                            "source": "PredictIt"
                        })
                        
                except Exception as e:
                    continue
            
            return json.dumps({"website_name": "PredictIt", "products": markets})
            
        except Exception as e:
            return json.dumps({"website_name": "PredictIt", "products": [], "error": str(e)})
    
    def _generic_scrape(self) -> str:
        """Generic scraping for unknown sites"""
        try:
            # Get page title and basic content
            title = self.driver.title
            
            # Look for common price/market patterns
            elements = self.driver.find_elements(By.CSS_SELECTOR, "[class*='market'], [class*='price'], [class*='bet']")
            
            content = []
            for elem in elements[:5]:
                text = elem.text.strip()
                if len(text) > 0 and len(text) < 200:
                    content.append(text)
            
            return json.dumps({
                "website_name": "Generic",
                "title": title,
                "content": content,
                "products": []
            })
            
        except Exception as e:
            return json.dumps({"website_name": "Generic", "products": [], "error": str(e)})
    
    def _parse_price(self, price_text: str) -> float:
        """Parse price from text"""
        try:
            # Remove common symbols and text
            import re
            
            # Look for decimal numbers
            matches = re.findall(r'(\d+\.?\d*)', price_text.replace('$', '').replace('¢', '').replace('%', ''))
            
            if matches:
                price = float(matches[0])
                
                # Convert percentage to decimal
                if '%' in price_text or price > 1:
                    price = price / 100
                
                # Ensure reasonable range
                return max(0.01, min(0.99, price))
            
            return 0.5  # Default fallback
            
        except:
            return 0.5
    
    def cleanup(self):
        """Cleanup WebDriver resources"""
        if self.driver:
            self.driver.quit()
            logger.info("WebDriver cleanup completed")