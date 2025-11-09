from datetime import datetime, timedelta
from enum import Enum
from typing import Optional, Dict, List


class StockType(Enum):
    COMMON = "Common"
    PREFERRED = "Preferred"


class OrderMode(Enum):
    BUY = "BUY"
    SELL = "SELL"


class Trade:
    def __init__(self, timestamp: datetime, quantity: int, order_mode : OrderMode, price: float) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be a positive integer")
        if price <= 0:
            raise ValueError("Price must be a positive number")
        
        self.timestamp: datetime = timestamp
        self.quantity: int = quantity
        self.order_mode : OrderMode = order_mode
        self.price: float = price


class Stock:
    """ It represents a stock with its properties and trade history"""
    
    def __init__(self, symbol: str, stock_type: StockType, last_dividend: float, par_value: float, 
                 fixed_dividend: Optional[float] = None) -> None:
        
        self.symbol: str = symbol.strip().upper()
        self.stock_type: StockType = stock_type
        self.last_dividend: float = last_dividend
        self.par_value: float = par_value
        self.fixed_dividend: Optional[float] = fixed_dividend
        self.trades: List[Trade] = []
    
    def calculate_dividend_yield(self, price: float) -> float:
        if price <= 0:
            raise ValueError("Price must be greater than zero")
        
        if self.stock_type == StockType.COMMON:
            return self.last_dividend / price
        else:
            if self.fixed_dividend is None:
                raise ValueError("Fixed dividend required for preferred stock")
            return (self.fixed_dividend * self.par_value) / price
    
    def calculate_pe_ratio(self, price: float) -> Optional[float]:
        if price <= 0:
            raise ValueError("Price must be greater than zero")
        
        dividend = self.last_dividend
        if dividend == 0:
            return None 
        
        return price / dividend
    
    def record_trade(self, quantity: int, order_mode: OrderMode, price: float) -> Trade:
        if quantity <= 0:
            raise ValueError("Quantity must be a positive integer")
        if price <= 0:
            raise ValueError("Price must be a positive number")
        
        timestamp = datetime.now()
        trade = Trade(timestamp, quantity, order_mode, price)
        self.trades.append(trade)
        return trade
    
    def calculate_volume_weighted_price(self, minutes: int = 5) -> Optional[float]:
        if minutes <= 0:
            raise ValueError("Minutes must be a positive integer")
        
        if not self.trades:
            return None
        
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        recent_trades = [t for t in self.trades if t.timestamp >= cutoff_time]
        
        if not recent_trades:
            return None
        
        total_price_quantity = sum(trade.price * trade.quantity for trade in recent_trades)
        total_quantity = sum(trade.quantity for trade in recent_trades)
        
        if total_quantity == 0:
            return None
        
        return total_price_quantity / total_quantity


class Exchange:
    """ It represents the exchange of stocks"""
    
    def __init__(self) -> None:
        self.stocks: Dict[str, Stock] = {}
    
    def add_stock(self, stock: Stock) -> None:
        if stock.symbol in self.stocks:
            raise ValueError(f"Stock with symbol '{stock.symbol}' already exists in exchange")
        self.stocks[stock.symbol] = stock
    
    def get_stock(self, symbol: str) -> Optional[Stock]:
        return self.stocks.get(symbol.strip().upper())
    
    def calculate_gbce_all_share_index(self) -> Optional[float]:
        prices: List[float] = []
        
        for stock in self.stocks.values():
            vwsp = stock.calculate_volume_weighted_price()
            if vwsp is not None:
                prices.append(vwsp)
        
        if not prices:
            return None
        
        product: float = 1.0
        for price in prices:
            product *= price
        
        n: int = len(prices)
        geometric_mean: float = product ** (1 / n)
        
        return geometric_mean

