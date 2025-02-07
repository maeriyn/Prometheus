from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies import Strategy
from lumibot.traders import Trader
from datetime import datetime
from alpaca_trade_api.rest import REST
from timedelta import Timedelta

API_KEY = "PKLYMJV11F3OGLU7OFBY"
API_SECRET = "krjSQsiCplG0AznPkwGC321KK1AhwMfCSyTw7gZS" 
BASE_URL = "https://paper-api.alpaca.markets/v2"

ALPACA_CREDS = {
    "API_KEY": API_KEY,
    "API_SECRET": API_SECRET,
    "PAPER": True
}

class Prometheus(Strategy):
    def initialize (self, symbol:str="SPY", cash_at_risk:float=.5):
        self.symbol = symbol
        self.sleeptime = "12H"
        self.last_trade = None
        self.cash_at_risk = cash_at_risk
        self.api = REST(base_url = BASE_URL, key_id = API_KEY, secret_key = API_SECRET)

    def position_sizing(self):
        cash = self.get_cash()
        last_price = self.get_last_price(self.symbol)
        quantity = round(cash * self.cash_at_risk / last_price, 0)
        return cash, last_price, quantity
    
    def get_dates(self):
        today = self.get_datetime()
        three_days_ago = today - Timedelta(days = 3)
        return today.strftime('Y-%m-%d'), three_days_ago.strftime('%Y-%m-%d')

    def get_news (self):
        today, three_days_ago = self.get_dates()
        self.api.get_news(symbol = self.symbol, start = three_days_ago, end = today)
        news = [ev.__dict__["raw"]["headline"] for ev in news]
        return news

    def on_trading_iteration(self):
        cash, last_price, quantity = self.position_sizing()

        if cash > last_price:
            if self.last_trade == None:
                news = self.get_news()
                print(news)
                order = self.create_order(
                    self.symbol, quantity, "buy", 
                    type = "bracket",
                    take_profit_price = last_price*1.075,
                    stop_loss_price = last_price*.95)
                self.submit_order(order)
                self.last_trade = "buy"

start_date = datetime(2024,12,15)
end_date = datetime(2024,12,20)

broker = Alpaca(ALPACA_CREDS)

strategy = Prometheus(name='mls', broker = broker, parameters = {"symbol": "NVDA", "cash_at_risk": .5})

strategy.backtest(
    YahooDataBacktesting,
    start_date,
    end_date,
    parameters = {"symbol": "SPY"}
)
