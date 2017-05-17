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
import rbf

root = Tk.Tk()
root.wm_title("RBF")


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


class Ventana():
	def __init__(self):	

		self.fig = plt.figure()
		canvas = FigureCanvasTkAgg( self.fig, master=root )

		self.grafica = Grafica( self.fig, 'RBF' )
		self.grafica.setCanvas( canvas )
		self.ax = self.grafica.ax

		canvas.show()
		canvas.get_tk_widget().grid( row = 0, column = 0, columnspan = 5 )
		canvas._tkcanvas.grid( row=1, column = 0 )

		self.btnEntrenar = Tk.Button(master=root, text="Entrenar", command=self.entrenar)
		self.btnEntrenar.grid( row = 2, column = 2)

		# self.btnEntrenar = Tk.Button(master=root, text="Reset", command=self.bla)
		# self.btnEntrenar.grid( row = 2, column = 3)

		root.protocol('WM_DELETE_WINDOW', self._quit)
		
	def entrenar(self):
		self.grafica.seguirDibujando = False

		rbf.RBF( self.grafica.vectoresEntrenamiento, self.grafica, self.grafica.vectorCluster )
		

	def plotPesos(self, entradas, bias, tipo):
		self.ax.plot(x,y,'--', color=c)
		self.fig.canvas.draw()
	
	def _quit(self):
		root.quit()
		root.destroy()

	def bla(self):
		#help(self.fig)
		# self.ax.cla()
		# self.grafica.setAx()
		# self.fig.canvas.draw()
		self.grafica.clear()

