"""El clasico juego del ahorcado programado usando python y librerias como tkinter para mostrar 
una interfaz grafica
"""
from tkinter import *
from tkinter import font
import random as random
from PIL import ImageTk, Image
import Juego_del_ahorcado_dificil as jd
import Juego_del_ahorcado_facil as jf
import Juego_del_ahorcado_medio as jm

#Creando la clase principal del juego, donde se define las dimensiones de la ventana raiz del juego,
#el titulo de la misma y el color de background de la misma
class Juego:
    def __init__(self,ventana):
        self.ventana = ventana
        #Inizializando tipo de fuente para todo el juego
        self.defaultFont = font.nametofont("TkDefaultFont") 
        self.defaultFont.configure(family="ALiberationSans-Italic", size=19, weight=font.BOLD)

        self.ventana.geometry('1280x720')      
        self.imagen()

    #Colocacion de la imagen de fondo de la ventana principal
    def imagen(self):
        ima = Image.open('imagenes\\ahorcado3.png')
        imagen = ImageTk.PhotoImage(ima)
        self.label1 = Label(self.ventana, image=imagen)
        self.label1.image = imagen
        self.label1.place(x=0,y=0)
    #Creacion de los botones para elegir el nivel de dificultad conque se desea jugar
        grado_dificultad = ['FACIL', 'MEDIO', 'DIFICIL']
        self.elegirdif = Label(self.label1,text='Elija dificultad',font=f'Helvetica 20 bold',bg='light green').place(x= 500,y=500)
        
        margen=200
        for dificultad in grado_dificultad:
            self.buttond = Button(self.label1, text=dificultad,width=10, height=3, command=lambda l=dificultad: self.elegir_dificultad(l),font=f'Helvetica 20 bold',bg='light green')
            self.buttond.place(x=margen,y=580)
            margen += 300
    #Eleccion del archivo que posee las palabras secretas, segun el nivel de dificultad elegido
    def elegir_dificultad(self,dificultad):
        if dificultad == 'FACIL':
            self.label1.place_forget()
            jf.JuegoDelAhorcado(self.ventana)

        elif dificultad == 'MEDIO':
            self.label1.place_forget()
            jm.JuegoDelAhorcado(self.ventana)
            
        elif dificultad == 'DIFICIL':
            self.label1.place_forget()
            jd.JuegoDelAhorcado(self.ventana)
            
        

def main():
    
    root = Tk()
    app = Juego(root)
    root.mainloop()

if __name__ == '__main__':
    main()
    
