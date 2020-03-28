from matplotlib.ticker import MaxNLocator
from os import system, name
import matplotlib.pyplot as plt
import numpy as np
import time
import timeit
import math
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
    plt.plot(xy[0]+0.5, xy[1]+0.5, marker='s', markersize=10, color=opt)
    plt.draw()


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
                    radius = calculateDistance(line[0], line[1])
                    # DDA without octets
                    print('Now painting with DDA (without octets)')
                    #draw_dda(line[0][0], line[0][1], radius)
                    # print("Execution time of DDA Algorithm without octets: {}".format(timeit.timeit(
                    #     stmt="draw_dda({}, {}, {})".format(line[0], line[1], radius), setup="from __main__ import draw_dda", number=1)))
                    plt.pause(1)
                    print('\n--------------------------------------\n')
                    # DDA without octets
                    print('Now painting with DDA')
                    draw_dda_oct(line[0][0], line[0][1], radius)
                    plt.pause(1)
                    print('\n--------------------------------------\n')
                    # DDA
                    print('Now painting with Bresenham')
                    #draw_bres(line[0][0], line[0][1], radius)
                    # print("Execution time of Bresenham Algorithm: {}".format(timeit.timeit(
                    #     stmt="draw_bres({}, {}, {})".format(line[0], line[1], radius), setup="from __main__ import draw_bres", number=1)))
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


def draw_octets(x_c, y_c, x, y, color):
    paint_pixel([x_c+x, y_c+y], color)
    plt.pause(0.03)
    paint_pixel([x_c-x, y_c+y], color)
    plt.pause(0.03)
    paint_pixel([x_c+x, y_c-y], color)
    plt.pause(0.03)
    paint_pixel([x_c-x, y_c-y], color)
    plt.pause(0.03)
    paint_pixel([x_c+y, y_c+x], color)
    plt.pause(0.03)
    paint_pixel([x_c-y, y_c+x], color)
    plt.pause(0.03)
    paint_pixel([x_c+y, y_c-x], color)
    plt.pause(0.03)
    paint_pixel([x_c-y, y_c-x], color)
    plt.pause(0.03)


def calculateDistance(xy_i, xy_f):
    dist = math.sqrt((xy_f[0] - xy_i[0])**2 + (xy_f[1] - xy_i[1])**2)
    return dist


def draw_dda(x_c, y_c, r):
    x_k = 0
    y_k = int(math.sqrt((r*r) - (x_k * x_k)))

    # Upper Circle
    paint_pixel([x_c+x_k, y_c+y_k], 'red')
    paint_pixel([x_c-x_k, y_c+y_k], 'red')

    # Lower Circle
    paint_pixel([x_c+x_k, y_c-y_k], 'red')
    paint_pixel([x_c-x_k, y_c-y_k], 'red')
    plt.pause(0.03)
    while(y_k > 0):
        x_k += 1
        y_k = round(math.sqrt((r*r) - (x_k * x_k)))

        # Upper Circle
        paint_pixel([x_c+x_k, y_c+y_k], 'red')
        paint_pixel([x_c-x_k, y_c+y_k], 'red')

        # Lower Circle
        paint_pixel([x_c+x_k, y_c-y_k], 'red')
        paint_pixel([x_c-x_k, y_c-y_k], 'red')

        plt.pause(0.03)

    y_k = 0
    x_k = int(math.sqrt((r*r) - (y_k * y_k)))
    while(x_k > 0):
        y_k += 1
        x_k = round(math.sqrt((r*r) - (y_k * y_k)))

        # Upper Circle
        paint_pixel([x_c+x_k, y_c+y_k], 'pink')
        paint_pixel([x_c-x_k, y_c+y_k], 'pink')

        # Lower Circle
        paint_pixel([x_c+x_k, y_c-y_k], 'pink')
        paint_pixel([x_c-x_k, y_c-y_k], 'pink')

        plt.pause(0.03)


def draw_dda_oct(x_c, y_c, r):
    coord = []
    x_k = 0
    y_k = int(math.sqrt((r*r) - (x_k * x_k)))

    #draw_octets(x_c, y_c, x_k, y_k, 'blue')
    coord.append([x_k, y_k])
    while(y_k > x_k):
        x_k += 1
        y_k = round(math.sqrt((r*r) - (x_k * x_k)))
        coord.append([x_k, y_k])
        #draw_octets(x_c, y_c, x_k, y_k, 'blue')

    return(coord)


def draw_bres(x_c, y_c, r):
    coord = []
    x = 0
    y = round(r)
    p = 3 - (2 * r)

    coord.append([x, y])
    #draw_octets(x_c, y_c, x, y, 'yellow')
    while (x <= y):
        if (p <= 0):
            p += (4 * x) + 6
        else:
            p += (4 * x) - (4 * y) + 10
            y -= 1
        x += 1
        coord.append([x, y])
        # draw_octets(x_c, y_c, x, y, 'yellow')


def epsilon(r):
    i = 1
    while(r > pow(2, i)):
        i += 1
    return pow(2, -i)


def draw_dda_eps(x_c, y_c, r):
    eps = epsilon(r)

    x_k = r
    y_k = 0

    start_x = x_k
    start_y = y_k

    while((y_k - start_y) < eps or (start_x - x_k) > eps):
        x_i = x_k + (eps * y_k)
        y_i = y_k - (eps * x_i)
        coord = [x_c + round(x_i), y_c + round(y_i)]
        paint_pixel(coord, 'gray')
        plt.pause(0.03)
        x_k = x_i
        y_k = y_i


def draw_dda_eps_oct(x_c, y_c, r):
    eps = epsilon(r)

    x_k = r
    y_k = 0
    y_i = 0
    while(round(y_k) > round(-r)):
        x_i = x_k + (eps * y_k)
        y_i = y_i - 1
        draw_octets(x_c, y_c, round(x_k), round(y_k), 'gray')
        plt.pause(0.03)
        x_k = x_i
        y_k = y_i


def draw_dda_oct_dx(x_c, y_c, r):
    rx = r
    x_i = round(rx)
    y_i = 0

    while(y_i <= x_i):
        draw_octets(x_c, y_c, x_i, y_i, 'green')
        rx -= y_i/x_i
        x_i = round(rx)
        y_i += 1


if __name__ == "__main__":
    create_grid()
