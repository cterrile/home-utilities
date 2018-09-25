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
from utilities.utils import write_info, write_error, determine_host, docopt_read
from utilities.certs import GOOGLE_PASSWORD, GOOGLE_USERNAME, GOOGLE_DOMAIN
from utilities.certs import IP_FILE
from integrations.slack import Slack
from integrations.discord import Discord
from integrations.Webhook import Webhook

IP_URL = "http://checkip.dyndns.org"
PRECEDING_STRING = "Current IP Address: "
PROCEEDING_STRING = "</body></html>"

CHAT_STRING = "`{server}` checking in with IP: `{ip}`"

GOOG_DNS_URL_BASE = "https://{username}:{password}@domains.google.com/nic/update?hostname={subdomain}&myip={ip}"


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

    host = determine_host()
    write_info("Retrieving IPV4 Address")
    ip_address = find_ip_address()

    if check_for_changes(ip_address) or program_args['notify']:

        formatted_chat_string = CHAT_STRING.format(server=host, ip=ip_address)

        # Notify Slack channel
        write_info("Sending Address to Slack Channel")
        Slack().notify(formatted_chat_string)

        # Notify Discord channel
        write_info("Sending Address to Discord Channel")
        Discord().notify(formatted_chat_string)
        
        # Notify Google DNS
        write_info("Sending Address to Google DNS")

        formatted_google_url = GOOG_DNS_URL_BASE.format(username=GOOGLE_USERNAME, password=GOOGLE_PASSWORD,
                                                        subdomain=GOOGLE_DOMAIN, ip=ip_address)
        Webhook("Google DNS", formatted_google_url).api_post()
        

if __name__ == "__main__":
    command_doc, main_args = docopt_read(__doc__, '2.2')
    main_execution(main_args)


