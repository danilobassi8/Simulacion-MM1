import numpy as np
import random as rand
import math
import os

os.system("cls") #para limpiar la pantalla al iniciar.
class RutinaInicio:
    def Inicializacion():
        global clock
        global estadoServidor
        global numeroDeClientesEnCola
        global tiempoDeArrivos
        global tiempoUltimoEvento
        global NCCD
        global acumuladoDemora
        global areaBajoQT
        global areaBajoBT

        global contadorDelSistema #esta la use para mostrar el numero de tabla solamente.
        contadorDelSistema = 0
        #la lista de eventos fue tratada
        #como clase por comodidad
        clock = 0
        estadoServidor = 0
        numeroDeClientesEnCola = 0
        tiempoDeArrivos = []
        tiempoUltimoEvento = 0
        NCCD = 0
        acumuladoDemora = 0
        areaBajoQT = 0
        areaBajoBT = 0
        ListaEventos.tiempoArribo = LibreriaDeRutinas.generaTiempoArrivo()
        ListaEventos.tiempoPartida = 999999999999999999 #para q no salga ese num.
class ListaEventos(object):
    tiempoArribo = 0
    tiempoPartida = 0

    mediaArribos = 5
    mediaPartida = 2        

class RutinaDeAvanceEnElTiempo:
    def ProximoEvento():
        global tiempoDeArrivos,clock

        nextEvent = "variable a rellenar con un evento-"

        
        if(ListaEventos.tiempoPartida > ListaEventos.tiempoArribo):
            nextEvent = Arrivo()
        else:
            nextEvent = Partida()
        

        clock = min([ListaEventos.tiempoArribo,ListaEventos.tiempoPartida])
        return nextEvent


    

class LibreriaDeRutinas:
    def generarNumeroAleatorio():
        return rand.uniform(0,1)

    def generaTiempoArrivo():
        r = LibreriaDeRutinas.generarNumeroAleatorio()
        return -1 * ListaEventos.mediaArribos * math.log(r,math.e)
    def generarTiempoPartida():
        r = LibreriaDeRutinas.generarNumeroAleatorio()
        return -1 * ListaEventos.mediaPartida * math.log(r,math.e)

class Arrivo:
    tiempoOcurrencia = -1
    nombre = "Evento: Arrivo"  #CUIDADO!  si se cambia, cambiar en Graficar()
    def __init__(self):
        global clock
        self.tiempoOcurrencia = ListaEventos.tiempoArribo
        


    def RutinaEventos(self):
        global estadoServidor,tiempoDeArrivos,tiempoUltimoEvento, contadorDelSistema,clock,NCCD,acumuladoDemora
        #actualiza estado del sistema
        
        

         
        if(estadoServidor == 1):            #servidor ocupado.
            if(self in tiempoDeArrivos): #si esta en la lista de los arrivos pendientes.
                tiempoDeArrivos.remove(self)
            else:
                tiempoDeArrivos.append(self)
        else:                               #servidor desocupado
            estadoServidor = 1

        tiempoUltimoEvento = self.tiempoOcurrencia
            
        #cambia contadores estadisticos

        #genera futuros eventos y actualiza estado del sistema.
        
        if(self.nombre == "Evento: Arrivo"):  
            ListaEventos.tiempoArribo = LibreriaDeRutinas.generaTiempoArrivo() + clock
            if(contadorDelSistema == 1): #si es la primera vez, tengo q generar el timpo de salida tmb
                ListaEventos.tiempoPartida = LibreriaDeRutinas.generarTiempoPartida() + clock
            if(ListaEventos.tiempoPartida == 999999999999999999): #si ya habia anulado la partida.
                ListaEventos.tiempoPartida = LibreriaDeRutinas.generarTiempoPartida() + clock
        else:                               #si es de la cola al servidor.
            tiempoUltimoEvento = clock
            NCCD = NCCD + 1
            acumuladoDemora = acumuladoDemora + (clock - self.tiempoOcurrencia)





        GraficarEstadoDelSistema(self)


class Partida:
    tiempoOcurrencia = -1
    nombre = "Evento: Partida" #CUIDADO!  si se cambia, cambiar en Graficar()
    def __init__(self):
        global clock
        self.tiempoOcurrencia = ListaEventos.tiempoPartida
        

    def RutinaEventos(self):
        global estadoServidor,tiempoDeArrivos,tiempoUltimoEvento,clock
        activaOtroEvento = False

        #cambia el estado del sistema
        if(len(tiempoDeArrivos) == 0): #si no quedan arrivos por venir en la lista.
            estadoServidor = 0
        else:
            activaOtroEvento = True

        tiempoUltimoEvento = self.tiempoOcurrencia

        #actualiza contadores estadisticos

        #genera futuros eventos y los agrega a la lista de eventos.
        if(len(tiempoDeArrivos) != 0):
            ListaEventos.tiempoPartida = LibreriaDeRutinas.generarTiempoPartida() + clock
        else:
            ListaEventos.tiempoPartida = 999999999999999999

        GraficarEstadoDelSistema(self)

        if(activaOtroEvento):
            proxEvento = tiempoDeArrivos[0]
            proxEvento.nombre = "Evento: De la cola al Servidor." #CUIDADO!  cambiar en Graficar()
            proxEvento.RutinaEventos()





    


def GraficarEstadoDelSistema(objProxEvent):
     global clock
     global estadoServidor
     global numeroDeClientesEnCola
     global tiempoDeArrivos
     global tiempoUltimoEvento
     global NCCD
     global acumuladoDemora
     global areaBajoQT
     global areaBajoBT
     global contadorDelSistema     
     
     numeroDeClientesEnCola = len(tiempoDeArrivos)
     #----------------------------------------------------------------------------------------------------#
     print("\u001b[35m#---------------------------------------------\u001b[35;1m[" + str(contadorDelSistema) + "]\u001b[0m\u001b[35m----------------------------------------------------#\u001b[0m")
     
     if(contadorDelSistema == 0):
         print("\u001b[37m Evento: \u001b[32m INICIALIZACION DEL SISTEMA")
     else:
         if(objProxEvent.nombre == "Evento: Arrivo"):
             print("\u001b[32mEvento:\u001b[37m Arribo")
         else:
             if(objProxEvent.nombre == "Evento: De la cola al Servidor."):
                print("\u001b[32mEvento:\u001b[37m De la cola al Servidor.")
             else:   
                print("\u001b[32mEvento:\u001b[37m Partida")



     print()
     print("\u001b[32mReloj: \u001b[37m" + str(clock))
     if(estadoServidor == 0):
         print("\u001b[32mEstado del Servidor: \u001b[37mDesocupado")
     else:
         print("\u001b[32mEstado del Servidor: \u001b[37mOcupado")

     print("\u001b[32mNumero de Clientes en Cola: \u001b[37m", str(numeroDeClientesEnCola))
     
     print("\u001b[34m")
     print("Tiempos en Cola: \u001b[36m")
     print("--------")
     print()
     if(len(tiempoDeArrivos) == 0):
         print("Vacio")
     else:
         for i in tiempoDeArrivos:
             print(i.tiempoOcurrencia)
     print()
     print("--------")
     print()
     print("\u001b[32mTiempo del ultimo Evento: \u001b[37m" + str(tiempoUltimoEvento))
     print()
     contadorDelSistema = contadorDelSistema + 1
     print()
     print("NCCD:" + str(NCCD))
     print("Acum demora: " + str(acumuladoDemora))
     print("Area bajo Q(t): " + str(areaBajoQT))
     print("Area bajo B(t): " + str(areaBajoBT))




RutinaInicio.Inicializacion()
GraficarEstadoDelSistema(0)

sigueSimulacion = True
while(sigueSimulacion):
    objProxEvent = RutinaDeAvanceEnElTiempo.ProximoEvento()
    objProxEvent.RutinaEventos()
       

