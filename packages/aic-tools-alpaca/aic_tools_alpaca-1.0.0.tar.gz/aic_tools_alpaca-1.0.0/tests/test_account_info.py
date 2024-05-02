import unittest
import random
from unittest.mock import patch
from aic_tools_alpaca.account_info import (
    CheckIfTradingBlocked, GetNonMarginableBuyingPower, GetTotalBuyingPower, GetAccountEquity
)


class TestAccountFunctions(unittest.TestCase):
    @staticmethod
    def _set_mock_acc_attribute(mock_acc, attribute_name, value):
        setattr(mock_acc, attribute_name, value)

    def _test_account_buying_powers(self, mock_acc, account_info_class, attribute_name):
        random_value = random.randint(0, 999999)
        self._set_mock_acc_attribute(mock_acc, attribute_name, random_value)
        self.assertEqual(account_info_class()._run(), f"{random_value}$")

    @patch('aic_tools_alpaca.account_info.acc')
    def test_check_trading_blocked_true(self, mock_acc):
        self._set_mock_acc_attribute(mock_acc, 'trading_blocked', True)
        self.assertTrue(CheckIfTradingBlocked()._run())

    @patch('aic_tools_alpaca.account_info.acc')
    def test_check_trading_not_blocked_false(self, mock_acc):
        self._set_mock_acc_attribute(mock_acc, 'trading_blocked', False)
        self.assertFalse(CheckIfTradingBlocked()._run())

    @patch('aic_tools_alpaca.account_info.acc')
    def test_total_buying_power(self, mock_acc):
        self._test_account_buying_powers(mock_acc, GetTotalBuyingPower, 'buying_power')

    @patch('aic_tools_alpaca.account_info.acc')
    def test_non_margin_buying_power(self, mock_acc):
        self._test_account_buying_powers(mock_acc, GetNonMarginableBuyingPower, 'non_marginable_buying_power')

    @patch('aic_tools_alpaca.account_info.acc')
    def test_account_equity(self, mock_acc):
        self._test_account_buying_powers(mock_acc, GetAccountEquity, 'equity')


if __name__ == '__main__':
    unittest.main()
