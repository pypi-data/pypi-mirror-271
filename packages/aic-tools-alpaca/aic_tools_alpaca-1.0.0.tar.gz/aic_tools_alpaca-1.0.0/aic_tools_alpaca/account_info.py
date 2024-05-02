import os

from crewai_tools import BaseTool

from dotenv import load_dotenv
from alpaca.trading.client import TradingClient

load_dotenv()
api_key_id = os.getenv('API_KEY_ID')
secret_key = os.getenv('SECRET_KEY')

trading_client = TradingClient(api_key_id, secret_key, paper=True)
acc = trading_client.get_account()


class CheckIfTradingBlocked(BaseTool):
    name: str = "Answer on: is trading prohibited?"
    description: str = """Answers the question whether trading is blocked for this account.
    If true, the account does not allow placing orders.
    If false, the account allows placing orders."""

    def _run(self) -> bool:
        # Your tool's logic here
        return acc.trading_blocked


class GetTotalBuyingPower(BaseTool):
    name: str = "Accountant total purchasing power."
    description: str = """Returns a string with the number of dollars as the purchasing power of the accountant.
    Current available cash buying power. If multiplier = 2 then buying_power = max(equity-initial_margin(0) * 2).
    If multiplier = 1 then buying_power = cash."""

    def _run(self) -> str:
        return f"{acc.buying_power}$"


class GetNonMarginableBuyingPower(BaseTool):
    name: str = "Accountant purchasing power without margin."
    description: str = "Returns a string with the number of dollars as the non marginable buying power for the account."

    def _run(self) -> str:
        return f"{acc.non_marginable_buying_power}$"


class GetAccountEquity(BaseTool):
    name: str = "Answer on: what is portfolio value?"
    description: str = """Returns a string with the numbers of dollars that tell us the account equity.
    This value is cash + long_market_value + short_market_value.
    This value isn’t calculated in the SDK it is computed on the server and we return the raw value here.
    """

    def _run(self) -> str:
        return f"{acc.equity}$"
