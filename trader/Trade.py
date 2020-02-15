from yahoo_fin import stock_info as sf


class Trade:

	def __init__(self, ticker, buy_price, amount, take_profit, stop_loss):
		self.ticker = ticker
		self.buy_price = buy_price
		self.amount = amount
		try:
			self.curr_price = sf.get_live_price(self.ticker)
		except Exception as e:
			print("Error in getting prices, defaulting to buy price")
			self.curr_price = self.buy_price
		self.take_profit = take_profit
		self.stop_loss = stop_loss

	def __repr__(self):
		return ("TRADE: " + str(self.ticker) + " * " + str(self.amount) + " @ " + str(self.buy_price) + " CURRENTLY FLYING AT " + str(self.curr_price))

	def check_profit(self):
		try:
			self.curr_price = sf.get_live_price(self.ticker)
		except Exception as e:
			print("Error in getting prices, defaulting to buy price")
			self.curr_price = self.buy_price
		# take profit
		if self.curr_price > ((1 + (self.take_profit / 100))*self.buy_price):
			return True
		else:
			return False

	def check_loss(self):
		try:
			self.curr_price = sf.get_live_price(self.ticker)
		except Exception as e:
			print("Error in getting prices, defaulting to buy price")
			self.curr_price = self.buy_price
		# take loss
		print()
		if self.curr_price < ((1 - (self.stop_loss / 100))*self.buy_price):
			return True
		else:
			return False	