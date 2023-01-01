#!/usr/bin/env python3
"""
This file contains a solution to Day 3 of Hanukkah of Data.

For details of the problem, refer to https://hanukkah.bluebird.sh/5783/3/
"""

import pandas as pd


def main():  # noqa: D103

    # read in the customers records and keep only the ones whose details are as follows:
    # - his birth year is the year of the dog (1934, 1946, 1958, 1970, 1982, 1994)
    # - his birth date is between Mar 21 – Apr 19
    # - he is in the same neigborhood as "Jeremy Davis" whoae address is "South Ozone Park"
    df_customers = pd.read_csv("data/noahs-customers.csv", parse_dates=["birthdate"])
    df_customers = df_customers[
        (df_customers["birthdate"].dt.year.isin([1934, 1946, 1958, 1970, 1982, 1994]))
        & (df_customers["birthdate"].dt.month.isin([3, 4]))
        & (df_customers["birthdate"].dt.day != 20)
        & (df_customers["citystatezip"].str.contains("South Ozone Park"))
    ]
    print(df_customers)


if __name__ == "__main__":
    main()
