# This is a script where the user is asked for a number.
# Depending on if the number is odd or even, an answer will be given

num = int(input("Please enter a number \n"))
check = int(input("Please enter another number \n"))

if num % check == 0:
    print("{} divides evenly into {} ".format(num,check))
else:
    print("{} does not divide evenly into {}".format(num,check))