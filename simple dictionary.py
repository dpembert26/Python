states = {"NY":"New York","CO":"Colorado","CT":"Connecticut","TX":"Texas"}

for key,value in states.items():
    print("%s is the abbreviation for the state of %s" % (key,value))

print("\nThese are the state abbreviations: ")
for key,value in states.items():
    print(key)

print("\nThese are the states proper names: ")
for key,value in states.items():
    print(value)

print("\nAdding another state to the states dictionary")
states["Other States"] = ["Georgia","Virginia","Hawaii","Florida"]
print(states)

print("\nPrint out all the other states")
for key in states["Other States"]:
    print(key)