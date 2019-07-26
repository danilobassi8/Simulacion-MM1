import numpy as np
import random as rand
import math
import os
import collections

os.system("cls") #para limpiar la pantalla al iniciar la ejecucion del script.
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
        #SOY CAMPI
        global numeradorQt
        numeradorQt=[]
        #SOY CAMPI
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
        
        #SOY CAMPI
        tiempoAnterior=self.tiempoOcurrencia

         
        if(estadoServidor == 1):            #servidor ocupado.
            if(self in tiempoDeArrivos): #si esta en la lista de los arrivos pendientes.
                tiempoDeArrivos.remove(self)
            else:
                tiempoDeArrivos.append(self)
        else:                               #servidor desocupado
            estadoServidor = 1
            NCCD = NCCD + 1

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


        AsignoAreaBajoQT(numeradorQt,numeroDeClientesEnCola,tiempoAnterior,ListaEventos.tiempoPartida)



def AsignoAreaBajoQT(numeradorQt,numeroDeClientesEnCola,tiempoAnterior,tiempoPartida):
        global areaBajoQT
        
        if(numeroDeClientesEnCola>=len(numeradorQt)): 
            numeradorQt.append(0)          #si hay mas clientes en cola que la longitud de la lista numeradorQt, agrego un elemento a la lista

        
        if(len(numeradorQt)==0): numeradorQt.append(0) #agrego el primer elemento a la lista

        numeroASumar = numeradorQt[numeroDeClientesEnCola] + (tiempoPartida - tiempoAnterior)     #al tiempo que tenia en la posicion numerodDeClienteEnCola le sumo el nuevo intervalo de tiempo.
        numeradorQt[numeroDeClientesEnCola] = numeroASumar 


        areaBajoQT=0 
        for x in range (len(numeradorQt)):  #recorro todo el arreglo numeradorQt y sumo el producto de lo que está en la posicion i por la posicion i
            Qt=x*numeradorQt[x]
            areaBajoQT = areaBajoQT +Qt



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


def CalculaAreaBajoBT():
    global areaBajoBT
    global estadoServidor
    global contadorDelSistema
    global clock

    global estadoAnteriorServidor #variable global que solamente se va a usar en este metodo.
    global tiempoAlmacenado #variable global que solo se usa para este metodo.
    
    if(contadorDelSistema == 0): #la primera vez se setea a falso.
        estadoAnteriorServidor = 0
    
    
    if(estadoServidor == 1): #el sv esta ocupado?
        if(estadoAnteriorServidor != 1): #antes estaba DESocupado
            tiempoAlmacenado = clock
            estadoAnteriorServidor = 1
        else:
            areaBajoBT = clock - tiempoAlmacenado + areaBajoBT
            tiempoAlmacenado = clock
            estadoAnteriorServidor = 1
    else: #el sv esta desocupado?
        if(estadoAnteriorServidor != 1): #antes estaba DESocupado
            pass
        else:
            areaBajoBT = clock - tiempoAlmacenado + areaBajoBT
            tiempoAlmacenado = clock
            estadoAnteriorServidor = 0

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

       #calculo el area bajo b(t).  lo meto aca porque es mas facil y porque se
     #agrego despues.
     CalculaAreaBajoBT()
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
     print("\u001b[35mNCCD: \u001b[31m" + str(NCCD))
     print("\u001b[35mAcum demora: \u001b[31m" + str(acumuladoDemora))
     print("\u001b[35mArea bajo Q(t): \u001b[31m" + str(areaBajoQT))
     print("\u001b[35mArea bajo B(t): \u001b[31m" + str(areaBajoBT))



RutinaInicio.Inicializacion()
GraficarEstadoDelSistema(0)

sigueSimulacion = True
while(sigueSimulacion):
    objProxEvent = RutinaDeAvanceEnElTiempo.ProximoEvento()
    objProxEvent.RutinaEventos()