from matplotlib import pyplot as plt

ListaClase1 = []
ListaClase2 = []

class LineBuilder:
    def __init__(self, line):
        self.line = line
        self.xs = list(line.get_xdata())
        self.ys = list(line.get_ydata())
        self.cid = line.figure.canvas.mpl_connect('button_press_event', self)

    def __call__(self, event):
        if event.inaxes!=self.line.axes: return
        print('click', event, event.button, event.xdata, event.ydata)
        print('Boton: ',event.button)
        if event.button == 1L:
            print('click izquierdo')
            ListaClase1.append( ( ( event.xdata, event.ydata ),0) )
        elif event.button == 3L:
            print('click derecho')
            ListaClase2.append( ( ( event.xdata, event.ydata ),1) )
        self.xs.append(event.xdata)
        self.ys.append(event.ydata)
        self.line.set_data(self.xs, self.ys)
        self.line.figure.canvas.draw()

fig = plt.figure()
ax = fig.add_subplot(111)
help(ax)
help(fig)
ax.set_title('Perceptron')
line, = ax.plot([0], [0],'r+')  # empty line
linebuilder = LineBuilder(line)

plt.show()

print(ListaClase1)
print(ListaClase2)