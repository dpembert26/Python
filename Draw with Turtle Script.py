import turtle

numsides = 6
for steps in ["Blue","Red","Green","Orange","Black"]:
    turtle.color(steps)
    turtle.forward(360/numsides)
    turtle.right(360/numsides)
    for moresteps in ["Blue","Red","Green","Orange","Black"]:
        turtle.color(moresteps)
        turtle.forward(180/numsides)
        turtle.right(360/numsides)