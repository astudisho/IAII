import sys
if sys.version_info.major >= 3:
	import tkinter as Tk
else:
	import Tkinter as Tk

import ventana

def main():
	v = ventana.Ventana()
	Tk.mainloop()

if __name__ == '__main__':
	main()