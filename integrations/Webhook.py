
import requests


from utilities.utils import write_info, write_warning


class Webhook:

    def __init__(self, webhook_url, integration_name):
        self.text = None
        self.attachments = None
        self.url = webhook_url
        self.webhook_payload = None
        self.webhook_headers = None
        self.integration_name = integration_name

    def api_post(self):
        notify_response = requests.post(self.url, json=self.webhook_payload, headers=self.webhook_headers)
        if notify_response.status_code not in [200, 204]:
            write_warning(notify_response.headers)

    def set_text(self, text):
        self.text = text
