"""Module that functions akin to OTL makeresults"""
import pandas as pd
from otlang.sdk.syntax import Keyword, OTLType
from pp_exec_env.base_command import BaseCommand, Syntax
import time


class MakeresultsCommand(BaseCommand):
    """Class that can makeresults"""
    # define syntax of your command here
    syntax = Syntax(
        [
            Keyword("count", required=False, otl_type=OTLType.INTEGER),
            Keyword("annotate", required=False, otl_type=OTLType.BOOLEAN)
        ],
    )

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        count = self.get_arg("count").value or 1
        annotate = self.get_arg("annotate").value or False
        timestamp = int(time.time())
        data = {"_time": [timestamp]*count}
        if annotate:
            annot_data = {"_raw": [None]*count,
                          "host": [None]*count,
                          "source": [None]*count,
                          "sourcetype": [None]*count}
            data = data | annot_data
        df = pd.DataFrame(data)
        return df
