


from kivy.app import App
from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty

from random import randint



FPS = 60  # <-- Constant:  Frames Per Second
LAUNCH_START_POS = (25, 25)  # <-- Constant:  Starting position for 'launch_ball()' (lower-left corner).



# App class to build the app container.
class trajectory(App):
    def build(self):
        # Create the 'display' variable to assign updates and return.
        display = screen()
        # Set 'display' framerate with constant FPS.
        Clock.schedule_interval(display.update, 1 / FPS)

        # At app initiation call launch_ball().
        display.launch_ball()

        return display



# Screen class after app class.  Contains the whole of the action of the app.
class screen(Widget):
    ball = ObjectProperty(None)

    # Function sets up primary initiating action of script, to "throw" the ball.
    def launch_ball(self):
        # Starting position of 'ball'.
        self.ball.center = LAUNCH_START_POS
        # Velocity and angle of 'launch_ball()'.
        self.ball.velocity = Vector(randint(5, 10), 0).rotate(randint(20, 85))

    def update(self, dt):
        self.ball.move()

        if (self.ball.y < 0) or (self.ball.top > self.height):

            # Apply friction at wall collision.
            self.ball.velocity_y -= self.ball.velocity_y * .2
            self.ball.velocity_x -= self.ball.velocity_x * .2

            # Reverse velocity at wall collision.
            self.ball.velocity_y *= -1

        if (self.ball.x < 0) or (self.ball.right > self.width):

            # Apply friction at wall collision.
            self.ball.velocity_y -= self.ball.velocity_y * .2
            self.ball.velocity_x -= self.ball.velocity_x * .2

            # Reverse velocity at wall collision.
            self.ball.velocity_x *= -1



class ball(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):

        #  Apply friction at all times. (air friction)
        self.velocity_x -= self.velocity_x * .005
        self.velocity_y -= self.velocity_y * .005

        self.pos = Vector(* self.velocity) + self.pos

        #  Apply gravity.
        self.velocity_y -= .2



# Call app.
if __name__ == '__main__':
    trajectory().run()
