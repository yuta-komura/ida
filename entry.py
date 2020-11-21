import traceback

import pandas as pd

from lib import bitflyer, message, repository
from lib.config import Bitflyer, HistoricalPrice


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


def save_entry(side):
    message.info(side, "entry")
    sql = "update entry set side='{side}'".format(side=side)
    repository.execute(database=DATABASE, sql=sql, write=False)


TIME_FRAME = HistoricalPrice.TIME_FRAME.value
CHANNEL_WIDTH = HistoricalPrice.CHANNEL_WIDTH.value
CHANNEL_BAR_NUM = TIME_FRAME * CHANNEL_WIDTH

bitflyer = bitflyer.API(api_key=Bitflyer.Api.value.KEY.value,
                        api_secret=Bitflyer.Api.value.SECRET.value)

DATABASE = "tradingbot"

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
        save_entry(side="BUY")
        has_buy = True
        has_sell = False

    if should_sell:
        save_entry(side="SELL")
        has_buy = False
        has_sell = True
