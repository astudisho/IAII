from matplotlib import pyplot as plt
import vectorEntrenamiento as vE

class Grafica(object):
	def __init__(self, figure):
		self.seguirDibujando = True
		self.estaProbando = False
		self.vectoresEntrenamiento = []
		self.vectorPrueba = []
		self.figure = figure
		self.ax = self.figure.add_subplot(111)
		self.ax.set_title('MLP')
		self.setAx()
		self.ax.plot()
		self.canvas = None

	def setCanvas(self, canvas):
		self.canvas = canvas
		self.figure.canvas.mpl_connect('button_press_event',self.plot)

	def setAx(self):
		self.ax.set_xlim([-5,5])
		self.ax.set_ylim([-5,5])
		self.ax.grid()
		self.ax.axvline(0, color="black")
		self.ax.axhline(0, color="black")

	def plot(self, event):
		if event.inaxes!=self.ax.axes or not self.seguirDibujando: 
			if self.estaProbando:
				self.vectorPrueba = vE.VectorEntrenamiento( ( event.xdata, event.ydata ), 2 )
				self.ax.plot(event.xdata, event.ydata, 'ok')
				self.figure.canvas.draw()
				self.estaProbando = False
			return

		if event.button == 1:
			self.vectoresEntrenamiento.append( vE.VectorEntrenamiento( ( event.xdata, event.ydata ),0 ) )
			self.ax.plot(event.xdata, event.ydata, 'ob')
		elif event.button == 3:
			self.vectoresEntrenamiento.append( vE.VectorEntrenamiento( ( event.xdata, event.ydata ),1 ) )
			self.ax.plot(event.xdata, event.ydata, 'or')
		self.figure.canvas.draw()

	def plotPrueba(self, x, y, color):
		self.ax.plot( x, y, color)
		self.figure.canvas.draw()

	def plotMapeo(self, x, y, color):
		self.ax.plot( x, y, color)