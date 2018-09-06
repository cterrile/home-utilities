#!/usr/bin/env python
"""
IPV4 Finder
Version : {version}

Usage:
    {program_name} [notify]

Description:
    This script parses the chosen website to find the IPV4 address of the of the Router's WAN Address.

Options:
    -h --help                   Show help.
    --version                   Show version.

Examples:

    Regular run
    ---------------------------------------

    {program_name}
    Retrieves WAN IPV4 Address of server and notifies systems if change is detected.

    {program_name} notify
    Retrieves WAN IPV4 Address of sever and notifies systems regardless of any change.
"""
import os
import json
import requests
from utilities.utils import write_info, write_error, write_warning, docopt_read
from utilities.certs import GOOGLE_PASSWORD, GOOGLE_USERNAME, GOOGLE_DOMAIN
from utilities.certs import DISCORD_WEBHOOK, SLACK_WEBHOOK, IP_FILE

IP_URL = "https://www.iplocation.net/find-ip-address"
PRECEDING_STRING = "Your IP Address is <span style='font-weight: bold; color:green;'>"
PROCEEDING_STRING = "</span>"

CHAT_STRING = "`{server}` checking in with IP: `{ip}`"

GOOG_DNS_URL_BASE = "https://{username}:{password}@domains.google.com/nic/update?hostname={subdomain}&myip={ip_port}"

SLACK_HOOK_URL_BASE = 'https://hooks.slack.com/services/{service_address}'
DISCORD_HOOK_URL_BASE = 'https://discordapp.com/api/webhooks/{service_address}'


def find_ip_address():
    try:
        ip_response = requests.get(IP_URL)
        response_page = ip_response.text
        address_start = response_page.find(PRECEDING_STRING) + len(PRECEDING_STRING)
        address_end = address_start + response_page[address_start:].find(PROCEEDING_STRING)
        ip_string = response_page[address_start:address_end]
        return ip_string

    except Exception as e:
        write_error(e)
        raise e


def notify_system(url, payload=None, headers=None):

    notify_response = requests.post(url, json=payload, headers=headers)
    if notify_response.status_code not in [200, 204]:
        write_warning(notify_response.headers)


def check_for_changes(ip_address):
    stored_ip_address = json.load(open(IP_FILE))

    if ip_address == stored_ip_address['ip']:
        write_info("No change to IP Address.")
        return False
    else:
        write_info("New IP address determined.")
        with open(IP_FILE, 'wb') as current_ip_file:
            stored_ip_address['ip'] = ip_address
            json.dump(stored_ip_address, current_ip_file)
            current_ip_file.close()
            write_info("Saved new address to {0}".format(IP_FILE))
        return True


def main_execution(program_args):

    host = os.environ['COMPUTERNAME']
    write_info("Retrieving IPV4 Address")
    ip_address = find_ip_address()

    if check_for_changes(ip_address) or program_args['notify']:
        # Notify Slack channel
        write_info("Sending Address to Slack Channel")
        formatted_chat_string = CHAT_STRING.format(server=host, ip=ip_address)
        slack_payload = {"text": formatted_chat_string}
        formatted_slack_url = SLACK_HOOK_URL_BASE.format(service_address=SLACK_WEBHOOK)
        notify_system(formatted_slack_url, slack_payload)

        # Notify Discord channel
        write_info("Sending Address to Discord Channel")
        discord_payload = {"content": formatted_chat_string}
        formatted_discord_url = DISCORD_HOOK_URL_BASE.format(service_address=DISCORD_WEBHOOK)
        notify_system(formatted_discord_url, discord_payload, {"Content-Type": "application/json"})
        
        # Notify Google DNS
        write_info("Sending Address to Google DNS")
        ip_port_string = "{ip}".format(ip=ip_address)
        formatted_google_url = GOOG_DNS_URL_BASE.format(username=GOOGLE_USERNAME, password=GOOGLE_PASSWORD,
                                                        subdomain=GOOGLE_DOMAIN, ip_port=ip_port_string)
        notify_system(formatted_google_url)
        

if __name__ == "__main__":
    command_doc, main_args = docopt_read(__doc__, '2.2')
    main_execution(main_args)


