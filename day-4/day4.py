#!/usr/bin/env python3
"""
This file contains a solution to Day 4 of Hanukkah of Data.

For details of the problem, refer to https://hanukkah.bluebird.sh/5783/4/
"""


import pandas as pd


def main():  # noqa: D103

    # read in all the orders and their items and merge them together
    df_orders = pd.read_csv("data/noahs-orders.csv", parse_dates=["ordered", "shipped"])
    df_order_items = pd.read_csv("data/noahs-orders_items.csv")
    df_orders = df_orders.merge(df_order_items)

    # keep only those orders where:
    # - the SKU starts with "BKY" (indicating bakery items)
    # - the ordering time was between 3am and 5am
    # - the shipping time is within 1 minute of the ordering time
    df_food = df_orders[
        (df_orders["sku"].str.match(r"BKY"))
        & (df_orders["ordered"].dt.hour >= 3)
        & (df_orders["ordered"].dt.hour <= 4)
        & ((df_orders["shipped"] - df_orders["ordered"]).dt.seconds <= 60)
    ]

    # now merge in this food data with the customers and keep only
    # those records with zipcodes in the five NYC boroughs
    # since the woman is supposed to have to have biked over;
    # these zip codes are:
    # - Manhattan: 10001-10282
    # - Staten Island: 10301-10314
    # - Bronx: 10451-10475
    # - Queens: 11004-11109, 11351-11697
    # - Brooklyn: 11201-11256
    df_customers = pd.read_csv("data/noahs-customers.csv")
    df_products = pd.read_csv("data/noahs-products.csv", usecols=["sku", "desc"])
    df_customers = df_food.merge(df_customers).merge(df_products)
    zipcodes = (
        list(range(10301, 10315))
        + list(range(10451, 10476))
        + list(range(11004, 11110))
        + list(range(11351, 11698))
        + list(range(11201, 11257))
    )
    df_customers["zipcode"] = df_customers["citystatezip"].str.extract(r" (\d{5})").astype(int)
    df_customers = df_customers[df_customers["zipcode"].isin(zipcodes)]

    # let's print it out and manually inspect the candidates
    print(df_customers[["name", "sku", "desc", "ordered", "shipped", "citystatezip", "phone"]])


if __name__ == "__main__":
    main()
