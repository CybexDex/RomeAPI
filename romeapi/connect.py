import requests

import struct
from binascii import unhexlify
from datetime import datetime
import time

from .core import operations, signedtransactions
# from bitsharesbase import operations, signedtransactions

from .core.ecdsa import quick_sign_message
import graphenebase.ecdsa

from graphenebase.account import PasswordKey

""" CCXT

The unified ccxt API is a subset of methods common among the exchanges. It currently contains the following methods:

fetch_markets (): Fetches a list of all available markets from an exchange and returns an array of markets (objects with properties such as assetPair, base, quote etc.). Some exchanges do not have means for obtaining a list of markets via their online API. For those, the list of markets is hardcoded.
load_markets ([reload]): Returns the list of markets as an object indexed by assetPair and caches it with the exchange instance. Returns cached markets if loaded already, unless the reload = true flag is forced.

fetch_order_book (assetPair[, limit = undefined[, params = {}]]): Fetch L2/L3 order book for a particular market trading assetPair.
fetchL2OrderBook (assetPair[, limit = undefined[, params]]): Level 2 (price-aggregated) order book for a particular assetPair.
fetch_trades (assetPair[, since[, [limit, [params]]]]): Fetch recent trades for a particular trading assetPair.
fetch_ticker (assetPair): Fetch latest ticker data by trading assetPair.
fetch_balance (): Fetch Balance.
create_order (assetPair, type, side, amount[, price[, params]])
create_limit_buy_order (assetPair, amount, price[, params])
createLimitSellOrder (assetPair, amount, price[, params])
createMarketBuyOrder (assetPair, amount[, params])
createMarketSellOrder (assetPair, amount[, params])
cancelOrder (id[, assetPair[, params]])
fetchOrder (id[, assetPair[, params]])
fetchOrders ([assetPair[, since[, limit[, params]]]])
fetchOpenOrders ([assetPair[, since, limit, params]]]])
fetchClosedOrders ([assetPair[, since[, limit[, params]]]])
fetchMyTrades ([assetPair[, since[, limit[, params]]]])
fetchOHLCV (assetPair, timeframe = '1m', since = undefined, limit = undefined, params = {})

"""

graphenebase.signedtransactions.sign_message = quick_sign_message

class CybexAPIException(Exception):
    def __init__(self, response):
        self.code = 0
        try:
            json_res = response.json()
        except ValueError:
            self.message = 'Invalid JSON error message from Cybex: {}'.format(response.text)
        else:
            self.code = json_res['code']
            self.message = json_res['msg']
        self.status_code = response.status_code
        self.response = response
        self.request = getattr(response, 'request', None)

    def __str__(self):  # pragma: no cover
        return 'API error (code=%s): %s' % (self.code, self.message)


class CybexRequestException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return 'CybexRequestException: %s' % self.message


class CybexSignerException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return 'CybexSignerException: %s' % self.message


class CybexException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return 'CybexException: %s' % self.message


TS_FORMAT = '%Y-%m-%dT%H:%M:%S'


class Pair:
    def __init__(self, pair, available_assets):
        if "/" in pair:
            _assets = pair.split("/")
            self.base = {"assetPair": _assets[0]}
            self.quote = {"assetPair": _assets[1]}

            for asset in available_assets:
                if asset['assetName'] == self.quote['assetPair']:
                    self.quote.update({
                        "id": asset["assetId"],
                        "precision": asset["precision"]
                    })
                if asset['assetName'] == self.base['assetPair']:
                    self.base.update({
                        "id": asset["assetId"],
                        "precision": asset["precision"]
                    })

    def get_dict(self, side, quantity, price):
        if side == 'buy':
            return self.buy(quantity, price)
        if side == 'sell':
            return self.sell(quantity, price)

        return None

    def sell(self, amount, price):

        return {
            "amount_to_sell": {
                "amount": int(
                    round(float(amount) * 10 ** self.base["precision"])
                ),
                "asset_id": self.base["id"]
            },
            "min_to_receive": {
                "amount": int(
                    round(
                        float(amount)
                        * float(price)
                        * 10 ** self.quote["precision"]
                    )
                ),
                "asset_id": self.quote["id"]
            }
        }

    def buy(self, amount, price):

        return {
            "amount_to_sell": {
                "amount": int(
                    round(float(amount) * float(price) * 10 ** self.quote["precision"])
                ),
                "asset_id": self.quote["id"]
            },
            "min_to_receive": {
                "amount": int(
                    round(
                        float(amount) * 10 ** self.base["precision"]
                    )
                ),
                "asset_id": self.base["id"]
            }
        }


def get_block_params(ref_block_id):
    ref_block_num = int(ref_block_id[:8], 16) & 0xFFFF
    ref_block_prefix = struct.unpack_from("<I", unhexlify(ref_block_id), 4)[0]

    return ref_block_num, ref_block_prefix


def time_string(time_param):
    if isinstance(time_param, datetime):
        return time_param.strftime(TS_FORMAT)
    return time_param

class Signer:
    def __init__(self, account, private_key, refData):

        self.account = account
        self.private_key = private_key

        self.chain = {'chain_id': refData['chainId'], 'core_symbol': 'CYB', 'prefix': 'CYB'}
        self.fees = refData['fees']
        self.pairs = refData['availableAssets']
        self.ref_block_num, self.ref_block_prefix = get_block_params(refData['refBlockId'])

    def signed(self, op, tx_expiration):

        tx = signedtransactions.Signed_Transaction(
            operations=[op],
            ref_block_num=self.ref_block_num,
            ref_block_prefix=self.ref_block_prefix,
            expiration=tx_expiration
        )

        tx.sign([self.private_key], self.chain)

        return tx

    def prepare_order_message(self, asset_pair, side, quantity, price, fillkill=False):

        if side != 'buy' and side != 'sell':
            if Cybex.verbose:
                print("Unsupported side", side)
            return None

        # Temporarily disable is_buy flag so that romeapi works with upgraded cybex uat and production systems
        # is_buy = side == 'buy'
        is_buy = 0

        # time calculation
        utcnow = datetime.utcnow()
        # calculate the time difference between utc now and utc end of day
        exp_utc = datetime(utcnow.year, utcnow.month, utcnow.day, 23, 59, 59)
        # this is the local time, use to timestamp to calculate utc timestamp
        exp = datetime.now() + (exp_utc - utcnow)

        pair = Pair(asset_pair, self.pairs)
        buy_sell = pair.get_dict(side, quantity, price)

        op_data = {
            "fee": {'amount': self.fees['newFee'], 'asset_id': self.fees['feeAssetId']},
            "seller": self.account,
            "amount_to_sell": buy_sell['amount_to_sell'],
            "min_to_receive": buy_sell['min_to_receive'],
            "expiration": exp_utc.strftime(TS_FORMAT),
            "fill_or_kill": fillkill,
        }

        op = operations.Limit_order_create(**op_data)
        tx_expiration_utc_tiemstamp = time.time() + 3600 * 23
        tx_expiration = datetime.utcfromtimestamp(tx_expiration_utc_tiemstamp)
        signed_tx = self.signed(op, tx_expiration.strftime(TS_FORMAT))
        signed_tx_json = signed_tx.json()

        fee = {
            'assetId': signed_tx_json['operations'][0][1]['fee']['asset_id'],
            'amount': signed_tx_json['operations'][0][1]['fee']['amount']
        }

        amountToSell = {
            'assetId': signed_tx_json['operations'][0][1]['amount_to_sell']['asset_id'],
            'amount': signed_tx_json['operations'][0][1]['amount_to_sell']['amount']
        }

        minToReceive = {
            'assetId': signed_tx_json['operations'][0][1]['min_to_receive']['asset_id'],
            'amount': signed_tx_json['operations'][0][1]['min_to_receive']['amount']
        }

        order_msg = {
            'transactionType': 'NewLimitOrder',
            'transactionId': signed_tx.id,
            'refBlockNum': signed_tx_json['ref_block_num'],
            'refBlockPrefix': signed_tx_json['ref_block_prefix'],
            'txExpiration': int(tx_expiration_utc_tiemstamp),
            'fee': fee,
            'seller': signed_tx_json['operations'][0][1]['seller'],
            'amountToSell': amountToSell,
            'minToReceive': minToReceive,
            'expiration': int(exp.timestamp()),
            #'fill_or_kill': int(signed_tx_json['operations'][0][1]['fill_or_kill']),
            'fill_or_kill': int(fillkill),
            'signature': signed_tx_json['signatures'][0],
            'is_buy': int(is_buy)
        }

        return order_msg

    def prepare_cancel_message(self, trxid):
        op = operations.Limit_order_cancel(**{
            'fee': {'amount': self.fees['cancelFee'], 'asset_id': self.fees['feeAssetId']},
            'fee_paying_account': self.account,
            'order': '1.7.0',
            'extensions': [[6, {'trx_id': trxid}]]})

        tx_expiration_utc_tiemstamp = time.time() + 3600 * 23
        tx_expiration = datetime.utcfromtimestamp(tx_expiration_utc_tiemstamp)
        signed_tx = self.signed(op, tx_expiration.strftime(TS_FORMAT))
        signed_tx_json = signed_tx.json()

        fee = {
            'assetId': signed_tx_json['operations'][0][1]['fee']['asset_id'],
            'amount': signed_tx_json['operations'][0][1]['fee']['amount']
        }

        cancel_msg = {
            'transactionType': 'Cancel',
            'transactionId': signed_tx.id,
            'originalTransactionId': trxid,
            'refBlockNum': signed_tx_json['ref_block_num'],
            'refBlockPrefix': signed_tx_json['ref_block_prefix'],
            'txExpiration': int(tx_expiration_utc_tiemstamp),
            'orderId': '0',
            'fee': fee,
            'feePayingAccount': self.account,
            'signature': signed_tx_json['signatures'][0]
        }

        if Cybex.verbose:
            print(cancel_msg)

        return cancel_msg

    def prepare_cancel_all_message(self, asset_pair):
        pair = Pair(asset_pair, self.pairs)
        op = operations.Cancel_all(**{
            "fee": {'amount': self.fees['cancelAllFee'], 'asset_id': self.fees['feeAssetId']},
            "seller": self.account,
            "sell_asset_id": pair.quote['id'],
            "receive_asset_id": pair.base['id']
        })

        tx_expiration_utc_tiemstamp = time.time() + 3600 * 23
        tx_expiration = datetime.utcfromtimestamp(tx_expiration_utc_tiemstamp)
        signed_tx = self.signed(op, tx_expiration.strftime(TS_FORMAT))
        signed_tx_json = signed_tx.json()

        fee = {
            'assetId': signed_tx_json['operations'][0][1]['fee']['asset_id'],
            'amount': signed_tx_json['operations'][0][1]['fee']['amount']
        }

        cancel_all_msg = {
            'transactionType': 'CancelAll',
            'transactionId': signed_tx.id,
            'refBlockNum': signed_tx_json['ref_block_num'],
            'refBlockPrefix': signed_tx_json['ref_block_prefix'],
            'txExpiration': int(tx_expiration_utc_tiemstamp),
            'fee': fee,
            'seller': self.account,
            'sellAssetId': pair.quote['id'],
            'recvAssetId': pair.base['id'],
            'signature': signed_tx_json['signatures'][0]
        }

        if Cybex.verbose:
            print(cancel_all_msg)

        return cancel_all_msg

    def _handle_response(self, response):
        # Return the json object if there is no error
        if not str(response.status_code).startswith('2'):
            raise CybexAPIException(response)
        try:
            data = response.json()
            if 'Status' in data and data['Status'] == 'Failed':
                msg = 'Unknown error'
                if 'Message' in data:
                    msg = data['Message']
                raise CybexSignerException(data[msg])
            return data
        except ValueError:
            raise CybexSignerException('Invalid Response: %s' % response.text)


# order_msg = signer.prepare_order_message(asset_pair='ETH/USDT', price=80, quantity=0.1, side='buy')
class Cybex:
    """Cybex Restful API implementation
    """

    verbose = True
    prod_api_endpoint_root = "https://api.cybex.io/v1"
    uat_api_endpoint_root = "https://apitest.cybex.io/v1"
    prod_chain_endpoint = "https://hongkong.cybex.io/"
    INTERVALS = ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M']

    def __init__(self, accountName, password=None, key=None, account=None, env='prod', timeout=None):

        self.accountName = accountName
        self.signer = None

        if account:
            self.account = account
        else:
            self.account = self._find_account(accountName)
        if env == 'prod':
            self.api_root = self.prod_api_endpoint_root
        elif env == 'uat':
            self.api_root = self.uat_api_endpoint_root
        self.timeout = timeout
        self.markets = []

        # Prepare HTTPS session
        self.session = requests.Session()

        self.session.headers.update({'content-type': 'application/json', 'accept': 'application/json'})
        self._load()

        # user key
        # TODO: verify the password
        user_key = None
        if key is not None:
            user_key = key

        elif password is not None:
            user_key = str(PasswordKey(accountName, password).get_private())

        # else:
        #     raise CybexSignerException('Cannot initialize signer, no valid password or key')

        # check if we find the account at last
        if self.account and user_key:
            self.signer = Signer(self.account, user_key, self.refData)
        # else:
        #     raise CybexSignerException('Cannot initialize signer, no valid account')


    def _load(self):
        url = "%s/refData" % self.api_root
        self.refData = self._handle_response(requests.get(url))

    def load_markets(self, reload=False):
        if reload:
            self._load()
        return self.refData.get('availableAssetPairs', [])

    @property
    def assetPairs(self):
        return [mkt['name'] for mkt in self.markets]

    def market(self, assetPair):
        if assetPair in self.markets:
            return self.markets[assetPair]
        return None

    def _find_account(self, accountName):
        url = self.prod_chain_endpoint+"rpc"
        data = {"method": "call", "params": [0, "lookup_accounts",[accountName, 50]], "id": 1}
        res = requests.get(url, json=data)
        result = res.json()
        if 'result' in result:
            for acc in result['result']:
                if accountName == acc[0]:
                    return acc[1]

    def fetch_ticker(self, assetPair):
        url = self.prod_chain_endpoint
        if '/' in assetPair:
            params = assetPair.split('/')
            newparams = []
            for asset in params:
                if asset != 'CYB' and '.' not in asset:
                    asset = 'JADE.' + asset
                newparams.append(asset)
        data = {"jsonrpc": "2.0", "method": "get_ticker", "params": newparams, "id": 1}
        return self._handle_response(requests.get(url, json=data))

    def fetch_order_book(self, assetPair, limit=3):
        url = '%s/orderBook' % self.api_root
        params = {'assetPair': assetPair, 'limit': limit}
        return self._handle_response(requests.get(url, params=params))

    def fetch_best_price(self, assetPair):
        result = self.fetch_order_book(assetPair)
        return float(result['bids'][0][0]), float(result['asks'][0][0])

    def _send_transaction(self, data):
        url = "%s/transaction" % self.api_root
        headers = {'Content-type': 'application/json'}
        return self._handle_response(requests.post(url, json=data, headers=headers))

    def _handle_response(self, response):
        # Return the json object if there is no error
        if not str(response.status_code).startswith('2'):
            raise CybexAPIException(response)
        try:
            data = response.json()
            if 'Status' in data and data['Status'] == 'Failed':
                msg = 'Unknown error.'
                if 'Message' in data:
                    msg = data['Message']
                if 'rejectReason' in data:
                    msg = data['rejectReason']
                raise CybexRequestException(msg)
            if 'jsonrpc' in data and 'result' in data:
                return data['result']
            return data
        except ValueError:
            raise CybexRequestException('Invalid Response: %s' % response.text)

    def create_order(self, assetPair, side, quantity, price, fillkill):
        if self.signer:
            order_msg = self.signer.prepare_order_message(assetPair, side, quantity, price, fillkill=fillkill)
            if Cybex.verbose:
                print('order_msg', order_msg)
            trx_id = order_msg['transactionId']

            result = self._send_transaction(order_msg)

            return trx_id, result

        return None

    def create_limit_buy_order(self, assetPair, quantity, price, fillkill=False):
        return self.create_order(assetPair, 'buy', quantity, price, fillkill)

    def create_limit_sell_order(self, assetPair, quantity, price, fillkill=False):
        return self.create_order(assetPair, 'sell', quantity, price, fillkill)

    def create_market_buy_order(self, assetPair, quantity, fillkill=False):
        bid, ask = self.fetch_best_price(assetPair)
        # put some buffer in price
        return self.create_order(assetPair, 'buy', quantity, ask * 1.01, fillkill)

    def create_market_sell_order(self, assetPair, quantity, fillkill=False):
        bid, ask = self.fetch_best_price(assetPair)
        # put some buffer in price
        return self.create_order(assetPair, 'sell', quantity, bid * 0.99, fillkill)

    def fetch_balance(self):
        url = "%s/position" % self.api_root
        payload = {'accountName': self.accountName}
        return self._handle_response(requests.get(url, params=payload))

    def cancel_order(self, id):
        if self.signer:
            cancel_msg = self.signer.prepare_cancel_message(id)
            cancel_result = self._send_transaction(cancel_msg)
            return cancel_result
        return None

    def cancel_all(self, assetPair):
        if self.signer:
            cancel_all_msg = self.signer.prepare_cancel_all_message(assetPair)
            cancel_all_result = self._send_transaction(cancel_all_msg)
            return cancel_all_result
        return None

    def fetch_order(self, id):
        url = "%s/order" % self.api_root
        payload = {'accountName': self.accountName, 'transactionId': id}
        return self._handle_response(requests.get(url, params=payload))

    def fetch_orders(self, assetPair=None, reverse=True):
        url = "%s/order" % self.api_root
        payload = {'accountName': self.accountName, "reverse": int(reverse)}
        if assetPair:
            payload["assetPair"] = assetPair
        return self._handle_response(requests.get(url, params=payload))

    def fetch_open_orders(self, since=None, reverse=True):
        url = "%s/order" % self.api_root
        payload = {'accountName': self.accountName, 'orderStatus': 'OPEN, PENDING_NEW, PENDING_CXL', "reverse": int(reverse)}
        if since:
            payload['startTime'] = time_string(since)
        return self._handle_response(requests.get(url, params=payload))

    def fetch_closed_orders(self, since=None, reverse=True):
        url = "%s/order" % self.api_root
        payload = {'accountName': self.accountName, 'orderStatus': 'FILLED, CANCELED, REJECTED', "reverse": int(reverse)}
        if since:
            payload['startTime'] = time_string(since)
        return self._handle_response(requests.get(url, params=payload))

    def fetch_my_trades(self, assetPair=None, since=None, reverse=True):
        url = "%s/trade" % self.api_root
        payload = {'accountName': self.accountName, "reverse": int(reverse)}
        if assetPair:
            payload['assetPair'] = assetPair
        if since:
            payload['startTime'] = time_string(since)
        return self._handle_response(requests.get(url, params=payload))

    def fetch_trades(self, assetPair, limit=20, reverse=True):
        url = "%s/trade" % self.api_root
        payload = {'assetPair': assetPair, "limit": limit, "reverse": int(reverse)}
        return self._handle_response(requests.get(url, params=payload))

    def get_interval(self):
        return self.INTERVALS

    def fetch_ohlcv(self, assetPair, interval='1m', limit=5, useTradePrice='true'):
        url = "%s/klines" % self.api_root

        if interval in self.INTERVALS:
            _interval = interval
        else:
            _interval = self.INTERVALS[0]
        payload = {'assetPair': assetPair, 'interval': _interval, 'useTradePrice': useTradePrice}

        if limit and limit>2:
            payload.update({"limit": limit})
        # payload.update(params)
        return self._handle_response(requests.get(url, params=payload))


# set an alias
Cybex.fetch_klines = Cybex.fetch_ohlcv
