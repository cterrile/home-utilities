"""

Integration for Slack Incoming Webhooks.

"""


from utilities.certs import DISCORD_WEBHOOK

from Webhook import Webhook


DISCORD_HOOK_URL_BASE = 'https://discordapp.com/api/webhooks/{service_address}'


class Discord(Webhook):

    def __init__(self):

        Webhook.__init__(self, "Discord", DISCORD_HOOK_URL_BASE.format(service_address=DISCORD_WEBHOOK))
        self.webhook_headers = {"Content-Type": "application/json"}

    def set_payload(self):
        self.webhook_payload = {}
        if self.text:
            self.webhook_payload['content'] = self.text

    def notify(self, text=None):
        if text:
            self.set_text(text)
        self.set_payload()
        self.api_post()


if __name__ == "__main__":
    Discord().notify("Test")
