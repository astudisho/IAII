import random as rnd

C_ZERO = 0
C_M_UNO = -1
C_UNO = 1


class Perceptron(object):
	"""docstring for Perceptron"""
	def __init__(self, pesoMin, pesoMax, dimensiones, 
				 maxEpocas = 100, setEntrenamiento = [], 
				 learningRate = 0.1):
		super(Perceptron, self).__init__()
		self.setEntrenamiento = setEntrenamiento
		self.pesoMin = pesoMin
		self.pesoMax = pesoMax
		self.pesos = []
		self.maxEpocas = maxEpocas
		self.__X0 = -1
		self.tieneError = True
		self.__lR = learningRate

		for i in range(dimensiones + 1):
			self.pesos.append( Perceptron.getRandom( self.pesoMin, self.pesoMax ) )

	def entrenarIteracion(self, punto ):
		salida = respuesta( punto )

	def respuesta(self, punto):
		suma = 0
		for i,p in enumerate(punto):
			if i == C_ZERO: 
				suma += self.__X0 * self.getPesos()[i]
			else:
				suma += self.p.getCoordenada() * self.getPesos()[i]

		if suma < C_ZERO: return C_ZERO
		else: return C_UNO

	def modificaPesos(self, error):
		for i in range()

	def getPesos(self):
		return self.pesos

	def setPesos(self, pesos):
		self.pesos = pesos

	@staticMethod
	def getRandom(min, max):
		return rnd.uniform(min, max)