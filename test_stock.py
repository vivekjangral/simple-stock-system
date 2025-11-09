import pytest
from datetime import datetime
from stock import Stock, StockType, OrderMode, Trade, Exchange


class TestTrade:
    
    def test_trade_creation_valid(self):
        timestamp = datetime.now()
        trade = Trade(timestamp, 100, OrderMode.BUY, 105.5)
        assert trade.quantity == 100
        assert trade.price == 105.5
    
    def test_trade_invalid_quantity(self):
        with pytest.raises(ValueError):
            Trade(datetime.now(), 0, OrderMode.BUY, 100)
    
    def test_trade_invalid_price(self):
        with pytest.raises(ValueError):
            Trade(datetime.now(), 100, OrderMode.BUY, 0)


class TestStock:
    
    def test_common_stock_creation(self):
        stock = Stock("TEA", StockType.COMMON, last_dividend=0, par_value=100)
        assert stock.symbol == "TEA"
        assert stock.stock_type == StockType.COMMON
        assert stock.trades == []
    
    def test_preferred_stock_creation(self):
        stock = Stock("GIN", StockType.PREFERRED, last_dividend=8, 
                     par_value=100, fixed_dividend=0.02)
        assert stock.symbol == "GIN"
        assert stock.fixed_dividend == 0.02
    
    def test_stock_symbol_normalization(self):
        stock = Stock("  pop  ", StockType.COMMON, last_dividend=8, par_value=100)
        assert stock.symbol == "POP"


class TestDividendYield:
    
    def test_common_stock_dividend_yield(self):
        stock = Stock("POP", StockType.COMMON, last_dividend=8, par_value=100)
        dividend_yield = stock.calculate_dividend_yield(120)
        expected = 8 / 120
        assert abs(dividend_yield - expected) < 0.0001
    
    def test_preferred_stock_dividend_yield(self):
        stock = Stock("GIN", StockType.PREFERRED, last_dividend=8, 
                     par_value=100, fixed_dividend=0.02)
        dividend_yield = stock.calculate_dividend_yield(120)
        expected = (0.02 * 100) / 120
        assert abs(dividend_yield - expected) < 0.0001
    
    def test_dividend_yield_invalid_price(self):
        stock = Stock("POP", StockType.COMMON, last_dividend=8, par_value=100)
        with pytest.raises(ValueError):
            stock.calculate_dividend_yield(0)


class TestPERatio:
    
    def test_pe_ratio_calculation(self):
        stock = Stock("POP", StockType.COMMON, last_dividend=8, par_value=100)
        pe_ratio = stock.calculate_pe_ratio(120)
        assert pe_ratio == 15.0
    
    def test_pe_ratio_zero_dividend(self):
        stock = Stock("TEA", StockType.COMMON, last_dividend=0, par_value=100)
        pe_ratio = stock.calculate_pe_ratio(120)
        assert pe_ratio is None
    
    def test_pe_ratio_invalid_price(self):
        stock = Stock("POP", StockType.COMMON, last_dividend=8, par_value=100)
        with pytest.raises(ValueError):
            stock.calculate_pe_ratio(0)


class TestTradeRecording:
    
    def test_record_single_trade(self):
        stock = Stock("TEA", StockType.COMMON, last_dividend=0, par_value=100)
        trade = stock.record_trade(100, OrderMode.BUY, 105)
        assert len(stock.trades) == 1
        assert trade.quantity == 100
    
    def test_record_multiple_trades(self):
        stock = Stock("POP", StockType.COMMON, last_dividend=8, par_value=100)
        stock.record_trade(100, OrderMode.BUY, 95)
        stock.record_trade(50, OrderMode.SELL, 98)
        assert len(stock.trades) == 2


class TestVolumeWeightedPrice:
    
    def test_vwsp_calculation(self):
        stock = Stock("TEA", StockType.COMMON, last_dividend=0, par_value=100)
        stock.record_trade(100, OrderMode.BUY, 105)
        stock.record_trade(50, OrderMode.SELL, 110)
        stock.record_trade(150, OrderMode.BUY, 108)
        vwsp = stock.calculate_volume_weighted_price()
        expected = (100*105 + 50*110 + 150*108) / (100 + 50 + 150)
        assert abs(vwsp - expected) < 0.01
    
    def test_vwsp_no_trades(self):
        stock = Stock("TEA", StockType.COMMON, last_dividend=0, par_value=100)
        vwsp = stock.calculate_volume_weighted_price()
        assert vwsp is None
    
    def test_vwsp_invalid_minutes(self):
        stock = Stock("TEA", StockType.COMMON, last_dividend=0, par_value=100)
        with pytest.raises(ValueError):
            stock.calculate_volume_weighted_price(minutes=0)


class TestExchange:
    
    def test_add_stock(self):
        exchange = Exchange()
        stock = Stock("TEA", StockType.COMMON, last_dividend=0, par_value=100)
        exchange.add_stock(stock)
        assert "TEA" in exchange.stocks
    
    def test_add_duplicate_stock(self):
        exchange = Exchange()
        stock1 = Stock("TEA", StockType.COMMON, last_dividend=0, par_value=100)
        stock2 = Stock("TEA", StockType.COMMON, last_dividend=5, par_value=100)
        exchange.add_stock(stock1)
        with pytest.raises(ValueError):
            exchange.add_stock(stock2)
    
    def test_get_stock(self):
        exchange = Exchange()
        stock = Stock("POP", StockType.COMMON, last_dividend=8, par_value=100)
        exchange.add_stock(stock)
        retrieved = exchange.get_stock("pop")
        assert retrieved == stock


class TestGBCEIndex:
    
    def test_gbce_index_calculation(self):
        exchange = Exchange()
        tea = Stock("TEA", StockType.COMMON, last_dividend=0, par_value=100)
        tea.record_trade(100, OrderMode.BUY, 100)
        pop = Stock("POP", StockType.COMMON, last_dividend=8, par_value=100)
        pop.record_trade(100, OrderMode.BUY, 200)
        exchange.add_stock(tea)
        exchange.add_stock(pop)
        index = exchange.calculate_gbce_all_share_index()
        expected = (100 * 200) ** 0.5
        assert abs(index - expected) < 0.01
    
    def test_gbce_index_no_trades(self):
        exchange = Exchange()
        index = exchange.calculate_gbce_all_share_index()
        assert index is None


class TestCompleteScenario:
    
    def test_complete_scenario(self):
        exchange = Exchange()
        tea = Stock("TEA", StockType.COMMON, last_dividend=0, par_value=100)
        pop = Stock("POP", StockType.COMMON, last_dividend=8, par_value=100)
        gin = Stock("GIN", StockType.PREFERRED, last_dividend=8, par_value=100, fixed_dividend=0.02)
        
        exchange.add_stock(tea)
        exchange.add_stock(pop)
        exchange.add_stock(gin)
        
        assert pop.calculate_dividend_yield(120) > 0
        assert gin.calculate_dividend_yield(120) > 0
        assert pop.calculate_pe_ratio(120) > 0
        assert tea.calculate_pe_ratio(120) is None
        
        tea.record_trade(100, OrderMode.BUY, 105)
        pop.record_trade(200, OrderMode.BUY, 95)
        
        assert tea.calculate_volume_weighted_price() == 105
        assert pop.calculate_volume_weighted_price() == 95
        
        index = exchange.calculate_gbce_all_share_index()
        assert index is not None
        assert index > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
