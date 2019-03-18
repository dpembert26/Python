'''
Python script designed to do the following:

1. Locate and take a list of users from a specific group in Active Directory that was created within the last 7 days
2. Take the list of users found and create the users.yml Ansible file with the users from the Active Directory group
3. Send an email to team members when the users.yml file is created with the new accounts that was found.

Author:  Darin Pemberton 5/11/2018
'''

import sys
import os
import re
from pyad import pyad
import datetime
from datetime import timedelta, timezone
import smtplib
from smtplib import SMTPException


# Path and filename for Ansible user file(yml)
ansible_file_path = r"C:\Users\xxxxxxxxxxxxx\Documents\Ansible Playbooks/"
file_name = r"users.yml"

# Declare empty lists to store user names from Active Directory
users_list =[]
users_for_email = []
user_names_list = []
days = 7
user_name = ''
user_acct = ''


# Function to remove duplicate accounts from the list
def remove_duplicate_accounts(accounts):
    accounts = set(accounts)
    accounts = list(accounts)
    return accounts


# Function to get account(s) full name
def get_full_name():
    global days
    global user_name
    ops_group = pyad.from_cn("xxxxxx")

    # Get 30 days before the current date
    days_within_30 = datetime.datetime.now(timezone.utc) - timedelta(days)
    for g_members in ops_group.get_members(recursive=False):
        if g_members.whencreated > days_within_30:
            user_names_list.append(g_members.name)
            if len(user_names_list) > 1:
                user_name = tuple(user_names_list)
            else:
                user_name = tuple(user_names_list)
                m = re.search(r"\(\'(\w+\,)\s(\w+)\'\,\)", str(user_name))
                user_name = m.group(1)
                user_name += ' ' + m.group(2)

    # Removing duplicate accounts from the list
    # list_names = remove_duplicate_accounts(user_names_list)
    return user_name


# Function to list new account
def list_accounts():
    global user_acct
    ops_group = pyad.from_cn("xxxxxxx")

    # Get 30 days before the current date
    days_within_30 = datetime.datetime.now(timezone.utc) - timedelta(days)
    for g_members in ops_group.get_members(recursive=False):
        m = re.search(r"(\w+),\s(\w).+", str(g_members.name))
        users = m.group(2)
        users += m.group(1)
        if g_members.whencreated > days_within_30:
            users_for_email.append(users.lower())
            if len(users_for_email) > 1:
                user_acct = tuple(users_for_email)
            else:
                user_acct = tuple(users_for_email)
                m = re.search(r"\(\'(\w+)\',\)", str(user_acct))
                user_acct = m.group(1)
    # Removing duplicate accounts from the list
    # list_final = remove_duplicate_accounts(users_for_email)
    return user_acct


# Message for email
message = """From: From xxxxxxx Team <xxxxxx@xxxxxxxx.com>
To: To Person <xxxxxxxx.xxxxxxxx@xxxxxxxxx.com>
MIME-Version: 1.0
Content-type: text/html
Subject: New Account created 

Hello Team,<br>
            &nbsp;&nbsp;&nbsp;&nbsp;Account(s) have been created within the last 7 days for the group xxxxxxxx(CN=xxxxxxx,OU=xxxxxxx Domain DLs,DC=xxxxxxx,DC=xx,DC=xxx).<br><br> \
            <b>Account(s):<br> {}</b><br><br><b>Full Name(s): <br> {} </b><br><br> Regards,<br>The xxxxxx Team""".format(list_accounts(), get_full_name())

# function to connect to Active Directory and get new user in the DevOps group
def get_new_accounts():
    # Find the group based on the base dn name and then get the users that belong to that group with specific attributes
    # base_dn = "CN=xxxxxx,OU=xxxxxxxx Domain DLs,DC=xxxxxxx,DC=xx,DC=xxx"
    ops_group = pyad.from_cn("xxxxxx")

    # Get 30 days before the current date
    days_within_30 = datetime.datetime.now(timezone.utc) - timedelta(days)
    for g_members in ops_group.get_members(recursive=False):
        m = re.search(r"(\w+),\s(\w).+", str(g_members.name))
        users = m.group(2)
        users += m.group(1)
        if g_members.whencreated > days_within_30:
            print("The user {} is new and was created {}. The account created date threshold is {}".format(users.lower(), g_members.whencreated, days_within_30))
            users_list.append(users.lower())
    # Removing duplicate accounts from the list
    users_list_final = remove_duplicate_accounts(users_list)
    return users_list_final


def send_email():
    # Setting up email to/from and body
    sender = "xxxxxxx@xxxxxxxx.com"
    receivers = "xxxxxxx.xxxxxxxxx@xxxxxxx.com"
    try:
        smtpObj = smtplib.SMTP('xxxxxxx.xxxxxxxx.com')
        smtpObj.sendmail(sender, receivers, message)
        print("Successfully sent email")
    except SMTPException:
        print("Error: unable to send email")


# Function to delete the users.yml file if it exists
def remove_yaml_file(file_path,yml_file,accounts):
    try:
        # Create full path for the file users.yml
        full_path = os.path.join(file_path, yml_file)
        # Check if users.yml file exist, check if accounts from the list are already in the file.
        # If so, erase the file contents and close it.
        # If not then close the file and delete the file
        if os.path.isfile(full_path):
            for account in accounts:
                if str(account) in open(full_path).read():
                    # open file, erase file contents and close the file
                    open(full_path, 'w').close()
                else:
                    with open(full_path, 'r') as file:
                        file.close()
                        # remove the users.yml file
                        os.unlink(full_path)
                        print("The file {} has been deleted".format(yml_file))
                        break

    except:
        errors = sys.exc_info()
        for idx, error in enumerate(errors):
            if idx < 2:
                print(error)


# Function to create full paths for files
def create_full_paths(dir_path,file):
    try:
        # joining path with file
        full_path = os.path.join(dir_path,file)
        return full_path

    except:
        errors = sys.exc_info()
        for idx, error in enumerate(errors):
            if idx < 2:
                print(error)


# Function to build the Yaml file based on the username.txt file
def build_yaml(users,full_path):
    try:
        # Create file if it does not exist and write to it
        with open(full_path, 'w') as file:
            file.write("---\n")
            file.write("users:\n")
            if len(users) > 0:
                for user in users:
                    file.write("  - username: " + user + "\n")
            else:
                file.write("  - username: " + users + "\n")
        file.close()


    except:
        Errors = sys.exc_info()
        for idx, error in enumerate(Errors):
            if idx < 2:
                print(error)


def main():
    # Get account list for email
    listed_accounts = list_accounts()

    # Close the users.yml file if it exists and then delete it
    remove_yaml_file(ansible_file_path,file_name, listed_accounts)

    # Creating full path for the users.yml file
    ansible_full_path = create_full_paths(ansible_file_path, file_name)

    # Check how many accounts are listed as new accounts ready to be created on the servers
    if len(listed_accounts) > 0:
        # Get the newest account(s) from AD for the group DevOps
        user_accounts = get_new_accounts()

        # send email showing that new account was created
        send_email()

        # Create Yaml file from user names
        build_yaml(user_accounts,ansible_full_path)


main()
