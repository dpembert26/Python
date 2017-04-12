import turtle

numsides = 6
for steps in ["Blue","Red","Green","Orange","Black"]:
    turtle.color(steps)
    turtle.forward(90/numsides)
    turtle.right(90/numsides)
    for moresteps in ["Blue","Red","Green","Orange","Black"]:
        turtle.color(moresteps)
        turtle.forward(90/numsides)
        turtle.right(180/numsides)