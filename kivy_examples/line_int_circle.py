

from math import sqrt, hypot

cx, cy = 0, 0.1
r = 1.1

x1, y1 = 1, 0
x2, y2 = 1.0001, 10

a = y1 - y2
b = x2 - x1
c = x1 * y2 - x2 * y1



# Check for collision with points first.
dist_p1 = hypot(cx - x1, cy - y1)
dist_p2 = hypot(cx - x2, cy - y2)
col_endpoints = (dist_p1 <= r) or (dist_p1 <= r)

distX = x1 - x2
distY = y1 - y2
len = sqrt( ( distX * distX ) + ( distY * distY ) )

dot = ( ( ( cx - x1 ) * ( x2 - x1 ) ) + ( ( cy - y1 ) * ( y2 - y1 ) ) ) / ( len ** 2 )

# 'closest_x' and 'closest_y' determine the closest point on the given line (not line segment, as if
# the given line continued on forever beyond the given points).
closest_x = x1 + ( dot * ( x2 - x1 ) )
closest_y = y1 + ( dot * ( y2 - y1 ) )

line_len = hypot(x2 - x1, y2 - y1)
dist_close_p1 = hypot(closest_x - x1, closest_y - y1)
dist_close_p2 = hypot(closest_x - x2, closest_y - y2)

# 'closest_on_line' is a boolean that returns whether the point ('closest_x', 'closest_y') is on the
# line of the given points.
closest_on_line = line_len == dist_close_p1 + dist_close_p2

###   IF 'closest_on_line' RETURNS FALSE, PROCEDURE CAN STOP.  NO FURTHER COMPUTATIONS NEEDED TO
###   DETERMINE IF CIRCLE COLLIDES WITH LINE SEGMENT.

dist_x = closest_x - cx
dist_y = closest_y - cy
distance = sqrt( ( dist_x * dist_x ) + ( dist_y * dist_y ) )

collision = closest_on_line and (distance <= r)

print("collision at endpoints        =", col_endpoints)
print("dot is on line segment        =", closest_on_line)
print("collision w/ line rel/ to dot =", collision)

