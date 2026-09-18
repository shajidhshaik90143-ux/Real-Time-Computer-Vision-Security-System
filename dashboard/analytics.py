import pandas as pd
import plotly.express as px
import streamlit as st


def show_analytics(database):

    st.header("📊 Security Analytics")

    events = database.get_events(1000)

    if not events:

        st.info(
            "No data available for analytics."
        )

        return

    dataframe = pd.DataFrame(
        events,
        columns=[
            "ID",
            "Event",
            "Description",
            "Severity",
            "Timestamp",
            "Evidence"
        ]
    )

    # Event distribution
    event_counts = (
        dataframe["Event"]
        .value_counts()
        .reset_index()
    )

    event_counts.columns = [
        "Event",
        "Count"
    ]

    figure = px.bar(
        event_counts,
        x="Event",
        y="Count",
        title="Security Events"
    )

    st.plotly_chart(
        figure,
        use_container_width=True
    )

    # Severity
    severity_counts = (
        dataframe["Severity"]
        .value_counts()
        .reset_index()
    )

    severity_counts.columns = [
        "Severity",
        "Count"
    ]

    figure2 = px.pie(
        severity_counts,
        names="Severity",
        values="Count",
        title="Event Severity"
    )

    st.plotly_chart(
        figure2,
        use_container_width=True
    )