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
                    r_x = abs(line[1][0] - line[0][0])
                    r_y = abs(line[1][1] - line[0][1])
                    if(r_x == 0 or r_y == 0):
                        print('That is just a regular line!')
                    else:

                        # DDA without quadrants
                        print('Now painting with DDA (without quadrants)')
                        coord = sorted(
                            draw_dda(line[0][0], line[0][1], r_x, r_y), key=lambda k: [k[1], k[0]])
                        for pixel in coord:
                            if((30 < pixel[0] < 1) or (30 < pixel[1] < 1)):
                                pass
                            else:
                                paint_pixel(
                                    [line[0][0]+pixel[0], line[0][1]+pixel[1]], 'red')
                            plt.pause(0.01)

                        print("Execution time of DDA Algorithm without quadrants: {}".format(timeit.timeit(
                            stmt="draw_dda({}, {}, {}, {})".format(line[0][0], line[1][1], r_x, r_y), setup="from __main__ import draw_dda", number=1)))
                        plt.pause(1)

                        print('\n--------------------------------------\n')

                        # DDA with quadrants
                        print('Now painting with DDA (with quadrants)')
                        coord = draw_dda_oct(line[0][0], line[0][1], r_x, r_y)
                        for pixel in coord:
                            if((30 < pixel[0] < 1) or (30 < pixel[1] < 1)):
                                pass
                            else:
                                draw_quad(line[0][0], line[0][1],
                                          pixel[0], pixel[1], 'blue')

                        print("Execution time of DDA Algorithm with quadrants: {}".format(timeit.timeit(
                            stmt="draw_dda_oct({}, {}, {}, {})".format(line[0][0], line[1][1], r_x, r_y), setup="from __main__ import draw_dda_oct", number=1)))
                        print('\n--------------------------------------\n')

                        # Bresenham
                        print('Now painting with Bresenham')
                        coord = draw_bres(line[0][0], line[0][1], r_x, r_y)
                        for pixel in coord:
                            if((30 < pixel[0] < 1) or (30 < pixel[1] < 1)):
                                pass
                            else:
                                draw_quad(line[0][0], line[0][1],
                                          pixel[0], pixel[1], 'yellow')
                        print("Execution time of Bresenham Algorithm: {}".format(timeit.timeit(
                            stmt="draw_bres({}, {}, {}, {})".format(line[0][0], line[1][1], r_x, r_y), setup="from __main__ import draw_bres", number=1)))

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


def draw_quad(x_c, y_c, x, y, color):
    paint_pixel([x_c+x, y_c+y], color)
    plt.pause(0.01)
    paint_pixel([x_c-x, y_c+y], color)
    plt.pause(0.01)
    paint_pixel([x_c+x, y_c-y], color)
    plt.pause(0.01)
    paint_pixel([x_c-x, y_c-y], color)
    plt.pause(0.01)


def draw_dda(x_c, y_c, r_x, r_y):
    coord = []

    a = r_x
    b = r_y

    y_k = b
    x_k = a
    sign = 1
    end = end2 = 0
    for i in range(4):
        if(i == 1):
            y_k = b
            sign = -1
        if(i == 2):
            y_k = 0
            end = -b
        if(i == 3):
            y_k = 0
            sign = 1

        while(y_k >= end):
            x_k = (a*sign) * math.sqrt(1 - ((y_k * y_k) / (b * b)))
            coord.append([round(x_k), round(y_k)])
            y_k -= 1

        if(i == 1):
            x_k = a
        if(i == 2):
            x_k = 0
            end2 = -a
        if(i == 3):
            x_k = 0

        while(x_k >= end2):
            y_k = (b*sign) * math.sqrt(1 - ((x_k * x_k) / (a * a)))
            coord.append([round(x_k), round(y_k)])
            x_k -= 1

    return(coord)


def draw_dda_oct(x_c, y_c, r_x, r_y):
    coord = []

    a = r_x
    b = r_y

    x_k = 0

    while(x_k <= a):
        y_k = b * math.sqrt(1 - ((x_k * x_k) / (a * a)))
        coord.append([round(x_k), round(y_k)])
        x_k += 1

    y_k = 0
    while(y_k <= b):
        x_k = a * math.sqrt(1 - ((y_k * y_k) / (b * b)))
        coord.append([round(x_k), round(y_k)])
        y_k += 1

    return(coord)


def draw_bres(x_c, y_c, r_x, r_y):
    coord = []
    x_k = 0
    y_k = r_y

    # Initial decision parameter of region 1
    p_k = ((r_y * r_y) - (r_x * r_x * r_y) +
           (0.25 * r_x * r_x))
    d_x = 2 * r_y * r_y * x_k
    d_y = 2 * r_x * r_x * y_k

    # For region 1
    while (d_x < d_y):
        coord.append([x_k, y_k])

        # Checking and updating value of
        # decision parameter based on algorithm
        if (p_k < 0):
            d_x += (2 * r_y * r_y)
            p_k += d_x + (r_y * r_y)
        else:
            y_k -= 1
            d_x += (2 * r_y * r_y)
            d_y -= (2 * r_x * r_x)
            p_k += d_x - d_y + (r_y * r_y)

        x_k += 1

    # Decision parameter of region 2
    p_k2 = (((r_y * r_y) * ((x_k + 0.5) * (x_k + 0.5))) +
            ((r_x * r_x) * ((y_k - 1) * (y_k - 1))) -
            (r_x * r_x * r_y * r_y))

    # Plotting points of region 2
    while (y_k >= 0):
        coord.append([x_k, y_k])

        # Checking and updating parameter
        # value based on algorithm
        if (p_k2 > 0):
            y_k -= 1
            d_y -= (2 * r_x * r_x)
            p_k2 += (r_x * r_x) - d_y
        else:
            y_k -= 1
            x_k += 1
            d_x += (2 * r_y * r_y)
            d_y -= (2 * r_x * r_x)
            p_k2 += d_x - d_y + (r_x * r_x)

    return coord


if __name__ == "__main__":
    create_grid()
