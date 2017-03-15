import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import numpy as np
import random
import tkinter as Tk
from grafica import Grafica
import vectorEntrenamiento as vE

root = Tk.Tk()
root.wm_title("Adaline")

C_ZERO = 0
MIN_VAL = -1.5
MAX_VAL = 1.5
MAX_DECIMALES = 5

X0 = -1
a2 = []

maxEpocas = Tk.StringVar()
lr = Tk.StringVar()
maxError = Tk.StringVar()
numAdalines = Tk.StringVar()
pruebaX = Tk.StringVar()
pruebaY = Tk.StringVar()

numAdalines.set('2')
maxEpocas.set('200')
lr.set('0.1')
maxError.set('0.2')
i = 0

W0_1 = []
W0_2 = []
W_1 = []
W_2 = []

adalines = int(numAdalines.get())

while(i < adalines):
	W0_1.append( vE.Entrada( vE.getRandom( MIN_VAL, MAX_VAL ) ) )
	W_1.append(	[ vE.Entrada( vE.getRandom( MIN_VAL, MAX_VAL ) ), vE.Entrada( vE.getRandom( MIN_VAL, MAX_VAL ) ) ] )

	W0_2.append( vE.Entrada(vE.getRandom( MIN_VAL, MAX_VAL ) ) )
	W_2.append( [ vE.Entrada( vE.getRandom( MIN_VAL, MAX_VAL ) ), vE.Entrada( vE.getRandom( MIN_VAL, MAX_VAL ) ) ] )

	i += 1

class Ventana():
	def __init__(self):
		self.fig = plt.figure()
		canvas = FigureCanvasTkAgg( self.fig, master=root )
		self.grafica = Grafica( self.fig )
		self.grafica.setCanvas( canvas )
		self.ax = self.grafica.ax
		canvas.show()
		canvas.get_tk_widget().grid( row = 0, column = 0, columnspan = 3 )
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

		self.btnEntrenar = Tk.Button(master=root, text="Entrenar", command=self.red)
		self.btnEntrenar.grid( row = 6, column = 0)

		self.lblEstado = Tk.Label(master=root, text="Estado: Configurando")
		self.lblEstado.grid( row = 7, column = 0 , columnspan = 3)

		self.lblPesos = Tk.Label( master = root, text = "")
		self.lblPesos.grid( row = 8, column = 0, columnspan = 3)

		self.btnPrueba = Tk.Button(master =  root, text="Probar", command = self.red)
		self.btnPrueba.grid( row = 9)

		self.lblPrueba = Tk.Label( master = root, text = "" )
		self.lblPrueba.grid( row = 9, column = 1, rowspan = 2 )

		root.protocol('WM_DELETE_WINDOW', self._quit)

	def red(self):
		iteracion = 0
		i = 0

		errorMax = float(maxError.get())
		epocasMax = float(maxEpocas.get())
		adalines = int(numAdalines.get())

		while(iteracion < epocasMax):
			while(i  < adalines):
				for vector in self.grafica.vectoresEntrenamiento:
					#forward prop
					a1 = vE.logsig( self.resC1( vector, i) )
					a2.insert( i, vE.logsig( self.resC2(a1, i ) ) )

					#backward prop
					e = vector.getClase() - a2[i]
					s2 = -2 * (1 - a2[i]**2) * float(e)
					s1 = np.diagonal(1 - a1**2) * W_2[i].T * s2

					#actualizar pesos
					W_2 = W_2 - float(lr) * s2 * a1
					W0_2 = W0_2 - float(lr) * s2

					W_1 = W_1 - self.calcular(vector, s1, float(lr))
					W0_1 = W0_1 - float(lr) * s1
				i += i
			iteracion += iteracion

	def resC1(self, vector, it):
		pos = 0
		suma = X0 * W0_1[it].getValor()
		for i in enumerate(W_1[it]):
			suma += vector.getCoordenadas()[pos] *  W_1[it][pos].getValor()
			pos += 1
		return suma

	def resC2(self, vector, it):
		pos = 0
		suma = X0 * W0_2[it].getValor()
		for i in enumerate(W_2[it]):
			suma += vector *  W_2[it][pos].getValor()
			pos += 1
		return suma

	def calcular(self, vector, S, LR):
		suma = 0
		for i in enumerate(vector):
			suma += vector.getCoordenadas()[i] * S * LR
		return suma

	def _quit(self):
		root.quit()
		root.destroy()