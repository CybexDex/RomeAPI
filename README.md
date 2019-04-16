# CYBEX ROME API Library

 The CYBEX ROME(Realtime Order Matching Engine) API library is designed to connect and trade on the exchange efficiently. Since Cybex is based on a decentralized blocchain, instead of logging in a session with passwords, all the API endpoints are public, but one would need his/her very own private key to sign a request for authentication.

 Here we utilized a library *coincurve* with high performance C extension *secp256k1* to accelerate the signing process, approximately 5ms for one signature. This API library is inspired by CCXT, an extendable, easy to use, exchange connection library. 
 
 We will try to get listed in *CCXT* in the coming future.

## Installation

 `pip install romeapi`

 NOTE: 
 1. python>=3.5 is required as python 2.x does not support *bytes* type, which is essential for signature generation.
 1. if both python 2.x and python 3.x exist, and python 3.x *virtual env* is not activated, then use `pip3 install romeapi`

## Demo Application

A [demo application](https://github.com/CybexDex/cybex-python-demo) is available for quick start on how to use the CYBEX ROME API library.

## API Methods

Please note the order type notation of Cybex ROME.
 
ID |Status | Type* | Details 
----|---------|---- | ------- 
1|PENDING_NEW| open |New valid order, confirmed by ROME but not yet confirmed on chain.  
2|OPEN| open | Open order, confirmed on chain. Status may change to either CANCELED or FILLED.   
3|PENDING_CXL| open |Cancel order confirmed by ROME, not yet confirmed on chain.
4|CANCELED| closed |Order cancelled by user or expired, confirmed on chain.
5|FILLED | closed |Order fully filled. Filled order cannot be canceled.
6|REJECTED| closed |Order rejected by ROME if not valid. Order rejected by ROME will not go to chain.

Order type is the category for function call get_open_orders and get_closed_orders. 

### Construct Cybex(account, password)  (Recommended)
Construct a *Cybex* object with your account name and password.

```Python
 from romeapi import Cybex
 # init with accountName and password
 cybex = Cybex(accountName="sample_user", password="sample_password")
 
 # market data
 cybex.load_markets()
 # ticker
 cybex.fetch_ticker("ETH/USDT")
 # check account balance
 cybex.fetch_balance()
 # query with transcation id
  # create a market buy order
 order_transaction_id, result = cybex.create_market_buy_order("ETH/USDT", 0.1)
 orders = cybex.fetch_order(order_transaction_id)
 # cancel order
 cancel_order = cybex.cancel_order(order_transaction_id)
```

### Construct Cybex(account, private_key) (Optional)
Optionally, you can construct a *Cybex* object with your account name and private key
NOTE that the private key is not your logon password on the CYBEX exchange. 
To find your private key, refer to [demo application](https://github.com/CybexDex/cybex-python-demo). 
 
```Python
cybex = Cybex(accountName="sample_user", key="private_key")
```

If you know your account id, you can optionally provide it to speed up the initialization, e.g.
```Python
cybex = Cybex(accountName="sample_user", password="sample_password", account="1.2.00000") 
# or
# cybex = Cybex(accountName="sample_user", key="private_key", account="1.2.00000") 
```


### fetch_markets
 Fetch the list of all available markets from an exchange and returns an array of markets (objects with properties such as asset_pair, base, quote etc.). Some exchanges do not have means to obtain a list of markets via their online API. For those, the list of markets is hardcoded.

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
 Fetch user's open orders with a given asset pair
 
### fetch_closed_orders([asset_pair[, since[, limit[, params]]]])
 Fetch user's closed orders with a given asset pair
 
### fetch_my_trades([asset_pair[, since[, limit[, params]]]])
 Fetch user's trade history
  
### fetch_best_price([asset_pair[, params]])
 Fetch current best bid and ask prices for a given asset pair
 
### fetch_ohlcv(self, asset_pair, interval='1m', limit=5, useTradePrice='true')
 Fetch kline data for a given asset pair. 

Parameter | Description |
---|---|
*interval* | The possible values are *1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M.* The default value is 1m. 
*useTradePrice* | The default value is *true*, and this api returns our exchange's prices. If it is specified as *false* then this api returns market prices.
 
### fetch_klines(self, asset_pair, interval='1m', limit=5, useTradePrice='true')
 Alias to *fetch_ohlcv*
 
 
 ## FAQ
 
 ### Why should we use this library?
 The CYBEX ROME API library provides convenient access to the CYBEX ROME (**R**ealtime **O**rder **M**atching **E**ngine) directly through the API server. High frequency trading or market making is thus made possible on our decentralized exchange. 
 This API library utilizes *coincurve* to improve performance, so that it is efficient, cross platform, responsive, and easy to use.
 
 ### Are the API endpoints connected to the CYBEX witness nodes/full nodes?
 No, the API server is connected to the ROME (**R**ealtime **O**rder **M**atching **E**ngine). Our previous library PyCybex is connected to full nodes.
 
 ### What is the difference of this library from PyCybex?
 PyCybex is forked from the bitshares python library, so that requests are executed mainly on full nodes. It takes at least one block time to confirm order. 
 
 Visit [PyCybex's site](#https://github.com/CybexDex/cybex-node-doc/tree/master/transaction/python) to find more details. 
 
 
 ### Can I choose to use PyCybex instead?
 Yes, you can. But you might find it less efficient. 
 
 Visit [PyCybex's site](#https://github.com/CybexDex/cybex-node-doc/tree/master/transaction/python) to find out more details.
