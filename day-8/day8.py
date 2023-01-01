#!/usr/bin/env python3
"""
This file contains a solution to Day 8 of Hanukkah of Data.

For details of the problem, refer to https://hanukkah.bluebird.sh/5783/8/
"""

import pandas as pd


def main():  # noqa: D103

    # read in all of the records in the product file with the SKU
    # and the description as the only columns
    df_products = pd.read_csv("data/noahs-products.csv", usecols=["sku", "desc"])
    df_collectibles = df_products[df_products.sku.str.startswith("COL")].copy()

    # all collectibles have a parenthetical so let's remove that
    df_clean_desc = df_collectibles.desc.str.extract(r"([^\(]+) \(.+\)").rename(
        columns={0: "clean_desc"}
    )
    df_collectibles["clean_desc"] = df_clean_desc["clean_desc"]

    # get the total number of unique collectibles that are available
    total_collectibles = len(df_collectibles.clean_desc.unique())

    # read in all the orders and their items and merge them together
    # and then restrict only to collecitble orders
    df_orders = pd.read_csv("data/noahs-orders.csv")
    df_order_items = pd.read_csv("data/noahs-orders_items.csv")
    df_orders = df_orders.merge(df_order_items)
    df_collectible_orders = df_orders[df_orders.sku.str.startswith("COL")]
    df_collectible_orders = df_collectible_orders.merge(df_collectibles)

    # group by cutomer ID and find out how many unique collectibles each
    # customer has
    df_collectible_counts = (
        df_collectible_orders.groupby("customerid", as_index=False)
        .clean_desc.nunique()
        .rename(columns={"clean_desc": "num_collectibles"})
    )

    # read in the customers and merge in the collectible counts
    df_customers = pd.read_csv("data/noahs-customers.csv")
    df_customers = df_customers.merge(df_collectible_counts)

    # now print out customers who have all 8 collectibles
    print(df_customers[df_customers.num_collectibles == total_collectibles])


if __name__ == "__main__":
    main()
