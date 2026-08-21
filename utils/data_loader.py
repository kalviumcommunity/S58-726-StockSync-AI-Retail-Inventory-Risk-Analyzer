import pandas as pd


def load_datasets():
    inventory = pd.read_csv("datasets/inventory.csv")
    sales = pd.read_csv("datasets/sales.csv")
    returns = pd.read_csv("datasets/returns.csv")

    return inventory, sales, returns


if __name__ == "__main__":
    inventory, sales, returns = load_datasets()

    print("Inventory dataset:")
    print(inventory.head())

    print("\nSales dataset:")
    print(sales.head())

    print("\nReturns dataset:")
    print(returns.head())