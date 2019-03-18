'''
This is a Python script(Running on xx.xx.xx.xxx 12AM every Monday) to get all of the backends from HAproxy as a list. Take that list and compare them to the
list of backends that is in the apps.txt file in the Github repository. Then the script will gather the differences
between the apps.txt and HAproxy to update the apps.txt in the Repo. The script will then update the apps.txt file on the
server as well. Before it does the update to the apps.txt file on the server, a backup is performed to apps.bak.
'''
# Import modules
import smtplib
from smtplib import SMTPException
import paramiko
import sys
import json
import requests
import base64



# Declare command and variables to get all the backends from HAproxy. Using Paramiko to access the server to issue commands
command = "grep -E  /etc/haproxy/haproxy.conf  -e  '^  use_backend\s(.+)\sif.+' | sed 's/use_backend//g' |  sed -r 's/if.+//g'  > /home/svc-xxxxxxxx/halist.txt"
pk = r"/home/svc-xxxxxxxx/id_rsa"
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
mykey = paramiko.RSAKey.from_private_key_file(pk)  # Paramiko using private key file for authentication
ssh.connect("xxx.xx.xxx.xx",username='svc-xxxxxxxx', pkey=mykey ) # ssh using Paramiko
file = 'halist.txt'


# Declaring variables to be used in the functions below
line_list = []
ssl_list =[]
result_list = []
list_str = ''


# Function to copy all of the sites from haproxy config to halist file
def copy_haproxy_conf():
    stdin, stdout, stderr = ssh.exec_command(command)
    #print(stderr.readlines())


# Function to get backend list from halist file and put into a list object
def get_halist():
    global line_list
    sftp_client = ssh.open_sftp()
    remote_file = sftp_client.open('/home/svc-xxxxxxxxx/%s' % file)
    try:
        line_list = [line for line in remote_file.readlines()]
        line_list = [x.strip() for x in line_list]
        line_list = [line.strip('\n') for line in line_list]
        # Add in these elements into the HAproxy list
        extra_list = ['xxxxxxx.xxxxxxxx.com','xxxxxxx-xxx.xxxxxxxx.com','xxxxxxxxxx.xxxxxxxxx.com']
        # Remove these elements from the HAproxy list
        not_wanted = ['xxxxxx-api','xxxxxx.xxxxxxx.com','xxxxxxx.xxxxxxxx.com','#xxxxxxxxx.xxxxxxxxx.com']
        line_list.extend(extra_list)
        line_list = [e for e in line_list if e not in not_wanted]
        # print('HA' , sorted(line_list))

    except:
        Errors = sys.exc_info()
        for idx, error in enumerate(Errors):
            if idx < 2:
                print(error)
    remote_file.close()
    return sorted(line_list)


# Function to get site list from the apps.txt file in the Github repo
def get_replist():
    global result_list, no_diff
    # Define Repo, owner and path
    owner = "xxxxxxxxx-Labs"
    repo = "xxx-xxxxxx-xxxxxxx"
    path = "apps.txt"

    # Token, headers and URL
    token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    url = "https://api.github.com/repos/{}/{}/contents/{}".format(owner,repo,path)

    headers = {
               "Authorization": 'Bearer {0}'.format(token) ,
               "Content-Type" : "application/json"
       }
    # get request to obtain the contents of the apps.txt file in the Github repo
    response = requests.get(url, headers=headers)
    response = json.loads(response.content.decode('utf-8'))  # Convert all data content to an object while decoding utf-8
    for key,value in response.items():
        if key == 'content':
            result = value
            result = base64.b64decode(result)  # Convert the file content from base64
            result = result.decode('utf-8')    # Decode the file content from utf-8
            result_list_spl = result.split('\n')  # Split the object by newline
            result_list = [line.strip('443') for line in result_list_spl]  # strip the 443 from the elements in the list
            result_list = [x.strip() for x in result_list]  # Strip whitespaces from either side of the elements in the list
            print('apps.txt', sorted(result_list))
            no_diff = result_list
    return sorted(result_list)


# Function to compare what is in HAproxy list to what is in the Repo list
def compare_list(halist,repo):
    global some_diff
    diff_list = list(set(halist) - set(repo)) # Get the differences between the two lists
    diff_list = sorted(diff_list) # Sort the list in order
    some_diff = diff_list  # Get values from diff_list into some_diff
    # print('diff', sorted(diff_list))
    return sorted(diff_list)


# Function to add the differences found in the compare function back to the list for the repo
def add_diff_to_repo(diff,github):
    global sha,final_diff
    github.extend(diff) # Add the difference from the halist to the repo list
    github = sorted(github)  # Alphabetise the final list
    github = list(filter(None, github)) # Remove empty elements from the list
    github = [s + " 443" for s in github]  # Add the 443 back to the elements in the repo list
    github = '\n'.join(github)  # Add newline after each element in the list
    print('Combine:' , github)
    print("=================================================")



    # Define Repo, owner and path
    owner = "xxxxxxx-xxxx"
    repo = "xxx-xxxx-xxxxx"
    path = "apps.txt"
    branch = "dev"



    # Token, headers and URL
    token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    url = "https://api.github.com/repos/{}/{}/contents/{}".format(owner,repo,path)
    url_pull = "https://api.github.com/repos/{}/{}/pulls".format(owner,repo)


    headers = {
        "Authorization": 'Bearer {0}'.format(token),
        "Content-Type": "application/json; charset=utf-8"
    }

    # get request to obtain the contents and information of the apps.txt file in the Github repo
    response = requests.get(url, headers=headers)
    response = json.loads(response.content.decode('utf-8'))  # Convert all data content to an object while decoding utf-8
    for key, value in response.items():
        if key == 'sha':
            sha = value    # Add value for the sha of the file to the variable named sha

    # Convert the file content to base64 for writing new content to the apps.txt file in the repo
    base64_github = base64.b64encode(github.encode('utf-8'))

    # Payload with file content and sha
    payload = {
        "branch": "dev",
        "message": "Update of apps.txt",
        "content" : base64_github.decode('utf-8'),  # Decode the file content from utf-8
        "sha"     : sha
    }
    # Payload with message and sha
    payload_del = {
        "branch": "dev",
        "message" : "Deletion of apps.txt",
        "sha"  : sha
    }

    # Payload for pull requests
    payload_request = {
        "title": "Pull Request for merge of dev branch to master due to apps.txt update",
        "body": "Update of apps.txt",
        "head": "dev",
        "base": "master"
    }

    # Payload for reviewers
    payload_reviewers ={
        "reviewers": [
            "txxxxxxxxxx",
            "fxxxxxxxxx",
            "Dxxxxxxxxxxx"
        ]
    }
    # Check if some_diff is an empty list or not
    print('some diff', some_diff)
    print('no diff', no_diff)
    if not some_diff:
        print("some_diff is empty")
        final_diff = "False" # final_diff gets the value "False"
    else:
        # Check if the lists have any elements that are different
        print("some_diff is not empty")
        for item in no_diff:
            for item1 in some_diff:
                if item == item1:
                    print(item)
                    final_diff = "False"
                else:
                    final_diff = "True"
                    break

    if final_diff == "True":
        # Delete the apps.txt file and then create it again with the updated/new content
        try:
            del_response = requests.delete(url, json=payload_del, headers=headers)
            response = requests.put(url, json=payload, headers=headers)
            pull_request = requests.post(url_pull, json=payload_request,headers=headers) # Create Pull request
            dict_resp = json.loads(pull_request.content) # Convert response from created pull request from bytes to dictionary
            for key,value in dict_resp.items(): # Get the number of the pull request
                if key == "number":
                    number = value
                    url_review = "https://api.github.com/repos/{}/{}/pulls/{}/requested_reviewers".format(owner, repo, number)
                    request_reviewers = requests.post(url_review, json=payload_reviewers, headers=headers) # Add reviewers to the existing request
                    print(request_reviewers.content)
        except:
            Errors = sys.exc_info()
            for idx, error in enumerate(Errors):
                if idx < 2:
                    print("There was an error while trying to update the apps.txt in the repo and create the pull request. Please see the error message.")
                    print(error)  # Print error
    else:
        print("No differences in the backends from HAProxy, no pull request created")
    return github


# Function to update the apps.txt file on the server
def update_hafile(repo_res):
    # Close previous ssh connection
    ssh.close()  # close previous Paramiko session
    file = '/root/xxxxxxxxxxxxx/apps.txt'
    command_mv = "cp /root/xxxxxxxxxxxx/apps.txt  /root/xxxxxxxxxxxxx/apps.bak"
    if final_diff == "True":
        # Establishing new Paramiko session for another server
        pk = r"C:\Users\xxxxxxxxxxxxx\Documents\Keys\id_rsa"
        ssh1 = paramiko.SSHClient()
        ssh1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        mykey = paramiko.RSAKey.from_private_key_file(pk)
        ssh1.connect("xx.xx.xx.xxx", username='svc-xxxxxxxxx', pkey=mykey)

        # Execute command to make backup file via Paramiko session to server
        stdin, stdout, stderr = ssh1.exec_command(command_mv)
        print(stdout)

        #Copy updated list of sites to the apps.txt file on the server
        sftp = ssh1.open_sftp()
        f = sftp.open('/root/xxxxxxxxxxxxx/apps.txt', 'w')
        f.write(repo_res)
        f.close()
        ssh1.close()
    else:
        print("No differences in the backends from HAProxy, no changes to the apps.txt files needed")

# Message for email sent to the xxxxxxxxx group
message = """From: From xxxxxxxx Team <xxxxxxxx@xxxxxxxxx.com>
To: To Person <xxxxxxxxx@xxxxxxxxx.com>
MIME-Version: 1.0
Content-type: text/html
Subject: Sites listed in Haproxy that are not in Apps.txt(Repo)

Hello Team,<br>
            &nbsp;&nbsp;&nbsp;&nbsp;These are the differences between the sites that are in HAproxy and the Apps.txt(In the Repo).<br><br>\
            <br><br>Sites that are in HAproxy but not in Apps.txt(Repo):<br> {} <br><br>\
            Regards,<br>The xxxxxxxxxx Team""".format('<br>'.join((compare_list(get_halist(),get_replist()))))


# Function to send email to the Devops group
def send_email():
    # Setting up email to/from and body
    sender = "xxxxxxxx@xxxxxxx.com"
    receivers = "xxxxxxx@xxxxxxxx.com"
    try:
        smtpObj = smtplib.SMTP('xxxxxxx.xxxxxxxx.com')
        smtpObj.sendmail(sender, receivers, message)
        print("Successfully sent email")
    except SMTPException:
        print("Error: unable to send email")


# Main which calls all the functions
def main():
    copy_haproxy_conf()
    haproxy_list = get_halist()
    github_repo_list = get_replist()
    diff_results = compare_list(haproxy_list,github_repo_list)
    repo_results = add_diff_to_repo(diff_results,github_repo_list)
    update_hafile(repo_results)
    send_email()


main()


