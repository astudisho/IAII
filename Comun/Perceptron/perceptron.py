import random as rnd
import PuntoEntrenamiento as pe

C_ZERO = 0
C_M_UNO = -1
C_UNO = 1


class Perceptron(object):
	"""docstring for Perceptron"""
	def __init__(self, pesoMin, pesoMax, dimensiones, learningRate = 0.1):
		super(Perceptron, self).__init__()
		self.pesoMin = pesoMin
		self.pesoMax = pesoMax
		self.pesos = []
		#self.__X0 = -1
		self.tieneError = False
		self.__lR = learningRate
		self.iteraciones = 0

		for i in range(dimensiones + 1):
			self.pesos.append( Perceptron.getRandom( self.pesoMin, self.pesoMax ) )

	def entrenarIteracion(self, punto, claseEsperada ):
		salida = self.respuesta( punto )
		error = claseEsperada - salida
		if ( error != C_ZERO ):
			self.modificaPesos(error,punto)
			self.tieneError = True
		else:
			self.tieneError = False
		return self.tieneError


	def respuesta(self, punto):
		suma = 0
		for i,entrada in enumerate(punto.getEntradas()):
			suma += entrada * self.getPesos()[i]

		if suma < C_ZERO: return C_ZERO
		else: return C_UNO


	def modificaPesos(self, error, punto):
		w = 0
		for i,entrada in enumerate(punto.getEntradas()):
			w = self.pesos[i] + self.__lR * ( error * punto.getEntradas()[i])
			self.pesos[i] = w
		return w

	def getPesos(self):
		return self.pesos

	def setPesos(self, pesos):
		self.pesos = pesos

	@staticmethod	
	def getRandom(min, max):
		return rnd.uniform(min, max)