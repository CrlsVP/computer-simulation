import numpy as np
import matplotlib.pyplot as plt

x = []
y = []


def abs_2_rel(x, y):
    pass


def rel_2_abs(x, y):
    pass


def on_click(event):
    ix, iy = event.xdata, event.ydata

    print('x = %d, y = %d' % (
        ix, iy))

    x.append(ix)
    y.append(iy)
    plt.scatter(x, y, color='green')
    plt.draw()


if __name__ == "__main__":
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set(xlim=(0, 100), ylim=(0, 100))
    fig.canvas.mpl_connect('button_press_event', on_click)

    plt.show()
    plt.draw()
