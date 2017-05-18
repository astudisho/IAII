#RBF

import math
import random
import vectorEntrenamiento as vE
import numpy as np

MAX_INT = 100000

class Cluster(object):
	"""docstring for Cluster"""
	def __init__(self, dimensiones, coordenadas):
		super(Cluster, self).__init__()
		self.dimensiones = dimensiones

		#self.centro = [-1 ] * dimensiones
		self.centro = coordenadas
		self.radio = -1
		self.setCluster = []
		self.sigma = 0
		self.beta = 0

	def getCentro(self): return self.centro

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

			if(len(self.setCluster)) == 0: pass
			else: resultado[i] = suma / float( len( self.setCluster ) )

		return resultado

	def setRadio(self):
		# PROMEDIO
		# suma = 0
		# for cluster in self.setCluster:
		# 	suma += self.calcularDistancia( cluster.getCoordenadas() )
        #
		# if len( self.setCluster ) > 0 :
		# 	self.radio = suma / len( self.setCluster )
        #
		# else:
		# 	self.radio = 0.1

		#MAS LEJANO
		aux = [ 0.25 ]
		for cluster in self.setCluster:
		 	aux.append( self.calcularDistancia( cluster.getCoordenadas() ) )

		self.radio = max(aux)
        #
		# if len( self.setCluster ) > 0 :
		# 	self.radio = suma / len( self.setCluster )
        #
		# else:
		# 	self.radio = 0.1

		#self.sigma = self.calcularDistancia( masLejano.getCoordenadas() )

		# self.beta = 1 / ( 2 * self.sigma ** 2 )

		return self.radio


class RBF(object):
	"""docstring for RBF"""
	def __init__(self, trainingSet, grafica,  clusterSet = None):
		super(RBF, self).__init__()
		self.trainingSet = trainingSet
		self.dimensiones = len( trainingSet[0].getCoordenadas() )

		print("Dimensiones: ", self.dimensiones)
		self.setRBF = clusterSet

		self.grafica = grafica
		#self.numRbf = int ( 2 * len( trainingSet ) / 3 )

		# #for i in range( self.dimensiones ):
		# for i in range(  self.numRbf ):
		# 	self.setRBF.append( Cluster( self.dimensiones ) )

		# for index,vector in enumerate ( random.sample( trainingSet, self.numRbf ) ):
		# 	self.setRBF[ index ].centro = vector.getCoordenadas()

		print( self.setRBF[0].centro )

		self.iniciarClustering()

	def iniciarClustering(self):
		detectoCambios = True
		epocas = 1

		while detectoCambios:

			detectoCambios = False		

			for vector in self.trainingSet:
				rbfGanador = self.setRBF[0]
				distanciaMin = MAX_INT

				for rbf in self.setRBF:
					#print( 'Distancia: ' , rbf.centro , ' --> ' ,vector.getCoordenadas() )
					distancia = rbf.calcularDistancia( vector.getCoordenadas() )
					#print( distancia )
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
					rbf.setRadio()
					print('Sigue')

				rbf.reset()
			epocas += 1
			print('Epoca')

		self.grafica.clear()

		for rbf in self.setRBF:
			print('Ploteando')
			self.grafica.plotCircle( rbf.getCentro(), rbf.radio )
			self.grafica.plotMapeo( rbf.getCentro()[0], rbf.getCentro()[1], 'xr' )

		for v in self.trainingSet:
			self.grafica.plotMapeo( v.getCoordenadas()[0], v.getCoordenadas()[1], 'og' )

		self.grafica.canvas.draw()


		print( 'Epocas: ', epocas )


def gaussiana( x, c , r ):
	math.exp( - ( ( x - c ) ** 2 / ( r ** 2 ) ) )


#Resultado de la gaussiana es -->	0(rj)
#Wkj --> random
#Omega --> 1

#Incremento de los pesos --> lr( deseada - zk ) gaussiana( rj )

def gaussian(beta, x, centro):
	x_array = np.array([value for value in x])
	centro_array = np.array([value for value in centro])
	return np.exp((-1*beta)*(np.linalg.norm(x_array - centro_array)**2))
