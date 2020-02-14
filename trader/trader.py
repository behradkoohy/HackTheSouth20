from yahoo_fin import stock_info as sf
import json
import time


CONST_start_cash = 50000.0
CONST_take_profit_percent = 2.5
CONST_stop_loss_percent = 10


def totalValue(assets, cash):
	val = 0.0
	for tick, amount in assets.items():
		val += (sf.get_live_price(tick) * amount)
	return (val + cash)

def main():
	liquid_cash = CONST_start_cash
	tang_assets = {}
	f = ""
	loop = True
	while loop:
		
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

			print("BUY", selected_ticker['tick'], ',', selected_ticker['price'],  '*', amount_to_buy, 'FOR', amount_to_buy*selected_ticker['price'])
			print(tang_assets)
		else:

			print("no money, sleeping. Total asset value:", totalValue(tang_assets, liquid_cash))

		# time.sleep(1)

		# loop = False

if __name__ == '__main__':
	main()

