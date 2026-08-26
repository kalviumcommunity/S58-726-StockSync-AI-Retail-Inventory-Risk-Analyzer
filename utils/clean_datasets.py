import pandas as pd

from product_normalizer import normalize_product_name


def clean_datasets():

    inventory = pd.read_csv("datasets/inventory.csv")
    sales = pd.read_csv("datasets/sales.csv")
    returns = pd.read_csv("datasets/returns.csv")

    inventory["normalized_product_name"] = (
        inventory["product_name"]
        .apply(normalize_product_name)
    )

    sales["normalized_product_name"] = (
        sales["product_name"]
        .apply(normalize_product_name)
    )

    returns["normalized_product_name"] = (
        returns["product_name"]
        .apply(normalize_product_name)
    )

    return inventory, sales, returns


if __name__ == "__main__":

    inventory, sales, returns = clean_datasets()

    print("\nINVENTORY")
    print(
        inventory[
            ["product_name", "normalized_product_name"]
        ].to_string(index=False)
    )

    print("\nSALES")
    print(
        sales[
            ["product_name", "normalized_product_name"]
        ].to_string(index=False)
    )

    print("\nRETURNS")
    print(
        returns[
            ["product_name", "normalized_product_name"]
        ].to_string(index=False)
    )