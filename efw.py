#!/usr/bin/python3

import json
import os
import re
import configparser

config = configparser.ConfigParser()
config.read('efw.ini')


def main():

    ignorelist = [
        r"^/some/directory/[0-9A-Za-z_\-]+/logs/.*",
        r"^/another/directory/[0-9A-Za-z_\-]+/backups/.*"
    ]

    current_folder = ""

    next_line_folder = False
    first_line = True
    new_filelist = {}
    old_filelist = load_savelist()

    with open(config['settings']['save_folder'] + '/filelist.txt') as f:
        for line in f:
            line = line.strip()

            if first_line:
                first_line = False
                current_folder = line[:-1]
                continue

            if line == "":
                next_line_folder = True
                continue

            if line != "" and next_line_folder:
                current_folder = line[:-1]
                next_line_folder = False
                continue

            items = line.split()

            if items[0] == 'total':
                continue

            if items[8] == '.' or items[8] == '..':
                continue

            if len(items) > 9:
                full_filename = ' '.join(items[8:])
            else:
                full_filename = items[8]

            full_filename = current_folder + "/" + full_filename

            skipping = False
            for ilist in ignorelist:
                match_result = re.match(ilist, full_filename)

                if match_result:
                    skipping = True

            if skipping:
                continue

            new_filelist[full_filename] = {
                'permissions': items[0],
                'size': items[4],
                'ctime': items[5] + " " + items[6] + " " + items[7]
            }

            if full_filename not in old_filelist:
                print("New file: " + full_filename)
            else:
                if old_filelist[full_filename]['permissions'] != new_filelist[full_filename]['permissions']:
                    print("Permissions changed: " + full_filename + " [" + old_filelist[full_filename]['permissions'] +
                          "] to [" + new_filelist[full_filename]['permissions'] + "]")

                if old_filelist[full_filename]['size'] != new_filelist[full_filename]['size']:
                    print("Size changed: " + full_filename + " [" + old_filelist[full_filename]['size'] +
                          "] to [" + new_filelist[full_filename]['size'] + "]")

                if old_filelist[full_filename]['ctime'] != new_filelist[full_filename]['ctime']:
                    print("Date changed: " + full_filename + " [" + old_filelist[full_filename]['ctime'] +
                          "] to [" + new_filelist[full_filename]['ctime'] + "]")

    # Now check full_filelist for deleted files
    for full_filename in old_filelist:
        if full_filename not in new_filelist:
            print("Deleted file: " + full_filename)

    with open(config['settings']['save_folder'] + '/savelist.txt', 'w') as fp:
        json.dump(new_filelist, fp)


def load_savelist():
    if not os.path.isfile(config['settings']['save_folder'] + '/savelist.txt'):
        return {}

    with open(config['settings']['save_folder'] + '/savelist.txt', 'r') as fp:
        data = json.load(fp)
    return data


if __name__ == "__main__":
    main()