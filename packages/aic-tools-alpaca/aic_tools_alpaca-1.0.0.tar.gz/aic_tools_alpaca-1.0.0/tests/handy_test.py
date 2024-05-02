from aic_tools_alpaca.account_info import (
    CheckIfTradingBlocked, GetNonMarginableBuyingPower, GetTotalBuyingPower, GetAccountEquity
)

print(f"Is trading prohibited: {CheckIfTradingBlocked()._run()}")
print(f"Accountant total purchasing power is: {GetTotalBuyingPower()._run()}")
print(f"Accountant purchasing power without margin is: {GetNonMarginableBuyingPower()._run()}")
print(f"Total equinty is: {GetAccountEquity()._run()}")
