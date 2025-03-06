import turtle
import time
screen = turtle.Screen()
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.title("ESCAPE THE MAZE")


ring = turtle.Turtle()
ring.color("white")
ring.pensize(4)
ring.hideturtle()
ring.speed(0)
ring.color("red")
ring.circle(30)


slit = turtle.Turtle()
slit.color("black")
slit.pensize(7)
slit.hideturtle()
slit.speed(0)  


def move_slit():

    slit.circle(30, 10)
    slit.clear()
    slit.circle(30, 30)
while True:
    time.sleep(0.3)
    move_slit()


screen.exitonclick()