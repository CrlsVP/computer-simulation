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
                    for pixel in draw_dda(line[0][0], line[0][1], radius):
                        if((30 < pixel[0] < 1) or (30 < pixel[1] < 1)):
                            pass
                        else:
                            paint_pixel(
                                [line[0][0]+pixel[0], line[0][1]+pixel[1]], 'red')
                        plt.pause(0.03)

                    print("Execution time of DDA Algorithm without octets: {}".format(timeit.timeit(
                        stmt="draw_dda({}, {}, {})".format(line[0][0], line[1][1], radius), setup="from __main__ import draw_dda", number=1)))
                    plt.pause(1)

                    print('\n--------------------------------------\n')

                    # DDA with octets
                    print('Now painting with DDA (with octets)')
                    for pixel in draw_dda_oct(line[0][0], line[0][1], radius):
                        if((30 < pixel[0] < 1) or (30 < pixel[1] < 1)):
                            pass
                        else:
                            draw_octets(line[0][0], line[0][1],
                                        pixel[0], pixel[1], 'blue')

                    print("Execution time of DDA Algorithm with octets: {}".format(timeit.timeit(
                        stmt="draw_dda_oct({}, {}, {})".format(line[0][0], line[1][1], radius), setup="from __main__ import draw_dda_oct", number=1)))
                    plt.pause(1)
                    print('\n--------------------------------------\n')

                    # Bresenham
                    print('Now painting with Bresenham')
                    for pixel in draw_bres(line[0][0], line[0][1], radius):
                        if((30 < pixel[0] < 1) or (30 < pixel[1] < 1)):
                            pass
                        else:
                            draw_octets(line[0][0], line[0][1],
                                        pixel[0], pixel[1], 'yellow')
                    print("Execution time of Bresenham Algorithm: {}".format(timeit.timeit(
                        stmt="draw_bres({}, {}, {})".format(line[0][0], line[1][1], radius), setup="from __main__ import draw_bres", number=1)))

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

# ! Algoritmo DDA sin uso de octetos
# * El algoritmo funciona basándose en la derivada de la ecuación de la circunferencia
# * la cual está dada por x^2 + y^2 - r^ = 0 (en donde r es constante), teniendo así
# * la ecuación y_k = sqrt(r^2 - x_k^2). Cabe mencionar que en este estrategia implementada
# * no se toman en cuenta los valores del punto central en la ecuación sino hasta después,
# * en el coloreado de los puntos.

# ! y_k = valor a seguir en el eje de las Y iterando en X
# ! para cuando se itera en Y, el x_k se obtiene de igual manera que cuando se itera en X
#  ! con la diferencia de que las variables cambian de posición solamente


def draw_dda(x_c, y_c, r2):
    r = round(r2)
    coord = []
    x_k = 0
    y_k = int(math.sqrt((r*r) - (x_k * x_k)))

    sign_y = 1
    sign_x = 1

    # Gracias a esta iteración es posible colorear los arcos superior e inferior (cuando se
    # itera sobre X) y los arcos derecho e izquierdo (cuando se itera sobre Y). Lo único que
    # hace es cambiar los signos cuando corresponda. Esto evita estructuras iterativas de más
    # y sólo emplea la misma para repetirse las veces que lo necesite
    for i in range(4):
        if(i == 1):
            sign_x = -1
        if(i == 2):
            sign_y = -1
        if(i == 3):
            sign_x = 1

        coord.append([(x_k * sign_x), (y_k * sign_y)])
        while(y_k > 0):
            x_k += 1
            y_k = round(math.sqrt((r*r) - (x_k * x_k)))
            coord.append([(x_k * sign_x), (y_k * sign_y)])

        y_k = 0
        x_k = int(math.sqrt((r*r) - (y_k * y_k)))

        while(x_k > 0):
            y_k += 1
            x_k = round(math.sqrt((r*r) - (y_k * y_k)))
            coord.append([(x_k * sign_x), (y_k * sign_y)])

    return(coord)


def draw_dda_oct(x_c, y_c, r2):
    r = round(r2)
    coord = []
    x_k = 0
    y_k = int(math.sqrt((r*r) - (x_k * x_k)))
    coord.append([x_k, y_k])

    while(y_k > x_k):
        x_k += 1
        y_k = round(math.sqrt((r*r) - (x_k * x_k)))
        coord.append([x_k, y_k])

    return(coord)


def draw_bres(x_c, y_c, r):
    coord = []
    x = 0
    y = round(r)
    p = 3 - (2 * r)
    coord.append([x, y])

    while (x <= y):
        if (p <= 0):
            p += (4 * x) + 6
        else:
            p += (4 * x) - (4 * y) + 10
            y -= 1
        x += 1
        coord.append([x, y])

    return(coord)


# ! Funciones adicionales de prueba
# * Las funciones enlistadas a continuación se utilizaron a modo
# * de prueba, ya que son implementaciones del algoritmo DDA con modificaciones
# * las cuales hacen uso de un valor epsilon que se detalla más a fondo en el
# * reporte de la actividad. La función draw_dda_dx utiliza una derivada parcial
# * para el cálculo de valores en y, de igual manera se detalla más a fondo en
# * el reporte
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
