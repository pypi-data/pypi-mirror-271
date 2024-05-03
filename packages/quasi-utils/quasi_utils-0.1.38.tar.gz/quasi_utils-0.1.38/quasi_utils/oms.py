import json
from datetime import datetime as dt

from quasi_utils.oms_utils import request, base, get_details, ticker_transform


class OMS:
	def __init__(self, config=None, data_dir=None, session=None):
		self.base_url = 'https://api.kite.trade'
		self.api_key, self.api_secret, self.access_token = get_details(config, data_dir)
		self.headers = {'X-Kite-Version': '3', 'User-Agent': 'Kiteconnect-python/4.2.0',
		                'Authorization': f'token {self.api_key}:{self.access_token}'}
		self.session = session
	
	def ltp(self, tickers):
		if not isinstance(tickers, list):
			tickers = [tickers]
		tickers_ = {'i': tickers}
		
		res = request('GET', f'{self.base_url}/quote/ltp', data=tickers_, params=tickers_,
		              headers=self.headers)
		if res.get('status_code') == 403:
			return None
		
		return {ticker_.split(':')[-1]: ltp['last_price'] for ticker_, ltp in res['data'].items()}
	
	def quote(self, tickers):
		if not isinstance(tickers, list):
			tickers = [tickers]
		
		res = request('GET', f'{self.base_url}/quote', params={'i': tickers}, headers=self.headers)
		if res.get('status_code') == 403:
			return None
		
		return res['data']
	
	def get_user(self):
		res = request('GET', f'{self.base_url}/user/profile', headers=self.headers)
		if res.get('status_code') == 403:
			return None
		
		return res
	
	def get_cash_needed(self, ticker, action, price, qty, price_type, trade_type='MIS', variety='regular',
	                    exchange='NFO'):
		data = {'tradingsymbol': ticker, 'exchange': exchange, 'transaction_type': action, 'price': price,
		        'quantity': qty, 'variety': variety, 'order_type': price_type, 'product': trade_type}
		
		res = request('POST', f'{self.base_url}/margins/orders', headers=self.headers, _json=[data])
		if res.get('status_code') == 403:
			return None
		
		return res
	
	def get_cash_details(self, verbose=False):
		res = request('GET', f'{self.base_url}/user/margins/equity', headers=self.headers)
		
		if res.get('status_code') == 403:
			return None
		
		data = res['data']
		
		if not data:
			return None
		
		return data if verbose else {'cash': round(data['net'], 1), 'pnl': data['utilised']['m2m_realised']}
	
	def get_instruments(self, tickers=None, exchange='NSE'):
		res = request('GET', f'{self.base_url}/instruments/{exchange}', data=None, headers=self.headers)
		if type(res) is dict and res.get('status_code') == 403:
			return None
		
		res = res.decode('utf-8').strip().split('\n')
		header, rows = res[0], res[1:]
		
		# handle special case of sensex index
		data = {'SENSEX': {'token': '265', 'name': 'SENSEX', 'expiry': '', 'strike': '0',
		                   'ticker_type': 'EQ', 'segment': 'INDICES'}} if exchange == 'NSE' else {}
		
		if not tickers:
			for idx, row in enumerate(rows):
				row = row.split(',')
				expiry = dt.strptime(row[5], '%Y-%m-%d') if row[5] != '' else ''
				name = row[3][1:-1]
				
				if name == '' or any(x in name for x in ['-', 'ETF']):
					continue
				
				name = row[2] if exchange == 'NSE' else name
				data[row[2]] = {'token': row[0], 'name': name, 'expiry': expiry, 'strike': row[-6],
				                'ticker_type': row[-3], 'segment': row[-2]}
		
		compareFn = lambda x: (f"z{x[1]['name']}" if x[1]['name'] != 'NIFTY' else x[1]['name'], x[1]['expiry'])
		data = dict(sorted(data.items(), key=compareFn))
		
		for ticker, ticker_data in data.items():
			if ticker_data['expiry'] != '':
				ticker_data['expiry'] = dt.strftime(ticker_data['expiry'], '%d %b %Y')
			
			data[ticker] = '|'.join([val for val in data[ticker].values()])
		
		return data
	
	def get_orders(self, status='all'):
		res = request('GET', f'{self.base_url}/orders', data=None, headers=self.headers)
		if res.get('status_code') == 403:
			return None
		
		orders, open_orders, executed_orders, all_orders = res['data'], [], [], []
		status_values = {'NRML': 'OVERNIGHT', 'MIS': 'INTRADAY', 'CNC': 'DELIVERY', 'COMPLETE': 'COMPLETED'}
		
		for order in orders:
			temp_order = {'order_id': order['order_id'],
			              'status': status_values.get(order['status']) or order['status'],
			              'time': order['order_timestamp'],
			              'variety': order['variety'],
			              'exchange': order['exchange'],
			              'ticker': ticker_transform(order['tradingsymbol']),
			              'token': order['instrument_token'],
			              'price_type': order['order_type'],
			              'action': order['transaction_type'].title(),
			              'trade_type': status_values[order['product']],
			              'total_qty': order['quantity'],
			              'price': round(order['price'], 2),
			              'average_price': round(order['average_price'], 2),
			              'filled_qty': order['filled_quantity'],
			              'pending_qty': order['pending_quantity']}
			
			if order['meta']:
				temp_order['total_qty'] = order['meta']['iceberg']['total_quantity']
			
			if temp_order['status'] in ['OPEN', 'AMO REQ RECEIVED']:
				open_orders.append(temp_order)
			else:
				executed_orders.append(temp_order)
			
			all_orders.append(temp_order)
		
		if status == 'open':
			return open_orders[::-1]
		elif status == 'executed':
			return executed_orders[::-1]
		else:
			return all_orders[::-1]
	
	def get_tax_details(self):
		executed_orders = self.get_orders(status='executed')
		
		if not executed_orders:
			return None
		
		brokerage, stt, transaction_charges, sebi_charges, stamp_charges, gst = 0, 0, 0, 0, 0, 0
		taxes = {'brokerage': brokerage, 'stt': stt, 'transaction_charges': transaction_charges,
		         'sebi_charges': sebi_charges, 'stamp_charges': stamp_charges, 'gst': gst}
		
		for order in executed_orders:
			if order['status'] != 'COMPLETED':
				continue
			
			order_value = order['average_price'] * order['filled_qty']
			exchange, trade_type = order['exchange'], order['trade_type']
			
			if exchange == 'NSE' and trade_type == 'DELIVERY':
				brokerage = 0
				stt = 0.1 / 100 * order_value
				transaction_charges = 0.00322 / 100 * order_value
				stamp_charges = 0.015 / 100 * order_value if order['action'] == 'Buy' else 0
			
			elif exchange == 'NSE' and trade_type == 'INTRADAY':
				brokerage = min(0.03 / 100 * order_value, 20)
				stt = 0.025 / 100 * order_value if order['action'] == 'Sell' else 0
				transaction_charges = 0.00322 / 100 * order_value
				stamp_charges = 0.003 / 100 * order_value if order['action'] == 'Buy' else 0
			
			elif exchange in ['NFO', 'BFO'] and order['ticker'].split()[-1] == 'FUT':
				brokerage = min(0.03 / 100 * order_value, 20)
				stt = 0.0125 / 100 * order_value if order['action'] == 'Sell' else 0
				transaction_charges = 0.00188 / 100 * order_value if exchange == 'NFO' else 0
				stamp_charges = 0.002 / 100 * order_value if order['action'] == 'Buy' else 0
			
			elif exchange in ['NFO', 'BFO'] and order['ticker'].split()[-1].endswith(('CE', 'PE')):
				brokerage = 20
				stt = 0.0625 / 100 * order_value if order['action'] == 'Sell' else 0
				transaction_charges = 0.05 / 100 * order_value if exchange == 'NFO' else 0.005 / 100 * order_value
				stamp_charges = 0.003 / 100 * order_value if order['action'] == 'Buy' else 0
			
			sebi_charges = 0.0001 / 100 * order_value
			gst = 0.18 * (brokerage + sebi_charges + transaction_charges)
			
			taxes['brokerage'] += brokerage
			taxes['stt'] += stt
			taxes['transaction_charges'] += transaction_charges
			taxes['sebi_charges'] += sebi_charges
			taxes['stamp_charges'] += round(stamp_charges)
			taxes['gst'] += gst
		
		taxes['brokerage'] = round(taxes['brokerage'], 2)
		taxes['stt'] = round(taxes['stt'], 2)
		taxes['transaction_charges'] = round(taxes['transaction_charges'], 2)
		taxes['sebi_charges'] = round(taxes['sebi_charges'], 2)
		taxes['stamp_charges'] = round(taxes['stamp_charges'], 2)
		taxes['gst'] = round(taxes['gst'], 2)
		taxes['total_tax'] = round(sum(taxes.values()), 2)
		
		return taxes
	
	def get_positions(self, only_open=False):
		res = request('GET', f'{self.base_url}/portfolio/positions', data=None, headers=self.headers)
		if res.get('status_code') == 403:
			return None
		
		positions = res['data']['net']
		
		final_positions = []
		for position in positions:
			temp_position = {'ticker': ticker_transform(position['tradingsymbol']),
			                 'exchange': position['exchange'],
			                 'token': position['instrument_token'],
			                 'trade_type': 'OVERNIGHT' if position['product'] == 'NRML' else 'INTRADAY',
			                 'qty': position['quantity'],
			                 'overnight_qty': position['overnight_quantity'],
			                 'avg_price': position['average_price'],
			                 'pnl': position['pnl'],
			                 'm2m': position['m2m'],
			                 'unrealised': position['unrealised'],
			                 'realised': position['realised'],
			                 'day_buy_price': position['day_buy_price'],
			                 'day_sell_price': position['day_sell_price']}
			final_positions.append(temp_position)
		
		return [position for position in final_positions if position['qty']] if only_open else final_positions
	
	def place_order(self, ticker, action, price, qty, price_type, trade_type='MIS', variety='regular', exchange='NFO',
	                trigger_price=None, iceberg_legs=None, iceberg_quantity=None):
		data = {'tradingsymbol': ticker, 'exchange': exchange, 'transaction_type': action, 'price': price,
		        'quantity': qty, 'variety': variety, 'order_type': price_type, 'product': trade_type,
		        'trigger_price': trigger_price, 'iceberg_legs': iceberg_legs, 'iceberg_quantity': iceberg_quantity}
		
		res = request('POST', f'{self.base_url}/orders/{variety}', data=data, headers=self.headers)
		if res.get('status_code') == 403:
			return None
		
		return res
	
	def cancel_order(self, order_ids, variety='regular'):
		res = {}
		
		order_ids = [order_ids] if not isinstance(order_ids, list) else order_ids
		for _id in order_ids:
			res = request('DELETE', f'{self.base_url}/orders/{variety}/{_id}',
			              headers=self.headers, data=None)
			if res.get('status_code') == 403:
				return None
			
			res[_id] = res
		
		return res
	
	def modify_order(self, order_id=None, price=None, qty=None, price_type=None, variety='regular'):
		data = {}
		if price:
			data['price'] = price
		if qty:
			data['quantity'] = qty
		if price_type:
			data['order_type'] = price_type
		
		res = request('PUT', f'{self.base_url}/orders/{variety}/{order_id}',
		              data=data, headers=self.headers)
		if res.get('status_code') == 403:
			return None
		
		return res
	
	def place_gtt(self, buy_price, trade_type, qty, thresh=None, ticker=None, prefix=None, strike=None, exchange='NFO'):
		base_price, ticker = base(buy_price * thresh) if thresh else base(buy_price), ticker or f'{prefix}{strike}'
		
		condition = {'exchange': exchange, 'tradingsymbol': ticker, 'trigger_values': [base_price],
		             'last_price': self.ltp(f'{exchange}:{ticker}')[ticker]}
		orders = [{'exchange': exchange, 'tradingsymbol': ticker, 'transaction_type': 'SELL', 'quantity': qty,
		           'order_type': 'LIMIT', 'product': trade_type, 'price': base(base_price * 0.98)}]
		data = {'condition': json.dumps(condition), 'orders': json.dumps(orders), 'type': 'single'}
		
		res = request('POST', f'{self.base_url}/gtt/triggers', data=data, headers=self.headers)
		if res.get('status_code') == 403:
			return None
		
		return res
	
	def delete_gtt_orders(self, ids):
		if ids == 'all':
			for order in self.fetch_gtt_orders():
				res = request('DELETE', f'{self.base_url}/gtt/triggers/{order["id"]}',
				              headers=self.headers, data=None)
				if res.get('status_code') == 403:
					return None
		else:
			if not isinstance(ids, list):
				ids = [ids]
			
			for id_ in ids:
				res = request('DELETE', f'{self.base_url}/gtt/triggers/{id_}',
				              headers=self.headers, data=None)
				if res.get('status_code') == 403:
					return None
	
	def fetch_gtt_orders(self):
		res = request('GET', f'{self.base_url}/gtt/triggers', headers=self.headers, data=None)
		if res.get('status_code') == 403:
			return None
		
		return res['data']


if __name__ == '__main__':
	obj = OMS(config='zerodha', data_dir='../../oms/oms/execute/data')
	# print(obj.ltp(['NSE:RELIANCE']))
	# print(obj.get_cash_details(verbose=True))
	# print(json.dumps(obj.get_orders(mould=True), indent=2))
	# print(obj.cancel_order(order_ids='231004203428841', variety='amo'))
	# print(obj.modify_order(order_id='231004203471297', price=12.9, qty=500, price_type='LIMIT', variety='amo'))
	# print(obj.get_instruments())
	print(obj.get_tax_details())
	# print(obj.get_user()['data'])
	# print(json.dumps(obj.get_positions(), indent=2))
	# print(json.dumps(obj.get_orders(status='executed'), indent=2))
