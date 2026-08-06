import pandas as pd


def load_data(file_path):
    return pd.read_csv(file_path)


def clean_data(df):
    df = df.copy()

    df["Offer"] = df["Offer"].fillna("No Offer")
    df["Multiple Lines"] = df["Multiple Lines"].fillna("No Phone Service")
    df["Internet Type"] = df["Internet Type"].fillna("No Internet Service")

    internet_columns = [
         "Online Security",
        "Online Backup",
        "Device Protection Plan",
        "Premium Tech Support",
        "Streaming TV",
        "Streaming Movies",
        "Streaming Music",
        "Unlimited Data"
    ]

    for column in internet_columns:
        df[column] = df[column].fillna("No Internet Service")

    df["Churn Category"] = df["Churn Category"].fillna("Not Applicable")
    df["Churn Reason"] = df["Churn Reason"].fillna("Not Applicable")

    df["Churned"] = df["Customer Status"].eq("Churned")

    df["Tenure Segment"] = pd.cut(
        df["Tenure in Months"],
        bins=[0, 6, 12, 24, 48, 72],
        labels=["0-6", "7-12", "13-24", "25-48", "49-72"],
        include_lowest=True
    )

    return df