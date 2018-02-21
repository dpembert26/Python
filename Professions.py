given_name = ""
person = []


class Professions:
    def __init__(self, name, job, skill_rating, salary):
        self.name = name
        self.job = job
        self.skill_rating = skill_rating
        self.salary = salary

    def say_who(self):
        print("Here is the information about {}".format(self.name))
        

    def print_info(self):
            print("Name: %s" % self.name)
            print("Job: %s" % self.job)
            print("Skill Rating: %s" % self.skill_rating)
            print("Salary: %s" % self.salary)
            print("\n")


def main():

    person.append(Professions("Darin Pemberton","Automation Engineer", "B+", "$100,000"))
    person.append(Professions("Larry Johnson", "Plumber", "A", "$130,000"))
    person.append(Professions("Pete Michigan","Sales Executive", "B", "$89,000"))

    for p_list in person:
        p_list.say_who()
        p_list.print_info()


main()