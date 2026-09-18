from datetime import datetime


def current_timestamp():

    return datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


def format_event(
    event_type,
    description,
    severity="INFO"
):

    return {
        "event_type": event_type,
        "description": description,
        "severity": severity,
        "timestamp": current_timestamp()
    }