#!/usr/bin/env python3
"""
This file contains a solution to Day 6 of Hanukkah of Data.

For details of the problem, refer to https://hanukkah.bluebird.sh/5783/6/
"""

import pandas as pd


def main():  # noqa: D103

    # read in all of the records in the product file with SKU
    # and wholesale cost as the only columns
    df_products = pd.read_csv("data/noahs-products.csv", usecols=["sku", "wholesale_cost"])

    # read in all the orders and their items and merge them together
    # also merge in the wholesale costs of the items
    df_orders = pd.read_csv("data/noahs-orders.csv", usecols=["orderid", "customerid", "total"])
    df_order_items = pd.read_csv("data/noahs-orders_items.csv", usecols=["orderid", "sku"])
    df_orders = df_orders.merge(df_order_items).merge(df_products)

    # read in all the customer records and keep only those who have an NYC zip code
    df_customers = pd.read_csv("data/noahs-customers.csv")
    zipcodes = (
        list(range(10301, 10315))
        + list(range(10451, 10476))
        + list(range(11004, 11110))
        + list(range(11351, 11698))
        + list(range(11201, 11257))
    )
    df_customers["zipcode"] = df_customers["citystatezip"].str.extract(r" (\d{5})").astype(int)
    df_customers = df_customers[df_customers["zipcode"].isin(zipcodes)]

    # filter our orders to only keep those from NYC customers
    df_orders = df_orders.merge(df_customers)

    # compute a "total_cost" column that contains the total wholesale
    # cost for each order that Noah's would have incurred
    df_cost = (
        df_orders.groupby("orderid", sort=False, as_index=False)
        .wholesale_cost.sum()
        .rename(columns={"wholesale_cost": "total_cost"})
    )
    df_orders = df_orders.merge(df_cost)

    # now compute a "profit" column that computes the difference between the
    # the total paid by the customer and the total cost incurred by Noah's
    df_orders["profit"] = df_orders["total"] - df_orders["total_cost"]

    # now find the customer who incurs Noah's a negative profit
    # the most number of times
    most_frugal_customer = df_orders[df_orders["profit"] < 0].name.value_counts().index[0]
    print(df_orders[df_orders.name == most_frugal_customer])


if __name__ == "__main__":
    main()
