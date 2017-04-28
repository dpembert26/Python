# This is a script that ask for a number and then print all divisors

number = int(input("Please enter a number\n"))


a_list = [num for num in range(1, number + 1) if number % num == 0]
print(a_list)