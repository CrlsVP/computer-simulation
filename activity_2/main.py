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


"""
    * Algorithm's explanation: Bresenham's integer-only line drawing algorithm:
    Assume y = mx+b represents the real variable equation of a line which is to be plotted using a
    grid of pixels where the two points (x_1, y_1) and (x_2, y_2) have integer coordinates and represent two
    known points on the line which are to be connected by drawing a simulated line segment (or segments)
    which connects them. Assume the x-pixel coordinates increase going to the right, and that the y-pixel
    coordinates increase going up. A further assumption is that:

            * m = dy/dx         such that 0 <= m <= 1
    
    This assumption insures that as we move point by point from left-to-right across the grid, y will never
    jump up by more than one pixel and that y is increasing as x is increasing. To make an accurate plot, we
    keep track of the accumulated error in the y-variable. Since the first point we plot, namely (x_1, y_1)
    is exact, the variable 'error' should be initialized with the value 0. As we move along the line from
    left-to-right, we will decide to increment y by 1 only when the accumulated y-error becomes greater than 1/2.
    The accumulated y-error is a signed real value that tracks the true error between the currently plotted y
    and the true y, for the currently plotted x. The accumulated y-error tells us how to correct the current
    y-value to get to the true y-value that we should have.

            * current_y + accumulated_y_error = true_y      so      accumulated_y_error = true_y - current_y

    Given the equation y = mx+b, note that if x is increased by 1, then y should be increased by m. If y is not
    increased at all when x is increased by 1, then the accumulated error in y should be increased by m. By the
    same token, if y is just increased by 1, without changing x at all, then the accumulated error in y should be
    decreased by 1. This approach assumes that the variables accumulated_y_error and dy and dx are all floating
    point real variables. In order to make the algorithm run at maximum speed, we avoid all decimals and
    fractions and make clever use of integer variables and values only.

"""


def draw_bres(start, end):
    # Setup initial conditions
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1
    points = []

    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)

    # Rotate line
    if (is_steep):
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    # Swap start and end points if necessary and store swap state
    swapped = False
    if (x1 > x2):
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True

    # Recalculate differentials
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    # # ! In a more efficient way we could do:
    # dx = x2 - x1
    # dy = y2 - y1

    # Calculate error
    error = 2 * (dy-dx)
    # # ! In a more efficient way we could do:
    # error = int(dx / 2.0)

    # Move forward or backwards depending on the orientation of the line
    ystep = 1 if y1 < y2 else -1

    # Iterate over bounding box generating points between start and end
    y = y1
    for x in range(x1, x2 + 1):
        # Once again, depending on the orientation of the line, the coordinates
        # would be (y, x) or (x, y)
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)

        # # ! In a more efficient way we could do:
        # error -= abs(dy)
        # if (error < 0):
        #     y += ystep
        #     error += (2 * dy)

        if (error < 0):
            #y += ystep
            error += (2 * dy)
        else:
            y += ystep
            error += ((2 * dy) - (2 * dx))

    # Reverse the list if the coordinates were swapped because of the slope
    if swapped:
        points.reverse()
    return points


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
        x += dx
        y += dy
        i = i+1
        coord.append([int(x+0.5), int(y+0.5)])
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
                    for pixel in draw_bres(line[0], line[1]):
                        paint_pixel(pixel, 0)
                        plt.pause(0.05)
                    print("Execution time of Bresenham Algorithm: {}".format(timeit.timeit(
                        stmt="draw_bres({}, {})".format(line[0], line[1]), setup="from __main__ import draw_bres", number=1)))
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
