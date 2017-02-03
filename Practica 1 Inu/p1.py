import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import numpy as np
import random
import Tkinter as Tk

MIN = -5
MAX = 5

root = Tk.Tk()
root.wm_title("Perceptron")

fig = plt.figure()
ax = fig.add_subplot(111)
vectoresEntrenamiento = []
W0 = random.uniform(MIN,MAX)
W1 = random.uniform(MIN,MAX)
W2 = random.uniform(MIN,MAX)
maxEpocas = Tk.StringVar()
lr = Tk.StringVar()
estado = Tk.StringVar()

class vEntrenamiento():
	def __init__(self, x, y, clase):
		self.x = x
		self.y = y
		self.xy = np.array([x, y])
		self.clase = clase
	def getClase(self):
		return self.clase


def main():
	setPlot()
	Tk.mainloop()
	
	
def setPlot():
	ax.set_xlim([MIN,MAX])
	ax.set_ylim([MIN,MAX])
	ax.grid()
	ax.axvline(0, color="black")
	ax.axhline(0, color="black")
	canvas = FigureCanvasTkAgg(fig, master=root)
	canvas.mpl_connect('button_press_event', plot)
	canvas.show()
	canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
	toolbar = NavigationToolbar2TkAgg(canvas, root)
	toolbar.update()
	canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
	btnQuit = Tk.Button(master=root, text="Salir", command=_quit)
	btnQuit.pack(side=Tk.BOTTOM)
	lblLr = Tk.Label(master=root, text="Learning rate: ")
	lblLr.pack(side=Tk.LEFT)
	entryLr = Tk.Entry(master=root, bd=5, textvariable=lr)
	entryLr.pack(side=Tk.LEFT)
	lblEpocas = Tk.Label(master=root, text="Epocas: ")
	lblEpocas.pack(side=Tk.LEFT)
	entryEpocas = Tk.Entry(master=root, bd=5, textvariable=maxEpocas)
	entryEpocas.pack(side=Tk.LEFT)
	btnEntrenar = Tk.Button(master=root, text="Entrenar", command=entrenar)
	btnEntrenar.pack(side=Tk.RIGHT)
	lblEstado = Tk.Label(master=root, text="Configurando")
	lblEstado.pack(side=Tk.TOP)

def entrenar():
	print("lr = " + lr.get())
	print("epocas = " + str(maxEpocas))
	global W0
	global W1
	global W2
	entrenado = False
	limiteEpocas = False
	epocas = 0
	while not entrenado:
		entrenado = True
		for vector in vectoresEntrenamiento:
			salida = None
			wx = W0*-1
			wx += W1*vector.x
			wx += W2*vector.y
			if wx >= 0:
				salida = 1
			else :
				salida = 0
			
			error = vector.getClase() - salida
			
			print("Error: " + str(error))
			
			if error!= 0:
				entrenado = False
				W0 = W0 + (float(lr.get())*error*-1)
				W1 = W1 + (float(lr.get())*error*vector.x)
				W2 = W2 + (float(lr.get())*error*vector.y)
				print("W0 = " + str(W0))
				print("W1 = " + str(W1))
				print("W2 = " + str(W2))
			plotPesos()
			
		if epocas == int(maxEpocas.get()):
			entrenado = True
			limiteEpocas = True
		epocas += 1
		print("Epoca: " + str(epocas) + "\n")
	if limiteEpocas:
		estado.set("Se ha llegado al limite de epocas")
	else:
		if entrenado:
			estado.set("Entrenado")
	
def plot(event):
	if(event.xdata is None or event.ydata is None):
			return
	button = event.button
	if button == 1:
		ax.plot(event.xdata, event.ydata, 'ro', color='red')
		vE = vEntrenamiento(event.xdata, event.ydata, 1)
		vectoresEntrenamiento.append(vE)	
	if button == 3:
		ax.plot(event.xdata, event.ydata, '^', color='blue')
		vE = vEntrenamiento(event.xdata, event.ydata, 1)
		vectoresEntrenamiento.append(vE)
	fig.canvas.draw()

def plotPesos():
	x = np.array(range(MIN,MAX))
	y = eval('('+str(W0)+'/'+str(W2)+')-(('+str(W1)+'/'+str(W2)+')*x)')
	ax.plot(x,y, color='green')
	fig.canvas.draw()

def _quit():
	root.quit()
	root.destroy()
	
if __name__ == '__main__':
	main()