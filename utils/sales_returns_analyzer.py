import pandas as pd


def load_sales_data():
    """
    Load sales data from the CSV file.
    """
    return pd.read_csv("datasets/sales.csv")


def load_returns_data():
    """
    Load returns data from the CSV file.
    """
    return pd.read_csv("datasets/returns.csv")


def load_inventory_data():
    """
    Load inventory data from the CSV file.
    """
    return pd.read_csv("datasets/inventory.csv")


def calculate_sales_summary(sales):
    """
    Calculate total units sold for each product.
    """

    summary = (
        sales.groupby("product_id")
        .agg(
            total_units_sold=("units_sold", "sum")
        )
        .reset_index()
    )

    return summary


def calculate_returns_summary(returns):
    """
    Calculate total returned units for each product.
    """

    summary = (
        returns.groupby("product_id")
        .agg(
            total_returned_units=("units_returned", "sum")
        )
        .reset_index()
    )

    return summary


def calculate_return_rate(summary):
    """
    Calculate return rate using total returned units
    divided by total units sold.
    """

    summary["return_rate"] = (
        summary["total_returned_units"]
        / summary["total_units_sold"]
    ) * 100

    summary["return_rate"] = (
        summary["return_rate"].round(2)
    )

    return summary


def classify_return_risk(return_rate):
    """
    Classify return risk based on the percentage
    of sold units that were returned.
    """

    if return_rate > 20:
        return "HIGH"

    if return_rate >= 10:
        return "MEDIUM"

    return "LOW"


def calculate_inventory_risk(stock_quantity, reorder_level):
    """
    Calculate inventory risk based on current stock
    and reorder level.
    """

    if stock_quantity <= reorder_level:
        return "HIGH"

    if stock_quantity <= reorder_level * 1.5:
        return "MEDIUM"

    return "LOW"


def calculate_shortage(stock_quantity, reorder_level):
    """
    Calculate the number of units needed to reach
    the reorder level.
    """

    shortage = reorder_level - stock_quantity

    return max(shortage, 0)


def calculate_overall_risk(inventory_risk, return_risk):
    """
    Calculate overall product risk using
    inventory risk and return risk.
    """

    if inventory_risk == "HIGH" and return_risk == "HIGH":
        return "CRITICAL"

    if inventory_risk == "HIGH":
        return "HIGH"

    if return_risk == "HIGH":
        return "HIGH"

    if inventory_risk == "MEDIUM" or return_risk == "MEDIUM":
        return "MEDIUM"

    return "LOW"


def analyze_sales_and_returns():
    """
    Combine inventory, sales, and returns data
    into a single product-level analysis.
    """

    sales = load_sales_data()
    returns = load_returns_data()
    inventory = load_inventory_data()

    sales_summary = calculate_sales_summary(sales)

    returns_summary = calculate_returns_summary(returns)

    summary = inventory.merge(
        sales_summary,
        on="product_id",
        how="left"
    )

    summary = summary.merge(
        returns_summary,
        on="product_id",
        how="left"
    )

    summary["total_units_sold"] = (
        summary["total_units_sold"]
        .fillna(0)
        .astype(int)
    )

    summary["total_returned_units"] = (
        summary["total_returned_units"]
        .fillna(0)
        .astype(int)
    )

    summary["risk_level"] = summary.apply(
        lambda row: calculate_inventory_risk(
            row["stock_quantity"],
            row["reorder_level"]
        ),
        axis=1
    )

    summary["shortage_units"] = summary.apply(
        lambda row: calculate_shortage(
            row["stock_quantity"],
            row["reorder_level"]
        ),
        axis=1
    )

    summary = calculate_return_rate(summary)

    summary["return_risk"] = (
        summary["return_rate"]
        .apply(classify_return_risk)
    )

    summary["overall_risk"] = summary.apply(
        lambda row: calculate_overall_risk(
            row["risk_level"],
            row["return_risk"]
        ),
        axis=1
    )

    return summary


if __name__ == "__main__":

    summary = analyze_sales_and_returns()

    print("\nCOMBINED INVENTORY, SALES AND RETURNS ANALYSIS")
    print("-" * 150)

    print(
        summary[
            [
                "product_id",
                "product_name",
                "stock_quantity",
                "reorder_level",
                "shortage_units",
                "risk_level",
                "total_units_sold",
                "total_returned_units",
                "return_rate",
                "return_risk",
                "overall_risk"
            ]
        ].to_string(index=False)
    )