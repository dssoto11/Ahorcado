"""El clasico juego del ahorcado programado usando python y librerias como tkinter para mostrar 
una interfaz grafica
"""
from tkinter import *
from tkinter.font import *
import random as random
from PIL import ImageTk, Image

#Creando la clase principal del juego, donde se define las dimensiones de la ventana raiz del juego,
#el titulo de la misma y el color de background de la misma
class JuegoDelAhorcado:
    def __init__(self,ventana):
        self.ventana = ventana
        self.ventana.geometry('1400x900')
        self.ventana.title('JUEGO DEL AHORCADO')        
        self.ventana.configure()
        self.ventana.configure(bg='yellow')
        self.inicializar()
    
    #Inicializacion de los sets donde almazenaremos las letras que corresponden tanto a los aciertos
    #como a los desaciertos, asi como el maximo numero de intentos incorrectos que puede tener
    def inicializar(self):
        self.intentos_correctos = set()
        self.intentos_incorrectos = set()     
        self.num_intentos_incorrectos = 9
        self.imagen()
    #Colocacion de la imagen de fondo de la ventana principal
    def imagen(self):
        fuente = Font(family="Roboto Cn", size=30)
        ima = Image.open('imagenes/ahorcado3.png')
        #new_ima = ima.resize((900,506))
        imagen = ImageTk.PhotoImage(ima)
        self.label1 = Label(self.ventana, image=imagen)
        self.label1.image = imagen
        self.label1.place(x=0,y=0)
    #Creacion de los bonones para elegir el nivel de dificultad conque se desea jugar
        grado_dificultad = ['FACIL', 'MEDIO', 'DIFICIL']
        self.elegirdif = Label(self.label1,text='Elija dificultad',fg='blue',font='Helvetica 80 bold').place(x= 400,y=500)
        
        margen=400
        for dificultad in grado_dificultad:
            self.buttond = Button(self.label1, text=dificultad,width=20, height=5,justify=LEFT, command=lambda l=dificultad: self.elegir_dificultad(l),font=f'Helvetica 80 bold',bg='light green')
            self.buttond.place(x=margen,y=580)
            margen += 300
    #Eleccion del archivo que posee las palabras secretas, segun el nivel de dificultad elegido
    def elegir_dificultad(self,dificultad):
        if dificultad == 'FACIL':
            filename = 'documentos/palabras_facil.txt'


        elif dificultad == 'MEDIO':
            filename = 'documentos/palabras_medio.txt'
            
        elif dificultad == 'DIFICIL':
            filename = 'documentos/palabras_dificil.txt'
    
        self.elegir_palabra_secreta(filename)
    #Eleccion de la palabra secreta
    def elegir_palabra_secreta(self,filename):
        with open(filename) as archivo_objeto:
            lineas = archivo_objeto.readlines()
            palabra_secreta = random.choice(lineas)
            self.palabra_secreta = palabra_secreta.upper().strip() 
            self.longitud = len(self.palabra_secreta) 
            
        self.label1.place_forget()
        self.ventana_dibujo()
        
    #Creacion de la ventana sobre la cual dibujaremos el hombre ahorcado
    def ventana_dibujo (self):
        self.ventana2 = Frame(self.ventana,width=400,height=400,bg='white')
        self.ventana2.pack(pady=20)
    #Mostrar la palabra secreta con guiones
        self.mostrar_palabra = Label(self.ventana,text=" _ " * self.longitud,font=('arial',30),bg='white')
        self.mostrar_palabra.pack(pady=10)
        
        self.boton_reinicio = Button(self.ventana,text='REINICIAR',command=self.reiniciar, width=10, height=2,fg='red',bg='light green')
        self.boton_reinicio.pack(pady=10)
        
        self.botones_del_alfabeto()
    #creacion de los botones con todas las letras del alfabeto, para ir eligiendo las letras 
    def botones_del_alfabeto(self):
        alfabeto = 'ABCDEFGHIJKLMNÑOPQRSTUVXYZ'
        self.primera_mitad = alfabeto[:13]
        self.segunda_mitad = alfabeto[13:]

        self.ventana_botones_alfabeto = Frame(self.ventana)
        self.ventana_botones_alfabeto.pack(pady=40)

        self.ventana_primera_mitad = Frame(self.ventana_botones_alfabeto)
        self.ventana_primera_mitad.pack()
        self.ventana_segunda_mitad = Frame(self.ventana_botones_alfabeto)
        self.ventana_segunda_mitad.pack()

        for letra in self.primera_mitad:
            botton = Button(self.ventana_primera_mitad, text=letra, command=lambda l=letra: self.adivinar_letra(l), width=6, height=3,font=('arial',18),fg='black',bg='light green')
            botton.pack(side='left',padx=2,pady=2)

        for letra in self.segunda_mitad:
            botton = Button(self.ventana_segunda_mitad, text=letra, command=lambda l=letra: self.adivinar_letra(l), width=6, height=3,font=('arial',18),fg='black',bg='light green')
            botton.pack(side='left',padx=2,pady=2)
      

    #Comparacion de las letras elegidas con la palabra secreta, almazenamos en los sets de intentos correctos
    #o incorrectos segun sea el caso, de ser incorrectos vamos restando el numero de intentos incorrectos, y 
    def adivinar_letra(self,letra):
        if letra in self.palabra_secreta and letra not in self.intentos_correctos:
            self.intentos_correctos.add(letra)
        elif letra not in self.intentos_incorrectos:
            self.intentos_incorrectos.add(letra)
            self.num_intentos_incorrectos -= 1
            self.actualizar_dibujo_ahorcado_dificil()
    
    #Vamos chequeamos si el juego se gano o se perdio
        self.actualizar_mostrar_palabra()
        self.chequear_condicion_ganadora()
    #Vamos actualizando la palabra mostrada, segun vamos adivinando letras
    def actualizar_mostrar_palabra(self):
        mostrar_palabra = " ".join([letra if letra in self.intentos_correctos else "_" for letra in self.palabra_secreta])
        self.mostrar_palabra.config(text=mostrar_palabra)        
    
    #Vamos chequeamos si el juego se gano o se perdio
    def chequear_condicion_ganadora(self): 
        if set(self.palabra_secreta).issubset(self.intentos_correctos):
            self.mostrar_mensajes('FELICIDADES!, HA GANADO EL JUEGO')
        elif self.num_intentos_incorrectos == 0:
            self.mostrar_mensajes(f'LO SENTIMOS!, HA CONSUMIDO TODOS LOS INTENTOS, LA PALABRA SECRETA ERA {self.palabra_secreta}')

    # y mostramos el mensaje correspondiente en cada caso
    def mostrar_mensajes(self,mensaje):
        self.ventana_botones_alfabeto.pack_forget() # quitar botones del alfabero para mostrar mensajes
        self.mensajes_fin_juego = Label(self.ventana,text=mensaje,fg= 'red')
        self.mensajes_fin_juego.pack(pady=15)

    # vamos actualizando el dibujo del hombre ahorcado, segun el numero de intentos incorrectos
    def actualizar_dibujo_ahorcado_dificil(self):
        dibujar = [self.cuerpo,self.pie_izquierdo, self.pie_derecho,self.brazo_derecho,self.brazo_izquierdo,self.palo_vertical,self.palo_arriba,self.soga,self.cabeza]
        for i in range(len(self.intentos_incorrectos)):
            if i < len(self.intentos_incorrectos):
              dibujar[i]()
    """
    def actualizar_dibujo_ahorcado_medio(self):
        dibujar = [self.pie_izquierdo, self.pie_derecho,self.brazo_derecho,self.brazo_izquierdo,self.cabeza,self.cuerpo,[self.palo_vertical,self.palo_arriba,self.soga]]
        for i in range(len(self.intentos_incorrectos)):
            if i < len(self.intentos_incorrectos):
              dibujar[i]()

    def actualizar_dibujo_ahorcado_facil(self):
        dibujar = [self.cuerpo,self.pie_izquierdo, self.pie_derecho,self.brazo_derecho,self.brazo_izquierdo,[self.palo_vertical,self.palo_arriba,self.soga,self.cabeza]]
        for i in range(len(self.intentos_incorrectos)):
            if i < len(self.intentos_incorrectos):
              dibujar[i]()
    """
    #mostramos la foto de cada parte del hombre ahorcado 
    def cabeza(self):
        ima = Image.open('imagenes/cabeza.png')
        new_ima = ima.resize((100,96))
        imagen = ImageTk.PhotoImage(new_ima)
        cabeza = Label(self.ventana2, image=imagen)
        cabeza.image = imagen
        cabeza.place(x=213,y=137)
    def cuerpo (self):
        ima = Image.open('imagenes/cuerpo.png')
        imagen = ImageTk.PhotoImage(ima)
        cuerpo = Label(self.ventana2, image=imagen)
        cuerpo.image = imagen
        cuerpo.place(x=256.5,y=233)
    def pie_izquierdo (self):
        ima = Image.open('imagenes/pie_izquierdo.png')
        imagen = ImageTk.PhotoImage(ima)
        pie_izquierdo = Label(self.ventana2, image=imagen)
        pie_izquierdo.image = imagen
        pie_izquierdo.place(x=180,y=310)
    def pie_derecho (self):
        ima = Image.open('imagenes/pie_derecho.png')
        imagen = ImageTk.PhotoImage(ima)
        pie_derecho = Label(self.ventana2, image=imagen)
        pie_derecho.image = imagen
        pie_derecho.place(x=264,y=310)
    def brazo_derecho (self):
        ima = Image.open('imagenes/brazo_derecho.png')
        new_ima = ima.resize((63,70))
        imagen = ImageTk.PhotoImage(new_ima)
        brazo_derecho = Label(self.ventana2, image=imagen)
        brazo_derecho.image = imagen
        brazo_derecho.place(x=269,y=233)
    def brazo_izquierdo (self):
        ima = Image.open('imagenes/brazo_izquierdo.png')
        new_ima = ima.resize((63,70))
        imagen = ImageTk.PhotoImage(new_ima)
        brazo_izquierdo = Label(self.ventana2, image=imagen)
        brazo_izquierdo.image = imagen
        brazo_izquierdo.place(x=196,y=233)
    def palo_vertical (self):
        ima = Image.open('imagenes/palo_vertical.png')
        new_ima = ima.resize((111,380))
        imagen = ImageTk.PhotoImage(new_ima)
        palo_vertical = Label(self.ventana2, image=imagen)
        palo_vertical.image = imagen
        palo_vertical.place(x=20,y=10)
    def palo_arriba (self):
        ima = Image.open('imagenes/palo_arriba.png')
        #new_ima = ima.resize((100,96))
        imagen = ImageTk.PhotoImage(ima)
        palo_arriba = Label(self.ventana2, image=imagen)
        palo_arriba.image = imagen
        palo_arriba.place(x=37,y=20)
    def soga (self):
        ima = Image.open('imagenes/soga.png')
        imagen = ImageTk.PhotoImage(ima)
        soga = Label(self.ventana2, image=imagen)
        soga.image = imagen
        soga.place(x=250,y=58)

    def reiniciar (self):
        self.intentos_correctos = set()
        self.intentos_incorrectos = set()     
        self.num_intentos_incorrectos = 9
        self.mostrar_palabra.pack_forget()
        self.actualizar_dibujo_ahorcado_dificil()
        self.inicializar()
        self.ventana_botones_alfabeto.pack_forget()
        self.ventana2.pack_forget()
        self.boton_reinicio.pack_forget()
        self.mensajes_fin_juego.pack_forget()

    



 

def main():
    root = Tk()
    app = JuegoDelAhorcado(root)
    root.mainloop()

if __name__ == '__main__':
    main()