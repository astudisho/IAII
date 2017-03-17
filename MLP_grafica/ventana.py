import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import numpy as np
import random
import sys

if sys.version_info.major >= 3:
	import tkinter as Tk
else:
	import Tkinter as Tk

from grafica import Grafica
import vectorEntrenamiento as vE

root = Tk.Tk()
root.wm_title("MLP BackProp")


MAX_PLOT = 5.
MIN_PLOT = -5.

C_ZERO = 0
MIN_VAL = -1.5
MAX_VAL = 1.5
MAX_DECIMALES = 5
X0 = -1

maxEpocas = Tk.StringVar()
maxEpocas.set('500')
lr = Tk.StringVar()
lr.set('0.1')
maxError = Tk.StringVar()
maxError.set('0.2')
pruebaX = Tk.StringVar()
pruebaY = Tk.StringVar()
capasOcultas = Tk.IntVar()
capasOcultas.set('2')
neuronas_capa1 = Tk.IntVar()
neuronas_capa1.set(16)
neuronas_capa2 = Tk.IntVar()
neuronas_capa2.set(8)

class Ventana():
	def __init__(self):	

		self.fig = plt.figure()
		canvas = FigureCanvasTkAgg( self.fig, master=root )

		self.grafica = Grafica( self.fig )
		self.grafica.setCanvas( canvas )
		self.ax = self.grafica.ax

		canvas.show()
		canvas.get_tk_widget().grid( row = 0, column = 0, columnspan = 4 )
		canvas._tkcanvas.grid( row=1, column = 0 )

		
		self.lblLr = Tk.Label(master=root, text="Learning rate: ")
		self.lblLr.grid( row = 2, column = 0 )
		self.entryLr = Tk.Entry(master=root, bd=5, textvariable=lr)
		self.entryLr.grid( row = 2, column = 1 )
		self.lblEpocas = Tk.Label(master=root, text="Epocas: ")
		self.lblEpocas.grid( row = 2, column = 2)
		self.entryEpocas = Tk.Entry(master=root, bd=5, textvariable=maxEpocas)
		self.entryEpocas.grid( row = 2, column = 3)
		self.lblError = Tk.Label(master = root, text='Error max:')
		self.lblError.grid( row = 4, column = 0)
		self.entryError = Tk.Entry(master = root, bd=5, textvariable=maxError)
		self.entryError.grid( row = 4, column = 1 )
		self.lblCapasOcultas = Tk.Label(master=root, text="Capas ocultas: ")
		self.lblCapasOcultas.grid( row=5, column=0)
		self.entryCapasOcultas = Tk.Entry(master=root, bd=5, textvariable=capasOcultas)
		self.entryCapasOcultas.grid( row=5, column=1)
		self.lblNoNeuronasCapa1 = Tk.Label(master=root, text="No. Neuronas Capa 1: ")
		self.lblNoNeuronasCapa1.grid( row=6, column=0)
		self.entryNoNeuronasCapa1 = Tk.Entry(master=root, bd=5, textvariable=neuronas_capa1)
		self.entryNoNeuronasCapa1.grid( row=6, column=1)
		self.lblNoNeuronasCapa2 = Tk.Label(master=root, text="No. Neuronas Capa 2: ")
		self.lblNoNeuronasCapa2.grid( row=6, column=2)
		self.entryNoNeuronasCapa2 = Tk.Entry(master=root, bd=5, textvariable=neuronas_capa2)
		self.entryNoNeuronasCapa2.grid( row=6, column=3)

		self.btnEntrenar = Tk.Button(master=root, text="Entrenar", command=self.entrenar)
		self.btnEntrenar.grid( row = 7, column = 0)

		self.lblEstado = Tk.Label(master=root, text="Estado: Configurando")
		self.lblEstado.grid( row = 8, column = 0 , columnspan = 3)

		self.lblPesos = Tk.Label( master = root, text = "")
		self.lblPesos.grid( row = 9, column = 0, columnspan = 3)

		self.btnPrueba = Tk.Button(master =  root, text="Probar", command = self.probar )
		self.btnPrueba.grid( row = 10)

		self.lblPrueba = Tk.Label( master = root, text = "" )
		self.lblPrueba.grid( row = 10, column = 1, rowspan = 2 )


		self.btnPlotear = Tk.Button(master =  root, text="Plotear", command = self.plotAreas )
		self.btnPlotear.grid( row = 11 )

		self.btnPlotear2 = Tk.Button(master =  root, text="Contour", command = self.plotContour )
		self.btnPlotear2.grid( row = 11, column = 1)

		root.protocol('WM_DELETE_WINDOW', self._quit)
		
		self.w = []
		self.neuronas_capas_i = []
	
	def feedForward(self, vector):
		#feedforward
				
		#convierte el vector de entrenamiento en un np.array para su manejo en las operaciones
		#a_i sirve para guardar los valores de f(n_i), empezando por el vector de entrada
		a_i = []
		a_i.append(np.array([[X0], [vector.getCoordenadas()[0]], [vector.getCoordenadas()[1]]]))
		#por cada capa oculta se genera la salida calculando la funcion logsig de la matriz de la capa i por la entrada a_i
		#a_i se actualiza cada vuelta
		for i in range(capasOcultas.get()):
			ai = self.w[i]*a_i[i]
			#se agrega el X0 = -1 despues de salir de la capa
			ai = np.append([X0], vE.logsig_array(ai))
			#se reacomoda el array en forma de columna para poder hacer operaciones
			ai = ai.reshape((len(ai), 1))
			a_i.append(ai)
				
		#se calcula la salida a_i de la capa de salida
		a_m = vE.logsig_array(self.w[capasOcultas.get()]*a_i[capasOcultas.get()])
		salida = a_m[0]

		return salida,a_i

	def entrenar(self):
		#crea matrices de las capas de neuronas a partir de los datos configurados
		self.crearCapas()
		self.grafica.seguirDibujando = False
		errorMax = float( maxError.get() )
		errorTotal = errorMax + 1
		llegoLimEpocas = False
		iteracion = 0

		self.fig2 = plt.figure()
		self.ax2 = self.fig2.add_subplot(111)
		self.ax.set_title('Error')
		self.ax2.set_xlim([0,int(maxEpocas.get())])
		self.ax2.set_ylim([0,4])
		self.ax2.grid()
		self.canvas2 = FigureCanvasTkAgg( self.fig2, master=root )
		self.canvas2.show()

		self.canvas2.get_tk_widget().grid( row = 0, column = 5, columnspan = 4 )
		self.canvas2._tkcanvas.grid( row=1, column = 5 )
		
		while (errorTotal > errorMax):
			errorTotal = 0
			for vector in self.grafica.vectoresEntrenamiento:
				
				salida,a_i = self.feedForward(vector)
							
				error = vector.getClase() - salida
				errorTotal += (pow(error, 2)/2)				

				#backprop
				
				#calculo de sensibilidades
				s = []
				#sensibilidad capa de salida
				s_m = np.array([-2*salida*(1 - salida)*error])
				s.append(s_m)
				s_i = s_m
				i = capasOcultas.get()
				#mientras que no sea la capa de entrada
				while i > 0:
					#borra el bias de a_i y saca el jacobiano de derivadas de f
					j_ai = np.diag([a*(1 - a) for a in np.delete(a_i[i], 0)])
					#quita w0 y transpone la matriz w_i
					w_i = np.transpose(np.delete(self.w[i], 0, axis=1))
					#calcula s'i
					si = j_ai*w_i*s_i
					s.append(si)
					s_i = si
					i -= 1
				
				#ajuste de pesos
				i = capasOcultas.get()
				j = 0
				while i > -1:
					delta_w = -1*float(lr.get())*s[j]*np.transpose(a_i[i])
					self.w[i] += delta_w
					i-=1
					j+=1
			
				
			self.lblEstado.config(text="Error total: "+str(errorTotal) + ' Epoca: ' + str(iteracion) )
			print("Error total: "+str(errorTotal) + ' Epoca: ' + str(iteracion))
			
			self.plotError(iteracion, errorTotal)

			if iteracion % 5 == 0:	
				self.grafica.canvas.draw()

			#Muestra los pesos
			#textoPesos = 'Pesos: W0 = ' + str( round( W0.getValor(), MAX_DECIMALES ) ) + '\t'
			#for i,entrada in enumerate(entradas):
			#	textoPesos += ' W' + str(i + 1) + ' = ' + str( round( entrada.getValor(), MAX_DECIMALES ) ) + '\t'
			#self.lblPesos.config( text = textoPesos )

			if iteracion == int(maxEpocas.get()):
				llegoLimEpocas = True
				break
			#self.plotPesos(entradas,W0.getValor(), 1)
			iteracion += 1
		#self.plotPesos(entradas, W0.getValor(), 2)
	
		if llegoLimEpocas:
			self.lblEstado.config(text="Estado: Maximo de epocas alcanzado \t Error Total: " +\
				str(errorTotal) + "  Epoca: " + str(iteracion) )
		else:
			self.lblEstado.config(text="Estado: Entrenado \t Error Total: " +\
				str(errorTotal) + "  Epoca: " + str(iteracion) )

		self.grafica.estaProbando = True
	
	def crearCapas(self):
		#crea una lista de los numeros de neuronas que tiene cada capa, a partir de lo que se configuro
		self.neuronas_capas_i.append(int(neuronas_capa1.get()))
		self.neuronas_capas_i.append(int(neuronas_capa2.get()))
		#la primer capa se configura de tamano n x 3
		for i in range(capasOcultas.get()):
			if i < 1:
				self.w.append(np.matrix([[vE.getRandom(MIN_VAL, MAX_VAL) for x in range(3)] for y in range(self.neuronas_capas_i[i])]))
			#las capas que siguen tienen el tamano de sus pesos dependiendo de la cantidad de neuronas de la capa anterior + el bias
			else:
				self.w.append(np.matrix([[vE.getRandom(MIN_VAL, MAX_VAL) for x in range(self.neuronas_capas_i[i-1]+1)] for y in range(self.neuronas_capas_i[i])]))
		#crea la capa de salida, es decir una sola neurona con el tamano de pesos que dependel tamano de neuronas de la capa anterior
		self.w.append(np.matrix([[vE.getRandom(MIN_VAL, MAX_VAL) for x in range(self.neuronas_capas_i[capasOcultas.get()-1]+1)]]))

	def respuesta(self, vector):
		suma = X0 * W0.getValor()
		for i, entrada in enumerate(entradas):
			suma += vector.getCoordenadas()[i] * entrada.getValor()
		return suma
	
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
		#res = self.respuesta( prueba )

		salida,a_i = self.feedForward( prueba )

		if salida >= 0.5:
			self.grafica.plotPrueba( prueba.getCoordenadas()[0], prueba.getCoordenadas()[1], 'or' )
		else:
			self.grafica.plotPrueba( prueba.getCoordenadas()[0], prueba.getCoordenadas()[1], 'ob' )

		res = salida[0]

		self.lblPrueba.config( text="Resultado: " + str( round( salida[0], MAX_DECIMALES ) ) )

		self.grafica.estaProbando = True

	def plotAreas(self):
		numSteps = 70
		step = round( ( abs(MIN_PLOT) + abs(MAX_PLOT) ) / numSteps, MAX_DECIMALES )
		rango = range( numSteps )
		sumaX = MIN_PLOT
		sumaY = MIN_PLOT
		
		X , Y, Z = [], [], []

		vector_areas = []

		for i in rango:
			sumaX += step
			sumaY = -5
			for j in rango:
				sumaY += step
				prueba = vE.VectorEntrenamiento( ( sumaX , sumaY ), 2 )

				print('Graficar',sumaX,sumaY)

				salida,a_i = self.feedForward( prueba )

				X.append( sumaX )
				Y.append( sumaY )
				Z.append( salida )

				if salida >= 0.5:
					self.grafica.plotMapeo( prueba.getCoordenadas()[0], prueba.getCoordenadas()[1], '.r' )
				else:
					self.grafica.plotMapeo( prueba.getCoordenadas()[0], prueba.getCoordenadas()[1], '.b' )

		self.fig.canvas.draw()

	def plotContour(self):
		numSteps = 70
		step = round( ( abs(MIN_PLOT) + abs(MAX_PLOT) ) / numSteps, MAX_DECIMALES )
		
		x = y = np.arange( MIN_PLOT, MAX_PLOT, step )
		Z = np.zeros( ( len(x), len(y) ) )
		
		X, Y = np.meshgrid( x, y )
		
		for i in range(numSteps):
			aux = []
			for j in range( numSteps ):
				prueba = vE.VectorEntrenamiento( ( x[ i ] , y[ j ] ), 2 )
				#salida,a_i = self.feedForward( prueba )
				salida,a_i = self.feedForward( prueba )

				Z[ i, j ] = salida
				
				#aux.append( salida )

			#Z.append( aux )
		CS = self.grafica.ax.contour( X, Y, Z)
		plt.clabel(CS, inline=1, fontsize=10)

		self.fig.canvas.draw()

	def plotError(self, epoca, error):
		self.ax2.plot(epoca,error, 'og')
		if epoca % 5 == 0:
			self.canvas2.draw()
		#self.fig2.draw()
		#self.ax2.draw()
		#help(self.ax2.draw)

	def crearMuestrasGrafica(self):
		aux = [ i for i in range(100) ]
		res = []