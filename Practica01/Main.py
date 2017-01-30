import PuntoEntrenamiento as PE
import matplotlib.pyplot as plt
from pylab import plot,show, norm

plt.style.use('ggplot')

MIN_VAL = -5
MAX_VAL = 5
C_ZERO = 0
LEARNING_RATE = 0.1
X0 = -1
W0 = PE.Input( PE.getRandom( MIN_VAL, MAX_VAL ) )

puntosEntrenamiento = [ PE.PuntoEntrenamiento((-1.,-1.),0.) ]

puntosEntrenamiento.append( PE.PuntoEntrenamiento((-2.,2.) ,0 ) )
puntosEntrenamiento.append( PE.PuntoEntrenamiento((-3.,3.),0 ) )
puntosEntrenamiento.append( PE.PuntoEntrenamiento((-4.,1.),0 ) )
puntosEntrenamiento.append( PE.PuntoEntrenamiento((-2.,0.),0 ) )
puntosEntrenamiento.append( PE.PuntoEntrenamiento((-2.,2.),0 ) )

puntosEntrenamiento.append( PE.PuntoEntrenamiento((2.,2.),1 ) )
puntosEntrenamiento.append( PE.PuntoEntrenamiento((3.,2.),1 ) )
puntosEntrenamiento.append( PE.PuntoEntrenamiento((1.5,2.),1 ) )
puntosEntrenamiento.append( PE.PuntoEntrenamiento((1.,2.),1 ) )
puntosEntrenamiento.append( PE.PuntoEntrenamiento((3.,2.),1 ) )
puntosEntrenamiento.append( PE.PuntoEntrenamiento((2.1,2.),1 ) )

Entradas = ( PE.Input( PE.getRandom( MIN_VAL, MAX_VAL ) ),
			 PE.Input( PE.getRandom( MIN_VAL, MAX_VAL ) ) )


def Training():
	tieneError = True
	iteracion = 0

	while tieneError:
		tieneError = False

		for punto in puntosEntrenamiento:
			salida = None
			suma = X0 * W0.getPeso()
			for i, entrada in enumerate(Entradas):
				suma += punto.getCoordenadas()[i] * entrada.getPeso()

			if suma >= C_ZERO:	
				salida = 1
			else:	
				salida = C_ZERO

			error = punto.getClase() - salida

			print("Error: " + str(error))

			if ( error != C_ZERO ):
				tieneError = True

				W0.setPeso( W0.getPeso() + LEARNING_RATE * error * X0 )
				for i,entrada in enumerate(Entradas):
					peso = entrada.getPeso() + LEARNING_RATE * error * punto.getCoordenadas()[i]
						   
					#print("Peso: " + str(peso))
					entrada.setPeso( peso )

		iteracion += 1
		print("Peso: " + str(W0.getPeso()))
		for entrada in Entradas:
			print("Peso:" + str(entrada.getPeso()) )

		#plot( W0.getPeso(), Entradas )
		print("Iteracion: " + str(iteracion))
		plotTrain(puntosEntrenamiento,Entradas, W0.getPeso())
		#raw_input()
		pass


def plotTrain( puntos, entradas, bias):
	for punto in puntos:
		if punto.getClase() == C_ZERO:
			plot(punto.getCoordenadas()[0],punto.getCoordenadas()[1],'ob')
		else :
			plot(punto.getCoordenadas()[0],punto.getCoordenadas()[1],'or')
		

	WeightArray = [entradas[0].getPeso(), entradas[1].getPeso()]
	X = 5

	n = norm(WeightArray)
	ww = WeightArray / n
	ww1 = [ww[1], -ww[0]]
	ww2 = [-ww[1], ww[0]]
	plot([ww1[0]*X , ww2[0]*X],[ww1[1]*X , ww2[1]*X],'--b')
	show()

if __name__ == '__main__':
	Training()