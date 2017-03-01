import perceptron as p
import PuntoEntrenamiento as pe

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

		while tieneError or iteracion >= self.maxEpocas:
			tieneError = False
			for i,neurona in enumerate(self.redNeuronal):
				for punto in self.setEntrenamiento:
					if neurona.entrenarIteracion(punto,punto.getClase()[i]):
						tieneError = True

			iteracion += 1
			print('Bla')


setEntrenamiento = []
pesoMin = 5
pesoMax = -5
dimensiones = 2
maxEpocas = 100
setEntrenamiento = []
learningRate = 0.1

pe0 = pe.PuntoEntrenamiento( [0,1], [1] )
RedNeuronal( [pe0] ).training()