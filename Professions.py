import re
from itertools import islice
given_name = ""

name_list = ["Darin Pemberton", "Larry Johnson", "Pete Michigan"]
job_list = ["Automation Engineer", "Plumber", "Sales Executive"]
skill_list = ["B+", "A", "C"]
salary_list = ["$100,000", "$130,000", "$89,000"]


def take(n, iterable):
    # "Return first n items of the iterable as a list"
    return list(islice(iterable, n))


class Professions:
    def __init__(self, name, job, skill_rating, salary):
        self.name = name
        self.job = job
        self.skill_rating = skill_rating
        self.salary = salary

    def say_who(self):
        global given_name
        given_name = input("Please enter the full name of the person to lookup:\n")
        if given_name != self.name:
            print("The name was not found")
        else:
            print("Here is the information about {}".format(self.name))

    def print_info(self):
            print("Name: %s" % self.name)
            print("Job: %s" % self.job)
            print("Skill Rating: %s" % self.skill_rating)
            print("Salary: %s" % self.salary)
            print("\n")


def main():
    # combine multiple list into a dictionary
    person_dict = dict((i[0],list(i[1:])) for i in zip(name_list,job_list,skill_list,salary_list))
    n_list = take(1, person_dict.items()) # list of interable key/value pair from dictionary
    # print(n_list)
    person1 = Professions("Darin Pemberton", "Automation Engineer", "B", "$100,000")
    person1.say_who()
    person1.print_info()

    person2 = Professions("Larry Johnson", "Plumber", "A" , "$130,000")
    person2.say_who()
    person2.print_info()

    person3 = Professions("Pete Michigan", "Sales Executive", "C", "$89,000")
    person3.say_who()
    person3.print_info()


main()