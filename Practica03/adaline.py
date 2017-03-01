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
root.wm_title("Adaline")

C_ZERO = 0
MIN_VAL = -0.5
MAX_VAL = 0.5
MAX_DECIMALES = 5
maxEpocas = Tk.StringVar()
maxEpocas.set('200')
lr = Tk.StringVar()
lr.set('0.1')
maxError = Tk.StringVar()
maxError.set('0.2')
pruebaX = Tk.StringVar()
pruebaY = Tk.StringVar()

X0 = -1
W0 = vE.Entrada( vE.getRandom( MIN_VAL, MAX_VAL ) )
entradas = ( vE.Entrada( vE.getRandom( MIN_VAL, MAX_VAL ) ),
			 vE.Entrada( vE.getRandom( MIN_VAL, MAX_VAL ) ) )


class Ventana():
	def __init__(self):
		self.fig = plt.figure()
		canvas = FigureCanvasTkAgg( self.fig, master=root )
		#canvas2 =  FigureCanvasTkAgg( self.fig, master = root )
		self.grafica = Grafica( self.fig )
		self.grafica.setCanvas( canvas )
		self.ax = self.grafica.ax
		canvas.show()
		#canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
		canvas.get_tk_widget().grid( row = 0, column = 0, columnspan = 3 )
		#canvas2.get_tk_widget().grid( row = 0, column = 5, columnspan = 4 )
		#self.toolbar = NavigationToolbar2TkAgg(canvas, root)
		#self.toolbar.update()
		canvas._tkcanvas.grid( row=1, column = 0 )
		
		self.lblLr = Tk.Label(master=root, text="Learning rate: ")
		self.lblLr.grid( row = 2, column = 0 )
		self.entryLr = Tk.Entry(master=root, bd=5, textvariable=lr)
		self.entryLr.grid( row = 2, column = 1 )
		self.lblEpocas = Tk.Label(master=root, text="Epocas: ")
		self.lblEpocas.grid( row = 3, column = 0)
		self.entryEpocas = Tk.Entry(master=root, bd=5, textvariable=maxEpocas)
		self.entryEpocas.grid( row = 3, column = 1)
				
		self.lblError = Tk.Label(master = root, text='Error max:')
		self.lblError.grid( row = 4, column = 0)
		self.entryError = Tk.Entry(master = root, bd=5, textvariable=maxError)
		self.entryError.grid( row = 4, column = 1 )

		self.btnEntrenar = Tk.Button(master=root, text="Entrenar", command=self.entrenar)
		self.btnEntrenar.grid( row = 6, column = 0)

		self.lblEstado = Tk.Label(master=root, text="Estado: Configurando")
		self.lblEstado.grid( row = 7, column = 0 , columnspan = 3)

		self.lblPesos = Tk.Label( master = root, text = "")
		self.lblPesos.grid( row = 8, column = 0, columnspan = 3)

		self.btnPrueba = Tk.Button(master =  root, text="Probar", command = self.probar )
		self.btnPrueba.grid( row = 9)

		self.lblPrueba = Tk.Label( master = root, text = "" )
		self.lblPrueba.grid( row = 9, column = 1, rowspan = 2 )

		root.protocol('WM_DELETE_WINDOW', self._quit)
	
	def entrenar(self):
		#maxError = 0.2
		self.grafica.seguirDibujando = False
		errorMax = float( maxError.get() )
		errorTotal = errorMax + 1
		llegoLimEpocas = False
		iteracion = 0
		self.plotPesos(entradas, W0.getValor(), 0)
		while (errorTotal > errorMax):
			errorTotal = 0
			for vector in self.grafica.vectoresEntrenamiento:
				salida = vE.logsig(self.respuesta(vector))			
				error = vector.getClase() - salida
				errorTotal += (pow(error, 2)/2)
				if ( error != C_ZERO ):
					#W0.setValor( W0.getValor() + float(lr.get()) * error * salida * (1 - vE.logsig(self.respuesta(vector))) * X0 )
					W0.setValor( W0.getValor() + float(lr.get()) * error * salida * ( 1 - salida ) * X0 )
					for i,entrada in enumerate(entradas):
						#peso = entrada.getValor() + float(lr.get()) * error * salida * (1 - vE.logsig(self.respuesta(vector))) * vector.getCoordenadas()[i]
						peso = entrada.getValor() + float(lr.get()) * error * salida * (1 - salida) * vector.getCoordenadas()[i]
						entrada.setValor(peso)
			self.lblEstado.config(text="Error total: "+str(errorTotal) + ' Epoca: ' + str(iteracion) )

			#Muestra los pesos
			textoPesos = 'Pesos: W0 = ' + str( round( W0.getValor(), MAX_DECIMALES ) ) + '\t'
			for i,entrada in enumerate(entradas):
				textoPesos += ' W' + str(i + 1) + ' = ' + str( round( entrada.getValor(), MAX_DECIMALES ) ) + '\t'
			self.lblPesos.config( text = textoPesos )

			if iteracion == int(maxEpocas.get()):
				llegoLimEpocas = True
				break
			self.plotPesos(entradas,W0.getValor(), 1)
			iteracion += 1
		self.plotPesos(entradas, W0.getValor(), 2)
		

		if llegoLimEpocas:
			self.lblEstado.config(text="Estado: Maximo de epocas alcanzado \t Error Total: " +\
				str(errorTotal) + "  Epoca: " + str(iteracion) )
		else:
			self.lblEstado.config(text="Estado: Entrenado \t Error Total: " +\
				str(errorTotal) + "  Epoca: " + str(iteracion) )

		self.grafica.estaProbando = True

	def respuesta(self, vector):
		suma = X0 * W0.getValor()
		for i, entrada in enumerate(entradas):
			suma += vector.getCoordenadas()[i] * entrada.getValor()
		return suma
		#if suma >= C_ZERO:	
		#	return 1
		#else:	
		#	return C_ZERO
	
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
	
	def probar(self):
		prueba = self.grafica.vectorPrueba
		res = self.respuesta( prueba )

		if res >= C_ZERO:
			self.grafica.plotPrueba( prueba.getCoordenadas()[0], prueba.getCoordenadas()[1], 'or' )
		else:
			self.grafica.plotPrueba( prueba.getCoordenadas()[0], prueba.getCoordenadas()[1], 'ob' )

		self.lblPrueba.config( text="Resultado: " + str( round( res, MAX_DECIMALES ) ) )

		self.grafica.estaProbando = True