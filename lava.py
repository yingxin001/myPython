#!/usr/bin/python
#Filename:lava.py
from __future__ import division
import urllib2
import json
import sys
import timeit 
import hmac
import hashlib
import time
import urllib
import os

BASE_URL = 'https://yunbi.com'

API_PATH_DICT={
  'makets' : '/api/v2/k.jason',
  'deposit_address' : '/api/v2/deposit_address.jason',
  'order_book':'/api/v2/order_book.json',
  'cancelOrder':'/api/v2/orders/clear.json'
}

def getUriPath(name):
  return API_PATH_DICT[name]

def makeurlparam(params):
  keys = params.keys()
  keys.sort()
  query = ''
  for key in keys:
     # print key,params[key]
	 value = params[key]
	 query = "%s&%s=%s" % (query, key, value) if len(query) else "%s=%s" % (key, value)
  return query


def kline():
	timestamp = time.mktime(time.strptime('2017-8-30 15:00','%Y-%m-%d %H:%M'))
	q = BASE_URL+getUriPath('makets')+'?'+makeurlparam({'market':'eoscny','limit':'10','period':'30','timestamp':timestamp})
	print q
	resp = urllib2.urlopen(q)
	respJason = resp.readlines()
	if len(respJason):
		data = json.loads(respJason[0])
		print 'jason:'
		print data

	for i in range(len(data)):
	  #print time.ctime(data[i][0])
	  print time.strftime('%Y-%m-%d %X',time.localtime(data[i][0]))
	  print 'time:%s O:%s H:%s L:%s C:%s vol:%s'%tuple(data[i])
	  print '\n'
#kline()


		 
from conf import ACCESS_KEY, SECRET_KEY
access_key = ACCESS_KEY
secret_key = SECRET_KEY
def genSignature(verb, uri, params):
    str2 = makeurlparam(params)
    msg = '|'.join([verb,uri,str2])
    print 'msg:'+msg
    signature = hmac.new(SECRET_KEY, msg=msg, digestmod=hashlib.sha256).hexdigest()    
    return signature
	

def doGET(base,uri,params=None):
    verb = 'GET'	
    signature = genSignature(verb,uri,params)
    print 'signature: %s'%(signature)
    params['signature']=signature
    header = {'Accept': 'application/json'}
    q = base+uri+'?'+ makeurlparam(params)
    print q

    try:
      req = urllib2.Request(url=q, headers=header)
      print 'req:  %s' %req
      print dir(req)
      resp = urllib2.urlopen(req)
      respJason = resp.readlines()
      if len(respJason):
	      data = json.loads(respJason[0])
	      print 'responseJason:%s'%data
    except  urllib2.URLError, e:
       print 'catch doGET http error:\n%s ' %e.reason
    except:
       print "do GET error:%s"%q

def doPOST(base,uri,params=None):
    verb = 'POST'	
    signature = genSignature(verb,uri,params)
    print 'signature: %s'%(signature)
    params['signature']=signature
    header = {'Accept': 'application/json','Content-Type': 'application/x-www-form-urlencoded'}
    q = base+uri
    print q

    try:
      jdata=makeurlparam(params)
      req = urllib2.Request(url=q, headers=header,data=jdata)
      print 'req:  %s' %q
      print 'jdata: %s' %jdata
      resp = urllib2.urlopen(req)#(q,jdata)
      respJason = resp.readlines()
      if len(respJason):
	      data = json.loads(respJason[0])
	      print 'responseJason:%s'%data
    except  urllib2.URLError, e:
       print 'catch doPOST http error:\n%s ' %e.reason
    except:
       print "do POST error:%s"%q
)


def getServerTimeStamp():
	q='https://yunbi.com/api/v2/timestamp.json'
	resp = urllib2.urlopen(q)
	respJason = resp.readlines()
	if len(respJason):
		data = json.loads(respJason[0])
		print 'timestamp:%s'%data
	return data

def getTonce():
	return int(1000*time.time())

def callDeposite():
  params = {'tonce':getTonce() , 'access_key': ACCESS_KEY, 'currency':'eos'}
  print params 
  doGET(BASE_URL,getUriPath('deposit_address'), params)
#callDeposite()


def getOrderBook():
   params = {'market':'eoscny', 'asks_limit':20, 'bids_limit':20}
   doGET(BASE_URL,getUriPath('order_book'), params)
#getOrderBook()

#
"""
If present, only sell orders (asks) or buy orders (bids) will be canncelled.
"""
def cancelOrders():
   params={'access_key':ACCESS_KEY, 'tonce':getTonce()}
   doPOST(BASE_URL,getUriPath('cancelOrder'), params)
cancelOrders()


