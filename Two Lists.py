# This script will take two lists and find the elements in common between them

a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
b = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

same_array = []
# remove duplicates from each list
a = set(a)
b = set(b)

for i in b:
    if i in a:
        same_array.append(i)
print(same_array)

