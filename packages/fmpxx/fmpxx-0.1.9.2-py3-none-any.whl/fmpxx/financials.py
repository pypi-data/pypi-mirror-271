import requests
import pandas as pd
from typing import Dict, Any
from fmpxx.client import FMPClient
import numpy as np


class Financials(FMPClient):
    def __init__(self, api_key: str, timeout: int = 10):
        super().__init__(api_key, timeout)

    def get_income_statement(self, symbol: str) -> pd.DataFrame:
        endpoint = f"{self.url}/v3/income-statement/{symbol}?period=quarter&limit=20"
        params = {}  # 如果需要其他参数，可以在这里添加
        response = self._handle_response(endpoint, params)
        return self.trans_to_df(response)

    def get_earnings_his(self, symbol:str) -> pd.DataFrame:
        endpoint = f"{self.url}/v3//historical/earning_calendar/{symbol}"
        params = {}  # 如果需要其他参数，可以在这里添加
        response = self._handle_response(endpoint, params)
        return self.trans_to_df(response)

    def get_pe(self, symbol:str, pe='est') -> pd.DataFrame:
        """
        这里没有考虑是盘前还是盘后发布的 earnings
        这里都是 Non-GAAP Diluted earnings
        :param symbol:
        :param pe:
        :return:
        """
        eps_df = self.get_earnings_his(symbol)
        eps_df = eps_df.sort_values(by='date', ascending=True, ignore_index=True)
        # 新建'est'列，初始值为False
        eps_df['est'] = False

        # 标记'eps'列为NaN的行，将这些行的'est'列设置为True
        eps_df.loc[eps_df['eps'].isnull(), 'est'] = True
        # 使用 'eps_estimated' 列的值来填充 'eps' 列中的空值 fixme 临时办法
        eps_df['eps'] = eps_df['eps'].fillna(eps_df['epsEstimated'])

        eps_df['eps_ttm'] = eps_df['eps'].rolling(4).sum()
        # print(eps_df)
        his_df = self.get_his_fmp(symbol)
        merged_df = pd.DataFrame()
        # 使用 'date' 列作为键，进行内连接合并
        if pe == 'now':
            merged_df = pd.merge(eps_df, his_df, on='date', how='right')
        if pe == 'est':
            merged_df = pd.merge(eps_df, his_df, on='date', how='outer', sort=True)
        # print(merged_df)
        # 使用 'ffill' 方法向前填充 'eps' 列中的缺失值
        merged_df['eps_ttm'] = merged_df['eps_ttm'].fillna(method='bfill')        # 查看合并后的DataFrame
        #fixme 暂时用现存的 eps 填充，也可以用 epsEstimated 填充
        merged_df['eps_ttm'] = merged_df['eps_ttm'].fillna(method='ffill')
        merged_df['est'].fillna(method='bfill', inplace=True)
        # 当 eps_ttm<=0时 pe 为 nan
        merged_df['pe'] = merged_df.apply(lambda row: row['close'] / row['eps_ttm'] if row['eps_ttm'] > 0 else np.nan, axis=1)
        # print(merged_df)
        selected = merged_df[['date', 'eps_ttm', 'pe', 'close', 'eps', 'est']]
        selected = selected.dropna(subset=['close'])
        return selected

    def get_eps(self, symbol:str) -> pd.DataFrame:
        """
        弃用，无法获得准确的财报发布日期，准确的日期在 k-8文件
        adjusted_date 是调整后的财报发布日期
        :param symbol:
        :return:
        """
        df = self.get_income_statement(symbol)
        new_df = df[['date', 'symbol', 'acceptedDate', 'eps', 'epsdiluted']].copy()
        print(new_df)
        # 将接受日期字符串转换为datetime对象
        new_df['acceptedDate'] = pd.to_datetime(new_df['acceptedDate'])

        # 设置股市收盘时间为16:00 (4 PM)，并与接受日期的日期部分合并，形成当天的股市收盘时间戳
        new_df['market_close_time'] = new_df['acceptedDate'].dt.normalize() + pd.Timedelta(hours=16)

        # 判断是否为盘后发布：如果接受日期大于股市收盘时间，则为True
        new_df['is_after_market'] = new_df['acceptedDate'] > new_df['market_close_time']

        # 如果是盘后发布，则接受日期加一天
        new_df['adjusted_date'] = new_df.apply(
            lambda x: x['acceptedDate'] + pd.Timedelta(days=1) if x['is_after_market'] else x['acceptedDate'], axis=1)
        # 去掉adjusted_date的时间部分，只保留日期
        new_df['adjusted_date'] = new_df['adjusted_date'].dt.date
        # 删除辅助列（如果不需要）
        new_df.drop(['market_close_time', 'is_after_market'], axis=1, inplace=True)

        print(new_df)
        return new_df


