# -*- coding: utf-8-spanish -*-
'''
Autor:  Abdias Alvarado
Fecha:  19/Nov/2017
Script: Subred.py
'''
from DireccionIP import DireccionIP
from colorama import init, Fore, Style
from Database_Proyectos import engine, tabla_proyectos
from sqlalchemy import select, and_
init()


class Subred(object):
    '''
    Clase que contiene las IP de broadcast, primera asignable,
    última asignable y su misma IP.
    '''

    def __init__(self):
        '''
        Constructor de la clase.
        '''
        self.hostDisponibles = 0
        self.hostSolicitados = 0
        self.direccionIP = DireccionIP()
        self.etiqueta = ""
        self.primeraAsignable = DireccionIP()
        self.ultimaAsignable = DireccionIP()
        self.broadcast = DireccionIP()
        self.mascara = 0

        self.hostPorMascaras = {'/1': 2147483646,
                                '/2': 1073741822,
                                '/3': 536870910,
                                '/4': 268435454,
                                '/5': 134217726,
                                '/6': 67108862,
                                '/7': 33554430,
                                '/8': 16777214,
                                '/9': 8388606,
                                '/10': 4194302,
                                '/11': 2097150,
                                '/12': 1048574,
                                '/13': 524286,
                                '/14': 262142,
                                '/15': 131070,
                                '/16': 65534,
                                '/17': 32766,
                                '/18': 16382,
                                '/19': 8190,
                                '/20': 4094,
                                '/21': 2046,
                                '/22': 1022,
                                '/23': 510,
                                '/24': 254,
                                '/25': 126,
                                '/26': 62,
                                '/27': 30,
                                '/28': 14,
                                '/29': 6,
                                '/30': 2
                                }

        self.mascarasDecimal = {'/1': '128.0.0.0',
                                '/2': '192.0.0.0',
                                '/3': '224.0.0.0',
                                '/4': '240.0.0.0',
                                '/5': '248.0.0.0',
                                '/6': '252.0.0.0',
                                '/7': '254.0.0.0',
                                '/8': '255.0.0.0',
                                '/09': '255.128.0.0',
                                '/10': '255.192.0.0',
                                '/11': '255.224.0.0',
                                '/12': '255.240.0.0',
                                '/13': '255.248.0.0',
                                '/14': '255.252.0.0',
                                '/15': '255.254.0.0',
                                '/16': '255.255.0.0',
                                '/17': '255.255.128.0',
                                '/18': '255.255.192.0',
                                '/19': '255.255.224.0',
                                '/20': '255.255.240.0',
                                '/21': '255.255.248.0',
                                '/22': '255.255.252.0',
                                '/23': '255.255.254.0',
                                '/24': '255.255.255.0',
                                '/25': '255.255.255.128',
                                '/26': '255.255.255.192',
                                '/27': '255.255.255.224',
                                '/28': '255.255.255.240',
                                '/29': '255.255.255.248',
                                '/30': '255.255.255.252'
                                }

    def buscarMascaraDecimal(self, abreviatura):
        '''
        Busca la máscara decimal que le corresponde a
        una abreviatura determinada.

        Parámetros:
        abreviatura => la abreviatura de máscara.
        '''
        ab = '/' + str(abreviatura)
        return self.mascarasDecimal.get(ab)

    def solicitarDatos(self, numeroIdentificador=1):
        '''
        Solicita al usuario los datos respectivos para
        la subred.

        Parámetros:
        numeroIdentificador => número de subred a llenar.
        '''
        print(Style.BRIGHT + Fore.WHITE +
              "=== Subred {0} ===".format(numeroIdentificador))
        self.hostSolicitados = int(input("Numero de host: "))

        if self.hostSolicitados > 254:
            temporal = self.hostSolicitados
            self.espacios = 0
            while temporal > 0:
                temporal -= 254
                self.espacios += 1
        else:
            self.espacios = 1

        self.etiqueta = input("Etiqueta: ")
        self.mascara = self.calcularmascara(self.hostSolicitados)
        self.direccionIP.mascara = self.mascara
        print("")

    def calcularmascara(self, numeroHosts):
        '''
        Calcula la máscara necesaria para un número
        determinado de host.

        Parámetros:
        numeroHosts => cantidad de host a encontrar.
        '''
        mascara = 0
        for bits in range(2, 30):
            if (2 ** bits) - 2 >= numeroHosts:
                self.hostDisponibles = (2 ** bits) - 2
                mascara = 32 - bits
                return mascara

        return mascara

    def mostrarDetalles(self, numeroIdentificador=1):
        '''
        Muestra toda la información de la subred.

        Parámetros:
        numeroIdentificador => número de subred que se muestra.
        '''
        print(Style.BRIGHT + Fore.CYAN +
              "Subred {0}".format(numeroIdentificador))
        print(Fore.WHITE + "Etiqueta:             {0}".format(self.etiqueta))
        print("Dirección de Subred:  {0}".format(self.direccionIP.mostrarDecimal()))
        print("Host Solicitados:     {0}".format(self.hostSolicitados))
        print("Host Disponibles:     {0}".format(self.hostDisponibles))
        print("Bits de Red:          {0}".format(self.mascara))
        print("Mascara Subred:       {0}".format(self.buscarMascaraDecimal(self.mascara)))
        print("Primera Asignable:    {0}".format(self.primeraAsignable.mostrarDecimal()))
        print("Última asignable:     {0}".format(self.ultimaAsignable.mostrarDecimal()))
        print("Broadcast:            {0}".format(self.broadcast.mostrarDecimal()))
        print(Style.RESET_ALL)

        print("")

    def subnetear(self, listaIpSubred):
        '''
        Realiza los cálculos principales del programa.

        Parámetros:
        listaIpSubred => dirección ip en formato lista.
        '''
        self.direccionIP.setIP(listaIpSubred, self.mascara)
        self.ultimaAsignable.setIP(listaIpSubred, self.mascara)
        self.broadcast.setIP(listaIpSubred, self.mascara)
        self.primeraAsignable.setIP(listaIpSubred, self.mascara)

        if self.espacios > 1:
            for x in range(self.espacios):
                self.broadcast.agregar(self.hostDisponibles + 1)
                self.broadcast.octeto4 = 255
        else:
            self.broadcast.agregar(self.hostDisponibles + 1)

        self.ultimaAsignable.setIP(self.broadcast.lista(), self.mascara)
        self.ultimaAsignable.agregar(-1)
        self.primeraAsignable.agregar(1)

    def guardarSubneteo(self, nombreProyecto, IdSubred):
        '''
        Ingresa a la base de datos los cálculos realizados.

        Parámetros:
        nombreProyecto => nombre del proyecto.
        IdSubred => el número identificador de la subred.
        '''
        connection = engine.connect()
        insertar = tabla_proyectos.insert(
                                          values=dict(
                                                     nombre=nombreProyecto,
                                                     idSubred=IdSubred,
                                                     etiqueta=self.etiqueta,
                                                     ipSubred=str(self.direccionIP.mostrarDecimal()),
                                                     hostSolicitados=str(self.hostSolicitados),
                                                     hostDisponibles=str(self.hostDisponibles),
                                                     bitsRed=str(self.mascara),
                                                     mascara=str(self.buscarMascaraDecimal(self.mascara)),
                                                     primeraAsignable=str(self.primeraAsignable.mostrarDecimal()),
                                                     ultimaAsignable=str(self.ultimaAsignable.mostrarDecimal()),
                                                     broadcast=str(self.broadcast.mostrarDecimal())
                                                     )
                                        )

        resultado = connection.execute(insertar)
        connection.close()
