# This is a Python script to get the value from a list in a dictionary

cars = {"Please Choose a model": "Please choose a model",
                 "Toyota":["Rav4","4Runner","Corola","Camery"],
                 "Honda": ["Civic","Accord"],
                 "Hundai": ["Sonata","SantaFe"],
                 "Kia": ["Sorento","Stinger"],
                 "BMW": ["X3","X5"],
                 "Mercedes Benz": ["S3","S9"],
                 "Ford": ["Escort","Escape","F150"]}

pick = input("Please choose a make of car\n")

for key,value in cars.items():
    if pick and pick == key:
        pick_again = input("Please choose the model of {} that you would like\n".format(key))
        for val in value:
            if pick_again and pick_again == val:
                print("You have chosen a {} {}".format(pick,val))
