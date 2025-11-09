from stock import Stock, StockType, OrderMode, Exchange
import time


def main():
    global_beverage_corporation_exchange = Exchange()
    
    tea = Stock("TEA", StockType.COMMON, last_dividend=0, par_value=100)
    pop = Stock("POP", StockType.COMMON, last_dividend=8, par_value=100)
    ale = Stock("ALE", StockType.COMMON, last_dividend=23, par_value=60)
    gin = Stock("GIN", StockType.PREFERRED, last_dividend=8, par_value=100, fixed_dividend=0.02)
    joe = Stock("JOE", StockType.COMMON, last_dividend=13, par_value=250)
    
    global_beverage_corporation_exchange.add_stock(tea)
    global_beverage_corporation_exchange.add_stock(pop)
    global_beverage_corporation_exchange.add_stock(ale)
    global_beverage_corporation_exchange.add_stock(gin)
    global_beverage_corporation_exchange.add_stock(joe)
    
    print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
    print("Global Beverage Corporation Exchange - Stock Trading System")
    print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
    
    print("\n")
    print("Dividend Yield & P/E Ratio Calculations")
    print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
    test_price = 120
    
    print(f"\nFor POP stock at price {test_price}p:")
    print(f"  Dividend Yield: {pop.calculate_dividend_yield(test_price):.4f}")
    pe_ratio = pop.calculate_pe_ratio(test_price)
    print(f"  P/E Ratio: {pe_ratio:.4f}")
    
    print(f"\nFor GIN (Preferred) stock at price {test_price}p:")
    print(f"  Dividend Yield: {gin.calculate_dividend_yield(test_price):.4f}")
    pe_ratio = gin.calculate_pe_ratio(test_price)
    print(f" P/E Ratio: {pe_ratio:.4f}")
    
    print("\n Recording Trades:")
    
    tea.record_trade(100, OrderMode.BUY, 105)
    tea.record_trade(50, OrderMode.SELL, 110)
    tea.record_trade(150, OrderMode.BUY, 108)
    print("3 trades recorded for TEA")
    
    pop.record_trade(200, OrderMode.BUY, 95)
    pop.record_trade(100, OrderMode.SELL, 98)
    print("2 trades recorded for POP")
    
    ale.record_trade(75, OrderMode.BUY, 115)
    ale.record_trade(125, OrderMode.BUY, 118)
    print("2 trades recorded for ALE")
    
    gin.record_trade(300, OrderMode.SELL, 102)
    gin.record_trade(50, OrderMode.BUY, 104)
    print("2 trades recorded for GIN")
    
    joe.record_trade(80, OrderMode.BUY, 125)
    joe.record_trade(120, OrderMode.SELL, 128)
    print("2 trades recorded for JOE")
    
    print("\n Volume Weighted Stock Prices (last 5 minutes):")
    for symbol in ["TEA", "POP", "ALE", "GIN", "JOE"]:
        stock = global_beverage_corporation_exchange.get_stock(symbol)
        vwsp = stock.calculate_volume_weighted_price()
        if vwsp:
            print(f"{symbol}: {vwsp:.2f}p")

    print("\n GBCE All Share Index:")
    index = global_beverage_corporation_exchange.calculate_gbce_all_share_index()
    if index:
        print(f"GBCE All Share Index: {index:.2f}")
    


if __name__ == "__main__":
    main()
