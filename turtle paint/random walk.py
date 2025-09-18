import turtle as t
import random

# colors = ["red", "orange", "yellow", "green", "blue", "purple", "pink", "cyan"]
directions = [0, 90, 180, 270]

tim = t.Turtle()
t.colormode(255)
tim.pensize(10)
tim.speed("fastest")


def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    random_color = (r, g, b)
    return random_color


for _ in range(200):
    tim.color(random_color())  # random.choice(colors)
    tim.forward(30)
    tim.setheading(random.choice(directions))

screen = t.Screen()
screen.exitonclick()
