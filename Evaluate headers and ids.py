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

filename = "vestahub.jpg"
path = r"C:\Users\Darin\Pictures/"


def create_file(file_contents):
    file_name = "header.txt"
    full_header_path = os.path.join(path,file_name)
    file = open(full_header_path, "w")
    file.write("Header content from PUT to S3 in JSON\n\n")
    file.write("  \n\n")
    # Convert the dictionary to a string before we write the contents to text
    file_contents = json.dumps(file_contents)
    file.write(file_contents)
    file.close()
    return file_name, full_header_path


def upload_to_s3():
    # Variable holding link
    coc_link = "https://mediarouting.vestahub.com/Media/93513673/box/270x406"

    # Begin download of image to local drive
    print("Downloading image file from Corcoran")

    # filename to call downloaded file(image) and full path below that

    full_file_name = os.path.join(path,filename)

    try:
        wget.download(coc_link,path + "" + filename)
        print("Download of file {} is complete".format(filename))
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
            bucket_name = m.group(1)
            response = s3_resource.Object(bucket_name,full_file_name).put(Body=open(full_file_name, 'rb'))
            # Creating file for the header contents
            created = create_file(response)
            print("The file {} was copied over to the bucket {}".format(filename,bucket_name))
            print("Writing header info to text file {}".format(created[0]))
            print(response)
            print("Uploading file {} to the bucket {}".format(created[0], bucket_name))
            file_resp = s3_resource.Object(bucket_name,created[1]).put(Body=open(created[1], 'rb'))
            print("Finished uploading file {} to bucket {}".format(created[0], bucket_name))
    except:
        Errors = sys.exc_info()
        for idx,error in enumerate(Errors):
            if idx < 2:
                print(error)


def main():
    upload_to_s3()


main()







'''
# Get s3 bucket and put file in it using s3 client method
try:
    for bucket in s3_resource.buckets.all():
        m = re.search(r".+\(\w+='(\w+)'", str(bucket))
        bucket_name = m.group(1)
        data = open(full_file_name,  'rb')
        s3 = boto3.client('s3')
        s3.put_object(Bucket=bucket_name, Key=full_file_name, Body=data)
        print("The file {} was copied to the bucket {}".format(filename, bucket_name))
except:
    Errors = sys.exc_info()
    for idx,error in enumerate(Errors):
        if idx < 2:
            print(error)
'''

