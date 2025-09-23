import turtle as t

tim = t.Turtle()
tim.penup()
tim.left(90)
tim.forward(100)
tim.pendown()
tim.right(90)

# List of colors to cycle through
colors = ["red", "orange", "yellow", "green", "blue", "purple", "pink", "cyan"]


def draw_shape(num_sides, color):
    angle = 360 / num_sides
    tim.pencolor(color)  # set the outline color
    for _ in range(num_sides):
        tim.forward(100)
        tim.right(angle)


for shape_side_n in range(3, 11):
    color = colors[(shape_side_n - 3) % len(colors)]  # pick a color based on index
    draw_shape(shape_side_n, color)

screen = t.Screen()
screen.exitonclick()
