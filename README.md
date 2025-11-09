
# Global Beverage Corporation Exchange

A simple object-oriented stock trading system for managing stocks and calculating market indices.

## Features

- Calculate dividend yield for common and preferred stocks
- Calculate P/E ratio for any stock
- Record trades with timestamp, quantity, type (buy/sell), and price
- Calculate Volume Weighted Stock Price based on trades in the last 5 minutes
- Calculate GBCE All Share Index using geometric mean

## Requirements

- Python 3.6+
- No external dependencies for core functionality
- pytest (optional, for running unit tests)

## Installation

Install dependencies (optional, for testing):

```bash
pip install -r requirements.txt
```

## Usage

Run the sample application:

```bash
python3 main.py
```

Run the test suite:

```bash
pytest test_stock.py -v
```

## Code Structure

- `stock.py` - Core classes (Stock, Trade, Exchange) with type hints
- `main.py` - Sample usage with demonstration data
- `test_stock.py` - Unit test suite (23 test cases)
- `requirements.txt` - Python dependencies

## Testing

The project includes 23 unit tests organized into 9 test classes:

- **TestTrade**: Trade creation and validation 
- **TestStock**: Common and preferred stock initialization  
- **TestDividendYield**: Common and preferred calculations  
- **TestPERatio**: Calculation and zero dividend handling   
- **TestTradeRecording**: Single and multiple trade recording   
- **TestVolumeWeightedPrice**: VWSP calculation and edge cases  
- **TestExchange**: Stock management and retrieval  
- **TestGBCEIndex**: Geometric mean calculation 
- **TestCompleteScenario**: End-to-end trading workflow 


