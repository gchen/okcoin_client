import okcoin
import time

# 从OKCoin客户QQ处开通交易API之后，在下面填入你的partner_key和secret_key，
partner_key = ''
secret_key = ''

okclient = okcoin.OkCoin(partner_key, secret_key)

def main():
	#获取市场深度
	print okclient.get_depth()	
	#获取账户信息
	print okclient.get_account()
	#下单交易
	order_id = okclient.place_order('btc_cny', 'buy', '47.62', '0.01')	
	#取消订单
	okclient.cancel_order(str( 'btc_cny'), order_id["order_id"])
	#查看交易订单状态
	print okclient.check_order(str('btc_cny'), order_id['order_id'] )['orders'][0]['status']
	
if __name__ == "__main__":
	main()
