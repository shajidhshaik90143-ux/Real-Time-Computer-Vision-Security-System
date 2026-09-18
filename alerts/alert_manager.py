from datetime import datetime


class AlertManager:

    def __init__(self):

        self.alerts = []

    def create_alert(
        self,
        alert_type,
        message,
        severity="HIGH"
    ):

        alert = {
            "type": alert_type,
            "message": message,
            "severity": severity,
            "time": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }

        self.alerts.append(alert)

        return alert

    def get_recent(self, limit=20):

        return self.alerts[-limit:]

    def clear(self):

        self.alerts.clear()