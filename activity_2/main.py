import matplotlib.pyplot as plt
import numpy as np
from os import system, name
import time
from matplotlib.ticker import MaxNLocator


x = []
y = []

line = {0: [], 1: []}
counter = 0


def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


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


def draw_dda(x1, y1, x2, y2):
    coord = []
    x, y = x1, y1
    length = (x2-x1) if (x2-x1) > (y2-y1) else (y2-y1)
    dx = (x2-x1)/float(length)
    dy = (y2-y1)/float(length)
    coord.append([round_dda(x), round_dda(y)])
    for _ in range(length):
        x += dx
        y += dy
        coord.append([round_dda(x), round_dda(y)])
    return(coord)


def paint_pixel(xy, opt):
    if(opt == 0):
        clr = 'red'
    else:
        clr = 'blue'
    plt.plot(xy[0]+0.5, xy[1]+0.5, marker='s', markersize=10, color=clr)
    plt.draw()


def on_click(event):
    global counter
    ix, iy = event.xdata, event.ydata
    ix = np.rint(ix) - 0.5
    iy = np.rint(iy) - 0.5
    x.append(ix)
    y.append(iy)
    plt.plot(ix, iy, marker='s', markersize=10, color='black')
    plt.draw()
    line[counter] = [int(ix-0.5), int(iy-0.5)]
    counter += 1
    if(counter == 2):
        counter = 0
        clear()
        print('Now painting with Bressenham\n')
        for pixel in draw_bress(line[0], line[1]):
            paint_pixel(pixel, 0)
            plt.pause(0.05)
        plt.pause(1)
        print('Now painting with DDA\n')
        for pixel in draw_dda(line[0][0], line[0][1], line[1][0], line[1][1]):
            paint_pixel(pixel, 1)
            plt.pause(0.05)

        line[0] = []
        line[1] = []


if __name__ == "__main__":

    fig = plt.figure(figsize=(7, 7))
    ax = fig.gca()
    plt.gca().set_aspect("equal")
    plt.title('DDA & Bressenham')
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

    fig.canvas.mpl_connect('button_press_event', on_click)

    plt.grid()
    plt.show()
