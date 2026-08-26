import pandas as pd

from product_normalizer import normalize_product_name


def detect_product_variations():

    inventory = pd.read_csv("datasets/inventory.csv")

    inventory["normalized_product_name"] = (
        inventory["product_name"]
        .apply(normalize_product_name)
    )

    variations = (
        inventory.groupby("normalized_product_name")["product_name"]
        .nunique()
        .reset_index(name="name_variation_count")
    )

    variations = variations[
        variations["name_variation_count"] > 1
    ]

    return inventory, variations


if __name__ == "__main__":

    inventory, variations = detect_product_variations()

    print("\nPRODUCT NAME VARIATIONS")
    print("-" * 50)

    if variations.empty:
        print("No product name variations detected.")
    else:
        for normalized_name in variations["normalized_product_name"]:

            names = (
                inventory[
                    inventory["normalized_product_name"]
                    == normalized_name
                ]["product_name"]
                .unique()
            )

            print(f"\nStandard name: {normalized_name}")
            print("Variations:")

            for name in names:
                print(f"  - {name}")