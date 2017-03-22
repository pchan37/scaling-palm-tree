from __future__ import division
from math import cos, pi, sin

from display import *
from matrix import *
from utils import check_for_valid_args

@check_for_valid_args
def add_circle( points, cx, cy, cz, r, step ):
    start_x = r + cx
    start_y = cy
    add_point(points, start_x, start_y)
    interval = 1 / step
    t = interval
    while t < 1:
        theta = 2 * pi * t
        x = r * cos(theta) + cx
        y = r * sin(theta) + cy
        add_point(points, x, y)
        add_point(points, x, y)
        t += interval
    add_point(points, start_x, start_y)

@check_for_valid_args
def add_curve( points, x0, y0, x1, y1, x2, y2, x3, y3, step, curve_type ):
    if curve_type == "hermite":
        x_coefficient = generate_curve_coefs(x0, x1, x2, x3, "hermite")[0]
        y_coefficient = generate_curve_coefs(y0, y1, y2, y3, "hermite")[0]
    else:
        x_coefficient = generate_curve_coefs(x0, x1, x2, x3, "bezier")[0]
        y_coefficient = generate_curve_coefs(y0, y1, y2, y3, "bezier")[0]

    add_point(points, x_coefficient[3], y_coefficient[3])
    t = interval = 1 / step
    while t < 1:
        x = x_coefficient[0] * (t ** 3) + x_coefficient[1] * (t ** 2) + x_coefficient[2] * t + x_coefficient[3]
        y = y_coefficient[0] * (t ** 3) + y_coefficient[1] * (t ** 2) + y_coefficient[2] * t + y_coefficient[3]
        add_point(points, x, y)
        add_point(points, x, y)
        t += interval
    add_point(points, sum(x_coefficient), sum(y_coefficient))


def draw_lines( matrix, screen, color ):
    if len(matrix) < 2:
        print 'Need at least 2 points to draw'
        return
    
    point = 0
    while point < len(matrix) - 1:
        draw_line( int(matrix[point][0]),
                   int(matrix[point][1]),
                   int(matrix[point+1][0]),
                   int(matrix[point+1][1]),
                   screen, color)    
        point+= 2
        
def add_edge( matrix, x0, y0, z0, x1, y1, z1 ):
    add_point(matrix, x0, y0, z0)
    add_point(matrix, x1, y1, z1)
    
def add_point( matrix, x, y, z=0 ):
    matrix.append( [x, y, z, 1] )
    



def draw_line( x0, y0, x1, y1, screen, color ):

    #swap points if going right -> left
    if x0 > x1:
        xt = x0
        yt = y0
        x0 = x1
        y0 = y1
        x1 = xt
        y1 = yt

    x = x0
    y = y0
    A = 2 * (y1 - y0)
    B = -2 * (x1 - x0)

    #octants 1 and 8
    if ( abs(x1-x0) >= abs(y1 - y0) ):

        #octant 1
        if A > 0:            
            d = A + B/2

            while x < x1:
                plot(screen, color, x, y)
                if d > 0:
                    y+= 1
                    d+= B
                x+= 1
                d+= A
            #end octant 1 while
            plot(screen, color, x1, y1)
        #end octant 1

        #octant 8
        else:
            d = A - B/2

            while x < x1:
                plot(screen, color, x, y)
                if d < 0:
                    y-= 1
                    d-= B
                x+= 1
                d+= A
            #end octant 8 while
            plot(screen, color, x1, y1)
        #end octant 8
    #end octants 1 and 8

    #octants 2 and 7
    else:
        #octant 2
        if A > 0:
            d = A/2 + B

            while y < y1:
                plot(screen, color, x, y)
                if d < 0:
                    x+= 1
                    d+= A
                y+= 1
                d+= B
            #end octant 2 while
            plot(screen, color, x1, y1)
        #end octant 2

        #octant 7
        else:
            d = A/2 - B;

            while y > y1:
                plot(screen, color, x, y)
                if d > 0:
                    x+= 1
                    d+= A
                y-= 1
                d-= B
            #end octant 7 while
            plot(screen, color, x1, y1)
        #end octant 7
    #end octants 2 and 7
#end draw_line
