import os
import time
import urllib.parse
from datetime import datetime, timedelta, timezone

import numpy as np
import pandas as pd
import requests
import yaml
from clickhouse_driver import Client
from requests import get

from runespreader import Runespreader
from runespreader import refresh_vol_list


class Spreadseer:
    def __init__(self, config):
        self.config = config
        return

    def gather_training_data(self, time_horizon = 1):
        r = Runespreader()
        timestamp, symbols_to_track = refresh_vol_list()
        client = Client(host="localhost", password=self.config.get("CH_PASSWORD"))
        rs_sells = client.execute(
            f"select low, lowTime, name, id from rs_sells where lowTime >= now() - interval {time_horizon} day and lowTime < now() - interval 15 minute"
        )
        high_df = pd.DataFrame(
            rs_buys, columns=["high", "high_time", "name", "id"]
        ).sort_values(["high_time"], ascending=False)
        low_df = pd.DataFrame(
            rs_sells, columns=["low", "low_time", "name", "id"]
        ).sort_values(["low_time"], ascending=False)

        """
        Logic

        sep tables hold buy and sells 

        need to understand the market at any given actionable interval

        since we open position when liquidity is present join on sells with last(highTime) < current_time in a window function 
        """

        return 




# https://gitlab.com/one-percenters/one-percenters/-/blob/charles-testing/tools/model_test.py?ref_type=heads