"""Task manager project misc utilites."""

import json
import os

from django.contrib.messages import get_messages

DIR_PATH = os.path.dirname(__file__)


def get_fixture_path(filename):
    """Return fixture path."""
    return os.path.join(DIR_PATH, 'fixtures', filename)


def read_file(filename):
    """Read fixture file."""
    with open(get_fixture_path(filename)) as data_file:
        return data_file.read()


def get_test_data():
    """Return parsed file."""
    return json.loads(read_file('test_data.json'))


def get_response_messages(response):
    """Read response and return messages."""
    return [
        messages.message for messages in get_messages(response.wsgi_request)
    ]
