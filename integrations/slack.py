"""

Integration for Slack Incoming Webhooks.

"""

from utilities.utils import write_info, write_warning

from utilities.certs import SLACK_WEBHOOK as SLACK_SERVICE_ADDRESS

from Webhook import Webhook


SLACK_HOOK_URL_BASE = "https://hooks.slack.com/services/{service_address}"


class Slack(Webhook):

    def __init__(self):

        Webhook.__init__(self,SLACK_HOOK_URL_BASE.format(SLACK_SERVICE_ADDRESS),"Slack")

    def set_payload(self):
        self.webhook_payload = {}
        if self.text:
            self.webhook_payload['content'] = self.text

    def notify(self,text=None):
        if text:
            self.set_text(text)
        self.set_payload()
        self.api_post()
