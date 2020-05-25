def calc_parabola_vertex(x1, y1, x2, y2, x3, y3):
	y1 = 480 - y1
	y2 = 480 - y2
	y3 = 480 - y3
	denom = (x1-x2) * (x1-x3) * (x2-x3);
	A = (x3 * (y2-y1) + x2 * (y1-y3) + x1 * (y3-y2)) / denom;
	B = (x3*x3 * (y1-y2) + x2*x2 * (y3-y1) + x1*x1 * (y2-y3)) / denom;
	C = (x2 * x3 * (x2-x3) * y1+x3 * x1 * (x3-x1) * y2+x1 * x2 * (x1-x2) * y3) / denom;

	return A,B,C

a, b, c = calc_parabola_vertex(631, 266, 575, 261, 507, 298)

y_value = (a * 442 * 442) + (b * 442) + c
print(480 - y_value)

#(631, 266)
#(631, 266)
#(575, 261)
#(575, 261)
#(507, 298)
#(442, 372)
#(442, 372)