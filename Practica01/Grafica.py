from matplotlib import pyplot as plt
import PuntoEntrenamiento as PE
from pylab import plot,show, norm

C_ZERO = 0

class Grafica(object):
	"""docstring for Grafica"""
	def __init__(self):
		super(Grafica, self).__init__()
		self.seguirDibujando = True
		self.Puntos = []

		self.figure = plt.figure()
		self.ax = self.figure.add_subplot(111)
		self.ax.set_title('Perceptron')
		self.setAx()
		self.ax.plot()
		self.canvas = self.ax.plot()
		self.figure.canvas.mpl_connect('button_press_event',self.plot)

	def setAx(self):
		self.ax.set_xlim([-5,5])
		self.ax.set_ylim([-5,5])
		self.ax.grid()
		self.ax.axvline(0, color="black")
		self.ax.axhline(0, color="black")

	def plot(self, event):
		if event.inaxes!=self.ax.axes or not self.seguirDibujando: return
		print('Event')
		if event.button == 1L:
			print('click izquierdo')
			self.Puntos.append( PE.PuntoEntrenamiento( ( event.xdata, event.ydata ),0 ) )
			self.ax.plot(event.xdata, event.ydata, 'ob')
		elif event.button == 3L:
			print('click derecho')
			self.Puntos.append( PE.PuntoEntrenamiento( ( event.xdata, event.ydata ),1 ) )
			self.ax.plot(event.xdata, event.ydata, 'or')

		self.figure.canvas.draw()

	def redraw(self, puntos, entradas, bias):
		plt.cla()
		self.setAx()

		for punto in puntos:
			if punto.getClase() == C_ZERO:
				plot(punto.getCoordenadas()[0],punto.getCoordenadas()[1],'ob')
			else :
				plot(punto.getCoordenadas()[0],punto.getCoordenadas()[1],'or')

		WeightArray = [entradas[0].getPeso(), entradas[1].getPeso()]
		X = 5

		n = norm(WeightArray)
		ww = WeightArray / n
		ww1 = [ww[1], -ww[0]]
		ww2 = [-ww[1], ww[0]]
		self.ax.plot([ww1[0]*X , ww2[0]*X],[ww1[1]*X , ww2[1]*X],'--b')
		self.figure.canvas.draw()
		plt.show()

if __name__ == '__main__':
	

	graf = Grafica()
	plt.show()

	graf.seguirDibujando = False
	graf.redraw()