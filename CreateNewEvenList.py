# This is a script that takes a list of numbers and creates a new one with only even numbers from the original

a = [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
b = [num for num in a if num % 2 == 0]
print(b)