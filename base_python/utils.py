from functools import wraps
from math import pi

def check_for_valid_args(function):
    @wraps(function)
    def inner(*args, **kwargs):
        try:
            startIndex = 1 if type(args[0]) == list else 0
            num_of_args = kwargs.get('expected_number_of_args')
            endIndex = num_of_args + 1 if num_of_args else len(args)
            additional_args = args[endIndex:] if len(args) > endIndex else []
            args = ([args[0]] if startIndex else []) + [float(arg) for arg in args[startIndex:endIndex]]
            args += additional_args
            return function(*args)
        except ValueError:
            line_num = kwargs.get('line_num')
            if line_num != None:
                print 'Line ' + str(line_num + 2)  +' contains non-numerical values...'
            else:
                print 'Non-numerical values found in arguments, pass line_num for more information'
                print 'Ex: function(arg1, arg2, arg3, ..., line_num=<current_line>)'
                print 'Note: current_line begins at 0 (the start of the script)'
            raise SystemExit(1)
    return inner
                
def deg_to_radians(function):
    @wraps(function)
    def convert(degree_measure):
        return function((pi / 180) * degree_measure)
    return convert
