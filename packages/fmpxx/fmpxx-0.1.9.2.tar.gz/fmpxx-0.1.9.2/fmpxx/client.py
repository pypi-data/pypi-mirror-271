import requests
import pandas as pd
from datetime import datetime
import datetime as dtt
from dotenv import load_dotenv, find_dotenv
from dateutil.relativedelta import relativedelta
from retry import retry
import numpy as np
from typing import Dict, Any

pd.set_option("expand_frame_repr", False)  # 当列太多时不换行
pd.set_option("display.max_rows", 5000)  # 最多显示数据的行数


load_dotenv(find_dotenv())


class FMPClient:
    DEFAULT_HOST = "https://financialmodelingprep.com/api"

    def __init__(self, api_key: str, timeout: int = 10):
        self.api_key = api_key
        self.url = self.DEFAULT_HOST
        self._session = requests.Session()
        self.timeout = timeout

    def _handle_response(self, endpoint: str, params: Dict[str, Any]) -> Any:
        params['apikey'] = self.api_key  # 将API密钥作为参数传递
        response = self._session.get(endpoint, params=params, timeout=self.timeout)
        if response.status_code != 200:
            response.raise_for_status()  # 如果响应状态码不是200，则抛出异常
        return response.json()

    @staticmethod
    def trans_to_df(res: Dict[str, Any]) -> pd.DataFrame:
        return pd.DataFrame(res)

    def get_8k_update(self, endpoint: str = "v4/rss_feed_8k", **query_params) -> pd.DataFrame:
        """
        返回8k报告update
        hasFinancial='true', limit=10
        """
        full_endpoint = f"{self.url}/{endpoint}"
        res = self._handle_response(full_endpoint, query_params)
        return self.trans_to_df(res)

    def get_sec_update(self, days):
        """
        获得sec更新
        type=10 包含10-K和10Q
        days是真天数，不用-1
        """
        end = dtt.datetime.today()
        start = end - dtt.timedelta(days=days)
        start = start.strftime("%Y-%m-%d")
        end = end.strftime("%Y-%m-%d")
        # type=10 include 10-K 10-Q
        endpoint = (f"https://financialmodelingprep.com/api/v4/rss_feed?"
                    f"type=10&from={start}&to={end}&isDone="
                    f"true")
        res = requests.get(endpoint).json()
        df = self.trans_to_df(res)
        return df

    def get_tickers(self, endpoint="v3/stock/list", **query_params):
        """
        7500
        和available的区别没有搞明白。。
        """
        endpoint = f"{self.url}/{endpoint}"
        res = self._handle_response(endpoint, query_params)
        # print(res)
        df: pd.DataFrame = self.trans_to_df(res)
        df = df[df["type"] == "stock"]
        df = df.loc[df["exchangeShortName"].isin(["NASDAQ", "NYSE"])]
        df.reset_index(inplace=True, drop=True)
        return df

    def get_available_tickers(self,
                              endpoint="v3/available-traded/list",
                              **query_params):
        """
        8300  包含etf etn 2x shares
        """
        endpoint = f"{self.url}/{endpoint}"
        res = self._handle_response(endpoint, query_params)
        # print(res)
        df: pd.DataFrame = self.trans_to_df(res)
        # df = df[df['type'] == 'stock']
        df = df.loc[df["exchangeShortName"].isin(["NASDAQ", "NYSE"])]
        df.reset_index(inplace=True, drop=True)
        return df

    def get_quote_short(self,
                        symbol,
                        endpoint="v3/quote-short",
                        **query_params):
        """
        获取实时报价price
        """
        endpoint = f"{self.url}/{endpoint}/{symbol}"
        res = self._handle_response(endpoint, query_params)
        # print(res)
        return res[0]["price"]

    def get_quote(self, symbol, endpoint="v3/quote", **query_params):
        """
        最新版的 api 用这个获取实时包括历史数据
        获取实时报价df
        timestamp请求的是当时的时间戳，如果是盘后请求就会有问题，在real his里去重
        """
        endpoint = f"{self.url}/{endpoint}/{symbol}"
        res = self._handle_response(endpoint, query_params)
        # print(res)
        df = pd.DataFrame.from_records(res)
        # print(df)
        df = df[[
            "timestamp",
            "open",
            "dayHigh",
            "dayLow",
            "price",
            "volume",
            "changesPercentage",
        ]]
        df.rename(
            columns={
                "timestamp": "date",
                "dayHigh": "high",
                "dayLow": "low",
                "price": "close",
                "changesPercentage": "pct",
            },
            inplace=True,
        )
        df["date"] = df["date"].apply(lambda x: datetime.utcfromtimestamp(
            x).replace(tzinfo=dtt.timezone.utc))  # timestamp时间转换
        df["date"] = df["date"].dt.tz_convert("US/Eastern")  # 转换为 NYC时间
        df["date"] = df["date"].apply(lambda x: x.strftime("%Y-%m-%d"))
        # print(df)
        return df

    def get_real_his_fmp(self, symbol, period):
        """
        获得包含实时数据的k线
        解决了盘后请求多一天数据的问题
        """
        real_df = self.get_quote(symbol)  # fixme 周末读取的话时间是周末，但是应该对实盘没有影响
        # print(real_df)
        his_df = self.get_his_fmp(symbol, period=period)
        # print(his_df)
        # new_df = his_df.append(real_df, ignore_index=True)
        new_df = pd.concat([his_df, real_df])
        # 去重 排序
        new_df.drop_duplicates(subset=["date"], inplace=True, keep="first")
        # 解决盘后请求的问题，volume会被数据修正，使用OCHL
        new_df.drop_duplicates(subset=["close", "open", "high", "low"],
                               inplace=True,
                               keep="first")
        new_df.sort_values(by=["date"],
                           ascending=True,
                           inplace=True,
                           ignore_index=True)
        # print(new_df)
        return new_df

    # 获取历史，不包含当日报价
    def get_his_fmp(
        self,
        symbol,
        endpoint="v3/historical-price-full",
        start="",
        end="",
        period=None,
        **query_params,
    ):
        """
        非实时
        close字段是前复权，adjclose不清楚
        """
        if period is not None:
            end = datetime.today()
            start = end - relativedelta(months=12 * period)
            end = end.strftime("%Y-%m-%d")
            start = start.strftime("%Y-%m-%d")
        endpoint = (f"{self.url}/{endpoint}/{symbol}?from={start}"
                    f"&to={end}")
        res = self._handle_response(endpoint, query_params)
        try:
            df = pd.DataFrame.from_records(res["historical"])
            # 删除不需要字段
            df.drop(
                columns=[
                    "change",
                    "changePercent",
                    "changeOverTime",
                    "label",
                    "adjClose",
                    "unadjustedVolume",
                    "vwap",
                ],
                inplace=True,
            )
            # 清洗数据
            df["date"].dropna(inplace=True)
            df["date"].drop_duplicates(inplace=True)
            df.sort_values(by=["date"], ignore_index=True, inplace=True)
            df["pct"] = df["close"].pct_change()
            # df.fillna(value=0.0, inplace=True)
            # df = df.replace({np.nan: None})
            # print(df.dtypes)
            return df
        except KeyError:
            print(symbol, "no data")
            pass

    @retry(tries=5, delay=5)
    def get_financials(self,
                       symbol,
                       statement,
                       endpoint="",
                       **query_params) -> pd.DataFrame:
        """
        period='quarter', limit=40
        """
        if statement == "income":
            endpoint = "v3/income-statement"
        if statement == "balance":
            endpoint = "v3/balance-sheet-statement"
        if statement == "cash":
            endpoint = "v3/cash-flow-statement"
        endpoint = f"{self.url}/{endpoint}/{symbol}"
        res = self._handle_response(endpoint, query_params)
        # print(res)
        df = pd.DataFrame.from_records(res)
        # print(df)
        # 如果其中一个是空，则返回空DF
        if df.empty:
            return df
        else:
            df = df.drop(columns=["link", "finalLink"])
            return df

    def get_merged_financials(self, symbol):
        """
        合并cf is bs三张财报
        应以filing date为准，但是少部分可能有bug，应该shift一天，因为有盘后发布
        特殊情况：
        BKR 三个财报date不一致，改用两次merge
        ALLE 2013年数据第几个季度标记不准确， 虽然period字段标记错误，但是可以不使用该字段
        AMCR 三个财报长度严重不一致，产生过多nan
        ANET 季度数据不连续，应该要检查Q1 2 3 4是否连续
        merge 使用inner，三个财报同时都有的情况下取交集。解决以上问题。
        SE, WB 属于海外股票，财报不全正常
        """
        income = self.get_financials(symbol,
                                     statement="income",
                                     period="quarter",
                                     limit=40)
        balance = self.get_financials(symbol,
                                      statement="balance",
                                      period="quarter",
                                      limit=40)
        cash = self.get_financials(symbol,
                                   statement="cash",
                                   period="quarter",
                                   limit=40)
        if income.empty or balance.empty or cash.empty:
            pass
        else:
            # concat合并依赖 index长度一致
            # income = income.set_index(keys=['fillingDate'])
            # balance = balance.set_index(keys=['fillingDate'])
            # cash = cash.set_index(keys=['fillingDate'])
            # print(income)
            # print(balance)
            # print(cash)
            # 用merge合并两次，BKR会出现三个财报date日期不一致的情况
            on_list = [
                "cik",
                "fillingDate",
                "date",
                "symbol",
                "period",
                "calendarYear",
                "reportedCurrency",
            ]
            merged_df = pd.merge(income, balance, how="inner", on=on_list)
            merged_df = pd.merge(merged_df, cash, how="inner", on=on_list)
            # print(merged_df)
            # 检查重复值和nan值
            if merged_df.isnull().values.any():
                print(f"{symbol}包含空值")
            if merged_df["date"].duplicated().sum() > 0:
                print(f"{symbol}包含重复值")
            # 清洗和校正数据
            # merged_df = merged_df.dropna(subset=['cik', 'acceptedDate_x'])
            # 如果cik为nan， 三个财报index长度不一样
            merged_df = merged_df.rename(
                columns={
                    "date": "period_date",
                    "fillingDate": "date",
                    "netIncome_x": "netIncome",
                })
            merged_df = merged_df.sort_values(
                by=["date", "acceptedDate_x"],
                ignore_index=True)  # acceptedDate_x参与排序，保留first
            # 通过观察FAST，第一个是正确的，且link和final link有值，没有2022-03-31这个日期的更新。怀疑是bug
            merged_df = merged_df.drop_duplicates(subset=["date"],
                                                  keep="first",
                                                  ignore_index=True)
            merged_df["period_date"] = pd.to_datetime(merged_df["period_date"])

            # 下列股票先drop掉第一行，通常就可以，WB和SE属于海外股票，CSC数据就是不对
            verify_list = [
                "ADT",
                "ALTR",
                "ARNC",
                "BEAM",
                "CEG",
                "CSC",
                "CTLT",
                "FTV",
                "HLT",
                "HPE",
                "LDOS",
                "LW",
                "MMI",
                "MRNA",
                "OTIS",
                "PLL",
                "S",
                "TWTR",
                "VNT",
            ]
            if symbol in verify_list:
                merged_df = merged_df.drop([0])  # fixme 没有重新排序
            merged_df["verify"] = merged_df["period_date"].diff()
            # print(merged_df)
            if symbol == "CSC":
                return None
            verify_list = merged_df["verify"].tolist()[1:]  # 第一个是naT
            # verify_list = [days.days > 45 for days in verify_list]
            for days in verify_list:
                if days.days > 150:  # 正常应该是91天，有的公司财报间隔久一些比如COST
                    print(symbol, "财报异常，数据周期不全")
                    break
                else:
                    # 已退市股票cik为nan，会被改为0
                    del merged_df["verify"]
                    merged_df = merged_df.fillna(value=0)  # nan值无法参与计算
                    return merged_df

    def sp500_constituent(self,
                          endpoint="v3/sp500_constituent",
                          **query_params):
        """
        获得当前sp500构成
        """
        endpoint = f"{self.url}/{endpoint}"
        resp = self._handle_response(endpoint, query_params)
        # print(resp)
        sp500_lst = [i["symbol"] for i in resp]
        return sp500_lst

    @retry(tries=5, delay=5)
    def sp500_his_list(self,
                       endpoint="v3/historical/sp500_constituent",
                       **query_params):
        """
        获得历史和现在的sp500
        """
        endpoint = f"{self.url}/{endpoint}"
        resp = self._handle_response(endpoint, query_params)
        df = pd.DataFrame.from_records(resp)
        df["date"] = pd.to_datetime(df["date"])
        df["addedTicker"] = df.apply(
            lambda x: x["symbol"] if len(x["addedSecurity"]) != 0 else np.nan,
            axis=1,
        )
        df["removedTicker"] = df["removedTicker"].apply(lambda x: np.nan
                                                        if len(x) == 0 else x)
        # print(df)
        added = df["addedTicker"].dropna().tolist()
        removed = df["removedTicker"].dropna().tolist()
        # print(sorted(added))
        # print(sorted(removed))
        # print(set(added) & set(removed))  # 判断交集，而且不少
        # 把现在的和曾经删除的都加在一起
        full_list = self.sp500_constituent()
        full_list = sorted(list(set(full_list + added + removed)))
        # print(len(full_list))  # 1063
        # print(sorted(set(full_list)))
        if "NWSA" in full_list:
            full_list.remove("NWSA")
        full_list = [x for x in full_list if ".A" not in x]  # 删除a类股票
        # print(len(full_list))
        return full_list
