#RBF

import math
import random
import vectorEntrenamiento as vE
import numpy as np

MAX_INT = 100000

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
	def __init__(self, trainingSet):
		super(RBF, self).__init__()
		self.trainingSet = trainingSet
		self.dimensiones = len( trainingSet[0].getCoordenadas() )
		print("Dimensiones: ", self.dimensiones)
		self.setRBF = []
		self.numRbf = int ( 2 * len( trainingSet ) / 3 )

		#for i in range( self.dimensiones ):
		for i in range(  self.numRbf ):
			self.setRBF.append( Cluster( self.dimensiones ) )
			print('a')

		for index,vector in enumerate ( random.sample( trainingSet, self.numRbf ) ):
			self.setRBF[ index ].centro = vector.getCoordenadas()
			print('b')

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
					print('Sigue')

				rbf.reset()
			epocas += 1
			print('Epoca')

		for rbf in self.setRBF:
			pass
			#rbf.setRadio()

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

if __name__ == '__main__':
	trainingSet = []
	
	trainingSet.append( vE.VectorEntrenamiento([0,3],0) )
	trainingSet.append( vE.VectorEntrenamiento([1,2],0) )
	trainingSet.append( vE.VectorEntrenamiento([3,3],0) )
	trainingSet.append( vE.VectorEntrenamiento([0,4],0) )
	trainingSet.append( vE.VectorEntrenamiento([1,5],0) )
	trainingSet.append( vE.VectorEntrenamiento([3,6],0) )


	trainingSet.append( vE.VectorEntrenamiento([2,3],1) )
	trainingSet.append( vE.VectorEntrenamiento([-2,2],1) )
	trainingSet.append( vE.VectorEntrenamiento([-3,3],1) )

	rbf = RBF( trainingSet )