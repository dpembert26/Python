'''
This is a Python script built to do the following:

    Visit www.corcoran.com.
    Determine the URL for one image of a property listing under the “New To Market” section of the homepage.

    Write a script(s) using bash, powershell, python, javascript, or php to do the following:
        Download/Copy the image file to a public S3 bucket
        Output the headers from the request to a text file and save the text file to an S3 bucket
        Determine if it is a cache hit or a cache miss and output the value to the screen
        Determine the value of the header titled “x-amz-cf-id“ and output it to the screen
        Paste the value of “x-amz-cf-id“ into a new text file and save it to an S3 bucket

        Author: Darin Pemberton

'''


# imports
import boto3
import wget
import sys
import os
import re
import json

created = ""
flag = ""
response = ""



# Filename and path declaration for image file that is downloaded
filename = "vestahub.jpg"
path = r"C:\Users\Darin\Pictures/"
# filename to call downloaded file(image) and full path below that
full_file_name = os.path.join(path,filename)


def create_file(file_contents):
    # File name for header.txt declared
    file_name = "header.txt"
    full_header_path = os.path.join(path,file_name)
    file = open(full_header_path, 'w')
    file.write("Header content from PUT to S3 in JSON\n")
    file.write("  \n\n")
    # Convert the dictionary to a string before we write the contents to text
    file_contents = json.dumps(file_contents)
    file.write(file_contents)
    file.close()
    return file_name, full_header_path


def check_for_header():
    # declare global variable called flag(This gets a value of yes if the header is present in the output)
    global flag
    # look for x-amz-cf-id(CloudFront) which is a header that has a value that identifies the request
    # iterating through nested dictionary
    for key, value in response.items():
        if value:
            if isinstance(value, dict):
                for key2,value2 in value.items():
                    if value2:
                        if isinstance(value2, dict):
                            for key3,value3 in value2.items():
                                if key3 == 'x-amz-request-id':
                                    print("The header {} is present in the response output with value {}".format(key3,value3))
                                    print("\n")
                                    flag = "yes"
                                    break



    if flag != "yes" and count != 1:
        print("The header is not present in the response output\n")
    return key3,value3

def remove_local_files():
    # remove files from the local drive that was created from this script or copied to the harddrive
    os.remove(full_file_name)
    os.remove(upload_header_file())
    os.remove(created[1])
    print("The files {},{} and {} has been deleted".format(full_file_name,created[1],upload_header_file()))


def upload_header_file():
    # get header key and value
    # create text file and write header to it
    file_name = "header_value.txt"
    match_header_path = os.path.join(path, file_name)
    file = open(match_header_path, 'w')
    if flag == "yes":
        file.write("The value of the header {} is  {}".format(check_for_header()[0],check_for_header()[1]))
        file.close()
    else:
        file.write("The header is not present in the response output\n")
        file.close()
    # Prepare connection to S3 bucket
    sts_client = boto3.client('sts')

    # Access temporary credentials from default profile (the user that the profile was created from assumed the role)
    role_object = sts_client.assume_role(RoleArn="arn:aws:iam::428411491348:role/darinS3",RoleSessionName="AssumeRoleSession1")
    credentials = role_object['Credentials']

    # Assign credentials from default profile
    s3_resource = boto3.resource(
        's3',
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'],
    )

    # Get s3 bucket and put files in it using https request PUT
    try:
        for bucket in s3_resource.buckets.all():
            m = re.search(r".+\(\w+='(\w+)'", str(bucket))
            # Getting the bucket name and uploading image
            bucket_name = m.group(1)
            s3_resource.Object(bucket_name, file_name).put(Body=open(match_header_path, 'rb'))
            # Creating file for the header contents
            print("The file {} was copied over to the bucket {}".format(file_name, bucket_name))
            print("\n")
    except:
        Errors = sys.exc_info()
        for idx, error in enumerate(Errors):
            if idx < 2:
                print(error)
    return match_header_path


def upload_to_s3():
    # declare global variable called created
    global created
    global response
    # Variable holding link
    coc_link = "https://mediarouting.vestahub.com/Media/93513673/box/270x406"

    # Begin download of image to local drive
    print("Downloading image file from Corcoran\n")

    # download image to local machine
    try:
        wget.download(coc_link,path + "" + filename)
        print("Download of file {} is complete".format(filename))
        print("\n")
    except:
        Errors = sys.exc_info()
        for idx,error in enumerate(Errors):
            if idx < 2:
                print(error)

    # Prepare connection to S3 bucket
    sts_client = boto3.client('sts')

    # Access temporary credentials from default profile (the user that the profile was created from assumed the role)
    role_object = sts_client.assume_role(RoleArn="arn:aws:iam::428411491348:role/darinS3", RoleSessionName="AssumeRoleSession1")
    credentials = role_object['Credentials']

    # Assign credentials from default profile
    s3_resource = boto3.resource(
        's3',
        aws_access_key_id = credentials['AccessKeyId'],
        aws_secret_access_key = credentials['SecretAccessKey'],
        aws_session_token = credentials['SessionToken'],
    )

    # Get s3 bucket and put files in it using https request PUT
    try:
        for bucket in s3_resource.buckets.all():
            m = re.search(r".+\(\w+='(\w+)'", str(bucket))
            # Getting the bucket name and uploading image
            bucket_name = m.group(1)
            response = s3_resource.Object(bucket_name,filename).put(Body=open(full_file_name, 'rb'))
            # Creating file for the header contents
            created = create_file(response)
            print("The file {} was copied over to the bucket {}".format(filename,bucket_name))
            print("\n")
            print("Writing header info to text file {}".format(created[0]))
            print("\n")
            print(response)
            print("\n")
            print("Uploading file {} with headers to the bucket {}".format(created[0], bucket_name))
            print("\n")
            file_resp = s3_resource.Object(bucket_name,created[0]).put(Body=open(created[1], 'rb'))
            print("Finished uploading file {} to bucket {}".format(created[0], bucket_name))
            print("\n")
    except:
        Errors = sys.exc_info()
        for idx,error in enumerate(Errors):
            if idx < 2:
                print(error)


def main():
    # call functions
    upload_to_s3()
    check_for_header()
    upload_header_file()
    # remove_local_files()

main()









