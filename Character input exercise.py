# This is a script to ask someone for their name and age.
# After that it will figure out what year they will turn 100 years old
import datetime

name = input("Please give your name: ")
print("Your name is " + name)

age = int(input("Please give your age: "))
print(name + ",you said you are %i " % age + "years old.")

num = int(input(name + ",please pick a number: \n"))
print(name + ",you picked the number %i" % num + "\n")

nowDate = datetime.datetime.now()
nowYear = nowDate.year

YearsToHundred = 100 - age

YearAtHundred = YearsToHundred + nowYear
for i in range(num):
    print(name + ". In the year %i " % YearAtHundred + ",you will be 100 years old.\n")



