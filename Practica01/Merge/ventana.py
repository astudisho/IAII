import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import numpy as np
import random
import Tkinter as Tk
from grafica import Grafica
import vectorEntrenamiento as vE

root = Tk.Tk()
root.wm_title("Perceptron")

C_ZERO = 0
MIN_VAL = -5
MAX_VAL = 5
maxEpocas = Tk.StringVar()
lr = Tk.StringVar()
X0 = -1
W0 = vE.Entrada( vE.getRandom( MIN_VAL, MAX_VAL ) )
entradas = ( vE.Entrada( vE.getRandom( MIN_VAL, MAX_VAL ) ),
			 vE.Entrada( vE.getRandom( MIN_VAL, MAX_VAL ) ) )

class Ventana():
	def __init__(self):
		self.fig = plt.figure()
		canvas = FigureCanvasTkAgg(self.fig, master=root)
		self.grafica = Grafica(self.fig)
		self.grafica.setCanvas(canvas)
		self.ax = self.grafica.ax
		canvas.show()
		canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
		toolbar = NavigationToolbar2TkAgg(canvas, root)
		toolbar.update()
		#canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
		btnQuit = Tk.Button(master=root, text="Salir", command=self._quit)
		btnQuit.pack(side=Tk.BOTTOM)
		lblLr = Tk.Label(master=root, text="Learning rate: ")
		lblLr.pack(side=Tk.LEFT)
		entryLr = Tk.Entry(master=root, bd=5, textvariable=lr)
		entryLr.pack(side=Tk.LEFT)
		lblEpocas = Tk.Label(master=root, text="Epocas: ")
		lblEpocas.pack(side=Tk.LEFT)
		entryEpocas = Tk.Entry(master=root, bd=5, textvariable=maxEpocas)
		entryEpocas.pack(side=Tk.LEFT)
		btnEntrenar = Tk.Button(master=root, text="Entrenar", command=self.entrenar)
		btnEntrenar.pack(side=Tk.RIGHT)
		self.lblEstado = Tk.Label(master=root, text="Estado: Configurando")
		self.lblEstado.pack(side=Tk.LEFT)
	
	def entrenar(self):
		tieneError = True
		sinEntrenar = False
		iteracion = 0
		self.plotPesos(entradas, W0.getValor(), 0)
		while tieneError:
			tieneError = False
			for vector in self.grafica.vectoresEntrenamiento:
				salida = self.respuesta(vector)			
				error = vector.getClase() - salida
				if ( error != C_ZERO ):
					tieneError = True
					W0.setValor( W0.getValor() + float(lr.get()) * error * X0 )
					for i,entrada in enumerate(entradas):
						peso = entrada.getValor() + float(lr.get()) * error * vector.getCoordenadas()[i]	   
						entrada.setValor(peso)
			if iteracion == int(maxEpocas.get()):
				tieneError = False
				sinEntrenar = True
			self.plotPesos(entradas,W0.getValor(), 1)
			iteracion += 1
		self.plotPesos(entradas, W0.getValor(), 2)
		if sinEntrenar:
			self.lblEstado.config(text="Estado: No converge")
		else:
			if not tieneError:
				self.lblEstado.config(text="Estado: Entrenado")

	def respuesta(self, vector):
		suma = X0 * W0.getValor()
		for i, entrada in enumerate(entradas):
			suma += vector.getCoordenadas()[i] * entrada.getValor()	
		if suma >= C_ZERO:	
			return 1
		else:	
			return C_ZERO
	
	def plotPesos(self, entradas, bias, tipo):
		o = None
		if tipo == 0: c = 'red'
		elif tipo == 1: c = 'cyan'
		else: c = 'green'
		weightArray = [entradas[0].getValor(), entradas[1].getValor()]
		x = np.array(range(-10,10))
		y = eval( '(' + str(bias)+'/'+str(weightArray[1]) + ')-((' +str(weightArray[0])+'/'+str(weightArray[1]) + ')*x)' )
		self.ax.plot(x,y,'--', color=c)
		self.fig.canvas.draw()
	
	def _quit(self):
		root.quit()
		root.destroy()
	

