import sys
class Animals:

    def __init__(self,kind,name,sound):
        self.kind = kind
        self.name = name
        self.sound = sound


    def getName(self):
        print("The %s" % self.kind + "'s name is %s " % self.name)

    def getSound(self):
        print("The %s" % self.kind + " " + self.sound + "s")

    def setName(self,new_name):
        global flag
        if new_name :
            self.name = new_name
            flag = 'true'
            return self.name
        else :
            print("The variable is not defined")
            flag = 'false'


def main():
    cat = Animals("cat", "Tabby", "Meow")
    dog = Animals("dog", "Ralph", "Woof")
    lion = Animals("lion","Leo", "Roar")


    lion.getSound()
    lion.setName("")
    if flag == 'true':
        lion.getName()
    else :
        print("Please insert a variable for the function setName")
main()



