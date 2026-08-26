import pandas as pd


def calculate_risk(stock_quantity, reorder_level):
    """
    Calculate inventory risk based on current stock
    and the product's reorder level.
    """

    if stock_quantity <= reorder_level:
        return "HIGH"

    if stock_quantity <= reorder_level * 1.5:
        return "MEDIUM"

    return "LOW"


def calculate_shortage(stock_quantity, reorder_level):
    """
    Calculate how many units are needed to reach
    the reorder level.
    """

    shortage = reorder_level - stock_quantity

    return max(shortage, 0)


def get_recommendation(risk_level):
    """
    Provide an action based on the inventory risk level.
    """

    recommendations = {
        "HIGH": "Reorder immediately",
        "MEDIUM": "Monitor stock and consider reordering",
        "LOW": "Stock level is healthy"
    }

    return recommendations.get(
        risk_level,
        "Review inventory"
    )


def analyze_inventory():
    """
    Load inventory data and calculate risk,
    shortage, and recommendations for every product.
    """

    inventory = pd.read_csv("datasets/inventory.csv")

    inventory["risk_level"] = inventory.apply(
        lambda row: calculate_risk(
            row["stock_quantity"],
            row["reorder_level"]
        ),
        axis=1
    )

    inventory["shortage_units"] = inventory.apply(
        lambda row: calculate_shortage(
            row["stock_quantity"],
            row["reorder_level"]
        ),
        axis=1
    )

    inventory["recommendation"] = (
        inventory["risk_level"]
        .apply(get_recommendation)
    )

    return inventory


def get_risk_summary(inventory):
    """
    Return the number of products in each risk category.
    """

    summary = inventory["risk_level"].value_counts()

    return {
        "HIGH": int(summary.get("HIGH", 0)),
        "MEDIUM": int(summary.get("MEDIUM", 0)),
        "LOW": int(summary.get("LOW", 0))
    }


if __name__ == "__main__":

    inventory = analyze_inventory()

    print("\nINVENTORY RISK ANALYSIS")
    print("-" * 110)

    print(
        inventory[
            [
                "product_id",
                "product_name",
                "stock_quantity",
                "reorder_level",
                "shortage_units",
                "risk_level",
                "recommendation"
            ]
        ].to_string(index=False)
    )

    print("\nRISK SUMMARY")
    print("-" * 60)

    summary = get_risk_summary(inventory)

    for risk_level, count in summary.items():
        print(f"{risk_level}: {count}")