from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies import Strategy
from lumibot.traders import Trader
from datetime import datetime

API_KEY = "PKLYMJV11F3OGLU7OFBY"
API_SECRET = "krjSQsiCplG0AznPkwGC321KK1AhwMfCSyTw7gZS" 
BASE_URL = "https://paper-api.alpaca.markets/v2"

ALPACA_CREDS = {
    "API_KEY": API_KEY,
    "API_SECRET": API_SECRET,
    "PAPER": True
}

class Prometheus(Strategy):
    def initialize (self, symbol:str="SPY"):
        self.symbol = symbol
        self.sleeptime = "12H"
        self.last_trade = None

    def on_trading_iteration(self):
        if self.last_trade == None:
            order = self.create_order(self.symbol, 10, "buy", type = "market")
            self.submit_order(order)
            self.last_trade = "buy"

start_date = datetime(2022,12,15)
end_date = datetime(2024,12,20)

broker = Alpaca(ALPACA_CREDS)

strategy = Prometheus(name='mls', broker = broker, parameters = {"symbol": "NVDA"})

strategy.backtest(
    YahooDataBacktesting,
    start_date,
    end_date,
    parameters = {"symbol": "SPY"}
)
