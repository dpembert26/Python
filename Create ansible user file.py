
'''
Python script designed to do the following:

1. Locate and take a list of users from a text file
2. Take the list of users and populate the users.yml Ansible file with the users from the text file
'''

import sys
import os
import re
import json
from io import StringIO

# Path and filename for Ansible user file(yml)
ansible_file_path = r"C:\Users\dpemberton\Documents/"
file_name = r"users.yml"

# Path and filename for username text file
text_file_path = r"C:\Users\dpemberton\Documents/"
text_name = r"username.txt"


# Empty list defined to collect user names
user_list = []


# Function to delete the users.yml file if it exists
def remove_yaml_file(file_path,yml_file):
    try:
        # Create full path for the file users.yml
        full_path = os.path.join(file_path, yml_file)
        # Check if users.yml file exist and close it
        if os.path.isfile(full_path):
            with open(full_path, 'r') as file:
                file.close()
                # remove the users.yml file
                os.unlink(full_path)
                print("The file {} has been deleted".format(yml_file))

    except:
        errors = sys.exc_info()
        for idx, error in enumerate(errors):
            if idx < 2:
                print(error)


# Function to create full paths for files
def create_full_paths(dir,file):
    try:
        # joining path with file
        full_path = os.path.join(dir,file)
        return full_path

    except:
        errors = sys.exc_info()
        for idx, error in enumerate(errors):
            if idx < 2:
                print(error)


# Function to get the contents of the username.txt file
def get_text_contents(full_path):
    try:
        # File name for username.txt read
        with open(full_path, 'r') as file:
            count = 0
            for line in file:
                # Perform regex to get desired username format
                m = re.search(r".+?(\w+.\w+)(?=@).+", str(line))
                username = m.group(1)
                user_list.append(username)
                count += 1
            print("There are {} user names to be setup and the List is {}".format(count,user_list))
        file.close()

    except:
        Errors = sys.exc_info()
        for idx, error in enumerate(Errors):
            if idx < 2:
                print(error)

    return user_list


# Function to build the Yaml file based on the username.txt file
def build_yaml(users,full_path):
    try:
        # Create file if it does not exist and write to it
        with open(full_path, 'w') as file:
            file.write("---\n")
            file.write("users:\n")
            for user in users:
                file.write("  - username: " + user + "\n")
        file.close()


    except:
        Errors = sys.exc_info()
        for idx, error in enumerate(Errors):
            if idx < 2:
                print(error)


def main():
    # Close the users.yml file if it exists and then delete it
    remove_yaml_file(ansible_file_path,file_name)

    # Creating full path for the username text file
    user_full_path = create_full_paths(text_file_path, text_name)

    # Creating full path for the users.yml file
    ansible_full_path = create_full_paths(ansible_file_path, file_name)

    # Get the user names from the username file
    get_text_contents(user_full_path)

    # Create Yaml file from user names
    build_yaml(user_list,ansible_full_path)


main()