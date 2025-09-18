from turtle import Turtle, Screen

tim = Turtle()
tim.shape("turtle")
tim.color("purple")


jon = Turtle()
jon.shape("turtle")
jon.color("yellow")

tom = Turtle()
tom.shape("turtle")
tom.color("red")

tony = Turtle()
tony.shape("turtle")
tony.color("blue")

for _ in range(4):
    tony.right(90)
    tony.forward(100)


tom.left(90)
for _ in range(3):
    tom.forward(100)
    tom.right(90)

tom.forward(100)
for _ in range(4):
    jon.left(90)
    jon.forward(100)

for _ in range(4):
    tim.forward(100)
    tim.right(90)


screen = Screen()
screen.exitonclick()
