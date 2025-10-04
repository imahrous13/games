import pandas as pd
import turtle

screen = turtle.Screen()
screen.title("U.S. States Game")
image = "day25/us-states-game/blank_states_img.gif"
screen.addshape(image)

turtle.shape(image)
# Getting X and Y values
# def get_mouse_click_coor(x, y):
#     print(x, y)
# turtle.onscreenclick(get_mouse_click_coor)
# turtle.mainloop()
data = pd.read_csv("day25/us-states-game/50_states.csv")
all_state = data.state.tolist()
guessed_states = []

while len(guessed_states) < 50:
    answer_state = screen.textinput(
        title=f"{len(guessed_states)}/ 50 Guess the State",
        prompt="what's another state's name?",
    ).title()
    if answer_state == "Exit":
        missing_states = []
        for state in all_state:
            if state not in guessed_states:
                missing_states.append(state)
        new_data = pd.DataFrame(missing_states)
        new_data.to_csv("day25/us-states-game/states to learn.csv")
        break
    if answer_state in all_state:
        guessed_states.append(answer_state)
        t = turtle.Turtle()
        t.hideturtle()
        t.penup()
        state_data = data[data.state == answer_state]
        t.goto(state_data.x.item(), state_data.y.item())
        t.write(answer_state)
print(missing_states)
