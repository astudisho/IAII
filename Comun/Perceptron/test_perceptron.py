#Test perceptron

import perceptron as perceptron
import PuntoEntrenamiento as pe

pe0 = pe.PuntoEntrenamiento( [0,1], 1 )

p = perceptron.Perceptron( 0, 1, 2 )
print(p.getPesos())
print(perceptron.Perceptron.getRandom( 0, 1 ) )
print(p.respuesta( pe0 ) )
print(p.modificaPesos( 1, pe0 ) )
print(p.entrenarIteracion( pe0, 0) )