#RBF

import math
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import numpy as np
import random
import Tkinter as Tk
from grafica import Grafica
import vectorEntrenamiento as vE

MAX_INT = 100000

root = Tk.Tk()
root.wm_title("Adaline")

class Cluster(object):
	"""docstring for Cluster"""
	def __init__(self, dimensiones):
		super(Cluster, self).__init__()
		self.dimensiones = dimensiones

		self.centro = [-1 ] * dimensiones
		self.radio = -1
		self.setCluster = []
		self.sigma = 0
		self.beta = 0

	def calcularDistancia(self, entrada):
		sumatoria = 0
		for i in ( range ( len( self.centro ) ) ):
			sumatoria += ( self.centro[i] - entrada[ i ] ) ** 2

		return math.sqrt( sumatoria )

	def reset( self ): self.setCluster = []

	def getPromedio( self ):
		resultado = [0] * self.dimensiones

		for i in range( self.dimensiones ):
			suma = 0
			for cluster in self.setCluster:
				suma += cluster.getCoordenadas()[i]
			resultado[i] = suma / float( len( self.setCluster ) )

		return resultado

	def setRadio(self):
		suma = 0
		for cluster in self.setCluster:
			suma += self.calcularDistancia( cluster.getCoordenadas() )

		self.radio = suma / len( self.setCluster )

		self.sigma = self.radio

		self.beta = 1 / ( 2 * self.sigma ** 2 )

		return self.radio


class RBF(object):
	"""docstring for RBF"""
	def __init__(self):
		self.fig = plt.figure()
		canvas = FigureCanvasTkAgg( self.fig, master = root )
		#canvas2 =  FigureCanvasTkAgg( self.fig, master = root )
		self.grafica = Grafica( self.fig )
		self.grafica.setCanvas( canvas )
		self.ax = self.grafica.ax
		canvas.show()
		canvas.get_tk_widget().grid( row = 0, column = 0, columnspan = 3 )
		canvas._tkcanvas.grid( row=1, column = 0 )

		self.trainingSet = self.grafica.vectoresEntrenamiento
		self.centroides = self.grafica.vectoresPrueba

		self.btnEntrenar = Tk.Button(master=root, text="Entrenar", command = self.Entrenar)
		self.btnEntrenar.grid( row = 6, column = 1)

	def Entrenar(self):
		self.dimensiones = len( self.trainingSet[0].getCoordenadas() )
		print("Dimensiones: ", self.dimensiones)
		self.setRBF = []
		self.numRbf = int ( 2 * len( self.trainingSet ) / 3 )

		#for i in range( self.dimensiones ):
		for i in range(  self.numRbf ):
			self.setRBF.append( Cluster( self.dimensiones ) )
			print('a')

		for index,vector in enumerate ( random.sample( self.trainingSet, self.numRbf ) ):
			self.setRBF[ index ].centro = vector.getCoordenadas()
			print('b')

		print( self.setRBF[0].centro )

		self.iniciarClustering()

	def iniciarClustering(self):
		detectoCambios = True
		epocas = 1

		while detectoCambios:

			detectoCambios = False	

			for centros in self.centroides:	

				print(centros.getCoordenadas)
				for vector in self.trainingSet:
					rbfGanador = centros
					distanciaMin = MAX_INT
					distanciaMax = 0

					for rbf in self.setRBF:
						#print( 'Distancia: ' , rbf.centro , ' --> ' ,vector.getCoordenadas() )
						distancia = rbf.calcularDistancia( vector.getCoordenadas() )
						#print( distancia )
						if distancia > distanciaMax:
							distanciaMax = distancia

						if distancia < distanciaMin:
							rbfGanador = rbf
							distanciaMin = distancia

					rbfGanador.setCluster.append( vector )
					#print('Algo')


				for rbf in self.setRBF:
					nuevoCentro = rbf.getPromedio()

					print( rbf.centro )
					print( nuevoCentro )
					print()

					if nuevoCentro != rbf.centro:
						rbf.centro = nuevoCentro
						detectoCambios = True
						print('Sigue')

					rbf.reset()

				self.grafica.plotPrueba(rbf.centro[0], rbf.centro[1], 'og', distanciaMax * 15)

			#self.grafica.plotPrueba(rbf.centro[0], rbf.centro[1], 'ow')

			epocas += 1
			print('Epoca')

		for rbf in self.setRBF:
			pass
			#rbf.setRadio()

		

		print( 'Epocas: ', epocas )


def gaussiana( x, c , r ):
	math.exp( - ( ( x - c ) ** 2 / ( r ** 2 ) ) )
		
