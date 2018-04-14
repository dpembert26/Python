# This is a simple Python script to show the use of classes
# Pushed to github

from tkinter import *

OPTIONS = ["Toyota","Honda","Mazda","Hundai","Kia","BMW","Mercedes Benz","Ford"]

master = Tk()
variable = StringVar(master)
variable.set(OPTIONS[0]) # default value

w = OptionMenu (master, variable,  *OPTIONS)
w.pack()


def ok():
    print("You chose a " + variable.get())
    master.quit()

button = Button(master, text="OK", command=ok)
button.pack()


mainloop()







