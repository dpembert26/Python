# This is a script that will check endpoints to see if they get a 500 error. If they get a 500 error, then the Caching on the CloudFront Distribution for that endpoint will set to not expire
# Author Darin Pemberton 11/9/2018

# Import modules
import urllib.request
import boto3
import sys
import time

# Variable Declarations
website = "https://xxxxxxxxx.xxxxxxxxxx.com"  # Endpoint url
username = "xxxxxxxxxxxxx"   # Endpoint username
password = "xxxxxxxxxxxxx"     # Endpoint password
key_id = 'xxxxxxxxxxxxxxxxxxxx'   # Key ID for CloudFront Distribution
secret_id = 'xxxxxxxxxxxxxxxxxxxx' # Secret ID Key for CloudFront Distribution
dist_id = 'xxxxxxxxxxxxxxxxxxxxx'

# Revert Default TTL
def revert_ttl():
    # Declare flag variable
    flag = "no"
    # Declare ETag/IfMatch variable
    IfMatch = ''
    # Supply credentials to access CloudFront distribution
    cloudfront = boto3.client('cloudfront',
                              aws_access_key_id=key_id,
                              aws_secret_access_key=secret_id)
    # Get current CloudFront Distribution configuration
    cloud_conf = cloudfront.get_distribution(Id=dist_id)

    # Get the ETag/IfMatch value
    for key1, value1 in cloud_conf.items():
        if key1 == "ETag":
            IfMatch = value1

    # extra keys = ("ResponseMetadata", "ETag" , "Distribution")
    cloud_conf["ResponseMetadata"] = cloud_conf["ETag"]  # Removing the key called "ETag"
    cloud_conf = cloud_conf["Distribution"]  # Removing the key called "Distribution"
    cloud_conf = cloud_conf["DistributionConfig"]  # Removing the key called "DistributionConfig"
    cloud_change = 86400 # Previous DefaultTTL value for the CloudFront Distribution
    cloud_change_min = 1800  # Previous MinTTL value for the CloudFront Distribution

    # Sort though nested dictionary for specific key for DefaultTTL and change its value
    for key1, value1 in cloud_conf.items():
        if value1:
            if isinstance(value1, dict):
                for key2, value2 in value1.items():
                    if key2 == "DefaultTTL":
                        if value1[key2] == 31536000:     # checking if DefaultTTL is set to 1 year
                            value1[key2] = cloud_change # Change to previous value if DefaultTTL value was set to 1 year
                            flag = "yes"  # Flag set to yes if the change was made
                    if key2 == "MinTTL":
                        if value1[key2] == 31536000:  # checking if DefaultTTL is set to 1 year
                            value1[key2] = cloud_change_min # Change to previous value if DefaultTTL value was set to 1 year
                            flag = "yes"  # Flag set to yes if the change was made

    if flag == "yes":
        # Change CloudFront cache behavior for sure
        cloud_final_result = cloudfront.update_distribution(DistributionConfig=cloud_conf, Id=dist_id,
                                                                                  IfMatch=str(IfMatch))

        print("Changing the cache behavior of the CloudFront Distribution {}".format(dist_id))
        print(type(cloud_final_result))
        print(cloud_final_result)
    else:
        print("No change to the DefaultTTL or MinTTL due to previous values of 86400 and 1800 respectively being present already")


# Update CloudFront Distribution Default TTL
def update_ttl():
    # Declare flag variable
    flag = "no"
    #Declare ETag/IfMatch variable
    IfMatch =''
    # Supply credentials to access CloudFront distribution
    cloudfront = boto3.client('cloudfront',
                              aws_access_key_id=key_id,
                              aws_secret_access_key=secret_id)
    # Get current CloudFront Distribution configuration
    cloud_conf = cloudfront.get_distribution(Id=dist_id)

    # Get the ETag/IfMatch value
    for key1, value1 in cloud_conf.items():
        if key1 == "ETag":
            IfMatch = value1

    # extra keys = ("ResponseMetadata", "ETag" , "Distribution")
    cloud_conf["ResponseMetadata"] = cloud_conf["ETag"] # Removing the key called "ETag"
    cloud_conf = cloud_conf["Distribution"] # Removing the key called "Distribution"
    cloud_conf = cloud_conf["DistributionConfig"] # Removing the key called "DistributionConfig"
    cloud_change = 31536000 # DefaultTTL value if website is down or has other problems


    # Sort though nested dictionary for specific key for DefaultTTL and change its value
    for key1,value1 in cloud_conf.items():
        if value1:
            if isinstance(value1, dict):
                for key2,value2 in value1.items():
                    if key2 == "DefaultTTL": # Check if there is a key that has a value called DefaultTTL
                        if value1[key2] == 86400:     # checking if DefaultTTL is set to 1 day
                            value1[key2] = cloud_change # Change to previous value if DefaultTTL value was set to 1 day
                            flag = "yes"  # Flag set to yes if the change was made
                    if key2 == "MinTTL": # Check if there is a key that has a value called DefaultTTL
                        if value1[key2] == 1800:     # checking if DefaultTTL is set to 1 day
                            value1[key2] = cloud_change # Change to previous value if DefaultTTL value was set to 30 mins
                            flag = "yes"

    if flag == "yes":
        # Change CloudFront cache behavior for sure
        cloud_final_result = cloudfront.update_distribution(DistributionConfig=cloud_conf, Id=dist_id, IfMatch=str(IfMatch))
        print("Changing the cache behavior of the CloudFront Distribution {}".format(dist_id))
        print(type(cloud_final_result))
        print(cloud_final_result)
    else:
        print("No change to the DefaultTTL or MinTTL due to the value of 3153600 being present already")

# Get Status Code from endpoint
def get_status():
    # Set initial loop count value
    loop_num = 0
    # Setting up password manager to handle credentials for the endpoint
    passwd_man = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    passwd_man.add_password(None, website, username, password)
    auth_handler = urllib.request.HTTPBasicAuthHandler(passwd_man)
    opener = urllib.request.build_opener(auth_handler)
    urllib.request.install_opener(opener)

    # While loop to try check a couple of times
    while loop_num < 2:
        # Get website status code
        try:
            request = urllib.request.urlopen(website).getcode()  # Checking the endpoint status
        except:
            request = 500  # Changing the request value to 500 if there is an error accessing the endpoint
            Errors = sys.exc_info()
            for idx,error in enumerate(Errors):
                if idx < 2:
                    print(error)  # Print error

        # Check endpoint status code
        if request == 500:  # If status code of endpoint is 500 then send message and also change cache behavior
            print("The website {} is down with error code {} ".format(website, request))
            update_ttl()
            time.sleep(30)
        elif request != 500 and loop_num == 1: # If status code is 200 and loop count is 1 then attempt to change caching behavior to previous value
            print("The website {} is up with error code {} ".format(website, request))
            print("The website has been consistently up for the max loop count, changing the DefaultTTL and MinTTL back to previous values")
            revert_ttl()
        else:  # If status code is 200 and the loop count is less than 1, send message and check the status again
            print("The website {} is up with error code {} ".format(website, request))
            time.sleep(30)
        # Increment loop count
        loop_num += 1



# Main function
def main():
    get_status()


main()
