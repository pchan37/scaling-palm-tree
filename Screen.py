from subprocess import Popen, PIPE
from os import remove

def new_screen(width, height, COLOR):
    screen = []
    for y in xrange(height):
        row = [COLOR[:] for x in xrange(width)]
        screen.append(row)
    return screen

class Screen:

    XRES = 500
    YRES = 500
    MAX_COLOR = 255
    RED = 0
    GREEN = 1
    BLUE = 2

    DEFAULT_COLOR = [0, 0, 0]
    
    def __init__(self, width=XRES, height=YRES):
        self.screen = new_screen(width, height, self.DEFAULT_COLOR)
        self.width = width
        self.height = height
        
    def __str__(self):
        pass

    def clear(self):
        for row in xrange(len(self.screen)):
            for col in xrange(len(self.screen[row])):
                self.screen[row][col] = self.DFEAULT_COLOR[:]
    
    def plot(self, color, xcor, ycor):
        adjusted_y = self.YRES - 1 - ycor
        if (xcor >= 0 and xcor < self.XRES and adjusted_y >= 0 and adjusted_y < self.YRES):
            self.screen[adjusted_y][xcor] = color[:]

    def save(self, filename):
        ppm_filename = filename[:filename.find('.')] + '.ppm'
        ppm = 'P3\n' + str(len(self.screen[0])) + ' ' + str(len(self.screen)) + ' ' + str(self.MAX_COLOR) + '\n'
        for row in xrange(len(self.screen)):
            row_string = ''
            for col in xrange(len(self.screen[row])):
                pixel = self.screen[row][col]
                row_string += str(pixel[self.RED]) + ' '
                row_string += str(pixel[self.GREEN]) + ' '
                row_string += str(pixel[self.BLUE]) + ' '
            ppm += row_string + '\n'
        with open(ppm_filename, 'w') as file_:
            file_.write(ppm)
        if '.ppm' not in filename:
            p = Popen(['convert', ppm_filename, filename], stdin=PIPE, stdout=PIP)
            p.communicate()
            remove(ppm_filename)

    def display(self):
        ppm_filename = 'pic.ppm'
        self.save(ppm_filename)
        p = Popen(['display', ppm_filename], stdin=PIPE, stdout=PIPE)
        p.communicate()
        remove(ppm_filename)

        
def main():
    screen = Screen()
    for i in xrange(500):
        screen.plot([255, 255, 255], i, i)
    screen.display()
    

if __name__ == '__main__':
    main()
            

