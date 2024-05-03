
from zern.Core.session import Session
from datetime import datetime,date,time,timedelta
from zern.utils.OrderedList import OrderedList
from zern.Core.websocket.ticker import Ticker
from zern.utils.Types import PRODUCT,VARIETY,TRANSACTION_TYPE,ORDER_TYPE,VALIDITY,EXCHANGE


class Trader:
    def __init__(self,user_name,password,totp_key) -> None:
        '''
        This Trader is the way to start the Process, the param cred_dict requires ["user_name","password","totp_key"]

        The "totp_key" can be extracted when creating the two factor authentication in the kite app, click on the QR code and use the same key.
        '''
        self.session = Session(user_name,password,totp_key)
        self.instruments = self.session.instruments
        self.startTicker()
        self.ticker = None
    
    def format_date(self,value):
        if isinstance(value,str):
            return value
        elif isinstance(value,datetime):
            return str(value.date())
        elif isinstance(value,date):
            return str(value)
        else:
            raise Exception('expected value types are ["str", "datetime", "date"]\nthe type of value provided is {}'.format(type(value)))
    
    def historical_data(self,instrument_token,start_date,end_date,interval='5minute'):
        url = 'https://kite.zerodha.com/oms/instruments/historical/{}/{}'.format(instrument_token,interval)
        params = {
            'user_id': self.session.user_name,
            'oi': '1',
            'from': self.format_date(start_date),
            'to': self.format_date(end_date),
        }
        return OrderedList(self.session.request(url=url,method=Session.TYPE_GET,params=params)['data']['candles'])
    
    def get_orders(self):
        url = 'https://kite.zerodha.com/oms/orders'
        return self.session.request(url=url,method=Session.TYPE_GET)['data']
    
    def get_positions(self):
        url = 'https://kite.zerodha.com/oms/portfolio/positions'
        return self.session.request(url=url,method=Session.TYPE_GET)['data']
    
    def get_holdings(self):
        url = 'https://kite.zerodha.com/oms/portfolio/holdings'
        return self.session.request(url=url,method=Session.TYPE_GET)['data']
    
    def get_margins(self):
        url = 'https://kite.zerodha.com/oms/user/margins'
        return self.session.request(url=url,method=Session.TYPE_GET)['data']
    
    def get_profile(self):
        url = 'https://kite.zerodha.com/oms/user/profile/full'
        return self.session.request(url=url,method=Session.TYPE_GET)['data']
    
    def check_app_sessions(self):
        url = 'https://kite.zerodha.com/api/user/app_sessions'
        return self.session.request(url=url,method=Session.TYPE_GET)['data']
    
    def place_order(self,symbol,exchange,transaction_type,quantity,
                    variety=VARIETY.REGULAR,
                    product=PRODUCT.NRML,
                    order_type=ORDER_TYPE.MARKET,
                    validity=VALIDITY.DAY,
                    price='0',
                    disclosed_quantity='0',
                    trigger_price='0',
                    squareoff='0',
                    stoploss='0',
                    trailing_stoploss='0'):
        payload = {
            'variety': variety,
            'exchange': exchange,
            'tradingsymbol': symbol,
            'transaction_type': transaction_type,
            'order_type': order_type,
            'quantity': quantity,
            'price': price,
            'product': product,
            'validity': validity,
            'disclosed_quantity': disclosed_quantity,
            'trigger_price': trigger_price,
            'squareoff': squareoff,
            'stoploss': stoploss,
            'trailing_stoploss': trailing_stoploss,
            'user_id': self.session.user_name
        }
        url = 'https://kite.zerodha.com/oms/orders/regular'
        return self.session.request(url=url,method=Session.TYPE_POST,data=payload)['data']

    def startTicker(self):
        self.ticker_ws = Ticker(session=self.session)
    
    def get_bnf_expiries(self):
        return list(self.instruments['derivatives']['BANKNIFTY']['derivatives'].keys())

    def get_expiries(self,derivative_name):
        return list(self.instruments['derivatives'][derivative_name]['derivatives'].keys())
    
    def get_derivatives_list(self):
        return list(self.instruments['derivatives'].keys())

    def get_current_expiries(self,derivative_name):
        current_expiry = self.get_bnf_expiries()[0]
        return self.instruments['derivatives'][derivative_name]['derivatives'][current_expiry[0]]['options']