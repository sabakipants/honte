





from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty

from random import randint



#####   CONSTANTS   #####
FPS = 60
# LAUNCH constants.
L_START_POS = (30, 30)
L_VEL_MIN, L_VEL_MAX = 5, 20
L_ROT_MIN, L_ROT_MAX = 30, 80
# PHYSICS constants.
DRAG = .005
GRAVITY = .2
ELASTICITY = .9



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



# Screen class, only child of app class.  Contains the whole of the action of the app.
class screen(Widget):
    # ball = ObjectProperty(None)

    # Function sets up primary initiating action of script, to "throw" the ball.
    def launch_ball(self):
        # Starting position of 'ball'.
        self.ball.center = L_START_POS
        # Velocity and angle of 'launch_ball()'.
        self.ball.velocity = Vector(randint(L_VEL_MIN, L_VEL_MAX), 0).rotate(randint(L_ROT_MIN, L_ROT_MAX))

    # The applications update-frame function.
    def update(self, dt):
        # Currently, only action to update is the ball moving.
        self.ball.move()



# Child of 'screen'.
class ball(Widget):
    # Globalizing ball's variables to be updated and maintained within app 'update' function.
    vel_x = NumericProperty(0)
    vel_y = NumericProperty(0)
    velocity = ReferenceListProperty(vel_x, vel_y)
    # collided = NumericProperty(0)                                                                                     #####

    def move(self):

        if self.y < 0:
            self.vel_y *= - ELASTICITY
        elif self.top > self.parent.height:
            self.vel_y *= - ELASTICITY
        else:
            self.vel_y -= self.vel_y * DRAG

        if self.x < 0:
            self.vel_x *= - ELASTICITY
        elif self.right > self.parent.width:
            self.vel_x *= - ELASTICITY
        else:
            self.vel_x -= self.vel_x * DRAG

        # if self.collided >= 1:  self.collided -= 1                                                                    #####

        # Collision detection ... Check self coordinates for intersection with designated boundaries (parent.size).  If
        # intersection is detected, reverse axis velocity and apply ELASTICITY.
        # if self.collided <= 0:                                                                                        #####
        # if self.y <= 0:
        #     self.vel_x *= ELASTICITY
        #     self.vel_y *= - ELASTICITY
        # elif self.top >= self.parent.height:
        #     self.vel_x *= ELASTICITY
        #     self.vel_y *= - ELASTICITY
        # if self.x <= 0:
        #     self.vel_x *= - ELASTICITY
        #     self.vel_y *= ELASTICITY
        # elif self.right >= self.parent.width:
        #     self.vel_x *= - ELASTICITY
        #     self.vel_y *= ELASTICITY
            # self.collided = 2                                                                                         #####

        #  Apply physics of drag and gravity, then update position with updated Vector.
        # self.vel_x -= self.vel_x * DRAG
        # self.vel_y -= self.vel_y * DRAG
        self.vel_y -= GRAVITY
        self.pos = Vector(* self.velocity) + self.pos



# Call app.
if __name__ == '__main__':
    trajectory().run()

