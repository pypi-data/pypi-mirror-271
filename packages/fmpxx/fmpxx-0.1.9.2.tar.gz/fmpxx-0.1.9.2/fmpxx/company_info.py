import requests
import pandas as pd
from typing import Dict, Any
from fmpxx.client import FMPClient


class CompanyInfo(FMPClient):
    def __init__(self, api_key: str, timeout: int = 10):
        super().__init__(api_key, timeout)

    def get_analyst_estimates(self, symbol: str) -> pd.DataFrame:
        endpoint = f"{self.url}/v3/analyst-estimates/{symbol}"
        params = {}  # 如果需要其他参数，可以在这里添加
        response = self._handle_response(endpoint, params)
        return self.trans_to_df(response)

