from yahoo_fin import stock_info as sf
import json
import time
from Trade import Trade



CONST_start_cash = 50000.0
CONST_take_profit_percent = 2.5
CONST_stop_loss_percent = 10.0


def get_live_price(tick, buy_price=0):
	try:
		return sf.get_live_price(tick)
	except Exception as e:
		print("Error in getting prices, defaulting to buy price")
		return buy_price

def totalValue(assets, cash):
	val = 0.0
	for tick, amount in assets.items():
		val += (sf.get_live_price(tick) * amount)
	return (val + cash)



def main():
	liquid_cash = CONST_start_cash
	tang_assets = {}
	act_trades = []
	f = ""
	loop = True
	while loop:
		# find buys
		
		with open('../predictions.json') as infile:
			f = json.load(infile)
		

		recent_key = (max(list(map(float,(list(f.keys()))))))
		recent_pred = (f[str(recent_key)])
		flatPred = {}

		for d in recent_pred:
		    flatPred.update(d)

		max_pred = 0
		max_tick = ""


		for tick, pred in flatPred.items():
			if pred > max_pred:
				max_pred = pred
				max_tick = tick



		selected_ticker = {"tick" : max_tick, "pred" : max_pred, "price" : sf.get_live_price(max_tick)}
		amount_to_buy = float(int((liquid_cash/2.0) / selected_ticker['price']))
		if amount_to_buy > 0:
			if selected_ticker['tick'] not in tang_assets:
				tang_assets[selected_ticker['tick']] = amount_to_buy
				liquid_cash = liquid_cash - (amount_to_buy*selected_ticker['price'])
			else:
				tang_assets[selected_ticker['tick']] = tang_assets[selected_ticker['tick']] + amount_to_buy
				liquid_cash = liquid_cash - (amount_to_buy*selected_ticker['price'])
			t = Trade(selected_ticker['tick'], selected_ticker['price'], amount_to_buy, CONST_take_profit_percent, CONST_stop_loss_percent)
			act_trades.append(t)
			print("BUY", selected_ticker['tick'], ',', selected_ticker['price'],  '*', amount_to_buy, 'FOR', amount_to_buy*selected_ticker['price'])
			print(tang_assets)
		else:

			print("no money, sleeping. Total asset value:", totalValue(tang_assets, liquid_cash))
		# loop = False
		# find sells
		continuing_trades = []

		for trade in act_trades:
			print(trade)
			if trade.check_profit():
				print('selling trade:' + trade.ticker + " for a profit")
				value_to_sell = trade.curr_price * trade.amount
				liquid_cash += value_to_sell
				tang_assets[trade.ticker] = tang_assets[trade.ticker] - trade.amount
			elif trade.check_loss():
				print('selling trade:' + trade.ticker + " for a loss")
				value_to_sell = trade.curr_price * trade.amount
				liquid_cash += value_to_sell
				tang_assets[trade.ticker] = tang_assets[trade.ticker] - trade.amount
			else:
				print('continuing with trade ' + str(trade))
				continuing_trades.append(trade)

		act_trades = continuing_trades




if __name__ == '__main__':
	main()

