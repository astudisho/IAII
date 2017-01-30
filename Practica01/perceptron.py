#!/usr/bin/python

# reference => http://glowingpython.blogspot.com/2011/10/perceptron.html

from pylab import rand,plot,show,norm

RANGO = 0.5

def generateData(n):
	"""
	generates a 2D linearly separable dataset with n samples, where the third element is the label
	"""
	xb = ( rand( n ) * 2 - 1 ) / 2 - RANGO
	yb = ( rand( n ) * 2 - 1 ) / 2 + RANGO
	xr = ( rand( n ) * 2 - 1 ) / 2 + RANGO
	yr = ( rand( n ) * 2 - 1 ) / 2 - RANGO

	inputs = []

	for i in range(len(xb)):
		inputs.append([xb[i],yb[i],1])
		inputs.append([xr[i],yr[i],-1])
	return inputs

class Perceptron:
	def __init__(self):
		self.w = rand(2)*2-1
		self.learningRate = 0.1

	def response(self,x):
		y = x[0]*self.w[0]+x[1]*self.w[1]
		if y >= 0:
			return 1
		else:
			return -1

	def updateWeights(self,x,iterError):
		"""
		w(t+1) = w(t) + learningRate * (d-r) * x where d is desired output, 
		r is the perceptron response and (d-r) is the iteration error
		"""
		self.w[0] += self.learningRate*iterError*x[0]
		self.w[1] += self.learningRate*iterError*x[1]

	def train(self,data):
		"""
		Every vector in data must have three elements, the third element (x[2]) 
		must be the label
		"""
		learned = False
		iteration = 0
		while not learned:
			globalError = 0.0
			for x in data:
				r = self.response(x)    
				if x[2] != r:
					iterError = x[2] - r
					self.updateWeights(x,iterError)
					globalError += abs(iterError)
				iteration += 1
				if globalError == 0.0 or iteration >= 100:
					print 'iterations',iteration
					learned = True

	@staticmethod
	def main():
		trainset = generateData(30)
		testset = generateData(20)
		
		perceptron = Perceptron()
		perceptron.train(trainset)
		for x in testset:
			r = perceptron.response(x)
			if r != x[2]:
				print 'error'
			if r == 1:
				plot(x[0],x[1],'ob')
			else:
				plot(x[0],x[1],'or')


		# plot of the separation line, which is orthogonal to w
		n = norm(perceptron.w)
		print("Perceptron w: ",perceptron.w)
		print("Norm: ", n)
		ww = perceptron.w/n
		ww1 = [ww[1], -ww[0]]
		ww2 = [-ww[1], ww[0]]
		plot([ww1[0], ww2[0]],[ww1[1], ww2[1]],'--g')
		show()

if __name__ == '__main__':
	Perceptron.main()