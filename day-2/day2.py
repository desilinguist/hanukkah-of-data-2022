#!/usr/bin/env python3
"""
This file contains a solution to Day 2 of Hanukkah of Data.

For details of the problem, refer to https://hanukkah.bluebird.sh/5783/2/
"""


import pandas as pd


def main():  # noqa: D103

    # read in all of the records in the product file and keep only those
    # that contains either coffee or bagel in the description
    df_products = pd.read_csv("data/noahs-products.csv")
    df_products = df_products[df_products["desc"].str.contains(r"coffee|bagel", case=False)]

    # iterate over all the records in the orders and keep only the ones
    # that match the following criteria:
    # - the items in the order contain coffee and/or bagels
    # - the "ordered" date is in 2017
    # - the "ordered" date and time are within one minute or less of
    #   the "shipped" date and time since coffes and bagels are consumed
    #   right there in the store.
    df_orders = pd.read_csv("data/noahs-orders.csv", parse_dates=["ordered", "shipped"])
    df_order_items = pd.read_csv("data/noahs-orders_items.csv")
    df_orders = df_orders.merge(df_order_items)

    # apply our filters above
    df_orders = df_orders[
        (df_orders["ordered"].dt.year == 2017)
        & ((df_orders["ordered"] - df_orders["shipped"]).dt.seconds <= 60)
    ]
    df_orders = df_orders.merge(df_products)

    # now take the filtered customer IDs and find them in the customers
    # file and only keep the ones that have the initial "J" and "D"
    df_customers = pd.read_csv("data/noahs-customers.csv")
    df_merged = pd.merge(df_customers, df_orders, left_on="customerid", right_on="customerid")
    print(df_merged[df_merged.name.str.match(r"J.*\bD.*|J.*\b[A-Z].*\bD.*")])


if __name__ == "__main__":
    main()
