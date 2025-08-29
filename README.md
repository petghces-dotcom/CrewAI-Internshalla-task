# CrowdWisdomTrading AI Agent - Prediction Market Unifier

A sophisticated CrewAI-powered system that scrapes, analyzes, and unifies prediction market data from multiple platforms using local Ollama LLM integration.

## 🎯 Project Overview

This project implements a multi-agent AI system that:
- Scrapes prediction market data from multiple platforms (Polymarket, Kalshi, PredictIt)
- Uses intelligent agents to identify and match similar products across platforms
- Generates unified CSV reports with confidence scoring
- Implements CrewAI Flow with proper guardrails for robust execution

## 🏗️ Architecture

The system uses a **CrewAI Flow** with three specialized agents:

1. **Data Collector Agent**: Scrapes prediction market websites using browser automation
2. **Product Analyzer Agent**: Analyzes and matches similar products across platforms using AI
3. **CSV Generator Agent**: Creates structured CSV outputs with comprehensive metrics

## 🚀 Features

- ✅ **CrewAI Flow Implementation** with guardrails
- ✅ **Local Ollama Integration** (llama3.2)
- ✅ **Multi-Platform Scraping** (Polymarket, Kalshi, PredictIt)
- ✅ **Intelligent Product Matching** with confidence scoring
- ✅ **Structured CSV Output** with comprehensive metrics
- ✅ **Robust Error Handling** and logging
- ✅ **Browser Automation** using Selenium
- ✅ **Data Validation** using Pydantic models

## 📋 Requirements

- Python 3.11+
- Ollama running locally with llama3.2 model
- Chrome/Chromium browser for scraping

## 🛠️ Installation & Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Setup Ollama

```bash
# Install and start Ollama
ollama pull llama3.2
ollama serve  # Keep this running in a separate terminal
```

### 3. Verify Ollama Connection

```bash
curl http://localhost:11434/api/tags
```

### 4. Run the Application

```bash
python main.py
```

## 📊 Output

The system generates a comprehensive CSV file: `unified_prediction_markets.csv`

### CSV Structure

| Column | Description |
|--------|-------------|
| `unified_name` | Unified product name across platforms |
| `source_products` | Original product names from each platform |
| `average_price` | Average price across all platforms |
| `price_variance` | Standard deviation of prices |
| `confidence_level` | AI confidence in product matching (0-100%) |
| `source_count` | Number of platforms offering this product |
| `sources` | List of source platforms |
| `category` | Product category (politics, sports, etc.) |
| `min_price` | Minimum price found |
| `max_price` | Maximum price found |

### Sample Output

```csv
# Summary Statistics
# Total Products: 15
# Average Confidence: 73.25%
# High Confidence Products (>80%): 8
# Multi-source Products: 6

unified_name,source_products,average_price,price_variance,confidence_level,source_count,sources,category,min_price,max_price
2024 Presidential Election,Trump Victory Market; Biden Win Probability,0.6250,0.0500,95.0,2,"Polymarket, Kalshi",politics,0.5750,0.6750
World Cup 2026 Winner,Brazil Championship; Brazil World Cup,0.4500,0.0200,88.5,2,"Kalshi, PredictIt",sports,0.4300,0.4700
```

## 🧪 Testing

Run the test suite:

```bash
python test_flow.py
```

Test coverage includes:
- Data collection validation
- Product matching algorithms
- CSV generation accuracy
- Price parsing robustness

## 🔧 Configuration

Edit `config.py` to customize:

- Target websites and selectors
- Confidence thresholds
- Output formats
- LLM settings

## 📁 Project Structure

```
├── main.py              # Main CrewAI Flow implementation
├── config.py            # Configuration settings
├── tools.py             # Custom scraping tools
├── test_flow.py         # Test suite
├── requirements.txt     # Python dependencies
├── unified_prediction_markets.csv  # Generated output
└── README.md           # This file
```

## 🤖 CrewAI Flow Details

### Flow Steps

1. **Data Collection** (`@start()`)
   - Scrapes target websites using Selenium
   - Extracts product names, prices, and probabilities
   - Returns structured JSON data

2. **Product Analysis** (`@listen(collect_data)`)
   - Uses AI to identify similar products across platforms
   - Calculates confidence scores for matches
   - Groups related products together

3. **CSV Generation** (`@listen(analyze_products)`)
   - Converts analyzed data to structured CSV
   - Adds statistical summaries
   - Validates data integrity

### Guardrails Implementation

- **Data Validation**: Pydantic models ensure type safety
- **Error Recovery**: Graceful handling of scraping failures
- **Confidence Thresholds**: Only high-confidence matches included
- **Rate Limiting**: Respectful scraping with delays
- **Fallback Mechanisms**: Alternative data sources on failure

## 🎯 Key Technical Decisions

### Why CrewAI Flow?
- **Event-driven architecture** for better control flow
- **Built-in state management** for complex workflows
- **Agent specialization** for modular development
- **Guardrails support** for production reliability

### Why Local Ollama?
- **Privacy**: No data sent to external APIs
- **Cost**: Free local inference
- **Control**: Custom model fine-tuning possible
- **Reliability**: No rate limits or API downtime

### Why Selenium for Scraping?
- **JavaScript rendering**: Handles modern SPAs
- **Dynamic content**: Waits for content loading
- **Browser simulation**: Bypasses basic bot detection
- **Reliable extraction**: Consistent element location

## 🚨 Error Handling

The system includes comprehensive error handling:

- **Network failures**: Retry logic with exponential backoff
- **Parsing errors**: Graceful degradation to default values
- **LLM failures**: Fallback to rule-based matching
- **File I/O errors**: Automatic backup generation

## 📈 Performance Optimizations

- **Parallel scraping**: Multiple sites scraped concurrently
- **Efficient selectors**: Optimized CSS selectors for speed
- **Caching**: Avoid re-scraping within sessions
- **Minimal dependencies**: Fast startup times

## 🔍 Monitoring & Logging

Comprehensive logging includes:
- Flow execution progress
- Scraping success/failure rates
- Agent decision reasoning
- Performance metrics

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🛡️ Security Considerations

- **Robots.txt compliance**: Respects site scraping policies
- **Rate limiting**: Prevents server overload
- **User-agent rotation**: Appears as regular browser traffic
- **Local processing**: No sensitive data transmission

## 🚀 Production Deployment

For production use:

1. **Containerization**: Docker support available
2. **Scheduling**: Cron jobs for regular updates
3. **Monitoring**: Integration with logging services
4. **Scaling**: Multi-instance deployment support

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Run tests: `python test_flow.py`
4. Submit a pull request

## 📝 License

MIT License - see LICENSE file for details

## 🆘 Troubleshooting

### Common Issues

**Ollama not responding:**
```bash
# Check if Ollama is running
curl http://localhost:11434/api/version

# Restart if needed
ollama serve
```

**Chrome driver issues:**
```bash
# Install Chrome driver
pip install webdriver-manager
```

**Scraping blocked:**
- Check site's robots.txt
- Adjust delay settings in config.py
- Verify selectors are current

### Getting Help

- Check the logs for detailed error messages
- Review the test suite for expected behavior
- Open an issue with reproduction steps

## 🎯 Future Enhancements

- [ ] Real-time market monitoring
- [ ] Price alert system
- [ ] API endpoint for data access
- [ ] Machine learning for better matching
- [ ] Web dashboard for visualization
- [ ] More prediction market platforms
- [ ] Historical data tracking
- [ ] Arbitrage opportunity detection

---

**Built with ❤️ for CrowdWisdomTrading Internship Assessment**