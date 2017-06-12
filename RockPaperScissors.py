# This is a game of Rock, Paper, Scissors

import random
robot = ""
pick = ""
name = ""


def get_names():
    global name
    name = input("Please enter your name: ")
    global robot
    option_list = ["rock", "paper", "scissors"]
    ran_num = random.randint(0, 2)
    robot = option_list[ran_num]
    return name


def start_game():
    start = input("{}, Would you like to start a new game?  Yes[y] or No[n] \n".format(name))
    start = start.lower()
    while start != 'y' and start != 'n' and start != 'yes' and start != 'no':
        print("{}, Please choose either Yes[y] or No[no] please! \n".format(name))
        start = input("Yes[y] or No[n]_ \n")
        start = start.lower()
    if start == 'y' or start == 'yes':
        play_game()
    else:
        print("Thanks {}, next time. Good bye \n".format(name))


def play_game():
    global pick
    pick = input("{}, Please choose: Rock[r], Paper[p] or Scissors[s] \n".format(name))
    pick = pick.lower()
    while pick != 'r' and pick != 'rock' and pick != 'p' and pick != 'paper' and pick != 's' and pick != 'scissors':
        print("{}, Please choose either Rock[r], Paper[p] or Scissors[s]_".format(name))
        pick = input("Rock[r], Paper[p] or Scissors[s]_")
        pick = pick.lower()
    if pick == 'r' or pick == 'rock':
        pick = 'rock'
    elif pick == 'p' or pick == 'paper':
        pick = 'paper'
    elif pick == 's' or pick == 'scissors':
        pick = 'scissors'
    else:
        "Do nothing for now"

    while robot == pick:
        print("{}, you and the robot chose the same thing %s \n".format(name) % pick.title())
        pick = ""
        start_game()
    if robot == "rock" and pick == "scissors" or robot == "scissors" and pick == "paper" or robot == "paper" and  \
       pick == "rock":
        print("{}, you have lost. {} beats {}! \n".format(name, robot.title(), pick.title()))
    elif robot == "":
        "Do nothing"
    else:
        print("{}, you have won. {} beats {}! \n".format(name, pick.title(), robot.title()))


def main():
    get_names()
    start_game()


main()
