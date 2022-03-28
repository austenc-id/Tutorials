from kivy.app import App
from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from random import randint

class PongPaddle(Widget):
    # player score
    score = NumericProperty(0)

    # speeds up the ball as it hits each players paddle
    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset

class PongBall(Widget):
    # defines the movement of the ball
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    # allows use of ball.velocity
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    # this will move the ball one step each time it's called
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

class PongGame(Widget):
    # allows reference to the ball
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    # define starting position and velocity
    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    # allows the game to move the ball
    def update(self, dt):
        self.ball.move()
        # bounces off paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)
        # bounces off top and bottom
        if (self.ball.y < 0) or (self.ball.top > self.height):
            self.ball.velocity_y *= -1
        # bounces off left and right
        if (self.ball.x < 0) or (self.ball.right > self.width):
            self.ball.velocity_x *= -1
        # awards a point if the ball bounces off a side
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(4,0))
        if self.ball.right > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(4,0))
    # allows the paddles to move up and down
    def on_touch_move(self, touch):
        # decides which paddle to move based on where the input was felt
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y



class PongApp(App):

    def build(self):
        # instantiate the game and move the ball 60 times/second
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game

if __name__ == '__main__':
    PongApp().run()