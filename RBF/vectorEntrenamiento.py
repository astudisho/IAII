import random as rnd
import math
import numpy as np

class VectorEntrenamiento():
	def __init__(self, coordenadas, clase):
		self.coordenadas = coordenadas
		self.clase = clase
		
	def getCoordenadas(self): return self.coordenadas
	def getClase(self): return self.clase

class Entrada():
	def __init__(self, valor):
		self.valor = valor
	
	def setValor(self, valor): self.valor = valor
	def getValor(self): return self.valor

def getRandom(min, max):
	return rnd.uniform(min, max)

def logsig(x):
	return 1 / (1 + math.exp(-x))

def logsig_array(array):
	x = np.array([logsig(value) for value in array]).reshape((len(array), 1))
	return x
	