#!/usr/bin/python3
""" This module is to open a yaml file and update the value of a passed key
found for all instances of it within the entire file or
within a specific top level key.
"""

import yaml
import argparse
import collections.abc


def update_yaml_file(filename, new_config):
    """ update a yaml file with new configuration details.
    :param filename: path to the file to be opened
    :param new_config: new confiruation details to add/updated the file with
    :return:
    """
    try:
        with open(filename, 'w') as f:
            yaml.dump(new_config, f)
    except Exception as e:
        print(str(e))


def open_yaml_file(filename):
    """ open a yaml file to extract configuration details.
    :param filename: path to the file to be opened
    :return config: configuration details located in the file
    """
    try:
        with open(filename, 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        return config
    except Exception as e:
        print(str(e))


def update_value_for_key(dictionary, key, value, top_level_key=None):
    """ Recursive key_value search. Supposed to search through any nested
    dictionary to a passed key and modify all current values to a new values
    passed with it.
    :param dictionary: dict to search through
    :param key: searched key
    :param value: its new value
    :top_level_key: to search only within this top level key if given
    :return dictionary: updated dictionary
    """
    if top_level_key:
        for i in dictionary:
            if i == top_level_key:
                for j in dictionary[top_level_key]:
                    for x in update_value_for_key(j, key, value):
                        x = value
                        yield dictionary
            else:
                yield dictionary
    else:
        if isinstance(dictionary, list):
            for i in dictionary:
                for x in update_value_for_key(i, key, value):
                   x = value
                   yield dictionary
        elif isinstance(dictionary, dict):
            if key in dictionary:
                dictionary[key] = value
                yield dictionary
            for j in dictionary.values():
                for x in update_value_for_key(j, key, value):
                    x = value
                    yield dictionary


def merge_list_of_dicts(dict_list):
    """ Merge list of dicts into one dict.
    :param dict_list: list of dicts to be merged
    :return dictionary: merged dictionary
    """
    dictionary = {k: v for d in dict_list for k, v in d.items()}
    return dictionary


def main(filename, item_key, item_value, top_level_key):
    config = open_yaml_file(filename)
    # update config paramter
    new_config = merge_list_of_dicts(list(update_value_for_key
                                    (config, item_key, item_value,
                                     top_level_key)))
    update_yaml_file(filename, new_config)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Update parameter in yaml configuration file')
    parser.add_argument("--file", help="yaml file to update", required=True)
    parser.add_argument("--item_key", help="parameter key to update", required=True)
    parser.add_argument("--item_value", help="value of the paramter key to update", required=True)
    parser.add_argument("--top_level_key", default=None, help="top level key to limit the search to")
    args = parser.parse_args()
    main(args.file, args.item_key, args.item_value, args.top_level_key)
