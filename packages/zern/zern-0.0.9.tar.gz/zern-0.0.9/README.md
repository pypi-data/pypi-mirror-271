# Zern Class Documentation

This is a free library. This doesn't require any subscription to use. 

## Documentation

```python
from zern import Trader
trader = Trader(user_name=YOUR_USERNAME,password=YOUR_PASSWORD,totp_key=YOUR_TOTP_KEY)
```

The `Trader` class is used to initiate the trading process and interact with the trading platform. It provides various methods to retrieve data, manage orders, and access trading information.

Check below in TOTP section if you need to get the totp key.

#### → GET YOUR INSTRUMENTS TOKENS HERE (If Required)
```python
trader.instruments #this will contain all the instrument tokens and symbols. feel free to search it as per your requirements. the helper functions also use this variable.
```


## Essential Methods

```python
trader.historical_data(instrument_token, start_date, end_date, interval='5minute')  #Retrieves historical data for a specific instrument within a specified time range.
```

- `instrument_token` (int): The unique identifier of the instrument.
- `start_date` (str or datetime.datetime): The start date of the historical data (format: 'YYYY-MM-DD').
- `end_date` (str or datetime.datetime): The end date of the historical data (format: 'YYYY-MM-DD').
- `interval` (str, optional): The interval for data (default: '5minute').


```python
trader.get_orders()  # Retrieves the list of orders placed by the trader.
```

```python
trader.get_positions() #Retrieves the current positions held by the trader.
```

```python
trader.get_holdings()  #Retrieves the holdings (securities owned) by the trader.
```

```python
trader.get_margins()  #Retrieves the margin details for the trader's account.
```

```python
trader.get_profile()  #Retrieves the trader's profile information.
```

```python
trader.check_app_sessions()  #Checks the active sessions for the trading application.
```
### buy and sell order placement
```python
trader.place_order(symbol, exchange, transaction_type, quantity)  #Places an order for a specific security. returns order_id 
```
required arguments:
- `symbol` (str): The symbol of the security.
- `exchange` (str or zern.utils.Types.EXCHANGE): The exchange where the security is listed (e.g., zern.utils.Types.EXCHANGE.NSE, zern.utils.Types.EXCHANGE.NFO).
- `transaction_type` (str or zern.utils.Types.TRANSACTION_TYPE): The type of transaction (e.g., zern.utils.Types.TRANSACTION_TYPE.BUY , zern.utils.Types.TRANSACTION_TYPE.SELL).
- `quantity` (int): The quantity of securities to transact.
optional keyword arguments
- `variety` (str or zern.utils.Types.VARIETY=VARIETY.REGULAR): if the order is regular, iceberg or cover order etc (e.g. VARIETY.REGULAR)
- `product`(str or zern.utils.Types.PRODUCT=PRODUCT.NRML): if order is normal or intraday (MIS) or cash n carry (CNC) (e.g. PRODUCT.NRML)
- `order_type` (str or zern.utils.Types.ORDER_TYPE=ORDER_TYPE.MARKET): if order is a type of market or limit order (e.g. ORDER_TYPE.MARKET)
- `validity` (str or zern.utils.Types.VALIDITY=VALIDITY.DAY): if order needs to be immediate (IOC) or in the day (DAY) (e.g. VALIDITY.DAY)
- `price` (str='0') : if order is limit order, it needs to be parsed into string.
- `trigger_price` (str='0') : if order is limit order, the price where it needs to trigger.
- `stoploss` (str='0') : if order needs a stoploss, the price where the stoploss is to be set.

## HELPER FUNCTIONS

```python
get_bnf_expiries()  #Retrieves the expiry dates for BANKNIFTY derivatives.
```

```python
get_expiries(derivative_name)  #Retrieves the expiry dates for a specific derivative.
```

- `derivative_name` (str): The name of the derivative.

```python
get_derivatives_list()  #Retrieves the list of available derivatives.
```

```python
get_current_expiries()  #Retrieves the expiry dates for BANKNIFTY derivative.
```

## Live WebSocket Instructions (Important if you want to use Live Data)

when `Trader` is initatiated, a Ticker is also instantiated with it and is subscribed to BANKNIFTY and NIFTY50 at the start. 

the data is then stored in `trader.ticker.last_msg` and the time recieved is recorded in `trader.ticker.last_msg_time`

the websocket updates these two variables `trader.ticker.last_msg` and `trader.ticker.last_msg_time`, so you you can keep a while loop fetching the variables as per your requirement.

## Live Functions

```python
trader.ticker.subscribe(tokens: Union[List[int], int],mode=MODE_STRING.modeLTPC)  #subscribe the tokens as a list of instrument tokens or just an instrument token
```
- `tokens` (list , int): Expects a list of integers (instrument tokens) or just an integer (one intrument token)
- `mode` (zern.utils.Types.MODE_STRING): Expects a MODE_STRING object which is usually a string. (inspect the zern.utils.Types for more information)

```python
trader.ticker.unsubscribe(self, tokens: Union[List[int], int],mode=MODE_STRING.modeLTPC)  #unsubscribes the tokens as a list of instrument tokens or just an instrument token
```
- `tokens` (list , int): Expects a list of integers (instrument tokens) or just an integer (one intrument token)
- `mode` (zern.utils.Types.MODE_STRING): Expects a MODE_STRING object which is usually a string. (inspect the zern.utils.Types for more information)

## getting TOTP key

**_TOTP key can only be extracted from PC (mobile does not have it)_**

1) go to MyProfile  -> password and Security.
2) ![final1](https://github.com/ExBlacklight/Zern/assets/37045428/6af536ff-11c2-4a2d-b6cd-93c1a72e861e)
3) ![final2](https://github.com/ExBlacklight/Zern/assets/37045428/672c1c1c-4aa0-4fa1-b75f-45a65469ff9e)
4) copy key from there to your script and you can use it as TOTP key for automatic TOTP authentication.
5) (Optional) if you already have TOTP enabled, you need to disable TOTP and do this process again to get the key, otherwise no other way.
