import datetime
import time
import traceback

import pandas as pd

from lib import bitflyer, message, repository
from lib.config import Bitflyer, HistoricalPrice


def save_entry(date, side, price):
    sql = "insert into forwardtest_entry values ('{date}','{side}',{price},0)"\
        .format(date=date, side=side, price=price)
    repository.execute(database=DATABASE, sql=sql, log=False)


def get_order_data(side):
    sql = "select * from ticker"
    ticker = repository.read_sql(database=DATABASE, sql=sql).iloc[0]
    if side == "BUY":
        order_price = ticker["best_bid"] + 1  # 1361825
    else:  # SELL
        order_price = ticker["best_ask"] - 1  # 1361969
    order_date = datetime.datetime.now()
    return order_date, order_price


def buy():
    side = "BUY"
    while True:
        date, price = get_order_data(side=side)
        time.sleep(1)
        sql = """
                select
                    *
                from
                    execution_history
                where
                    side = 'SELL'
                    and date > '{date}'
                    and price <= '{price}'
                """.format(date=date, price=price)
        eh = repository.read_sql(database=DATABASE, sql=sql)
        if eh.empty:
            time.sleep(1)
        else:
            date = datetime.datetime.now()
            save_entry(date, side, price)
            break


def sell():
    side = "SELL"
    while True:
        date, price = get_order_data(side=side)
        time.sleep(1)
        sql = """
                select
                    *
                from
                    execution_history
                where
                    side = 'BUY'
                    and date > '{date}'
                    and price >= '{price}'
                """.format(date=date, price=price)
        eh = repository.read_sql(database=DATABASE, sql=sql)
        if eh.empty:
            time.sleep(1)
        else:
            date = datetime.datetime.now()
            save_entry(date, side, price)
            break


def get_historical_price() -> pd.DataFrame or None:
    try:
        limit = CHANNEL_BAR_NUM + 1
        hp = bitflyer.get_historical_price(limit=limit)
        if len(hp) != limit:
            return None
        return hp
    except Exception:
        message.error(traceback.format_exc())
        return None


TIME_FRAME = HistoricalPrice.TIME_FRAME.value
CHANNEL_WIDTH = HistoricalPrice.CHANNEL_WIDTH.value
CHANNEL_BAR_NUM = TIME_FRAME * CHANNEL_WIDTH

bitflyer = bitflyer.API(api_key=Bitflyer.Api.value.KEY.value,
                        api_secret=Bitflyer.Api.value.SECRET.value)

DATABASE = "tradingbot"

sql = "truncate forwardtest_entry"
repository.execute(database=DATABASE, sql=sql, log=False)

has_buy = False
has_sell = False
while True:
    hp = get_historical_price()
    if hp is None:
        continue

    i = len(hp) - 1
    latest = hp.iloc[i]
    Date = latest["Date"]
    Price = latest["Close"]

    before = hp.iloc[:i]
    high_line = before["High"].max()
    low_line = before["Low"].min()

    should_buy = Price > high_line and not has_buy
    should_sell = Price < low_line and not has_sell

    if should_buy:
        buy()
        has_buy = True
        has_sell = False

    if should_sell:
        sell()
        has_buy = False
        has_sell = True
