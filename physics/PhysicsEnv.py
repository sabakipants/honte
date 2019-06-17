
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.properties import NumericProperty, ReferenceListProperty

from random import randint
from math import hypot





#####   CONSTANTS   #####
# RENDER constants.
FPS = 60
# LAUNCH constants.
L_START_POS = (30, 30)
L_VEL_MIN, L_VEL_MAX = 10, 30
L_ROT_MIN, L_ROT_MAX = 30, 80
# PHYSICS constants.
DRAG = 0.01
GRAVITY = 0.2
ELASTICITY = 0.9





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





class Window(Widget):  # Only child of 'PhysicsEnv'.
	def build(self):  # Self 'build()' contains children 'build()' as well.
		self.obstacle.build()

	# Function sets up primary initiating action of script, to "throw" the ball.
	def launchBall(self):
		# Starting position of 'ball'.
		self.ball.center = L_START_POS
		# Velocity and angle of 'launchBall()'.
		vel = randint(L_VEL_MIN, L_VEL_MAX)
		vel = 100
		rot = randint(L_ROT_MIN, L_ROT_MAX)
		rot = 55
		self.ball.velocity = Vector(vel, 0).rotate(rot)

	# The applications update-frame function.
	def render(self, dt):
		# Currently, only action to update is the ball moving.
		self.ball.move(self.obstacle)
		




class Obstacle(Widget):  # Child of 'Window'.
	# Globalizing 'Obstacle's variables for use inside 'Window'.  'p1', 'p2', 'p3', and 'p4' are
	# corners of 'Obstacle' to be collision points and used to build collision edges.
	ob_x, ob_y = NumericProperty(0), NumericProperty(0)
	ob_right, ob_top = NumericProperty(0), NumericProperty(0)
	p1 = ReferenceListProperty(ob_x, ob_y)
	p2 = ReferenceListProperty(ob_x, ob_top)
	p3 = ReferenceListProperty(ob_right, ob_top)
	p4 = ReferenceListProperty(ob_right, ob_y)
	# Reference list to pass through App.
	points = ReferenceListProperty(p1, p2, p3, p4)
	
	# Variables for normals.																		### Have not established glitch
	n1x, n1y = NumericProperty(0), NumericProperty(0)												#	avoidance with normals yet.
	n2x, n2y = NumericProperty(0), NumericProperty(0)												#	So, currently not using these,
	n3x, n3y = NumericProperty(0), NumericProperty(0)												#	but will in the future.
	n4x, n4y = NumericProperty(0), NumericProperty(0)
	n1 = ReferenceListProperty(n1x, n1y)
	n2 = ReferenceListProperty(n2x, n2y)
	n3 = ReferenceListProperty(n3x, n3y)
	n4 = ReferenceListProperty(n4x, n4y)
	normals = ReferenceListProperty(n1, n2, n3, n4)
	
	# Set positional variables.
	def build(self):
		self.ob_x, self.ob_y = self.x, self.y
		self.ob_right, self.ob_top = self.right, self.top
		
		
		
		"""																							### Again, not using these normals
		def getPtNorm(leg_1, origin, leg_2):														#	functions but will in the future.
			""""""
			input:	leg_1 =	 The right leg of the origin point on the polygon.
					origin = The point the function is getting the normal for.
					leg_2 =	 The left leg of the origin point on the polygon.
			output:	Return the Vector normal of the 'origin' with respects to 'leg_1' and 'leg_2'.
					The normal is the point used to express the reflection orientation of the
					'origin'.  It is used to determine the trajectory of an object after collision.
			""""""
			leg_1 = Vector(leg_1)
			origin = Vector(origin)
			leg_2 = Vector(leg_2)
			
			acute = False  # Working variable for when 'origin' is an internal corner.
			
			# Get the angle from the 'origin' point between 'leg_1' and 'leg_2'.
			legs_dif = Vector(leg_2 - origin).angle(leg_1 - origin)
			if legs_dif < 0:  acute = True  # Detect internal corner and label as 'acute'.
			
			# Get the global angle of 'leg_1' from 'origin'.
			leg_angle = Vector(1, 0).angle(leg_1 - origin)
			
			# With 'legs_dif' and 'leg_angle' get the global angle of the 'origin' normal.
			norm_angle = - (leg_angle - (legs_dif / 2)) + 180
			if acute:  norm_angle += 180  # Adjust norm_angle for internal corner.

			# Return an extension of 1 unit from 'origin' by calculated angle 'norm_angle'.
			return Vector(1, 0).rotate(norm_angle) + origin

		def getNormals(poly_pts):
			""""""
			input:	poly_pts = List of Vectors as coordinates representing a polygon.
			output:	Return list of Vectors that are normals for coordinates in input list of
					Vectors.
			""""""
			normals = []  # Initiate return variable.

			# Get new list of points, extending beginning of list with 'last' item and extending end
			# of list with 'first' item.
			points = poly_pts[:]
			first, last = points[0], points[len(points) - 1]
			points.insert(0, last), points.append(first)
			
			# Convert point type to 'Vector'.
			for index, point in enumerate(points):  points[index] = Vector(point)
			
			# With extended 'points', loop through and calculate normals with 'getPtNorm()'.
			for index, point in enumerate(points):
				# Do not get normal for first or last item in extended 'points' list.
				if index == 0 or index == len(points) - 1:  continue
				
				# Get normal with 'getPtNorm()' from list of 'points'.  Because 'points' is a list
				# of coordinates representing a polygon in clockwise positional order, to get the
				# previous and next point of polygon just 'index - 1' and 'index + 1'.
				normal = getPtNorm(points[index - 1], point, points[index + 1])
				normals.append(normal)

			return normals
		
		self.n1x, self.n1y = getPtNorm(self.p4, self.p1, self.p2)
		self.n2x, self.n2y = getPtNorm(self.p1, self.p2, self.p3)
		self.n3x, self.n3y = getPtNorm(self.p2, self.p3, self.p4)
		self.n4x, self.n4y = getPtNorm(self.p3, self.p4, self.p1)
		
		# normals = getNormals(self.points)
		# print(normals)
		"""





class Ball(Widget):  # Child of 'Window'.
	# Globalizing ball's variables to be updated and maintained within app 'update' function.
	vel_x, vel_y = NumericProperty(0), NumericProperty(0)
	velocity = ReferenceListProperty(vel_x, vel_y)

	def windowCol(self):
		# Have to use absolute values ('abs()') of velocities to avoid "sticky" collisions.

		# Check for collision with floor.
		if self.y < 0:							self.vel_y = abs(self.vel_y) * ELASTICITY
		# Check for collision with ceiling.
		elif self.top > self.parent.height:	self.vel_y = - abs(self.vel_y) * ELASTICITY
		# If no collisions, update position without affecting velocity direction and apply gravity.
		else:									self.vel_y -= (self.vel_y * DRAG) + GRAVITY
		# Check for collision with left wall.
		if self.x < 0:							self.vel_x = abs(self.vel_x) * ELASTICITY
		# Check for collision with right wall.
		elif self.right > self.parent.width:	self.vel_x = - abs(self.vel_x) * ELASTICITY
		# If no collision then update position without affecting velocity direction.
		else:									self.vel_x -= self.vel_x * DRAG

		# Update position by applying new velocity with Vector.
		self.pos = Vector(self.velocity) + self.pos

		
		
"""   \/   UNDER CONSTRUCTION   \/   """
	"""
	These are working functions for collision with corners of 'obstacle'.  Still need to integrate
	functions for collision with sides of 'obstacle'.  Also, need to integrate normals to avoid
	glitch phasing and sticking.
	"""

	def pointCol(self, cx, cy, cr, px, py):  return hypot(cx - px, cy - py) <= cr

	def move(self, obstacle):
		self.windowCol()
		# Perform 'pointCol()' on each point from 'obstacle'.
		for p in obstacle.points:
			if self.pointCol(self.center[0], self.center[1], self.size[0] / 2, p[0], p[1]):
				# If collision is detected...
				
				# Get angle from origin 'ball.center' and points 'ball.velocity' and point
				# collided with.
				dif = (Vector(p) - Vector(self.center)).angle(Vector(self.velocity))
				# Get angle of reflection point.  It is the angle to be added to current velocity
				# angle to get new trajectory.
				refl = (90 - abs(dif)) * 2

				# Handle two possible scenarios differently:  If angle from collision point to
				# velocity is negative, then reflection is positive.  If angle from collision point
				# to velocity is positive, then reflection is negative.
				if dif < 0:  self.velocity = Vector(self.velocity).rotate(refl)
				else:  self.velocity = Vector(self.velocity).rotate(-refl)

"""   /\   UNDER CONSTRUCTION   /\   """





# Call app.
if __name__ == '__main__': PhysicsEnv().run()
