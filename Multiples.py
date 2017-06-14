# This is a script that will look at multiples of 3 or 5 for numbers less than 10. Those are 3,5,6,9. These add up to 23
# Then the script will do the same thing for numbers less than 1000 and find the sum

total = 0
total_list = []
for num in range(1, 1000):
    if num % 3 == 0 or num % 5 == 0:
        total_list.append(num)
        total += num
print(total)
print(total_list)