from flask import Flask, render_template

from utils.risk_engine import build_risk_engine


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    df = build_risk_engine()

    total_products = df["product_id"].nunique()
    total_stores = df["store_id"].nunique()

    critical_products = int(
        (df["overall_risk"] == "CRITICAL").sum()
    )

    high_risk_products = int(
        df["overall_risk"].isin(["HIGH", "CRITICAL"]).sum()
    )

    risk_summary = (
        df["overall_risk"]
        .value_counts()
        .to_dict()
    )

    return render_template(
        "dashboard.html",
        total_products=total_products,
        total_stores=total_stores,
        high_risk_products=high_risk_products,
        critical_products=critical_products,
        risk_summary=risk_summary,
    )


@app.route("/upload")
def upload():
    return render_template("upload.html")


@app.route("/analysis")
def analysis():
    df = build_risk_engine()

    risk_summary = (
        df["overall_risk"]
        .value_counts()
        .to_dict()
    )

    products = df.to_dict(orient="records")

    return render_template(
        "analysis.html",
        products=products,
        risk_summary=risk_summary,
    )


@app.route("/reports")
def reports():
    df = build_risk_engine()

    total_products = df["product_id"].nunique()
    total_stores = df["store_id"].nunique()

    critical_products = int(
        (df["overall_risk"] == "CRITICAL").sum()
    )

    high_risk_products = int(
        df["overall_risk"].isin(["HIGH", "CRITICAL"]).sum()
    )

    risk_summary = (
        df["overall_risk"]
        .value_counts()
        .to_dict()
    )

    products = df.to_dict(orient="records")

    return render_template(
        "reports.html",
        total_products=total_products,
        total_stores=total_stores,
        critical_products=critical_products,
        high_risk_products=high_risk_products,
        risk_summary=risk_summary,
        products=products,
    )


if __name__ == "__main__":
    app.run(debug=True)
