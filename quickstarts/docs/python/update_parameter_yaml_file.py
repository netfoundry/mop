#!/usr/bin/python3

import yaml
import argparse


def update_yaml_file(filename, new_config):
    # update yaml file
    try:
        with open(filename, 'w') as f:
            yaml.dump(new_config, f)
    except Exception as e:
        print(str(e))


def open_yaml_file(filename):
    # open yaml file to update
    try:
        with open(filename, 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        return config
    except Exception as e:
        print(str(e))


def main(filename, item_key, item_value):
    config = open_yaml_file(filename)
    # update config paramter
    config[item_key] = item_value
    update_yaml_file(filename, config)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Update parameter in yaml configuration file')
    parser.add_argument("--file", help="yaml file to update", required=True)
    parser.add_argument("--item_key", help="parameter key to update", required=True)
    parser.add_argument("--item_value", help="value of the paramter key to update", required=True)
    args = parser.parse_args()
    main(args.file, args.item_key, args.item_value)
