#!/usr/bin/env python3
"""
This file contains a solution to Day 7 of Hanukkah of Data.

For details of the problem, refer to https://hanukkah.bluebird.sh/5783/7/
"""

import pandas as pd


def main():  # noqa: D103

    # read in all of the records in the product file with the SKU
    # and the description as the only columns
    df_products = pd.read_csv("data/noahs-products.csv", usecols=["sku", "desc"])

    # read in all the orders and their items and merge them together
    # and also merge in the product descriptions
    df_orders = pd.read_csv("data/noahs-orders.csv", parse_dates=["ordered", "shipped"])
    df_order_items = pd.read_csv("data/noahs-orders_items.csv", usecols=["orderid", "sku"])
    df_orders = df_orders.merge(df_order_items).merge(df_products)

    # it looks like Noah's specifies colors in parentheses for all its products
    # so let's split the colors out into a separate column
    df_color = df_orders.desc.str.extract(r"([^\(]+) \(([a-z]+)\)").rename(
        columns={0: "non_color_desc", 1: "color"}
    )
    df_orders["non_color_desc"] = df_color["non_color_desc"]
    df_orders["color"] = df_color["color"]

    # now only keep the orders thave
    df_orders = df_orders[~df_orders.color.isnull()]

    # now merge in the customer information
    df_customers = pd.read_csv("data/noahs-customers.csv")
    df_orders = df_orders.merge(df_customers)

    # now find all items that purchased by Emily Randolph
    df_emily = df_orders[df_orders["name"] == "Emily Randolph"]

    # for each of Emily's purchases, find another order made on the
    # same date within around an hour and with the same item but in
    # a different color
    all_candidates = []
    for _, series in df_emily.iterrows():
        candidates = df_orders[
            (df_orders.ordered.dt.date == series.ordered.date())
            & ((df_orders.ordered - series.ordered).dt.seconds <= 3600)
            & (df_orders.non_color_desc == series.non_color_desc)
            & (df_orders.color != series.color)
        ]
        all_candidates.append(candidates.copy())

    df_candidates = pd.concat(all_candidates)
    print(df_candidates[["desc", "name", "phone", "ordered"]])


if __name__ == "__main__":
    main()
