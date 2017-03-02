import random as rnd

class PuntoEntrenamiento(object):
	"""docstring for PuntoWntrenamiento"""
	def __init__(self, coordenadas, clase):
		self.__coordenadas = coordenadas
		self.__clase = clase
		print(coordenadas)
		#self.__peso = peso

	def getCoordenadas(self): return self.__coordenadas
	def getClase(self): return self.__clase
	#def getPeso(self): return self.__peso
	#def setPeso(self, val): self.__peso = val

class Input(object):
	"""docstring for Input"""
	def __init__(self, peso):
		super(Input, self).__init__()
		self.__peso = peso

	def getPeso(self): return self.__peso
	def setPeso(self, val): self.__peso = val

def getRandom(min, max):
	return rnd.uniform(min, max)