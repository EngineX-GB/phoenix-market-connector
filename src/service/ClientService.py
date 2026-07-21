import requests


class ClientService:

    def __init__(self):
        pass

    @staticmethod
    def send_notification(notification_type, operation, status, detail):
        payload = {
            "notificationType" : notification_type,
            "content" : {
                "operation" : operation,
                "serviceName" : "phoenix-market-connector",
                "status" : status,
                "detail" : detail
            }
        }
        response = requests.post("http://localhost:8081/notifications/publish", json=payload)
        if response.status_code != 201:
            print(f'[ERROR] An error has occurred when sending a notification to the phoenix client service : {response.status_code}')
