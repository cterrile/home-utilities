
import requests


from utilities.utils import write_info, write_warning


class Webhook:

    def __init__(self, integration_name, webhook_url):
        self.text = None
        self.attachments = None
        self.url = webhook_url
        self.webhook_payload = None
        self.webhook_headers = None
        self.integration_name = integration_name
        self.debug = False

    def api_post(self):
        notify_response = requests.post(self.url, json=self.webhook_payload, headers=self.webhook_headers)
        if self.debug:
            write_info("Webhook Payload: {0}".format(self.webhook_payload))
        if notify_response.status_code not in [200, 204]:
            write_warning(notify_response.status_code)
            write_warning(notify_response.headers)
            write_warning(notify_response.text)

    def set_text(self, text):
        self.text = text
