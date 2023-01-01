#!/usr/bin/env python3
"""
This file contains a solution to Day 1 of Hanukkah of Data.

For details of the problem, refer to https://hanukkah.bluebird.sh/5783/1/
"""

import numpy as np
import pandas as pd

# define a map of phone letter digits to letters
KEYMAP = {
    "2": ["A", "B", "C"],
    "3": ["D", "E", "F"],
    "4": ["G", "H", "I"],
    "5": ["J", "K", "L"],
    "6": ["M", "N", "O"],
    "7": ["P", "Q", "R", "S"],
    "8": ["T", "U", "V"],
    "9": ["W", "X", "Y", "Z"],
}

# define another map from each letter to its equivalence class
LETTERMAP = {letter: eqclass for eqclass in KEYMAP.values() for letter in eqclass}


def main():  # noqa: D103

    # read in the customrs records into a data frame
    df_customers = pd.read_csv("data/noahs-customers.csv")

    # normalize the phone numbers by receiving all hyphens
    df_customers["phone"] = df_customers["phone"].str.replace("-", "")

    # if the phone number contains 0 or 1, we can skip it as those
    # digits do npt map to any letters
    df_customers = df_customers[~df_customers["phone"].str.contains(r"0|1")]

    # get the name and split it into components
    df_names = df_customers["name"].str.split(expand=True)
    df_names.columns = ["first", "middle_or_last", "last_or_suffix"]
    df_customers = pd.concat([df_customers, df_names], axis="columns")

    # if the third component is a suffix, then use the penultimate
    # component as the true last name, otherwise use the last component
    have_middle_names = (~df_customers["last_or_suffix"].isnull()) & (
        ~df_customers["last_or_suffix"].isin(["Jr.", "II", "III"])
    )
    df_customers["true_last"] = np.where(
        have_middle_names, df_customers["last_or_suffix"], df_customers["middle_or_last"]
    )

    # get rid of any non-letter characters from the last name
    df_customers["true_last"] = df_customers["true_last"].str.replace("\W", "", regex=True)

    # "expand" the last name letters into their equivalent character classes
    df_customers["expanded_last_name"] = (
        df_customers["true_last"]
        .str.upper()
        .apply(lambda name: [LETTERMAP[letter] for letter in name])
    )
    # expand the phone number into the same equivalence classes
    df_customers["expanded_phone_number"] = df_customers["phone"].apply(
        lambda number: [KEYMAP[digit] for digit in number]
    )

    # if the two expansions match, we have our record
    print(
        df_customers[
            df_customers["expanded_last_name"] == df_customers["expanded_phone_number"]
    ][["name", "phone"]]
    )


if __name__ == "__main__":
    main()
