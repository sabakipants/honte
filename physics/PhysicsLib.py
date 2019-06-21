


####################################################################################################
"""
A library for game-play physics generation.
"""
####################################################################################################
 
from kivy.vector import Vector



def getPtNorm(leg_1, origin, leg_2):
	"""
	input:	leg_1 =	 The right leg of the origin point on the polygon.
	    origin = The point the function is getting the normal for.
			leg_2 =	 The left leg of the origin point on the polygon.
	output:	Return the Vector normal of the 'origin' with respects to 'leg_1' and 'leg_2'.
			The normal is the point used to express the reflection orientation of the
			'origin'.  It is used to determine the trajectory of an object after collision.
	"""
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
	"""
	input:	poly_pts = List of Vectors as coordinates representing a polygon.
	output:	Return list of Vectors that are normals for coordinates in input list of
			Vectors.
	"""
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



def pointCol(cx, cy, cr, px, py):
	"""
	Return bool of whether circle (represented with arguments 'cx', 'cy', and 'cr') collides with
	point (represented with arguments 'px' and 'py'.)
	"""
	return Vector(cx, cy).distance(Vector(px, py)) <= cr



def edgeProj(cx, cy, p1x, p1y, p2x, p2y, edge_col=False):
	"""
	Return bool of whether circle's center (represented with arguments 'cx' and 'cy') is within a
	perpendicular projection of line segment (represented with arguments 'p1x', 'p1y', 'p2x', and
	'p2y'.  'edge_col' is default argument so function will return 'package' of values if called
	by 'edgeCol()'.)
	"""
	# Get 'length' of line segment.  Then, get 'dot_prod' (needed to determine circles projected
	# points on line).  Then designate 'proj_x' and 'proj_y' as coordinates circle's projected point
	# on line.
	length = Vector(p1x, p1y).distance(Vector(p2x, p2y))
	dot_prod = (((cx - p1x) * (p2x - p1x)) + ((cy - p1y) * (p2y - p1y))) / length ** 2
	proj_x = p1x + (dot_prod * (p2x - p1x))
	proj_y = p1y + (dot_prod * (p2y - p1y))

	# The projected point of 'proj_x' and 'proj_y' is the projected point on the ABSOLUTE line.
	# Next is to determine if the projected point is actually on the given line segment.  This is
	# done by comparing the length of the line segment to the length of the distance between the
	# projected point and the two endpoints.
	proj_to_p1 = Vector(p1x, p1y).distance(Vector(proj_x, proj_y))
	proj_to_p2 = Vector(p2x, p2y).distance(Vector(proj_x, proj_y))

	# When called from 'edgeCol()', return pre-calculated variables.
	if edge_col:  return (proj_x, proj_y, length == proj_to_p1 + proj_to_p2)

	# If projected point is on line segment, return True, if not, return False.
	if proj_to_p1 + proj_to_p2 == length:  return True
	else:  return False



def edgeCol(cx, cy, cr, p1x, p1y, p2x, p2y):
	"""
	Return True if circle (represented with arguments 'cx', 'cy', and 'cr') collides with line
	segment (represented with arguments 'p1x', 'p1y', 'p2x', and 'p2y').
	"""

	# Get calculations from 'edgeProj()'.
	package = edgeProj(cx, cy, p1x, p1y, p2x, p2y, edge_col=True)

	# Third value from 'package' is bool determining if circle is inside edge projection.
	if not package[2]:  return False

	# Measure distance between projected point and circle's coordinates.  If it is less than the
	# circle's radius, then return True, else return False.
	if Vector(cx, cy).distance(Vector(package[0], package[1])) <= cr:  return True
	else: return False
