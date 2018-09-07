"""

Integration for Slack Incoming Webhooks.


"""

from utilities.certs import SLACK_WEBHOOK as SLACK_SERVICE_ADDRESS

from Webhook import Webhook


SLACK_HOOK_URL_BASE = "https://hooks.slack.com/services/{service_address}"


class Slack(Webhook):

    def __init__(self):

        Webhook.__init__(self, "Slack", SLACK_HOOK_URL_BASE.format(service_address=SLACK_SERVICE_ADDRESS))

    def set_payload(self):
        self.webhook_payload = {}
        if self.text:
            self.webhook_payload['text'] = self.text

    def notify(self, text=None):
        if text:
            self.set_text(text)
        self.set_payload()
        self.api_post()


if __name__ == "__main__":
    Slack().notify("Test")
