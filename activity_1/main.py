import itertools
import matplotlib.pyplot as plt
import numpy as np
import os
import shutil
import time

from os import system, name


def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux
    else:
        _ = system('clear')


counter = 0
current_file = ''
abs_coord = []
rel_coord = []
x = []
y = []


def abs_2_rel(xy_i, xy_f):
    rel_coord.append([xy_i[0] - xy_f[0], xy_i[1] - xy_f[1]])
    return(rel_coord[-1])


def read_from_file():
    clear()
    global current_file
    found = False
    while(not found):
        found = True
        try:
            path = 'C:/dev/computer-simulation/activity_1/files/' + str(
                input("Please introduce the name of the file (files must be inside /files path and without .txt): ")) + '.txt'

            f = open(path, "r")
        except FileNotFoundError:
            print("File does not exist! Try again")
            found = False
    current_file = path[:-4]
    lines = f.readlines()
    file_coord = []
    # for each line in the file, appends a coordinate ignoring the line break
    for line in lines:
        if(line[:-1] != '\n'):
            line += '\n'
        xy = line.split(',')
        file_coord.append([float(xy[0]), float(xy[1][:-1])])

    f.close()
    interactive(file_coord)


def write_to_file(txt):
    f = open(current_file + '.txt', 'a+')
    f.write(txt)
    f.close()


def on_click(event):
    ix, iy = event.xdata, event.ydata
    global counter

    if(ix == None or iy == None):
        pass
    else:
        abs_coord.append([ix, iy])
        write_to_file('{}, {}\n'.format(ix, iy))
        if(counter == 0):
            rel_coord.append(abs_coord[0])
        else:
            #abs_2_rel(abs_coord[counter], rel_coord[counter-1])
            abs_2_rel(abs_coord[counter], abs_coord[counter-1])

        x.append(ix)
        y.append(iy)
        plt.scatter(x, y, color='green')
        plt.draw()
        print_table()
        counter += 1


def interactive(coord=None):
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set(xlim=(0, 100), ylim=(0, 100))
    if(coord == None):
        fig.canvas.mpl_connect('button_press_event', on_click)
        plt.show()
        plt.draw()
    else:
        i = 0
        for xy in coord:
            abs_coord.append([xy[0], xy[1]])
            if(i == 0):
                rel_coord.append(abs_coord[0])
            else:
                abs_2_rel(abs_coord[counter], abs_coord[counter-1])
            i += 1
            plt.scatter(xy[0], xy[1], color='red')
            plt.draw()

        for (i, xy) in zip(range(len(abs_coord)), abs_coord):
            plt.annotate(i+1, xy, fontsize=8, ha='center')
        print_table()
        # plt.show()

        fig.canvas.mpl_connect('button_press_event', on_click)
        plt.show()
        plt.draw()


def print_table():
    clear()
    print('ABSOLUTE COORD\t\tRELATIVE COORD\n\n')
    for (a, r) in zip(abs_coord, rel_coord):
        print('{}\t\t{}\n'.format(
            np.around(a, decimals=3), np.around(r, decimals=3)))


if __name__ == "__main__":
    opt = None
    print('Welcome to Activity 1\n\n')
    print('1. Interactive plot\n')
    print('2. Read from file\n')
    while(not opt or (opt > 2 or opt < 1)):
        try:
            opt = int(input('\nPlease select an option: '))
        except ValueError:
            print('Please just introduce integers.')

    if(opt == 1):
        current_file = 'C:/dev/computer-simulation/activity_1/files/' + str(input(
            'Please introduce a name for the file where the coordinates will be saved (do not include the .txt extension): '))

        num = 0
        clear()
        while(os.path.exists(current_file + '.txt')):
            num += 1
            if(num > 1):
                current_file = current_file[:-1]
            current_file += str(num)

        temp = open(current_file + '.txt', 'w')
        temp.close()

        interactive()
    else:
        read_from_file()
