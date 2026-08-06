import pandas as pd


def churn_by_category(df, column):
    summary = (
        df.groupby(column, dropna=False)
        .agg(
            customers=("Customer ID", "count"),
            churned_customers=("Churned", "sum"),
            churn_rate=("Churned", "mean")
        )
        .reset_index()
    )

    summary["churn_rate"] = (summary["churn_rate"] * 100).round(2)

    return summary.sort_values("churn_rate", ascending=False)


def get_contract_analysis(df):
    summary = (
        df.groupby("Contract")
        .agg(
            customers=("Customer ID", "count"),
            churn_rate=("Churned", "mean"),
            avg_monthly_charge=("Monthly Charge", "mean")
        )
    )

    summary["churn_rate"] *= 100

    return summary.sort_values("churn_rate", ascending=False)


def get_tenure_analysis(df):
    summary = (
        df.groupby("Tenure Segment", observed=True)
        .agg(
            customers=("Customer ID", "count"),
            churn_rate=("Churned", "mean")
        )
    )

    summary["churn_rate"] *= 100

    return summary


def get_risk_matrix(df):
    return pd.pivot_table(
        df,
        values="Churned",
        index="Tenure Segment",
        columns="Contract",
        aggfunc="mean",
        observed=True
    ) * 100


def get_priority_segments(df):
    summary = (
        df.groupby(
            ["Tenure Segment", "Contract"],
            observed=True
        )
        .agg(
            customers=("Customer ID", "count"),
            churned_customers=("Churned", "sum"),
            churn_rate=("Churned", "mean"),
            avg_monthly_charge=("Monthly Charge", "mean")
        )
        .reset_index()
    )

    summary["churn_rate"] *= 100

    return summary.sort_values(
        "churned_customers",
        ascending=False
    )


def get_churn_reasons(df, top_n=10):
    churned_df = df[df["Churned"]]

    if churned_df.empty:
        return pd.DataFrame(
            columns=["Churn Reason", "customers", "share_pct"]
        )

    summary = (
        churned_df["Churn Reason"]
        .value_counts()
        .head(top_n)
        .rename_axis("Churn Reason")
        .reset_index(name="customers")
    )

    summary["share_pct"] = (
        summary["customers"] / len(churned_df) * 100
    ).round(1)

    return summary


def get_retention_insights(df):
    total_churned = int(df["Churned"].sum())

    if total_churned == 0:
        return None

    priority_segments = get_priority_segments(df)
    top_segment = priority_segments.iloc[0]

    top_reason = get_churn_reasons(df, top_n=1).iloc[0]

    return {
        "tenure_segment": top_segment["Tenure Segment"],
        "contract": top_segment["Contract"],
        "segment_churned": int(top_segment["churned_customers"]),
        "segment_churn_rate": float(top_segment["churn_rate"]),
        "segment_share": float(
            top_segment["churned_customers"] / total_churned * 100
        ),
        "top_reason": top_reason["Churn Reason"],
        "reason_customers": int(top_reason["customers"]),
        "reason_share": float(top_reason["share_pct"])
    }


def get_financial_impact(df):
    churned_df = df[df["Churned"]]

    if churned_df.empty:
        return {
            "monthly_charge_exposure": 0,
            "historical_revenue": 0,
            "avg_churned_charge": 0
        }
    
    return {
        "monthly_charge_exposure": churned_df["Monthly Charge"].sum(),
        "historical_revenue": churned_df["Total Revenue"].sum(),
        "avg_churned_charge": churned_df["Monthly Charge"].mean()
    }