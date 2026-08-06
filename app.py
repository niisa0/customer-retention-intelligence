import streamlit as st
from data_processing import load_data, clean_data
from analytics import (
    get_contract_analysis,
    get_tenure_analysis,
    get_risk_matrix,
    get_churn_reasons,
    get_retention_insights,
    get_financial_impact,
    churn_by_category
    )
from visualizations import (
    create_contract_churn_chart,
    create_tenure_churn_chart,
    create_risk_heatmap,
    create_churn_reasons_chart,
    create_driver_chart
)
from export_utils import to_csv_bytes, to_excel_bytes

st.set_page_config(
    page_title="Customer Retention Intelligence",
    page_icon="📊",
    layout="wide"
)

@st.cache_data
def get_data():
    raw_df = load_data("data/telecom_customer_churn.csv")
    return clean_data(raw_df)


@st.cache_data
def prepare_csv(df):
    return to_csv_bytes(df)


@st.cache_data
def prepare_excel(df):
    return to_excel_bytes(df)


df = get_data()

st.sidebar.header("Filters")
st.sidebar.caption(
    "Filters update all metrics, charts, insights, and exported data."
)

contract_options = [
    "Month-to-Month",
    "One Year",
    "Two Year"
]

selected_contracts = st.sidebar.multiselect(
    "Contract Type",
    options=contract_options,
    default=contract_options
)

tenure_options = df["Tenure Segment"].cat.categories.tolist()

selected_tenure = st.sidebar.multiselect(
    "Tenure Segment",
    options=tenure_options,
    default=tenure_options
)

filtered_df = df[
    (df["Contract"].isin(selected_contracts)) &
    (df["Tenure Segment"].isin(selected_tenure))
]

if filtered_df.empty:
    st.warning("No customers match the selected filters.")
    st.stop()

st.title("Customer Retention Intelligence")
st.caption(
    "Interactive churn analysis and customer retention intelligence dashboard."
)
st.subheader("Customer Overview")

total_customers = len(filtered_df)
churned_customers = int(filtered_df["Churned"].sum())
churn_rate = filtered_df["Churned"].mean() * 100
avg_tenure = filtered_df["Tenure in Months"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Customers", f"{total_customers:,}")
col2.metric("Churned Customers", f"{churned_customers:,}")
col3.metric("Churn Rate", f"{churn_rate:.1f}%")
col4.metric("Average Tenure", f"{avg_tenure:.1f} months")

contract_analysis = get_contract_analysis(filtered_df)
tenure_analysis = get_tenure_analysis(filtered_df)

left_chart, right_chart = st.columns(2)

with left_chart:
    st.plotly_chart(
        create_contract_churn_chart(contract_analysis),
        width="stretch"
    )

with right_chart:
    st.plotly_chart(
        create_tenure_churn_chart(tenure_analysis),
        width="stretch"
    )

risk_matrix = get_risk_matrix(filtered_df)
churn_reasons = get_churn_reasons(filtered_df)

risk_col, reasons_col = st.columns(2)

with risk_col:
    st.plotly_chart(
        create_risk_heatmap(risk_matrix),
        width="stretch"
    )

with reasons_col:
    if churn_reasons.empty:
        st.info("No churned customers in the selected segment.")
    else:
        st.plotly_chart(
            create_churn_reasons_chart(churn_reasons),
            width="stretch"
        )

st.subheader("Churn Driver Explorer")

driver_options = [
    "Internet Type",
    "Premium Tech Support",
    "Online Security",
    "Payment Method",
    "Offer"
]

selected_driver = st.selectbox(
    "Choose a factor to analyze",
    driver_options
)

driver_data = churn_by_category(
    filtered_df,
    selected_driver
)

st.plotly_chart(
    create_driver_chart(driver_data, selected_driver),
    width="stretch"
)

insights = get_retention_insights(filtered_df)

st.subheader("Retention Intelligence")

if insights is None:
    st.success("No churn detected in the selected customer segment.")
else:
    insight_col1, insight_col2 = st.columns(2)

    with insight_col1:
        with st.container(border=True):
            st.markdown("#### Priority Segment")
            st.write(
                f"**{insights['tenure_segment']} months · "
                f"{insights['contract']}**"
            )
            st.write(
                f"{insights['segment_churned']:,} churned customers · "
                f"{insights['segment_churn_rate']:.1f}% churn rate"
            )
            st.caption(
                f"This segment accounts for "
                f"{insights['segment_share']:.1f}% of churn "
                f"under the current filters."
            )

    with insight_col2:
        with st.container(border=True):
            st.markdown("#### Top Reported Churn Reason")
            st.write(f"**{insights['top_reason']}**")
            st.write(
                f"{insights['reason_customers']:,} customers · "
                f"{insights['reason_share']:.1f}% of churn"
            )
            st.caption(
                "Use this as an investigation priority, "
                "not as proof of causation."
            )

financial = get_financial_impact(filtered_df)

st.subheader("Financial Impact")

fin1, fin2, fin3 = st.columns(3)

fin1.metric(
    "Monthly Charge Exposure",
    f"${financial['monthly_charge_exposure']:,.0f}"
)

fin2.metric(
    "Historical Revenue from Churned Customers",
    f"${financial['historical_revenue']:,.0f}"
)

fin3.metric(
    "Avg. Monthly Charge — Churned",
    f"${financial['avg_churned_charge']:,.2f}"
)

st.subheader("Export Data")

csv_data = prepare_csv(filtered_df)
excel_data = prepare_excel(filtered_df)

download_col1, download_col2 = st.columns(2)

with download_col1:
    st.download_button(
        label="Download CSV",
        data=csv_data,
        file_name="filtered_customer_data.csv",
        mime="text/csv",
        on_click="ignore",
        width="stretch"
    )

with download_col2:
    st.download_button(
        label="Download Excel",
        data=excel_data,
        file_name="filtered_customer_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        on_click="ignore",
        width="stretch"
    )