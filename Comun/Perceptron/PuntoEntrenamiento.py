import random as rnd

class PuntoEntrenamiento(object):
	"""docstring for PuntoWntrenamiento"""
	def __init__(self, Entradas, clase):
		self.__Entradas = [-1] + Entradas
		self.__clase = clase
		print(Entradas)
		#self.__peso = peso

	def getEntradas(self): return self.__Entradas
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