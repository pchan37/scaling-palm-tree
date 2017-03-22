from display import *
from matrix import *
from draw import *

"""
Goes through the file named filename and performs all of the actions listed in that file.
The file follows the following format:
     Every command is a single character that takes up a line
     Any command that requires arguments must have those arguments in the second line.
     The commands are as follows:
         line: add a line to the edge matrix - 
	    takes 6 arguemnts (x0, y0, z0, x1, y1, z1)
	 ident: set the transform matrix to the identity matrix - 
	 scale: create a scale matrix, 
	    then multiply the transform matrix by the scale matrix - 
	    takes 3 arguments (sx, sy, sz)
	 translate: create a translation matrix, 
	    then multiply the transform matrix by the translation matrix - 
	    takes 3 arguments (tx, ty, tz)
	 rotate: create a rotation matrix,
	    then multiply the transform matrix by the rotation matrix -
	    takes 2 arguments (axis, theta) axis should be x, y or z
	 yrotate: create an y-axis rotation matrix,w
	    then multiply the transform matrix by the rotation matrix -
	    takes 1 argument (theta)
	 zrotate: create an z-axis rotation matrix,
	    then multiply the transform matrix by the rotation matrix -
	    takes 1 argument (theta)
	 apply: apply the current transformation matrix to the 
	    edge matrix
	 display: draw the lines of the edge matrix to the screen
	    display the screen
	 save: draw the lines of the edge matrix to the screen
	    save the screen to a file -
	    takes 1 argument (file name)
	 quit: end parsing

See the file script for an example of the file format
"""

def valid_num_of_args(line_num, args, expected_number_of_args):
    if len(args) != expected_number_of_args:
        # Add one more to index + 1 because of zero-based index
        print 'Line ' + str(line_num + 2) + ' has ' + str(len(args)) + ' arguments, expecting ' + str(expected_number_of_args) + '...'
        raise SystemExit(1)
    return True
        
def parse_file( fname, points, transform, screen, color ):
    one_liners = {'ident': ident, 'apply': matrix_mult, 'display': display}
    two_liners = {'line': add_edge, 'scale': make_scale, 'move': make_translate, 'rotate': 'make_rot', 'save': save_extension, 'circle': add_circle, 'hermite': add_curve, 'bezier': add_curve}
    with open(fname) as file_:
        file_content = file_.readlines()
    for line_num, line in enumerate(file_content):
        line = line.strip()
        if not line:
            raise SystemExit(0)
        if line[0].isdigit() or file_content[line_num - 1].strip() == 'rotate' or file_content[line_num - 1].strip() == 'save':
            continue
        if line in one_liners:
            if line == 'ident':
                one_liners[line](transform)
            elif line == 'apply':
                one_liners[line](transform, points)
            else:
                clear_screen(screen)
                draw_lines(points, screen, color)
                one_liners[line](screen)
        elif line in two_liners:
            if line == 'line':
                next_line = file_content[line_num + 1].strip()
                args = next_line.split(' ')
                if valid_num_of_args(line_num, args, 6):
                    two_liners[line](points, args[0], args[1], args[2], args[3], args[4], args[5], line_num=line_num)
            elif line == 'scale':
                next_line = file_content[line_num + 1].strip()
                args = next_line.split(' ')
                if valid_num_of_args(line_num, args, 3):
                    scale_matrix = two_liners[line](args[0], args[1], args[2], line_num=line_num)
                    matrix_mult(scale_matrix, transform)
            elif line == 'move':
                next_line = file_content[line_num + 1].strip()
                args = next_line.split(' ')
                if valid_num_of_args(line_num, args, 3):
                    translate_matrix = two_liners[line](args[0], args[1], args[2], line_num=line_num)
                    matrix_mult(translate_matrix, transform)
            elif line == 'rotate':
                next_line = file_content[line_num + 1].strip()
                args = next_line.split(' ')
                if valid_num_of_args(line_num, args, 2):
                    if args[0] in 'xyzXYZ':
                        function = eval(two_liners[line] + args[0].upper())
                    else:
                        print 'Line ' + str(line_num + 2) + ' provided an invalid axis...'
                        raise SystemExit(1)                    
                    rotate_matrix = function(args[1], line_num=line_num)
                    matrix_mult(rotate_matrix, transform)
            elif line == 'save':
                next_line = file_content[line_num + 1].strip()
                args = next_line.split(' ')
                if valid_num_of_args(line_num, args, 1):
                    clear_screen(screen)
                    draw_lines(points, screen, color)
                    display(screen)
                    if args[0].endswith('.png'):
                        two_liners[line](screen, args[0])
                    else:
                        print 'Invalid filename at line ' + str(line_num + 2)
                        raise SystemExit(1)
            elif line == 'circle':
                next_line = file_content[line_num + 1].strip()
                args = next_line.split(' ')
                if valid_num_of_args(line_num, args, 4):
                    two_liners[line](points, args[0], args[1], args[2], args[3], 100, line_num=line_num)
            elif line == 'hermite' or line == 'bezier':
                next_line = file_content[line_num + 1].strip()
                args = next_line.split(' ')
                if valid_num_of_args(line_num, args, 8):
                    two_liners[line](points, args[0], args[1], args[2], args[3], args[4], args[5], args[6],
                                     args[7], 100, line, line_num=line_num, expected_number_of_args=8)
        else:
            print 'Invalid command found at line ' + str(line_num)
            raise SystemExit(1)
