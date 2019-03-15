# CYBEX ROME API Library

 The CYBEX ROME API library is used to connect and trade with the decentralized realtime cryptocurrency exchange - CYBEX. The trading process on a decentralized exchange is different from others by nature, instead of logging in a session with passwords, all the API endpoints are publicly open, but one would need his/her very own private key to sign a request for authentication.

 This API library is inspired by CCXT, an extendable, easy to use, exchange connection library. Structures and function calls are roughly the same. We also utilized a library *coincurve* with high performance C extension *secp256k1* to accelerate the signing process, approximately 5ms for one signature. We will try to get listed in *CCXT* soon.

## Installation

 `pip3 install romeapi`

 requirements: python>=3.5. As python 2 dont support bytes type, which is essential at generating signatures.

## Demo Application

A [demo application](https://github.com/CybexDex/cybex-python-demo) is available for quick start on how to use the CYBEX ROME API library.

## Supported function calls

### Construct Cybex(account, private_key)
Construct a *Cybex* object with your account name and private key, optionally with an account id. 
Note that the private key is not your login password on the CYBEX exchange.


  ```Python
 from romeapi import Cybex
 # init with accountName and password
 cybex = Cybex(accountName="sampleuser", password="samplepassword")
 # If you know your account id and private key, you may use it for initialization
 # API will find account for you with given accountName, which might take a little time.
 # cybex = Cybex(accountName="sampleuser", key="xxxxxxxxxxxxxxxxxxxxxx", account="1.2.00000")
 
 # market data
 cybex.load_markets()
 # ticker
 cybex.fetch_ticker("ETH/USDT")
 # private methods
 cybex.fetch_balance()
 ```


### fetch_markets
 Fetch the list of all available markets from an exchange and returns an array of markets (objects with properties such as asset_pair, base, quote etc.). Some exchanges do not have means for obtaining a list of markets via their online API. For those, the list of markets is hardcoded.

### load_markets ([reload]):
 Return the list of markets as an object indexed by asset_pair and caches it with the exchange instance. Return the cached markets if loaded already, unless the reload = true flag is forced.
    
### fetch_order_book(asset_pair[, limit = undefined[, params = {}]]): 

 Fetch the order book for a particular market trading asset pair.

### fetch_trades(asset_pair[, [limit, [params]]]): 
 Fetch the recent trades for a particular trading asset pair.

### fetch_balance(): 
 Fetch the user account balance.

### create_order(asset_pair, type, side, amount[, price[, params]])
 Create a limit order with given params 
 
### create_limit_buy_order(asset_pair, amount, price[, params])
 Create a new limit buy order
 
### create_limit_sell_order(asset_pair, amount, price[, params])
 Create a new limit sell order
 
### create_market_buy_order(asset_pair, amount[, params])
 As the CYBEX exchange does not support market order, this function creates a new limit buy order with the best price
 
### create_market_sell_order(asset_pair, amount[, params])
 As the CYBEX exchange does not support market order, this function creates a new limit sell order with the best price
 
### cancel_order(id[, params])
 Cancel an order with a given transaction id
 
### fetch_order(id[, asset_pair[, params]])
 Fetch an order's detail with a given transaction id
 
### fetch_orders([asset_pair[, since[, limit[, params]]]])
 Fetch orders with a given asset pair
 
### fetch_open_orders([asset_pair[, since, limit, params]]]])
 Fetch users' open orders with a given asset pair
 
### fetch_closed_orders([asset_pair[, since[, limit[, params]]]])
 Fetch users' closed orders with a given asset pair
 
### fetch_my_trades([asset_pair[, since[, limit[, params]]]])
 Fetch users' trade history
  
### fetch_best_price([asset_pair[, params]])
 Fetch currently best bid and ask prices for a given asset pair
 
 
 ## FAQ
 
 ### Why should we use this library?
 The CYBEX API library is connected to the CYBEX ROME (Realtime Order Matching Engine) directly through the API server. High frequency trading, like market making, is thus made possible on our decentralized exchange. 
 This API library utilizes *coincurve* to improve performance, so that it is efficient, cross platform, responsive, and easy to use.
 
 ### Are API endpoints connected to CYBEX witness node/full node?
 No, the API server is connected to ROME(Realtime Order Matching Engine)
 
 ### What is the difference of this library from PyCybex?
 PyCybex is forked from the bitshares python library, so that requests are executed mainly on full nodes. 
 
 Visit [PyCybex's site](#https://github.com/CybexDex/cybex-node-doc/tree/master/transaction/python) to find more details. 
 
 
 ### Can I choose to use PyCybex instead?
 Sure, but you might find it less efficient. 
 
 Visit [PyCybex's site](#https://github.com/CybexDex/cybex-node-doc/tree/master/transaction/python) to find more details.
