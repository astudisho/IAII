import perceptron as p
import PuntoEntrenamiento as pe
import random as rnd
import numpy as np
import matplotlib as plt
from pylab import plot,show, norm, ylim, xlim, grid, axvline, axhline

def plotTrain( puntos, neurona):
	for punto in puntos:
		if punto.getClase()[0] == 0:
			plot(punto.getEntradas()[1],punto.getEntradas()[2],'ob')
		else :
			plot(punto.getEntradas()[1],punto.getEntradas()[2],'or')


	WeightArray = [neurona[0].pesos[1], neurona[0].pesos[2]]
	X = 5

	ylim([-5,5])
	xlim([-5,5])
	grid()
	axvline(0, color="black")
	axhline(0, color="black")

	'''n = norm(WeightArray)
				ww = WeightArray / n
				ww1 = [ww[1], -ww[0]]
				ww2 = [-ww[1], ww[0]]
				plot([ww1[0]*X , ww2[0]*X],[ww1[1]*X , ww2[1]*X],'--b')'''

	#Alternativa
	x = np.array(range(-5,5))
	y = eval( '(' + str(neurona[0].pesos[0])+'/'+str(WeightArray[1]) + ')-((' +str(WeightArray[0])+'/'+str(WeightArray[1]) + ')*x)' )
	plot(x,y,'--b')

	show()

#rnd.seed(1920)

class RedNeuronal(object):
	"""docstring for RedUnitaria"""
	def __init__(self, setEntrenamiento,maxEpocas = 100,numeroNeuronas = 1, 
				 pMin = -1, pMax = 1, dimensiones = 2, lr = 0.1):
		super(RedNeuronal, self).__init__()
		self.maxEpocas = maxEpocas
		self.setEntrenamiento = setEntrenamiento

		self.redNeuronal = []

		for i in range(numeroNeuronas):
			self.redNeuronal.append(p.Perceptron(pMin,pMax,dimensiones, lr))


	def training(self):
		tieneError = True
		iteracion = 0

		while tieneError and iteracion <= self.maxEpocas:
			tieneError = False
			for i,neurona in enumerate(self.redNeuronal):
				for punto in self.setEntrenamiento:
					if neurona.entrenarIteracion(punto,punto.getClase()[i]):
						tieneError = True

			iteracion += 1
			print('iteracion: ' + str(iteracion))
			plotTrain(self.setEntrenamiento,self.redNeuronal)




setEntrenamiento = []
pesoMin = 5
pesoMax = -5
dimensiones = 2
maxEpocas = 100
setEntrenamiento = []
learningRate = 0.1

setEntrenamiento.append(pe.PuntoEntrenamiento( [0,1], [1] ))
setEntrenamiento.append(pe.PuntoEntrenamiento( [0,2], [1] ))
setEntrenamiento.append(pe.PuntoEntrenamiento( [0,3], [1] ))
setEntrenamiento.append(pe.PuntoEntrenamiento( [-1,1], [1] ))
setEntrenamiento.append(pe.PuntoEntrenamiento( [-3,3], [1] ))
setEntrenamiento.append(pe.PuntoEntrenamiento( [-2,1], [1] ))
setEntrenamiento.append(pe.PuntoEntrenamiento( [-4,1], [1] ))
setEntrenamiento.append(pe.PuntoEntrenamiento( [-1,2], [1] ))

setEntrenamiento.append(pe.PuntoEntrenamiento( [2,1], [0] ))
setEntrenamiento.append(pe.PuntoEntrenamiento( [1,2], [0] ))
setEntrenamiento.append(pe.PuntoEntrenamiento( [2,3], [0] ))
setEntrenamiento.append(pe.PuntoEntrenamiento( [3,1], [0] ))
setEntrenamiento.append(pe.PuntoEntrenamiento( [3,3], [0] ))
setEntrenamiento.append(pe.PuntoEntrenamiento( [2,1], [0] ))
setEntrenamiento.append(pe.PuntoEntrenamiento( [4,1], [0] ))
setEntrenamiento.append(pe.PuntoEntrenamiento( [1,2], [0] ))

a = RedNeuronal( setEntrenamiento,pMin=-5,pMax=5 )
a.training()

print("Pruebas")
print(a.redNeuronal[0].respuesta(pe.PuntoEntrenamiento( [3,2], [] )))
print(a.redNeuronal[0].respuesta(pe.PuntoEntrenamiento( [-3,2], [] )))
print(a.redNeuronal[0].respuesta(pe.PuntoEntrenamiento( [-3,3], [] )))