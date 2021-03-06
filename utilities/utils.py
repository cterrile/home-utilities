
import sys
import docopt
import datetime
import os
from socket import gethostname


def evaluate_date(date):
    """Returns datetime object when give a date string or 'yesterday'"""
    if date.lower() == "yesterday":
        new_date = datetime.datetime.today() - datetime.timedelta(days=1)
    else:
        new_date = datetime.datetime.strptime("%Y-%M-%d")

    return new_date


def determine_host():
    """Determines the name of the operating host."""
    if 'COMPUTERNAME' in os.environ.keys():
        return os.environ['COMPUTERNAME']
    elif 'HOST' in os.environ.keys():
        return os.environ['HOST']
    else:
        return gethostname()


def docopt_read(doc, version):
    script_name = os.path.basename(sys.argv[0])

    command = doc.format(program_name=script_name, version=version)
    arguments = docopt.docopt(command)
    return command, arguments


def docopt_error(doc):
    write_clear(doc.strip('\n'))


def write_info(text):
    sys.stdout.write("[INFO] {0}\n".format(str(text)))


def write_clear(text):
    sys.stdout.write("{0}\n".format(text))


def write_warning(text):
    sys.stdout.write("[WARN] {0}\n".format(str(text)))


def write_debug(text):
    sys.stdout.write("[DEBUG] {0}\n".format(str(text)))


def write_error(text):
    sys.stdout.write("[ERROR] {0}\n".format(str(text)))
