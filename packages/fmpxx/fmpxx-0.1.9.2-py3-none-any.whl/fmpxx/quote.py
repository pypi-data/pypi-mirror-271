import requests
import pandas as pd
from typing import Dict, Any
from fmpxx.client import FMPClient


class Quote(FMPClient):
    def __init__(self, api_key: str, timeout: int = 10):
        super().__init__(api_key, timeout)

    def get_simple_quote(self, symbol: str) -> pd.DataFrame:
        endpoint = f"{self.url}/v3/quote-short//{symbol}"
        params = {}  # 如果需要其他参数，可以在这里添加
        response = self._handle_response(endpoint, params)
        return self.trans_to_df(response)

    def get_full_quote(self, symbol: str) -> pd.DataFrame:
        """
        :param symbol:
        :return:
        """
        endpoint = f"{self.url}/v3/quote/{symbol}"
        params = {}  # 如果需要其他参数，可以在这里添加
        response = self._handle_response(endpoint, params)
        return self.trans_to_df(response)