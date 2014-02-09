import okcoin
import time

# 从OKCoin客户QQ处开通交易API之后，在下面填入你的partner_key和secret_key，
partner_key = ''
secret_key = ''

okclient = okcoin.OkCoin(partner_key, secret_key)

def main():
	print okclient.get_depth()	
	print okclient.get_account()
	order_id = okclient.place_order('btc_cny', 'buy', '47.62', '0.01')	
	okclient.cancel_order(str( 'btc_cny'), order_id["order_id"])
	print okclient.check_order(str('btc_cny'), order_id['order_id'] )['orders'][0]['status']
	
if __name__ == "__main__":
	main()
