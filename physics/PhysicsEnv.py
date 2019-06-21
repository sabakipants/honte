


#####   \/   NOTES   \/   ##########################################################################



"""
Currently working on:
Need to convert hardcoded velocity adjustments to functions in PhysicsLib library.
"""



#####   \/   IMPORTS   \/   ########################################################################



from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.vector import Vector

from random import randint
from math import hypot

import PhysicsLib



#####   \/   CONSTANTS   \/   ######################################################################



# RENDER constants.
FPS = 60
# LAUNCH constants.
L_START_POS = (30, 30)
L_VEL_MIN, L_VEL_MAX = 20, 40
L_ROT_MIN, L_ROT_MAX = 20, 70
# PHYSICS constants.
DRAG = 0.01
GRAVITY = 0.3
ELASTICITY = 0.9



#####   \/   CLASS (PhysicsEnv)   \/   #############################################################



class PhysicsEnv(App):  # App container.
    def build(self):
        # Build child 'window' from class 'Window'.
        window = Window()
        window.build()
        # Set 'window' framerate with constant FPS.
        Clock.schedule_interval(window.render, 1 / FPS)
        # At app initiation call 'launchBall()'.
        window.launchBall()

        return window



#####   \/   CLASS (Window)   \/   #################################################################



class Window(Widget):  # Only child of 'PhysicsEnv'.
    def build(self):  # Self 'build()' contains children 'build()' as well.
        self.obstacle.build()

    # Function sets up primary initiating action of script, to "throw" the ball.
    def launchBall(self):
        # Starting position of 'ball'.
        self.ball.center = L_START_POS
        # Velocity and angle of 'launchBall()'.
        vel = randint(L_VEL_MIN, L_VEL_MAX)
        # vel = 20
        rot = randint(L_ROT_MIN, L_ROT_MAX)
        # rot = 50
        self.ball.velocity = Vector(vel, 0).rotate(rot)

    # The applications update-frame function.
    def render(self, dt):
        # Currently, only action to update is the ball moving.
        self.ball.move(self.obstacle)



#####   \/   CLASS (Obstacle)   \/   ###############################################################



class Obstacle(Widget):  # Child of 'Window'.
    # Create variables for building 'points' list.
    ob_x, ob_y = NumericProperty(0), NumericProperty(0)
    ob_right, ob_top = NumericProperty(0), NumericProperty(0)
    p1 = ReferenceListProperty(ob_x, ob_y)
    p2 = ReferenceListProperty(ob_x, ob_top)
    p3 = ReferenceListProperty(ob_right, ob_top)
    p4 = ReferenceListProperty(ob_right, ob_y)
    points = ReferenceListProperty(p1, p2, p3, p4)
    # Create variables for building 'normals' list.
    n1x, n1y = NumericProperty(0), NumericProperty(0)
    n2x, n2y = NumericProperty(0), NumericProperty(0)
    n3x, n3y = NumericProperty(0), NumericProperty(0)
    n4x, n4y = NumericProperty(0), NumericProperty(0)
    n1 = ReferenceListProperty(n1x, n1y)
    n2 = ReferenceListProperty(n2x, n2y)
    n3 = ReferenceListProperty(n3x, n3y)
    n4 = ReferenceListProperty(n4x, n4y)
    normals = ReferenceListProperty(n1, n2, n3, n4)
    # Create variables for 'edges' list.
    e1 = ReferenceListProperty(p1, p2)
    e2 = ReferenceListProperty(p2, p3)
    e3 = ReferenceListProperty(p3, p4)
    e4 = ReferenceListProperty(p4, p1)
    edges = ReferenceListProperty(e1, e2, e3, e4)
    # Create variables for 'legs' list.
    l1 = ReferenceListProperty(e4, e1)
    l2 = ReferenceListProperty(e1, e2)
    l3 = ReferenceListProperty(e2, e3)
    l4 = ReferenceListProperty(e3, e4)
    legs = ReferenceListProperty(l1, l2, l3, l4)

    def build(self):
        # Build 'points' list.
        self.ob_x, self.ob_y = self.x, self.y
        self.ob_right, self.ob_top = self.right, self.top
        # Build 'normals' list.
        self.n1x, self.n1y = PhysicsLib.getPtNorm(self.p4, self.p1, self.p2)
        self.n2x, self.n2y = PhysicsLib.getPtNorm(self.p1, self.p2, self.p3)
        self.n3x, self.n3y = PhysicsLib.getPtNorm(self.p2, self.p3, self.p4)
        self.n4x, self.n4y = PhysicsLib.getPtNorm(self.p3, self.p4, self.p1)



#####   \/   CLASS (Ball)   \/   ###################################################################



class Ball(Widget):  # Child of 'Window'.
    # Globalizing ball's variables to be updated and maintained within app 'update' function.
    vel_x, vel_y = NumericProperty(0), NumericProperty(0)
    velocity = ReferenceListProperty(vel_x, vel_y)

    def windowCol(self):
        # Have to use absolute values ('abs()') of velocities to avoid "sticky" collisions.

        # Check for collision with floor.
        if self.y < 0:                        self.vel_y = abs(self.vel_y) * ELASTICITY
        # Check for collision with ceiling.
        elif self.top > self.parent.height:   self.vel_y = - abs(self.vel_y) * ELASTICITY
        # If no collisions, update position without affecting velocity direction and apply gravity.
        else:                                 self.vel_y -= (self.vel_y * DRAG) + GRAVITY
        # Check for collision with left wall.
        if self.x < 0:                        self.vel_x = abs(self.vel_x) * ELASTICITY
        # Check for collision with right wall.
        elif self.right > self.parent.width:  self.vel_x = - abs(self.vel_x) * ELASTICITY
        # If no collision then update position without affecting velocity direction.
        else:                                 self.vel_x -= self.vel_x * DRAG

        # Update position by applying new velocity with Vector.
        self.pos = Vector(self.velocity) + self.pos










#####   \/   UNDER CONSTRUCTION   \/   #############################################################

    """
    Still need to convert hardcoded modifications to self.velocity as a result of detected
    collisions, to functions in PhysicsLib library.
    """

    def move(self, obstacle):

        self.windowCol()

        # Perform 'pointCol()' on each point from 'obstacle'.
        for i, p in enumerate(obstacle.points):
            cx, cy, cr = self.center[0], self.center[1], self.size[0] / 2
            if PhysicsLib.pointCol(cx, cy, cr, p[0], p[1]):
                # If collision is detected...

                for l in obstacle.legs[i]:
                    lp1, lp2 = l
                    lp1x, lp1y = lp1
                    lp2x, lp2y = lp2
                    if PhysicsLib.edgeProj(cx, cy, lp1x, lp1y, lp2x, lp2y):
                        """ perform 'edgeCol()' on 'l' """
                        vel_ang = (Vector(1, 0).angle(Vector(self.velocity)))                       # NEED TO WRITE PHYSICS FUNCTION FOR BLOCK...
                        # if vel_ang < 0:  vel_ang = abs(vel_ang) + 180                             #
                        print("vel_ang", vel_ang)                                                   #
                        edge_ang = (Vector(1, 0).angle(Vector(lp2) - Vector(lp1)))                  #
                        print("edge_ang", edge_ang)                                                 #
                        # dif = (Vector(p2) - Vector(p)).angle(Vector(self.velocity))               #
                        dif = (edge_ang - vel_ang)                                                  #
                        print("dif", dif)                                                           #
                        # dif = edge_ang - vel_ang                                                  #
                        refl = dif * 2                                                              #
                        if dif < 0:  self.velocity = Vector(self.velocity).rotate(-refl)            #
                        else:  self.velocity = Vector(self.velocity).rotate(refl)                   # ...

                        return

                # Get angle from origin 'ball.center' and points 'ball.velocity' and point          # NEED TO WRITE PHYSICS FUNCTION FOR BLOCK...
                # collided with.                                                                    #
                dif = (Vector(p) - Vector(self.center)).angle(Vector(self.velocity))                #
                # Get angle of reflection point.  It is the angle to be added to current velocity   #
                # angle to get new trajectory.                                                      #
                refl = (90 - abs(dif)) * 2                                                          #
                # Handle two possible scenarios differently:  If angle from collision point to      #
                # velocity is negative, then reflection is positive.  If angle from collision point #
                # to velocity is positive, then reflection is negative.                             #
                if dif < 0:  self.velocity = Vector(self.velocity).rotate(refl)                     #
                else:  self.velocity = Vector(self.velocity).rotate(-refl)                          # ...

                return  # New velocity determined.  Proceed to next frame.

        for i, e in enumerate(obstacle.edges):
            cx, cy, cr = self.center[0], self.center[1], self.size[0] / 2
            p1, p2 = e
            p1x, p1y = p1
            p2x, p2y = p2

            if PhysicsLib.edgeCol(cx, cy, cr, p1x, p1y, p2x, p2y):
                vel_ang = (Vector(1, 0).angle(Vector(self.velocity)))                               # NEED TO WRITE PHYSICS FUNCTION FOR BLOCK...
                # if vel_ang < 0:  vel_ang = abs(vel_ang) + 180                                     #
                print("vel_ang", vel_ang)                                                           #
                edge_ang = (Vector(1, 0).angle(Vector(p2) - Vector(p1)))                            #
                print("edge_ang", edge_ang)                                                         #
                # dif = (Vector(p2) - Vector(p)).angle(Vector(self.velocity))                       #
                dif = (edge_ang - vel_ang)                                                          #
                print("dif", dif)                                                                   #
                # dif = edge_ang - vel_ang                                                          #
                refl = dif * 2                                                                      #
                if dif < 0:  self.velocity = Vector(self.velocity).rotate(-refl)                    #
                else:  self.velocity = Vector(self.velocity).rotate(refl)                           # ...

                return

#####   /\   UNDER CONSTRUCTION   /\   #############################################################










#####   \/   CALL APP   \/   #######################################################################



if __name__ == '__main__':  PhysicsEnv().run()
