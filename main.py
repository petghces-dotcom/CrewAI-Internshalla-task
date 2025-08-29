# main.py
import os
import json
import pandas as pd
import logging
from typing import List, Dict, Any
from crewai import Agent, Task, Crew, Flow
from crewai.flow.flow import listen, start
from crewai_tools import ScrapeWebsiteTool, SeleniumScrapingTool
from crewai.llm import LLM
from pydantic import BaseModel
import litellm
import json
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configure LiteLLM for local Ollama
os.environ["OLLAMA_API_BASE"] = "http://localhost:11434"

class ProductData(BaseModel):
    """Model for product data validation"""
    name: str
    description: str
    price: float
    probability: float
    source: str
    category: str = "prediction"

class UnifiedProduct(BaseModel):
    """Model for unified product data"""
    unified_name: str
    products: List[ProductData]
    average_price: float
    confidence_level: float
    sources: List[str]

class PredictionMarketFlow(Flow):
    """Main flow for prediction market data processing"""
    
    def __init__(self):
        super().__init__()
        # Initialize LLM with Ollama
        self.llm = LLM(
            model="ollama/llama3.2",
            base_url="http://localhost:11434"
        )
        
        # Initialize tools
        self.scrape_tool = ScrapeWebsiteTool()
        self.selenium_tool = SeleniumScrapingTool()
        
        # Initialize agents
        self.data_collector = self._create_data_collector()
        self.product_analyzer = self._create_product_analyzer()
        self.csv_generator = self._create_csv_generator()
        
        logger.info("PredictionMarketFlow initialized successfully")

    def _create_data_collector(self) -> Agent:
        """Create the data collection agent"""
        return Agent(
            role="Data Collector",
            goal="Scrape and collect prediction market data from multiple websites",
            backstory="""You are an expert web scraper specialized in extracting 
            prediction market data. You understand the structure of betting platforms 
            and can efficiently gather product information including names, prices, 
            and probabilities.""",
            tools=[self.scrape_tool, self.selenium_tool],
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )

    def _create_product_analyzer(self) -> Agent:
        """Create the product analysis agent"""
        return Agent(
            role="Product Analyzer",
            goal="Analyze collected data to identify similar products across platforms",
            backstory="""You are a data analyst expert in prediction markets. 
            You can identify when different platforms offer the same or similar 
            betting products by analyzing their descriptions, categories, and 
            market characteristics.""",
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )

    def _create_csv_generator(self) -> Agent:
        """Create the CSV generation agent"""
        return Agent(
            role="CSV Generator",
            goal="Transform analyzed data into a well-structured CSV format",
            backstory="""You are a data formatting specialist who creates 
            clean, organized CSV files from complex data structures. You ensure 
            proper formatting and include all necessary columns for analysis.""",
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )

    @start()
    def collect_data(self) -> Dict[str, Any]:
        """Step 1: Collect data from prediction market websites"""
        logger.info("Starting data collection phase")
        
        websites = [
            "https://www.polymarket.com",
            "https://www.kalshi.com", 
            "https://www.predictit.org"
        ]
        
        collection_task = Task(
            description=f"""
            Scrape prediction market data from these websites: {websites}
            
            For each website, extract:
            1. Product/market names
            2. Current prices/odds
            3. Probabilities (if available)
            4. Categories
            5. Descriptions
            
            Focus on active markets and popular categories like politics, 
            sports, economics, and current events.
            
            Return the data in JSON format with the following structure:
            {{
                "website_name": "site_url",
                "products": [
                    {{
                        "name": "product_name",
                        "description": "product_description", 
                        "price": 0.65,
                        "probability": 65.0,
                        "category": "politics",
                        "source": "website_name"
                    }}
                ]
            }}
            
            Guardrail: Ensure you only scrape publicly available data and 
            respect robots.txt. If a site blocks scraping, document this 
            and continue with other sites.
            """,
            agent=self.data_collector,
            expected_output="JSON formatted data containing prediction market products from multiple websites"
        )
        
        try:
            result = collection_task.execute_sync()
            logger.info("Data collection completed successfully")
            return {"raw_data": result, "status": "success"}
        except Exception as e:
            logger.error(f"Data collection failed: {str(e)}")
            return {"raw_data": [], "status": "failed", "error": str(e)}

    @listen(collect_data)
    def analyze_products(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Step 2: Analyze and identify similar products"""
        logger.info("Starting product analysis phase")
        
        if context.get("status") != "success":
            logger.warning("Skipping analysis due to collection failure")
            return {"unified_products": [], "status": "skipped"}
        
        analysis_task = Task(
            description=f"""
            Analyze the collected prediction market data to identify similar 
            or identical products across different platforms.
            
            Input data: {context.get('raw_data', '')}
            
            Your analysis should:
            1. Group similar products together based on:
               - Market subject/topic
               - Event being predicted
               - Time frame
               - Category
            
            2. Calculate confidence levels for matches (0-100%):
               - 90-100%: Identical markets
               - 70-89%: Very similar markets
               - 50-69%: Somewhat similar markets
               - Below 50%: Different markets
            
            3. For each unified product group, provide:
               - Unified name (most descriptive)
               - List of source products
               - Average price across platforms
               - Confidence level for the grouping
            
            Return results in JSON format:
            {{
                "unified_products": [
                    {{
                        "unified_name": "descriptive_name",
                        "products": [list_of_source_products],
                        "average_price": 0.67,
                        "confidence_level": 85.5,
                        "sources": ["site1", "site2"]
                    }}
                ]
            }}
            
            Guardrail: Only group products with confidence level >= 50%. 
            Be conservative in matching to avoid false positives.
            """,
            agent=self.product_analyzer,
            expected_output="JSON formatted unified product analysis with confidence levels"
        )
        
        try:
            result = analysis_task.execute_sync()
            logger.info("Product analysis completed successfully")
            return {"unified_products": result, "status": "success"}
        except Exception as e:
            logger.error(f"Product analysis failed: {str(e)}")
            return {"unified_products": [], "status": "failed", "error": str(e)}

    @listen(analyze_products)
    def generate_csv(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Step 3: Generate final CSV output"""
        logger.info("Starting CSV generation phase")
        
        if context.get("status") != "success":
            logger.warning("Skipping CSV generation due to analysis failure")
            return {"csv_path": None, "status": "skipped"}
        
        csv_task = Task(
            description=f"""
            Convert the unified product analysis into a well-formatted CSV file.
            
            Input data: {context.get('unified_products', '')}
            
            Create a CSV with the following columns:
            1. unified_name - The unified product name
            2. source_products - Comma-separated list of source product names
            3. average_price - Average price across platforms
            4. price_variance - Standard deviation of prices
            5. confidence_level - Confidence in product matching
            6. source_count - Number of sources offering this product
            7. sources - Comma-separated list of source websites
            8. category - Product category
            9. min_price - Minimum price found
            10. max_price - Maximum price found
            
            Additional requirements:
            - Sort by confidence_level (descending) then by source_count (descending)
            - Include summary statistics at the top (total products, average confidence, etc.)
            - Handle missing data gracefully
            - Ensure proper CSV formatting with escaped commas in text fields
            
            Save the file as 'unified_prediction_markets.csv' and return the file path.
            
            Guardrail: Validate all numerical values and handle edge cases 
            like division by zero or missing price data.
            """,
            agent=self.csv_generator,
            expected_output="File path to generated CSV and summary statistics"
        )
        
        try:
            result = csv_task.execute_sync()
            
            # Additional CSV processing using pandas for robustness
            csv_path = self._process_csv_output(context.get('unified_products', []))
            
            logger.info(f"CSV generation completed successfully: {csv_path}")
            return {"csv_path": csv_path, "status": "success", "agent_result": result}
        except Exception as e:
            logger.error(f"CSV generation failed: {str(e)}")
            return {"csv_path": None, "status": "failed", "error": str(e)}

    def _process_csv_output(self, unified_products) -> str:
        """Process and validate CSV output using pandas"""
        try:
            rows = []
            
            # Debug: Print the actual structure we're working with
            print(f"Type of unified_products: {type(unified_products)}")
            print(f"unified_products.raw type: {type(unified_products.raw)}")
            
            # Handle the TaskOutput object - the actual data is in the raw attribute
            if hasattr(unified_products, 'raw'):
                raw_content = unified_products.raw
            else:
                raw_content = unified_products
            
            # The raw content is a string description with embedded JSON
            if isinstance(raw_content, str):
                print(f"Raw content length: {len(raw_content)}")
                print(f"Raw content preview: {raw_content[:1000]}")
                
                # Try to extract and fix the JSON
                product_groups = []
                
                # First, try to find the complete JSON structure
                import re
                
                # Find the start of the JSON
                json_start = raw_content.find('{\n    "unified_products":')
                if json_start == -1:
                    json_start = raw_content.find('{\n  "unified_products":')
                if json_start == -1:
                    json_start = raw_content.find('"unified_products":')
                    if json_start != -1:
                        # Back up to find the opening brace
                        for i in range(json_start, -1, -1):
                            if raw_content[i] == '{':
                                json_start = i
                                break
                
                if json_start != -1:
                    # Find the end - look for the closing brace that matches
                    brace_count = 0
                    json_end = -1
                    for i in range(json_start, len(raw_content)):
                        if raw_content[i] == '{':
                            brace_count += 1
                        elif raw_content[i] == '}':
                            brace_count -= 1
                            if brace_count == 0:
                                json_end = i + 1
                                break
                    
                    if json_end != -1:
                        json_str = raw_content[json_start:json_end]
                        print(f"Extracted JSON: {json_str[:500]}...")
                        
                        # Try to parse the JSON, with error recovery
                        try:
                            data = json.loads(json_str)
                            product_groups = data.get("unified_products", [])
                            print(f"Successfully parsed JSON with {len(product_groups)} groups")
                        except json.JSONDecodeError as e:
                            print(f"JSON parse error: {e}")
                            # Try to extract individual product groups manually
                            product_groups = self._extract_products_manually(raw_content)
                    else:
                        print("Could not find JSON end")
                        product_groups = self._extract_products_manually(raw_content)
                else:
                    print("Could not find JSON start")
                    product_groups = self._extract_products_manually(raw_content)
                    
            else:
                # If raw_content is already a dict/object
                if isinstance(raw_content, dict):
                    product_groups = raw_content.get("unified_products", [])
                else:
                    print(f"Unexpected raw_content type: {type(raw_content)}")
                    return self._create_fallback_csv()
            
            if not product_groups:
                print("No product groups found")
                return self._create_fallback_csv()
            
            print(f"Processing {len(product_groups)} product groups")
            
            # Process each product group
            for i, product_group in enumerate(product_groups):
                print(f'Processing group {i+1}: {product_group}')
                
                if not isinstance(product_group, dict):
                    print(f'Skipping non-dict item: {product_group}')
                    continue
                
                products = product_group.get('products', [])
                
                # Handle different product formats
                product_names = []
                prices = []
                
                if products:
                    for product in products:
                        if isinstance(product, str):
                            # Product is just a string name
                            product_names.append(product)
                        elif isinstance(product, dict):
                            # Product is a dict with name/price/site
                            name = product.get('name', str(product))
                            product_names.append(name)
                            
                            # Try to get price from individual product
                            if 'price' in product:
                                try:
                                    price = float(product['price'])
                                    prices.append(price)
                                except (ValueError, TypeError):
                                    pass
                        else:
                            product_names.append(str(product))
                
                # Use individual prices if available, otherwise use group average
                if prices:
                    avg_price = sum(prices) / len(prices)
                    min_price = min(prices)
                    max_price = max(prices)
                    price_variance = pd.Series(prices).std() if len(prices) > 1 else 0
                else:
                    # Fall back to group average price
                    group_avg_price = product_group.get('average_price', 0)
                    if group_avg_price > 0:
                        avg_price = float(group_avg_price)
                        min_price = max_price = avg_price
                        price_variance = 0
                    else:
                        avg_price = min_price = max_price = price_variance = 0
                
                print(f'Calculated prices - avg: {avg_price}, min: {min_price}, max: {max_price}')
                
                # Extract category from unified name
                unified_name = str(product_group.get('unified_name', 'Unknown'))
                unified_name_lower = unified_name.lower()
                category = 'Other'  # Default
                
                if any(keyword in unified_name_lower for keyword in ['bitcoin', 'ethereum', 'solana', 'crypto', 'financial', 'market']):
                    category = 'Financial Markets'
                elif any(keyword in unified_name_lower for keyword in ['election', 'presidential', 'politics']):
                    category = 'Politics'
                elif any(keyword in unified_name_lower for keyword in ['world cup', 'super bowl', 'world series', 'uefa', 'champions', 'f1', 'nfl', 'sports']):
                    category = 'Sports'
                elif 'nobel' in unified_name_lower:
                    category = 'Awards'
                
                # Create row
                row = {
                    'unified_name': unified_name,
                    'source_products': '; '.join(product_names),
                    'average_price': round(avg_price, 4),
                    'price_variance': round(price_variance, 4),
                    'confidence_level': round(float(product_group.get('confidence_level', 0)), 2),
                    'source_count': len(products),
                    'sources': '; '.join(str(s) for s in product_group.get('sources', [])),
                    'category': category,
                    'min_price': round(min_price, 4),
                    'max_price': round(max_price, 4)
                }
                rows.append(row)
                print(f'Created row: {row}')
            
            print("============================")
            print(f"Total rows created: {len(rows)}")
            print("============================")
            
            # Create DataFrame and sort
            df = pd.DataFrame(rows)
            if not df.empty:
                df = df.sort_values(['confidence_level', 'source_count'], ascending=[False, False])
                print(f"DataFrame created with {len(df)} rows")
            else:
                print("No valid data found, creating fallback")
                return self._create_fallback_csv()
            
            # Save CSV
            csv_path = 'unified_prediction_markets.csv'
            df.to_csv(csv_path, index=False, quoting=1)
            
            # Add summary statistics
            summary_stats = f"""# Summary Statistics
    # Total Products: {len(df)}
    # Average Confidence: {df['confidence_level'].mean():.2f}%
    # High Confidence Products (>80%): {len(df[df['confidence_level'] > 80])}
    # Multi-source Products: {len(df[df['source_count'] > 1])}
    #
    """
            
            # Read CSV and prepend summary
            with open(csv_path, 'r') as f:
                csv_content = f.read()
            
            with open(csv_path, 'w') as f:
                f.write(summary_stats + csv_content)
            
            print(f"Successfully created CSV: {csv_path}")
            return csv_path
            
        except Exception as e:
            logger.error(f"CSV processing error: {str(e)}")
            print(f"Exception details: {e}")
            import traceback
            traceback.print_exc()
            return self._create_fallback_csv()

    def _extract_products_manually(self, raw_content: str) -> list:
        """Manually extract product data when JSON parsing fails"""
        import re
        
        product_groups = []
        
        # Look for unified_name patterns
        name_pattern = r'"unified_name":\s*"([^"]*)"'
        price_pattern = r'"average_price":\s*([\d.]+)'
        confidence_pattern = r'"confidence_level":\s*([\d.]+)'
        
        # Find all unified names
        names = re.findall(name_pattern, raw_content)
        prices = re.findall(price_pattern, raw_content)
        confidences = re.findall(confidence_pattern, raw_content)
        
        print(f"Manual extraction found: {len(names)} names, {len(prices)} prices, {len(confidences)} confidences")
        
        # Create basic product groups from what we can extract
        for i, name in enumerate(names):
            group = {
                'unified_name': name,
                'products': [name],  # Use the unified name as the product
                'average_price': float(prices[i]) if i < len(prices) else 0,
                'confidence_level': float(confidences[i]) if i < len(confidences) else 0,
                'sources': ['extracted']
            }
            product_groups.append(group)
        
        return product_groups

    def _create_fallback_csv(self) -> str:
        """Create a fallback CSV when main processing fails"""
        print("Creating fallback CSV")
        fallback_df = pd.DataFrame([{
            'unified_name': 'Error in processing',
            'source_products': 'N/A',
            'average_price': 0,
            'price_variance': 0,
            'confidence_level': 0,
            'source_count': 0,
            'sources': 'N/A',
            'category': 'Error',
            'min_price': 0,
            'max_price': 0
        }])
        csv_path = 'unified_prediction_markets_fallback.csv'
        fallback_df.to_csv(csv_path, index=False, quoting=1)
        print(f"Fallback CSV saved to: {csv_path}")
        return csv_path

    def run_flow(self) -> str:
        """Execute the complete flow"""
        logger.info("Starting PredictionMarketFlow execution")
        
        try:
            # Execute the flow
            result = self.kickoff()
            print('===================================')
            print('===================================')
            print('===================================')
            print(f'RESULT : {result}')
            print(f'TYPE OF RESULT : {type(result)}')
            print('===================================')
            print('===================================')
            print('===================================')
            # Extract final CSV path
            if 'csv_path' in result and result['csv_path']:
                logger.info(f"Flow completed successfully. Output: {result['csv_path']}")
                return result['csv_path']
            else:
                logger.warning("Flow completed but no CSV path found")
                return "unified_prediction_markets_fallback.csv"
                
        except Exception as e:
            logger.error(f"Flow execution failed: {str(e)}")
            # Create error report
            error_df = pd.DataFrame([{
                'unified_name': 'Flow execution failed',
                'source_products': str(e),
                'average_price': 0,
                'price_variance': 0,
                'confidence_level': 0,
                'source_count': 0,
                'sources': 'Error',
                'category': 'Error',
                'min_price': 0,
                'max_price': 0
            }])
            error_path = 'unified_prediction_markets_error.csv'
            error_df.to_csv(error_path, index=False)
            return error_path

def main():
    """Main execution function"""
    try:
        # Initialize and run the flow
        flow = PredictionMarketFlow()
        csv_output = flow.run_flow()
        
        print(f"\n{'='*50}")
        print("PREDICTION MARKET FLOW COMPLETED")
        print(f"{'='*50}")
        print(f"Output CSV: {csv_output}")
        
        # Display results
        if os.path.exists(csv_output):
            df = pd.read_csv(csv_output, comment='#')
            print(f"\nTotal unified products: {len(df)}")
            print(f"\nTop 5 products by confidence:")
            print(df.head().to_string(index=False))
        
        return csv_output
        
    except Exception as e:
        logger.error(f"Main execution failed: {str(e)}")
        print(f"Error: {str(e)}")
        return None

if __name__ == "__main__":
    main()