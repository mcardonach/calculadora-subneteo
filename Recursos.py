# -*- coding: utf-8-spanish -*-
'''
Autor:  Abdias Alvarado
Fecha:  19/Nov/2017
Script: Calculadora.py
'''
import platform
import os
import time
from colorama import init, Fore, Style
init()


class Recursos(object):
    '''
    Clase que contiene los recursos gráficos del programa.
    '''

    def __init__(self):
        self.hora = time.localtime()

    def mostrarEncabezado(self):
        '''
        Despliega el encabezado del programa con la
        información correspondiente al mismo.
        '''
        self.hora = time.localtime()
        print(Style.BRIGHT + Fore.WHITE)
        print("""
 ██████╗ █████╗ ██╗      ██████╗██╗   ██╗██╗      █████╗ ██████╗  ██████╗ ██████╗  █████╗
██╔════╝██╔══██╗██║     ██╔════╝██║   ██║██║     ██╔══██╗██╔══██╗██╔═══██╗██╔══██╗██╔══██╗
██║     ███████║██║     ██║     ██║   ██║██║     ███████║██║  ██║██║   ██║██████╔╝███████║
██║     ██╔══██║██║     ██║     ██║   ██║██║     ██╔══██║██║  ██║██║   ██║██╔══██╗██╔══██║
╚██████╗██║  ██║███████╗╚██████╗╚██████╔╝███████╗██║  ██║██████╔╝╚██████╔╝██║  ██║██║  ██║
 ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝

██████╗ ███████╗    ███████╗██╗   ██╗██████╗ ███╗   ██╗███████╗████████╗███████╗ ██████╗
██╔══██╗██╔════╝    ██╔════╝██║   ██║██╔══██╗████╗  ██║██╔════╝╚══██╔══╝██╔════╝██╔═══██╗
██║  ██║█████╗      ███████╗██║   ██║██████╔╝██╔██╗ ██║█████╗     ██║   █████╗  ██║   ██║
██║  ██║██╔══╝      ╚════██║██║   ██║██╔══██╗██║╚██╗██║██╔══╝     ██║   ██╔══╝  ██║   ██║
██████╔╝███████╗    ███████║╚██████╔╝██████╔╝██║ ╚████║███████╗   ██║   ███████╗╚██████╔╝
╚═════╝ ╚══════╝    ╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚══════╝ ╚═════╝
█████████████████████████████████████████████████████████████████████████████████████████
                                            ███
    Autor:      Abdias E. Alvarado          ███       UNIVERSIDAD CATÓLICA DE HONDURAS
    Cuenta:     0318-1997-00125             ███           CAMPUS: JESÚS SACRAMENTADO
    Email:      abdias.alvarado@unah.hn     ███            TERCER PERIODO ACADÉMICO
    Clase:      Programación Científica I   ███                  2017
                                            ███        Fecha: {0}
█████████████████████████████████████████████████████████████████████████████████████████
    """.format(time.asctime(self.hora)))

    def desplegarAyuda(self):
        '''
        Muestra un pequeño manual de uso del programa
        para referencia del usuario.
        '''
        os.system(self.limpiar())

        print("""
  █████████████████████████████████████████████████████████████████████
  ██                                                                 ██
██████                      A   Y   U   D   A                      ██████
  ██                                                                 ██
  █████████████████████████████████████████████████████████████████████

  CALCULADORA DE SUBNETEO
  Autor:    Abdias Alvarado
  Versión:  1.0
  Email:    alvaradoabdias@gmail.com

                                PREFACIO
  Realizar el subneteo de una red es de suma importancia para evitar el
  agotamiento de las direcciones IP. Una de las técnicas de subneteo es
  la VLSM, que nos permite construir las redes basándose en los números
  de host solicitados para cada segmento de red.

  En la práctica, es un poco confuso trabajar con las direcciones IP en
  código binario. Esta calculadora facilita el trabajo del ingeniero, o
  encargado de redes al momento de realizar el subneteo correspondiente.

                              MODO DE USO
  Para comenzar es necesario introducir lo datos de la siguiente manera:

  PASO 1: Ingrese la dirección IP sin espacios con su respectiva másca-
    ██    ra. Si la máscara debe ser menor que 31 y mayor o igual que 8.
    ██    Asegúrese de agregar un cero (0) para máscaras menores que 10.
    ██
    ██    Correcto:
    ██    192.168.0.1/24
    ██    192.168.0.1/08
    ██
    ██    Incorrecto:
    ██    192.168.0.1/8
    ██    192 168 0 1 /24
    ██    192. 168.0.1/24
    ██    192.168.0.1 /24
    ██
  PASO 2: Ingrese la cantidad de redes que desea calcular. Esto depende
    ██    del planteamiento del problema dado.
    ██
    ██    Correcto:
    ██    5
    ██
    ██    Incorrecto:
    ██    Cinco
    ██    cinco
    ██    5.0
    ██
  PASO 3: Ingrese la cantidad de hosts/dispositivos que contendrá cada
    ██    una de las subredes, descartando el orden por tamaño.
    ██
  PASO 4: Asigne una etiqueta para cada una de las subredes con el fin
    ██    de identificarlas a la hora del cálculo.
    ██
    ██
    ██
  PASO 5: Espere los resultados del cálculo.
        """)
        input()

    def limpiar(self):
        '''
        Evalúa el sistema operativo sobre el que se ejecutará
        el programa y devuelve el comando correcto para limpiar
        la pantalla.
        '''
        limpiar = "cls"
        plataforma = platform.system()
        if plataforma == 'Linux':
            limpiar = "clear"

        return limpiar
