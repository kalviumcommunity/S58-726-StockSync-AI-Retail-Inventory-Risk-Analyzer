from utils.sales_returns_analyzer import analyze_sales_and_returns


def generate_recommendation(row):
    """
    Generate a business recommendation based
    on the overall product risk.
    """

    if row["overall_risk"] == "CRITICAL":
        return "Urgent review required: low stock and high return risk"

    if row["overall_risk"] == "HIGH":
        if row["shortage_units"] > 0:
            return "Reorder stock and review product performance"

        return "Review product performance and return rate"

    if row["overall_risk"] == "MEDIUM":
        return "Monitor inventory and product performance"

    return "Inventory and product performance are healthy"


def build_risk_engine():
    """
    Build the unified risk analysis dataset.
    """

    analysis = analyze_sales_and_returns()

    analysis["recommendation"] = analysis.apply(
        generate_recommendation,
        axis=1
    )

    return analysis


def get_critical_products():
    """
    Return products classified as CRITICAL.
    """

    analysis = build_risk_engine()

    return analysis[
        analysis["overall_risk"] == "CRITICAL"
    ]


def get_high_risk_products():
    """
    Return products classified as HIGH or CRITICAL.
    """

    analysis = build_risk_engine()

    return analysis[
        analysis["overall_risk"].isin(
            ["HIGH", "CRITICAL"]
        )
    ]


if __name__ == "__main__":

    risk_data = build_risk_engine()

    print("\nSTOCKSYNC UNIFIED RISK ENGINE")
    print("-" * 120)

    print(
        risk_data[
            [
                "product_id",
                "product_name",
                "stock_quantity",
                "shortage_units",
                "total_units_sold",
                "return_rate",
                "risk_level",
                "return_risk",
                "overall_risk",
                "recommendation"
            ]
        ].to_string(index=False)
    )

    print("\nCRITICAL PRODUCTS")
    print("-" * 60)

    critical = get_critical_products()

    if critical.empty:
        print("No critical products found.")
    else:
        print(
            critical[
                [
                    "product_id",
                    "product_name",
                    "overall_risk",
                    "recommendation"
                ]
            ].to_string(index=False)
        )

    print("\nHIGH-RISK PRODUCTS")
    print("-" * 60)

    high_risk = get_high_risk_products()

    print(
        high_risk[
            [
                "product_id",
                "product_name",
                "overall_risk"
            ]
        ].to_string(index=False)
    )