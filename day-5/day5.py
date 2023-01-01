#!/usr/bin/env python3
"""
This file contains a solution to Day 6 of Hanukkah of Data.

For details of the problem, refer to https://hanukkah.bluebird.sh/5783/6/
"""

import pandas as pd


def main():  # noqa: D103

    # read in all of the records in the product file and keep only those
    # that contains either "Jersey" (since the woman was wearing a Noah's
    # Jersey) or "cat food" (since she has cats)
    df_products = pd.read_csv("data/noahs-products.csv")
    df_products = df_products[df_products["desc"].str.contains(r"jersey\b|cat\b", case=False)]

    # read in all the orders and their items and merge them together
    df_orders = pd.read_csv("data/noahs-orders.csv")
    df_order_items = pd.read_csv("data/noahs-orders_items.csv")
    df_orders = df_orders.merge(df_order_items)

    # filter on the specific products we want
    df_orders = df_orders[df_orders["sku"].isin(df_products["sku"])]

    # read in all the customer records
    df_customers = pd.read_csv("data/noahs-customers.csv")

    # now keep only those customers who:
    # - have a customer ID that matches those who placed
    #   our subset of orders above
    # - have a zip code of either 11427, 11428, or 11429 (Queens Village)
    df_customers = df_customers[
        (df_customers["customerid"].isin(df_orders["customerid"]))
        & (df_customers["citystatezip"].str.contains(r"1142[789]"))
    ]

    # now print this out so we can inspect it manually to
    # find our mystery woman
    print(df_customers)


if __name__ == "__main__":
    main()
