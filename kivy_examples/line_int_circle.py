
from math import sqrt

c_x, c_y = 0, 0
c_r = 1

p1_x, p1_y = 1, 2
p2_x, p2_y = 1, -2

a = p1_y - p2_y
b = p2_x - p1_x
c = p1_x * p2_y - p2_x * p1_y

dist = ( abs(a * c_x + b * c_y + c) / sqrt(a * a + b * b) )

if c_r >= dist:  print("intersecting")
else:  print("nope")
