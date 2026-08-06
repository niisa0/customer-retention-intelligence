import plotly.express as px


CHART_HEIGHT = 430

def create_contract_churn_chart(data):
    plot_data = data.reset_index()
    plot_data["churn_rate"] = plot_data["churn_rate"].round(1)

    fig = px.bar(
        plot_data,
        x="Contract",
        y="churn_rate",
        text="churn_rate",
        title="Churn Rate by Contract Type"
    )

    fig.update_traces(
        texttemplate="%{y:.1f}%",
        textposition="outside"
    )

    fig.update_layout(
        xaxis_title=None,
        yaxis_title="Churn Rate (%)",
        showlegend=False,
        height=CHART_HEIGHT
    )

    return fig


def create_tenure_churn_chart(data):
    plot_data = data.reset_index()

    fig = px.line(
        plot_data,
        x="Tenure Segment",
        y="churn_rate",
        markers=True,
        title="Churn Rate by Customer Tenure"
    )

    fig.update_traces(
        line_width=3,
        marker_size=9
    )

    fig.update_layout(
        xaxis_title="Tenure (Months)",
        yaxis_title="Churn Rate (%)",
        height=CHART_HEIGHT
    )

    return fig


def create_risk_heatmap(data):
    fig = px.imshow(
        data,
        text_auto=".1f",
        aspect="auto",
        color_continuous_scale="Reds",
        labels={
            "x": "Contract Type",
            "y": "Tenure Segment",
            "color": "Churn Rate (%)"
        },
        title="Churn Risk Matrix"
    )

    fig.update_layout(
        height=CHART_HEIGHT,
        margin=dict(l=40, r=20, t=60, b=40)

    )

    fig.update_xaxes(tickangle=0)

    return fig


def create_churn_reasons_chart(data):
    plot_data = data.sort_values("customers")

    fig = px.bar(
        plot_data,
        x="customers",
        y="Churn Reason",
        orientation="h",
        text="customers",
        title="Top Churn Reasons",
        hover_data=["share_pct"]
    )

    fig.update_layout(
        xaxis_title="Churned Customers",
        yaxis_title=None,
        height=CHART_HEIGHT
    )

    return fig


def create_driver_chart(data, category):
    plot_data = data.sort_values("churn_rate", ascending=False)

    fig = px.bar(
        plot_data,
        x=category,
        y="churn_rate",
        text="churn_rate",
        hover_data=["customers", "churned_customers"],
        title=f"Churn Rate by {category}"
    )

    fig.update_traces(
        texttemplate="%{y:.1f}%",
        textposition="outside"
    )

    fig.update_layout(
        xaxis_title=None,
        yaxis_title="Churn Rate (%)",
        height=CHART_HEIGHT
    )

    return fig