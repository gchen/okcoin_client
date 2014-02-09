#!/usr/bin/evn python
# -*- coding: utf-8 -*-

import time
import re
import md5
import hashlib
import base64
import httplib
import simplejson as json
import urllib2

class OkCoin():
	def __init__(self,partner=None,secret=None):
		self.partner_key=partner
		self.secret_key=secret
		self.conn=httplib.HTTPSConnection("www.okcoin.com")

	def _get_tonce(self):
		return int(time.time()*1000000)

	def _get_params_hash(self,pdict):
		pstring=""
		# The order of params is critical for calculating a correct hash
		fields=['amount','order_id','partner','rate','symbol','type']
		for f in fields:
			if f in pdict:
				pstring += f + '='+ str(pdict[f]) + '&'
		pstring=pstring.strip('&') # remove the last '&'
		phash = md5.new(pstring + self.secret_key).hexdigest().upper()
		final_url = '?' + pstring + '&sign=' + phash 
		#print "final_url	" + final_url
		return final_url 

	def _private_request(self, post_data, method, url):
		# fill in common post_data parameters
		post_data['partner']=self.partner_key
	
		sub_url=self._get_params_hash(post_data)

		if method == "GET":
			req = urllib2.Request("https://www.okcoin.com" + url)
		elif method == "POST":
			req = urllib2.Request("https://www.okcoin.com" + url + sub_url, {})

		response = urllib2.urlopen(req)

		if response.code == 200:
			# this might fail if non-json data is returned
			resp_dict = json.loads(response.read())
			#print resp_dict
			return resp_dict

		else:
			print "status:", response.code
			print "reason:", response.reason

		return None

	def get_account(self,post_data={}):
		return self._private_request(post_data,'POST', '/api/userinfo.do')

	def get_depth(self,post_data={}):
		return self._private_request(post_data,'GET', '/api/depth.do')
	
	def place_order(self, symbol, type, rate, amount, post_data={}):
		post_data['symbol'] = symbol
		post_data['type'] = type
		post_data['rate'] = rate
		post_data['amount'] = amount
		res = self._private_request(post_data,'POST', '/api/trade.do')
		if res["result"] == True:
			return res
		elif res["result"] == False:
			if res["errorCode"] == "10001":
				# too much api request, 2s interval
				# TODO need to check whether the order was placed or not
				print  ("# too frequent api request, pls retry after 2s interval")
				return res
			
		else:
			print "place order error" #TODO add a auto-retry method here
			print "========= DEBUG okcoin.place_order() ==========="
			print res
			return res

	def cancel_order(self, symbol, order_id, post_data={}):
		post_data['order_id'] = order_id
		post_data['symbol'] = symbol
		res = self._private_request(post_data,'POST', '/api/cancelorder.do')
		if res["result"] == True:
			return res
		else:
			print "cancel order failed!" #TODO add a auto-retry method here
			return res
		
	def check_order(self, symbol, order_id = "-1", post_data={}):
		post_data['order_id'] = order_id
		post_data['symbol'] = symbol
		return self._private_request(post_data,'POST', '/api/getorder.do')

