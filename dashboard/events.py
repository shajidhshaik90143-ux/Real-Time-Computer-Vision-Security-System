import pandas as pd
import streamlit as st


def show_events(database):

    st.header("📋 Security Event History")

    events = database.get_events(200)

    if not events:

        st.info(
            "No security events recorded yet."
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

    st.dataframe(
        dataframe,
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "⬇️ Download Event Report",
        dataframe.to_csv(index=False),
        file_name="security_events.csv",
        mime="text/csv"
    )