import turtle

screen = turtle.Screen()
screen.bgcolor("black")
screen.setup(width = 800,height = 600)
screen.title("ESCAPE THE MAZE")
# screen.tracer(0)
#ball = Ball()

ring = turtle.Turtle()
ring.color("white")
ring.pensize(4)
ring.hideturtle()
clr = ["red","green","blue","yellow","pink","pink"]
ring.speed(0)
for i in range(6):
    if i<=3:
        ring.circle(30*i,315)
    elif i==4:
        ring.circle(30*i,330)
    elif i==5:
        ring.circle(30*i,340)
    ring.up()
    ring.color(clr[i])
    ring.goto(-30*i,0)
    ring.setheading(270)
    ring.down()
    
screen.exitonclick()