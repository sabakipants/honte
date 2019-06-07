


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
L_VEL_MIN, L_VEL_MAX = 10, 30
L_ROT_MIN, L_ROT_MAX = 30, 80
# PHYSICS constants.
DRAG = 0.01
GRAVITY = 0.2
ELASTICITY = 0.9



# App class to build the app container.
class PhysicsEnv(App):
    def build(self):
        # Build child 'window' from class 'Window'.
        window = Window()
        window.build()
        # Set 'window' framerate with constant FPS.
        Clock.schedule_interval(window.update, 1 / FPS)
        # At app initiation call launchBall().
        window.launchBall()

        return window



# Window class, only child of app class.  Contains the whole of the action of the app.
class Window(Widget):
    # Build self and children.
    def build(self):
        self.obstacle.build()

    # Function sets up primary initiating action of script, to "throw" the ball.
    def launchBall(self):
        # Starting position of 'ball'.
        self.ball.center = L_START_POS
        # Velocity and angle of 'launchBall()'.
        vel = randint(L_VEL_MIN, L_VEL_MAX)
        rot = randint(L_ROT_MIN, L_ROT_MAX)
        self.ball.velocity = Vector(vel, 0).rotate(rot)

    # The applications update-frame function.
    def update(self, dt):
        # Currently, only action to update is the ball moving.
        self.ball.move()

        # print(self.obstacle.p4, self.obstacle.p3)
        # print(self.obstacle.p1, self.obstacle.p2)


# Child of 'Window'.
class Obstacle(Widget):
    # Globalizing 'Obstacle's variables for use inside 'Window'.  'p1', 'p2', 'p3', and 'p4' are
    # corners of 'Obstacle' to be collision points and used to build collision edges.
    ob_x, ob_y = NumericProperty(0), NumericProperty(0)
    ob_right, ob_top = NumericProperty(0), NumericProperty(0)
    p1 = ReferenceListProperty(ob_x, ob_y)
    p2 = ReferenceListProperty(ob_right, ob_y)
    p3 = ReferenceListProperty(ob_right, ob_top)
    p4 = ReferenceListProperty(ob_x, ob_top)
    # Set positional variables.
    def build(self):
        self.ob_x, self.ob_y = self.x, self.y
        self.ob_right, self.ob_top = self.right, self.top



# Child of 'Window'.
class Ball(Widget):
    # Globalizing ball's variables to be updated and maintained within app 'update' function.
    vel_x, vel_y = NumericProperty(0), NumericProperty(0)
    velocity = ReferenceListProperty(vel_x, vel_y)

    def move(self):
        # ... COLLISION DETECTIONS ... Have to use absolute values ('abs()') of velocities to avoid
        #                          ... "sticky" collisions.

        # Check for collision with floor.
        if self.y < 0:                       self.vel_y = abs(self.vel_y) * ELASTICITY
        # Check for collision with ceiling.
        elif self.top > self.parent.height:  self.vel_y = - abs(self.vel_y) * ELASTICITY
        # If no collisions, update position without affecting velocity direction and apply gravity.
        else:                                self.vel_y = self.vel_y - (self.vel_y * DRAG) - GRAVITY

        # Check for collision with left wall.
        if self.x < 0:                       self.vel_x = abs(self.vel_x) * ELASTICITY
        # Check for collision with right wall.
        elif self.right > self.parent.width: self.vel_x = - abs(self.vel_x) * ELASTICITY
        # If no collision then update position without affecting velocity direction.
        else:                                self.vel_x -= self.vel_x * DRAG

        # Update position by applying new velocity with Vector.
        self.pos = Vector(* self.velocity) + self.pos

        # print(self.center, " ... ", self.velocity)



# Call app.
if __name__ == '__main__':  PhysicsEnv().run()
