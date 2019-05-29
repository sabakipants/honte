


"""
circle_int_line.py

Return True if any point within designated circle is on designated line segment.  Accept 7
arguments:  coordinates of circle, radius of circle, and coordinates of both endpoints of line
segment.

First determine if either endpoint is inside circle, if so return True.  Then designate closest
point of circle on extended line.  Check if closest point is on line, if not return False.  If so,
do final check and see if distance of from circle's coordinates to closest point on line is less
than circle's radius.  If so, return True.

- last updated 2019-05-29 by David Lang
"""



from math import hypot

# Circle variables.
circ_x, circ_y = 0, 0
radius = 1

# Line segment variables.
p1_x, p1_y = 1, 10
p2_x, p2_y = 1, -10



"""
Note...  The function 'cornerCol()' is used because of it's need for future development.  Vector
reflection from object bounce will be different if the object is colliding with a corner.
"""

def cornerCol(cx, cy, cr, px, py):
    """
    Return True if distance between ('cx', 'cy') and ('px', 'py') is less than 'cr'.
    """
    return hypot(cx - px, cy - py) <= cr



def circleLineSegCol(cx, cy, cr, p1x, p1y, p2x, p2y):
    """
    Return True if circle (represented with arguments 'cx', 'cy', and 'cr') collides with line
    segment (represented with arguments 'p1x', 'p1y', 'p2x', and 'p2y').
    """
    # First, use 'cornerCol()' to determine if endpoints of line segment collide with circle.  if
    # so, return True, else continue.
    if cornerCol(cx, cy, cr, p1x, p1y) or cornerCol(cx, cy, cr, p2x, p2y):  return True

    # Get 'length' of line segment.
    length = hypot(p2x - p1x, p2y - p1y)

    # First, get 'dot_prod' (needed to determine circles projected points on line).  Then designate
    # 'proj_x' and 'proj_y' as coordinates circle's projected point on line.
    dot_prod = (((cx - p1x) * (p2x - p1x)) + ((cy - p1y) * (p2y - p1y))) / length ** 2
    proj_x = p1x + (dot_prod * (p2x - p1x))
    proj_y = p1y + (dot_prod * (p2y - p1y))

    # The projected point of 'proj_x' and 'proj_y' is the projected point on the ABSOLUTE line.
    # Next is to determine if the projected point is actually on the given line segment.  This is
    # done by comparing the length of the line segment to the length of the distance between the
    # projected point and the two endpoints.  If projected point is on line segment, continue, if
    # not, return False.
    proj_to_p1 = hypot(proj_x - p1x, proj_y - p1y)
    proj_to_p2 = hypot(proj_x - p2x, proj_y - p2y)
    if not proj_to_p1 + proj_to_p2 == length:  return False

    # Measure distance between projected point and circle's coordinates.  If it is less than the
    # circle's radius, then return True, else return False.
    if hypot(proj_x - cx, proj_y - cy) <= cr:  return True
    else:  return False



print(circleLineSegCol(circ_x, circ_y, radius, p1_x, p1_y, p2_x, p2_y))
