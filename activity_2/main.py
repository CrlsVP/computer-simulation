from matplotlib.ticker import MaxNLocator
from os import system, name
import matplotlib.pyplot as plt
import numpy as np
import time
import timeit

x = []
y = []

line = {0: [], 1: []}
counter = 0
is_painting = False


def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def paint_pixel(xy, opt):
    if(opt == 0):
        clr = 'red'
    else:
        clr = 'blue'
    plt.plot(xy[0]+0.5, xy[1]+0.5, marker='s', markersize=10, color=clr)
    plt.draw()


def draw_bress(start, end):
    # Setup initial conditions
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1

    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)

    # Rotate line
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    # Swap start and end points if necessary and store swap state
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True

    # Recalculate differentials
    dx = x2 - x1
    dy = y2 - y1

    # Calculate error
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1

    # Iterate over bounding box generating points between start and end
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx

    # Reverse the list if the coordinates were swapped
    if swapped:
        points.reverse()
    return points


def round_dda(a):
    return int(a + 0.5)


def draw_dda(start, end):
    coord = [start]
    x0, y0 = start
    x1, y1 = end

    dx = x1 - x0
    dy = y1 - y0

    if(abs(dx) >= abs(dy)):
        steps = abs(dx)
    else:
        steps = abs(dy)

    dx = dx/steps
    dy = dy/steps

    x = x0
    y = y0

    i = 1
    while(i <= steps):
        #putpixel(x, y, RED);
        x += dx
        y += dy
        i = i+1
        coord.append([round_dda(x), round_dda(y)])
    return(coord)


def on_click(event):
    global counter
    global is_painting
    if not(is_painting):
        ix, iy = event.xdata, event.ydata

        if(ix == None or iy == None):
            plt.close()
            create_grid()
            # pass
        else:
            # * Get the coordinates of the grid and substract the diff;
            # * the grid is divided by .5 ticks, and the clicks
            # * retrieve real numbers, so:
            ix = int(ix) + 0.5
            iy = int(iy) + 0.5

            plt.plot(ix, iy, marker='s', markersize=10, color='black')
            plt.draw()

            # Add points to the line
            line[counter] = [int(ix), int(iy)]

            counter += 1
            if(counter == 2):
                counter = 0
                if(line[0] == line[1]):
                    print('That is just a dot!\n')
                else:
                    clear()
                    is_painting = True
                    plt.pause(1)
                    # Bresenham's
                    print('Now painting with Bresenham')
                    for pixel in draw_bress(line[0], line[1]):
                        paint_pixel(pixel, 0)
                        plt.pause(0.05)
                    print("Execution time of Bresenham Algorithm: {}".format(timeit.timeit(
                        stmt="draw_bress({}, {})".format(line[0], line[1]), setup="from __main__ import draw_bress", number=1)))
                    plt.pause(1)
                    print('\n--------------------------------------\n')
                    # DDA
                    print('Now painting with DDA')
                    for pixel in draw_dda(line[0], line[1]):
                        paint_pixel(pixel, 1)
                        plt.pause(0.05)
                    print("Execution time of DDA Algorithm: {}".format(timeit.timeit(
                        stmt="draw_dda({}, {})".format(line[0], line[1]), setup="from __main__ import draw_dda", number=1)))
                    # Restart the line
                    line[0] = []
                    line[1] = []
                    is_painting = False


def create_grid():
    fig = plt.figure(figsize=(7, 7))

    ax = fig.gca()
    plt.gca().set_aspect("equal")
    plt.title('DDA & Bressenham\n(for cleaning the grid, just click outside)')
    ax.set(xlim=(0, 30), ylim=(0, 30))  # arbitrary data
    ax.yaxis.set_major_locator(MaxNLocator(nbins=30, integer=True))
    ax.xaxis.set_major_locator(MaxNLocator(
        nbins=30, integer=True))    # ax.plot(x)

    ax.set_xticklabels('')
    ax.set_yticklabels('')
    ax.set_xticks(np.arange(0, 30, 0.5), minor=True)
    ax.set_yticks(np.arange(0, 30, 0.5), minor=True)
    ax.set_xticklabels(np.arange(1, 31), minor=True, fontsize=6)
    ax.set_yticklabels(np.arange(1, 31), minor=True, fontsize=6)
    ax.tick_params(axis=u'both', which=u'both', length=0)

    plt.grid()
    fig.canvas.mpl_connect('button_press_event', on_click)
    plt.show()


if __name__ == "__main__":
    #fig = plt.figure(figsize=(7, 7))
    create_grid()
    #fig.canvas.mpl_connect('button_press_event', on_click)
    # plt.show()
