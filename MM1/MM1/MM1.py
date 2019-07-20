import numpy as np
import random as rand
import math
import Graficos as gx

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
        ListaEventos.tiempoArribo = "cero"
        ListaEventos.tiempoPartida = "inf"

        

class RutinaDeAvanceEnElTiempo:
    def ProximoEvento():
        global clock

        proximoevento = "null"
        if(ListaEventos.tiempoArribo == "cero" and ListaEventos.tiempoPartida == "inf"):
            #primera vez de ejecucion.
            proximoevento = Arrivo()
            tiempoEvento = LibreriaDeRutinas.generaTiempoArrivo() #la primera vez genera el nro aleatorio solo
            
            proximoevento.tiempoOcurrencia = tiempoEvento + clock 
            clock = clock + tiempoEvento
            ListaEventos.tiempoArribo = "pasa a la segunda vez"

        elif(ListaEventos.tiempoPartida == "inf" and ListaEventos.tiempoArribo != "cero"):
            #segunda vez
            #genero arrivo.
            proxArrivo = Arrivo()
            proxArrivo.tiempoOcurrencia = LibreriaDeRutinas.generaTiempoArrivo() + clock
            
            #genero partida.
            proxPartida = Partida()
            proxPartida.tiempoOcurrencia = LibreriaDeRutinas.generarTiempoPartida() + clock
            
            
            #determino quien va a ser el proximo evento y lo mando.
            if(proxPartida.tiempoOcurrencia >= proxArrivo.tiempoOcurrencia):
                proximoevento = proxArrivo
            else:
                proximoevento = proxPartida

            clock = clock + proximoevento.tiempoOcurrencia
            ListaEventos.tiempoArribo = LibreriaDeRutinas.generaTiempoArrivo() + clock
            ListaEventos.tiempoPartida = LibreriaDeRutinas.generarTiempoPartida() + clock



        else:
            #resto de veces.
            if(len(tiempoDeArrivos) != 0): #si hay gente esperando.
                if(min(tiempoDeArrivos) <= ListaEventos.tiempoPartida): #si el min tiempo de arrivo es menor al tiempodepartida
                    proximoevento = Arrivo()
                    proximoevento.tiempoOcurrencia = min(tiempoDeArrivos)
                    clock = clock + proximoevento.tiempoOcurrencia
                else:
                    proximoevento = Partida()
                    proximoevento.tiempoOcurrencia = ListaEventos.tiempoPartida
                    #genero un futuro tiempo de salida en la lista de eventos
                    clock = clock + proximoevento.tiempoOcurrencia
                    ListaEventos.tiempoPartida = LibreriaDeRutinas.generarTiempoPartida() + clock
            else:
                proximoevento = Arrivo()
                proximoevento.tiempoOcurrencia = ListaEventos.tiempoArribo
                #genero futuro tiempo de arrivo.
                clock = clock + proximoevento.tiempoOcurrencia
                ListaEventos.tiempoArribo = LibreriaDeRutinas.generaTiempoArrivo() + clock
                ListaEventos.tiempoPartida = LibreriaDeRutinas.generarTiempoPartida() + clock

        return proximoevento

        

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
    def __init__(self):
        pass

class Partida:
    tiempoOcurrencia = -1
    def __init__(self):
        pass

class ListaEventos(object):
    tiempoArribo = "cero"
    tiempoPartida = "inf"

    mediaArribos = 5
    mediaPartida = 5


def RutinaEventos(evento):
    global estadoServidor,clock,tiempoDeArrivos,tiempoUltimoEvento,numeroDeClientesEnCola

    tiempoUltimoEvento = evento.tiempoOcurrencia

    if(type(evento) is Arrivo):
        if(estadoServidor == 1):            #servidor ocupado.
            if(evento.tiempoOcurrencia in tiempoDeArrivos): #si el cliente estaba previamente en la cola
                tiempoDeArrivos.remove(evento.tiempoOcurrencia) #lo saco.  sino: lo sumo
            else:                                           
                tiempoDeArrivos.append(evento.tiempoOcurrencia) 
                
                
        else:                               #servidor desocupado
            estadoServidor = 1
            if(evento.tiempoOcurrencia in tiempoDeArrivos):
                tiempoDeArrivos.remove(evento.tiempoOcurrencia)
            
            

    elif(type(evento) is Partida):
        if(estadoServidor == 1):
            if(len(tiempoDeArrivos) == 0): #si no hay nadie esperando a ser atendido.
                estadoServidor = 0
            else:
                estadoServidor = 1     
        else:
            raise Exception("Hubo un error en el proximo evento: Salida de cliente del servidor sin haber clientes en el servidor.")

    numeroDeClientesEnCola = len(tiempoDeArrivos)
    return 0


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
     
     #----------------------------------------------------------------------------------------------------#
     print("#---------------------------------------------[" + str(contadorDelSistema) + "]----------------------------------------------------#")
     print("Estado del sistema numero: " + str(contadorDelSistema))
     if(type(objProxEvent) is Arrivo):
         print("Evento: Arrivo")
     else:
         if(objProxEvent == 0):
             print("Inicializacion del sistema.")
         else:
             print("Evento: Partida")


     print()
     print("Reloj: " + str(clock))
     if(estadoServidor == 0):
         print("Estado del Servidor: Desocupado")
     else:
         print("Estado del Servidor: Ocupado")

     print("Numero de Clientes en Cola: ", str(numeroDeClientesEnCola))
     print("tiempoDeArrivos: ")
     print("******----")
     if(len(tiempoDeArrivos) == 0):
         print("Vacio")
     else:
         print(tiempoDeArrivos)
     print()
     print("******----")
     print()
     print("Tiempo del ultimo Evento: " + str(tiempoUltimoEvento))
     print()
     contadorDelSistema = contadorDelSistema + 1








RutinaInicio.Inicializacion()
GraficarEstadoDelSistema(0)

sigueSimulacion = True
while(sigueSimulacion):
    objProxEvent = RutinaDeAvanceEnElTiempo.ProximoEvento()
    RutinaEventos(objProxEvent)
    GraficarEstadoDelSistema(objProxEvent)
       
