# CYBEX API library

 The CYBEX API library is used to connect and trade with decentralized realtime cryptocurrency exchange CYBEX. Trading process on decentralized exchange is different from others by nature, instead of logging in a session with passwords, all API endpoints are publicly open, but one would need his/her very own private key to sign a request for authentication.

 This library is inspired by CCXT, an extendable, easy to use, exchange connection library. Structures and function calls are roughly the same. We also utilized a library coincurve with high performance C extension secp256k1 to accelerate signing process, approximately 5ms for one signature. We will try to get listed in ccxt in the coming future.

## Installation

 `pip install cybex-rome`

 requirements: python>2.7 or python>3.5. We will drop support for python 2 later.

## Supported function calls

### Construct Cybex(account, private_key)
 Construct an cybex object with your account name and private key. Note that account name is not your login account name and password.
 
  ```Python
 from romeapi import Cybex
 cybex = Cybex(accountName="xxxx", private_key="xxxxxxxxxxxxxxxxxxxxxx")
 # if you know your account, you may also provide it at initialization
 # otherwise, it will find for you, which might take a little time
 # cybex = Cybex(accountName="xxxx", private_key="xxxxxxxxxxxxxxxxxxxxxx",account="1.2.xxxx")
 
 # market data
 cybex.load_markets()
 # ticker
 cybex.fetch_ticker("ETH/USDT")
 # private methods
 cybex.fetch_balance()
 ```

### fetch_markets
 Fetches a list of all available markets from an exchange and returns an array of markets (objects with properties such as asset_pair, base, quote etc.). Some exchanges do not have means for obtaining a list of markets via their online API. For those, the list of markets is hardcoded.

### load_markets ([reload]):
 Returns the list of markets as an object indexed by asset_pair and caches it with the exchange instance. Returns cached markets if loaded already, unless the reload = true flag is forced.
    
### fetch_order_book(asset_pair[, limit = undefined[, params = {}]]): 

 Fetch order book for a particular market trading asset_pair.

### fetch_trades(asset_pair[, [limit, [params]]]): 
 Fetch recent trades for a particular trading asset_pair.

### fetch_balance(): 
 Fetch user account Balance.

### create_order(asset_pair, type, side, amount[, price[, params]])
 Create an LIMIT order with given params 
 
### create_limit_buy_order(asset_pair, amount, price[, params])
 Create a new limit buy order
 
### create_limit_sell_order(asset_pair, amount, price[, params])
 Create a new limit sell order
 
### create_market_buy_order(asset_pair, amount[, params])
 As cybex exchange don't support market order, this function creates a new limit buy order with the best price
 
### create_market_sell_order(asset_pair, amount[, params])
 As cybex exchange don't support market order, this function creates a new limit sell order with the best price
 
### cancel_order(id[, params])
 Cancel order with given id
 
### fetch_order(id[, asset_pair[, params]])
 Fetch an order detail with given id
 
### fetch_orders([asset_pair[, since[, limit[, params]]]])
 Fetch orders with a given asset pair
 
### fetch_open_orders([asset_pair[, since, limit, params]]]])
 Fetch users open orders with a given asset pair
 
### fetch_closed_orders([asset_pair[, since[, limit[, params]]]])
 Fetch users closed orders with a given asset pair
 
### fetch_my_trades([asset_pair[, since[, limit[, params]]]])
 Fetch users trade history
  
### fetch_best_price([asset_pair[, params]])
 Fetch currently best bid and ask price of a given asset pair
 
 
 ## FAQ
 
 ### Why we should use this library?
 Cybexapi library is connected to CYBEX ROME (Realtime Order Matching Engine) directly through API server. High frequency trading, like market making, is thus made possible on a decentralized exchange. 
 This library utilized coincurve to improve performance, so that it is efficient, cross platform, responsive, and easy to use.
 
 ### Are API endpoints connected to CYBEX witness node/full node?
 No, api server is connected to ROME(Realtime Order Matching Engine)
 
 ### What is the difference of this library from PyCybex?
 PyCybex is forked from the bitshares python library, so that requests are executed mainly on full node. 
 
 Visit [PyCybex's site](#https://github.com/CybexDex/cybex-node-doc/tree/master/transaction/python) to find more details. 
 
 
 ### Can I choose to use PyCybex instead?
 Sure, but you might find it less efficient. 
 
 Visit [PyCybex's site](#https://github.com/CybexDex/cybex-node-doc/tree/master/transaction/python) to find more details.
