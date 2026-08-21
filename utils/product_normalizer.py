import re


def normalize_product_name(product_name):
    """
    Standardize product names so that small differences
    in capitalization and spacing do not create separate products.
    """

    if not isinstance(product_name, str):
        return ""

    # Convert to lowercase
    name = product_name.lower()

    # Remove extra spaces
    name = re.sub(r"\s+", " ", name).strip()

    # Remove spaces around hyphens and slashes
    name = re.sub(r"\s*([-/])\s*", r"\1", name)

    # Remove spaces between letters and numbers
    name = re.sub(r"([a-z])\s+(\d)", r"\1\2", name)

    return name


if __name__ == "__main__":

    test_names = [
        "Apple iPhone 15",
        "Apple iPhone15",
        "Boat Airdopes 141",
        "boAt Airdopes 141",
        "Dell Inspiron 15",
        "Dell Inspiron15"
    ]

    print("Product Name Normalization Test")
    print("-" * 50)

    for name in test_names:
        normalized = normalize_product_name(name)
        print(f"{name}  ->  {normalized}")