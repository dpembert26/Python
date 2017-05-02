# This is a script to check for strings that are the same when read backwards and forwards

string_name = input("Please enter a string\n")

string_reverse = string_name[:: -1]

if string_reverse == string_name[0:] :
    print("This string is a palindrome")
else:
    print("This string is not a palindrome")