from __future__ import unicode_literals
from pathlib import Path

# TODO: decide what to do with logger and progress hook for youtube-dl

class MyLogger(object):
    def debug(self, msg):
        print(msg)

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)

def remove_suffix(input_string, suffix):
    if suffix and input_string.endswith(suffix):
        return input_string[:-len(suffix)]
    return input_string


def parse_ultrastar(file):
    config = {}
    for curr_line in file:
        if ("#" in curr_line):
            splitted_string = curr_line[1:].split(":")
            config[splitted_string[0]] = splitted_string[1]
        else:
            break

    return config

# Check if file has been parsed correctly
def check_ultrastar(parsed_config):
    # We need artist, title and song
    if ("ARTIST" not in parsed_config):
        return -1
    if ("TITLE" not in parsed_config):
        return -1
    if ("MP3" not in parsed_config):
        return -1
    return 0




