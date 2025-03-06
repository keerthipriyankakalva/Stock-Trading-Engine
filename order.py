import random
import threading


# Order class to represent each order
class Order:
    def __init__(self, order_type, ticker_symbol, quantity, price):
        self.order_type = order_type  # 'buy' or 'sell'
        self.ticker_symbol = ticker_symbol  # Stock ticker symbol
        self.quantity = quantity  # Quantity of shares
        self.price = price  # Price per share


# StockOrderBook class manages orders for different tickers
class StockOrderBook:
    def __init__(self):
        # We will use a list to hold orders for 1,024 tickers
        # Each ticker will have its own list for buy and sell orders
        self.orders = [[] for _ in range(1024)]
        self.lock = threading.Lock()  # Lock to prevent issues with multiple threads

    def add_order(self, order_type, ticker_symbol, quantity, price):
        # We map ticker symbol to an index between 0-1023
        ticker_index = hash(ticker_symbol) % 1024

        # Create a new order object
        new_order = Order(order_type, ticker_symbol, quantity, price)

        # Add the order to the correct list (buy or sell) for that ticker
        with self.lock:  # Using lock to avoid issues when multiple threads are accessing the orders
            if order_type == 'buy':
                self.orders[ticker_index].append(('buy', new_order))
            elif order_type == 'sell':
                self.orders[ticker_index].append(('sell', new_order))
            else:
                print("Invalid order type. Please use 'buy' or 'sell'.")

    def match_orders(self, ticker_symbol):
        # Map the ticker symbol to its index
        ticker_index = hash(ticker_symbol) % 1024

        # Get the buy and sell orders for the ticker
        with self.lock:
            buy_orders = [order for order in self.orders[ticker_index] if order[0] == 'buy']
            sell_orders = [order for order in self.orders[ticker_index] if order[0] == 'sell']

            # Sort buy orders from highest price to lowest
            buy_orders.sort(key=lambda order: order[1].price, reverse=True)

            # Sort sell orders from lowest price to highest
            sell_orders.sort(key=lambda order: order[1].price)

            matched_orders = []

            # Now, let's try to match the buy and sell orders
            while buy_orders and sell_orders:
                buy_order = buy_orders[0][1]
                sell_order = sell_orders[0][1]

                # Check if the buy price is greater than or equal to the sell price
                if buy_order.price >= sell_order.price:
                    # We can match these orders
                    quantity_to_match = min(buy_order.quantity, sell_order.quantity)
                    matched_orders.append((buy_order, sell_order, quantity_to_match))

                    # Update the quantities of the buy and sell orders
                    buy_order.quantity -= quantity_to_match
                    sell_order.quantity -= quantity_to_match

                    # If the quantity is 0, remove the order from the list
                    if buy_order.quantity == 0:
                        buy_orders.pop(0)
                    if sell_order.quantity == 0:
                        sell_orders.pop(0)
                else:
                    break  # No more orders can be matched

            return matched_orders


# Simulate some random stock orders for testing
def simulate_stock_transactions(stock_order_book, num_transactions=10):
    order_types = ['buy', 'sell']
    tickers = [f"Ticker{i}" for i in range(1, 1025)]  # We have 1024 tickers

    for _ in range(num_transactions):
        order_type = random.choice(order_types)
        ticker = random.choice(tickers)
        quantity = random.randint(1, 100)
        price = random.uniform(10, 1000)  # Random price between 10 and 1000
        stock_order_book.add_order(order_type, ticker, quantity, price)


# Create the stock order book
stock_order_book = StockOrderBook()

# Simulate 10 random stock transactions in multiple threads
threads = []
for _ in range(5):  # Simulate 5 threads adding random orders
    thread = threading.Thread(target=simulate_stock_transactions, args=(stock_order_book, 10))
    threads.append(thread)
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()

# Now, try to match orders for a specific ticker (e.g., Ticker1)
matched_orders = stock_order_book.match_orders('Ticker1')
for buy_order, sell_order, quantity in matched_orders:
    print(
        f"Matched {quantity} shares of {buy_order.ticker_symbol}: Buy at {buy_order.price} and Sell at {sell_order.price}")

# Show remaining orders for a specific ticker
print("Remaining Buy Orders for Ticker1:",
      len([order for order in stock_order_book.orders[hash('Ticker1') % 1024] if order[0] == 'buy']))
print("Remaining Sell Orders for Ticker1:",
      len([order for order in stock_order_book.orders[hash('Ticker1') % 1024] if order[0] == 'sell']))

