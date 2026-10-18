import requests


class ClientService:

    def __init__(self):
        pass

    @staticmethod
    def send_notification(client_service_base_endpoint, notification_type, operation, status, detail):
        payload = {
            "notificationType" : notification_type,
            "content" : {
                "operation" : operation,
                "serviceName" : "phoenix-market-connector",
                "status" : status,
                "detail" : detail
            }
        }
        response = requests.post(f"{client_service_base_endpoint}/notifications/publish", json=payload)
        if response.status_code != 201:
            print(f'[ERROR] An error has occurred when sending a notification to the phoenix client service : {response.status_code}')
