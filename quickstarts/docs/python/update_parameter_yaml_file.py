#!/usr/bin/python3
"""
The module opens a yaml file and updates the value of a passed key.

Updates all instances of the passed key found within the entire file or within a specific top
level key
"""
import yaml
import argparse


def update_yaml_file(filename, new_config):
    """
    Update a yaml file with new configuration details.

    Paramters
    ---------
    filename : STRING
        path to the file to be opened.
    new_config : STRING
        new confiruation details to add/updated the file with.

    Returns
    -------
    None.
    """
    try:
        with open(filename, 'w') as f:
            yaml.dump(new_config, f)
    except Exception as e:
        print(str(e))


def open_yaml_file(filename):
    """
    Open a yaml file to extract configuration details.

    Paramters
    ---------
    filename : STRING
        path to the file to be opened.

    Returns
    -------
    config : STRING
        configuration details located in the file.
    """
    try:
        with open(filename, 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        return config
    except Exception as e:
        print(str(e))


def update_value_for_key(dictionary, key, value, top_level_key=None):
    """
    Recursive key_value search.

    Search through any nested dictionary with a passed key and
    modify all current values to a new value passed with it.

    Paramters
    ---------
    dictionary: dict to search through
    key: searched key
    value: new value for searched key
    top_level_key: to search only within this top level key if given

    Returns
    -------
    dictionary: updated dictionary
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


def merge_list_of_dicts(list_of_dicts):
    """
    Merge list of dicts into one dict.

    Paramters
    ---------
    list_of_dicts : STRING
        list of dicts to be merged.

    Returns
    -------
    merged_dict : STRING
    """
    merged_dict = {k: v for d in list_of_dicts for k, v in d.items()}
    return merged_dict


def main(filename, item_key, item_value, top_level_key):
    """
    Update key parameter in a yaml file with a new value.

    Parameters
    ----------
    filename : STRING
        path to the file to be opened.
    item_key : STRING
        searched key.
    item_value : STRING
        new value of searched key.
    top_level_key : STRING
        limit search to top level only within the dictionary.

    Returns
    -------
    None.

    """
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
    parser.add_argument("--top_level_key", default=None,
                        help="top level key to limit the search to")
    args = parser.parse_args()
    main(args.file, args.item_key, args.item_value, args.top_level_key)
