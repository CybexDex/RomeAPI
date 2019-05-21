#romejs

Romejs is a javascript binding for the Cybex ROME API. Romejs is released with built-in signer, so that there is no 
need to run separate signing program. 

Here is the basic usage example.

````javascript

const Cybex = require('romejs');

(async () => {
    const cybex = new Cybex();
    const assetPair = "ETH/USDT";
    
    const orderbook = await cybex.fetchOrderBook(assetPair, 1);
    console.log(orderbook);
    
    const olhcv = await cybex.fetchOHLCV(assetPair);
    console.log(olhcv);
    
    const balance = await cybex.fetchBalance("shanti001");
    console.log(balance);
    
    const pubTrades = await cybex.fetchTrades(assetPair, true, 5);
    console.log(pubTrades);
    
 
    const r = await cybex.setSigner({accountName:"accountName", "password":"password"});
    // accountName is always necessary
    // const r = await cybex.setSigner({accountName:"accountName", account:"1.2.xxxxx", "key":"private_key"});
    const res= cybex.createMarketBuyOrder(assetPair, 0.01);
    console.log(res);
    
})();

````


## supported methods

Please note that, instead of orderId, transactionId is used to track orders in ROME API, like querying and cancelling. 
TransactionId can be obtained as the result of order creation.

All methods are async. 

### Market Data

**fetchMarkets ():** 
Fetches a list of all available markets from an exchange and returns an array of markets (objects with properties such as assetPair, base, quote etc.). Some exchanges do not have means for obtaining a list of markets via their online API. For those, the list of markets is hardcoded.

**loadMarkets ([reload]):**
Returns the list of markets as an object indexed by assetPair and caches it with the exchange instance. Returns cached markets if loaded already, unless the reload = true flag is forced.

**fetchOrderBook (assetPair[, limit = undefined[, params = {}]]):** 
Fetch order book for a particular market trading assetPair.

**fetchTrades (assetPair[, since[, [limit, [params]]]]):**
Fetch recent trades for a particular trading assetPair.

**fetchOHLCV (assetPair, interval = '1m')**
Fetch OHLCV(Kline) information of given assetPair and interval.

### Account specific query

**fetchBalance (accountName)** 
Fetch Balance of the given accountName.

**fetchOrder (transactionId[, accountName[, params]])**
Fetch the order details of a given transactionId of the given accountName.

**fetchOrders ([assetPair[, accountName[, limit[, params]]]])**
Fetch all orders of an assetPair of the given accountName

**fetchOpenOrders ([assetPair[, accountName, params]]]])**
Fetch all open orders of an assetPair of the given accountName

**fetchClosedOrders ([assetPair[, accountName[, params]]])**
Fetch all closed orders of an assetPair of the given accountName

**fetchMyTrades ([assetPair[, accountName[, limit[, params]]]])**
Fetch all trades of an assetPair of the given accountName

### Order Execution

**createOrder(assetPair, side, amount, price)**
Create order with given params

**createLimitBuyOrder (assetPair, amount, price[, params])**
Create limit buy order with given params

**createLimitSellOrder (assetPair, amount, price[, params])**
Create limit sell order with given params

**createMarketBuyOrder (assetPair, amount[, params])**
Create limit buy order with given params and best ask price

**createMarketSellOrder (assetPair, amount[, params])**
Create limit sell order with given params and best bid price

**cancelOrder (transactionId[, params])**
Cancel order with transactionId

**cancelAll(assetPair[, params])**
Cancel all orders
