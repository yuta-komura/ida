# import matplotlib.pyplot as plt

import time

from lib import math, repository

database = "tradingbot"

while True:

    asset = 1000000

    sql = """
            select
                *
            from
                forwardtest_entry
            """

    fe = repository.read_sql(database="tradingbot", sql=sql)

    start_time = fe.loc[0]["date"]
    finish_time = fe.loc[len(fe) - 1]["date"]

    profits = []
    asset_flow = []
    elapsed_secs = []
    for i in range(len(fe)):
        if i == 0:
            continue

        past_position = fe.iloc[i - 1]
        now_position = fe.iloc[i]

        if past_position["side"] == "BUY" and (
                now_position["side"] == "SELL" or now_position["side"] == "CLOSE"):

            amount = asset / past_position["price"]
            profit = (amount * now_position["price"]) - asset

            elapsed_sec = (
                now_position["date"] -
                past_position["date"]).seconds

            elapsed_secs.append(elapsed_sec)
            profits.append(profit)
            asset += profit

        if past_position["side"] == "SELL" and (
                now_position["side"] == "BUY" or now_position["side"] == "CLOSE"):

            amount = asset / past_position["price"]
            profit = asset - (amount * now_position["price"])

            elapsed_sec = (
                now_position["date"] -
                past_position["date"]).seconds

            elapsed_secs.append(elapsed_sec)
            profits.append(profit)
            asset += profit

    wins = []
    loses = []
    for i in range(len(profits)):
        if profits[i] > 0:
            wins.append(profits[i])
        elif profits[i] < 0:
            loses.append(profits[i])

    pf = None
    if sum(loses) != 0:
        pf = abs(sum(wins) / sum(loses))
    wp = None
    if len(wins) + len(loses) != 0:
        wp = len(wins) / (len(wins) + len(loses)) * 100

    print("----------------------------------------------")
    print(str(start_time).split(".")[0],
          "〜", str(finish_time).split(".")[0])
    print("profit", int(sum(profits)))
    if pf:
        print("pf", math.round_down(pf, -2))
    if wp:
        print("wp", math.round_down(wp, 0), "%")
    if elapsed_secs:
        print("max elapsed_sec", max(elapsed_secs))
        elapsed_secs.sort()
        print("med elapsed_sec",
              elapsed_secs[int((len(elapsed_secs) - 1) / 2)])
    print("trading cnt", len(profits))

    time.sleep(10)

# profit_flow = []
# p = 0
# for i in range(len(profits)):
#     profit_flow.append(p)
#     p += profits[i]

# fig = plt.figure(figsize=(48, 24), dpi=50)
# ax1 = fig.add_subplot(1, 1, 1)
# ax1.plot(list(range(len(profit_flow))), profit_flow)
# plt.show()
