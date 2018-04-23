# This is a simple Python script to show the use of classes
# Pushed to github


class Car:
    def __init__(self,model,make,color):
        self.model = model
        self.make = make
        self.color = color
        self.features = []

    def add_features(self,feature):
        self.features.append(feature)

toyota = Car("Toyota","Rav4","Silver")
audi = Car("Audi","Quatro","Black")
mercedes = Car("Mercedes Benz","C class","White")
bmw = Car("BMW","C3","Red")


toyota.add_features("Backup Camera")
audi.add_features("Heated leather seats")
mercedes.add_features("Automatic braking system")
bmw.add_features("interactive windshield console")

print("The {} {} comes in {} with a {} as an added feature".format(toyota.model,toyota.make,toyota.color,toyota.features))



