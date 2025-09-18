import turtle

timmy = turtle.Turtle()

print(timmy)
timmy.shape("turtle")
timmy.color("yellow")
timmy.shapesize(5, 5, 5)
timmy.forward(250)


my_screen = turtle.Screen()
print(my_screen.canvheight)
my_screen.exitonclick()
