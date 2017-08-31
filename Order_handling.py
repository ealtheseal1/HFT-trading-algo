# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 22:06:44 2017

@author: ealun
"""

#Orderhandling

#API, Pandas
import pandas_datareader as pdr
import datetime 

#API , IBPy
from ib.ext.Contract import Contract   
from ib.ext.Order import Order
from ib.opt import Connection, message

def error_handler(msg):
    """Handles the capturing of error messages"""
    print "Server Error: %s" % msg

def reply_handler(msg):
    """Handles of server replies"""
    print "Server Response: %s, %s" % (msg.typeName, msg)

    
def create_contract(symbol, sec_type, exch, prim_exch, curr):
  
    contract = Contract()
    contract.m_symbol = symbol
    contract.m_secType = sec_type
    contract.m_exchange = exch
    contract.m_primaryExch = prim_exch
    contract.m_currency = curr
    return contract
    
def create_order(order_type, quantity, action):
    """Create an Order object (Market/Limit) to go long/short.

    order_type - 'MKT', 'LMT' for Market or Limit orders
    quantity - Integral number of assets to order
    action - 'BUY' or 'SELL'"""
    order = Order()
    order.m_orderType = order_type
    order.m_totalQuantity = quantity
    order.m_action = action
    return order
    
    
if __name__ == '__main__':
    
    tws_conn = Connection.create(port=7496, clientId=100)
    tws_conn.connect()
    tws_conn.register(error_handler, 'Error')
    tws_conn.registerAll(reply_handler)

    # Create an order ID which is 'global' for this session. This
    # will need incrementing once new orders are submitted.
    order_id = 1

    # Create a contract in GOOG stock via SMART order routing
    goog_contract = create_contract('GOOG', 'STK', 'SMART', 'SMART', 'USD')

    # Go long 100 shares of Google
    goog_order = create_order('MKT', 100, 'BUY')

    # Use the connection to the send the order to IB
    tws_conn.placeOrder(order_id, goog_contract, goog_order)

    # Disconnect from TWS
    tws_conn.disconnect()