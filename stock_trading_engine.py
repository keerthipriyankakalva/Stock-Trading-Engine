import random


# Define an Order class to represent each stock order
class Order:
    def __init__(self, order_type, ticker_symbol, quantity, price):
        self.order_type = order_type
        self.ticker_symbol = ticker_symbol
        self.quantity = quantity
        self.price = price


# StockOrderBook class will manage the stock orders
class StockOrderBook:
    def __init__(self):
        # Initialize a dictionary to store orders for each ticker symbol
        self.orders = {f"Ticker{i}": {'buy': [], 'sell': []} for i in range(1, 1025)}

    def add_order(self, order_type, ticker_symbol, quantity, price):
        # Ensure that only supported tickers are used
        if ticker_symbol not in self.orders:
            print(f"Ticker {ticker_symbol} is not supported.")
            return

        # Create an Order object and add it to the respective order list (buy or sell)
        new_order = Order(order_type, ticker_symbol, quantity, price)
        if order_type == 'buy':
            self.orders[ticker_symbol]['buy'].append(new_order)
        elif order_type == 'sell':
            self.orders[ticker_symbol]['sell'].append(new_order)
        else:
            print("Invalid order type. Use 'buy' or 'sell'.")
            return

        print(f"Order added: {order_type} {quantity} shares of {ticker_symbol} at {price}.")


# Simulating active stock transactions by randomly calling addOrder function
def simulate_stock_transactions(stock_order_book, num_transactions=10):
    order_types = ['buy', 'sell']
    tickers = [f"Ticker{i}" for i in range(1, 1025)]  # Simulate 1024 tickers

    for _ in range(num_transactions):
        order_type = random.choice(order_types)
        ticker = random.choice(tickers)
        quantity = random.randint(1, 100)
        price = random.uniform(10, 1000)  # Random price between 10 and 1000
        stock_order_book.add_order(order_type, ticker, quantity, price)


# Create the stock order book and simulate stock transactions
stock_order_book = StockOrderBook()
simulate_stock_transactions(stock_order_book, 10)  # Simulate 10 random transactions