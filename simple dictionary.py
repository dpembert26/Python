states = {"NY":"New York","CO":"Colorado","CT":"Connecticut","TX":"Texas"}

for key,value in states.items():
    print("%s is the abbreviation for the state of %s" % (key,value))

print("These are the state abbreviations: ")
for key,value in states.items():
    print(key)

print("These are the states proper names: ")
for key,value in states.items():
    print(value)

