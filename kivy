
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector

from kivy.effects.kinetic import KineticEffect

from kivy.clock import Clock

from random import randint

class test02(App):
    def build(self):
        test = collisionTest()
        test.serve_ball()
        Clock.schedule_interval(test.update, 1 / 60)

        return test

class collisionTest(Widget):
    ball = ObjectProperty(None)

    def serve_ball(self):
        self.ball.center = (50, 50)
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

        print(self.velocity)

if __name__ == '__main__':
    test02().run()
