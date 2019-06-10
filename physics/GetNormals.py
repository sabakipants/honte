
from kivy.vector import Vector

p1, p2, p3 = Vector(+1, +1), Vector(+1, +2), Vector(+2, +3)
p4, p5, p6 = Vector(+3, +3), Vector(+4, +2), Vector(+4, +1)
poly = [p1, p2, p3, p4, p5, p6]



def getPtNorm(leg_1, origin, leg_2):
	"""
	input:	leg_1 =	The right leg of the origin point on the polygon.
		origin = The point the function is getting the normal for.
		leg_2 =	The left leg of the origin point on the polygon.
	output:	Return the Vector normal of the 'origin' with respects to 'leg_1' and 'leg_2'.  The
		normal is the point used to express the reflection orientation of the 'origin'.  It is
		used to determine the trajectory of an object after collision.
	"""
	# Get the angle from the 'origin' point between 'leg_1' and 'leg_2'.
	legs_dif = Vector(leg_2 - origin).angle(leg_1 - origin)
	# Get the global angle of 'leg_1' from 'origin'.
	leg_angle = Vector(1, 0).angle(leg_1 - origin)
	# With 'legs_dif' and 'leg_angle' get the global angle of the 'origin' normal.
	norm_angle = - (leg_angle - (legs_dif / 2)) + 180

	return Vector(1, 0).rotate(norm_angle) + origin
	


####################################################################################################   \/   UNDER CONSTRUCTION   \/   #####
"""
NEED TO ...

Function 'getPtNorm()' works correctly.  Function 'getNormals()' does not.  The reshaping of the
'poly' list seems to work correctly.  'getNormals()' seems to work for some points but not all.
It looks like the hang up is near the beginning or end of the point list.  But not sure.  Still
needs work.
"""

# print(getPtNorm(p5, p6, p1))
# exit()
	
# print(poly, "\n")
# print(p1, "normal =", getPtNorm(p3, p1, p2))
	
# print(p1)
# print(getPtNorm(p3, p1, p2))
# print(p2)
# print(p2, "normal =", getPtNorm(p1, p2, p3))
# print(p3)
# print(p3, "normal =", getPtNorm(p2, p3, p1))

def getNormals(poly_points):
	points = poly_points.copy()
	points.insert(0, points[len(points) - 1])
	points.append(points[1])
	
	# print(poly_points)
	# print(points)
	# exit()
	
	normals = []
	for p in points:
		i = points.index(p)
		if i == 0 or i == len(points) - 1:  continue
		normals.append(getPtNorm(points[i - 1],p ,points[i + 1]))

	return normals

# print(poly)
# print(getNormals(poly))

normals = getNormals(poly)

for each in range(len(poly)):
	print(poly[each], "=", normals[each])

####################################################################################################   /\   UNDER CONSTRUCTION   /\   #####
