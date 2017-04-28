# This is a script to manipulate lists
# List comprehension was used

a_list = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]

number = int(input("Please enter a number\n"))
b_list = [num for num in a_list if num < number]
print(b_list)