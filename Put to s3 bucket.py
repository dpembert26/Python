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


# Function to create full paths for files
def create_full_paths(dir,file):
    try:
        full_path = os.path.join(dir,file)
        return full_path
    except:
        Errors = sys.exc_info()
        for idx, error in enumerate(Errors):
            if idx < 2:
                print(error)

# Filename/url and path declaration for all files
image_name = "vestahub.jpg"
dir_path = r"C:\Users\Darin\Pictures/"
# filename to call downloaded file(image)
coc_link = "https://mediarouting.vestahub.com/Media/93513673/box/270x406"
# File name for header.txt declared
file_name = "header.txt"
# Create full path for image file
full_image_path = create_full_paths(dir_path,image_name)
# Create full path for header.txt file
full_text_path = create_full_paths(dir_path,file_name)


# Function to download image file to local machine
def download_to_local(link,file,path):
    # Begin download of image to local drive
    print("Downloading image file from Corcoran\n")

    # download image to local machine
    try:
        wget.download(link, path + "" + file)
        print("Download of file {} is complete".format(file))
        print("\n")
    except:
        Errors = sys.exc_info()
        for idx, error in enumerate(Errors):
            if idx < 2:
                print(error)


# Function that creates and write content to header.txt file on local machine
def create_file(file_contents,path):
    try:
        # File name for header.txt declare
        file = open(path, 'w')
        file.write("Header content from PUT to S3 in JSON\n")
        file.write("  \n\n")
        # Convert the dictionary to a string before we write the contents to text
        file_contents = json.dumps(file_contents)
        file.write(file_contents)
        file.close()
    except:
        Errors = sys.exc_info()
        for idx, error in enumerate(Errors):
            if idx < 2:
                print(error)


# Function to upload files to s3 bucket
def upload_to_s3(file_path,file):
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
            response = s3_resource.Object(bucket_name,file).put(Body=open(file_path, 'rb'))
            print("The file {} was copied over to the bucket {}".format(file,bucket_name))
            print("\n")
    except:
        Errors = sys.exc_info()
        for idx,error in enumerate(Errors):
            if idx < 2:
                print(error)
    return response


def check_for_header(file_contents):
    # declare global variable called flag(This gets a value of yes if the header is present in the output)
    global flag
    # look for x-amz-cf-id(CloudFront) which is a header that has a value that identifies the request
    # iterating through nested dictionary
    for key, value in file_contents.items():
        if value:
            if isinstance(value, dict):
                for key3,value3 in value.items():
                    if key3 == 'x-amz-request-id':
                        print("Key: %s " % key3 % "  Value: %s" % value3 )
                        print("The header {} is present in the response output with value {}".format(key3,value3))
                        print("\n")
                        flag = "yes"
                        break

        if flag != "yes":
            print("The header is not present in the response output\n")


def main():
    # call functions

    # Download image file to local machine
    download_to_local(coc_link,image_name,dir_path)

    # Upload image file to s3
    response_json =  upload_to_s3(full_image_path,image_name)

    # Create and write content to header.txt
    create_file(response_json,full_text_path)

    # Upload header.txt to s3
    upload_to_s3(full_text_path,file_name)


main()