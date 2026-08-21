from flask import Flask, render_template, jsonify

from utils.risk_engine import build_risk_engine


app = Flask(__name__)


@app.route("/")
def home():
    """
    Home page.
    """
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    """
    Display the unified StockSync risk analysis.
    """

    risk_data = build_risk_engine()

    records = risk_data.to_dict(orient="records")

    risk_summary = (
        risk_data["overall_risk"]
        .value_counts()
        .to_dict()
    )

    return render_template(
        "dashboard.html",
        products=records,
        risk_summary=risk_summary
    )


@app.route("/api/risk-analysis")
def risk_analysis_api():
    """
    Return unified risk analysis as JSON.
    """

    risk_data = build_risk_engine()

    records = risk_data.to_dict(orient="records")

    return jsonify(records)


if __name__ == "__main__":
    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )