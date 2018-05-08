'''
Python script designed to do the following:

1. Locate and take a list of users from a text file
2. Take the list of users and populate the users.yml Ansible file with the users from the text file
'''

import sys
import os
import re
import json
import argparse
from io import StringIO

# Path and filename for Ansible user file(yml)
ansible_file_path = r"C:\Users\dpemberton\Documents/"
file_name = r"users.yml"

# Path and filename for username text file
text_file_path = r"C:\Users\dpemberton\Documents/"
text_name = r"username.txt"


# Empty list defined to collect usernames
user_list = []


# Function to create full paths for files
def create_full_paths(dir,file):
    try:
        full_path = os.path.join(dir,file)
        return full_path

    except:
        errors = sys.exc_info()
        for idx, error in enumerate(errors):
            if idx < 2:
                print(error)


# Creating full path for the username text file
user_full_path = create_full_paths(text_file_path,text_name)
print(user_full_path)


def get_text_contents(full_path):
    try:
        # File name for username.txt read
        with open(full_path, 'r') as file:
            for line in file:
                # Perform regex to get desired username format
                # m = re.search(r".+(\w+\.\w+).+")
                # username = m.group(1)
                user_list.append(line)
                file.close()


    except:
        Errors = sys.exc_info()
        for idx, error in enumerate(Errors):
            if idx < 2:
                print(error)

    return user_list


def main():
    # parse = argparse.ArgumentParser(description="Usernames to be extracted from username.txt")
    # parse.add_argument("user_args", nargs='+', help="Arguments gathered from username file")
    # args = parse.parse_args()
    # if args.user_args:
        # sys.argv[1:] = args.user_args
        # del sys.argv[1:]

    final_list = get_text_contents(user_full_path)
    print(final_list)

    main()