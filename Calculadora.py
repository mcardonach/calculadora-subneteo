# -*- coding: utf-8-spanish -*-
'''
Autor:  Abdias Alvarado
Fecha:  19/Nov/2017
Script: Calculadora.py
'''
from DireccionIP import DireccionIP
from Subred import Subred
from colorama import init, Fore, Style, Back
from Recursos import Recursos
from Database_Proyectos import engine, tabla_proyectos
from sqlalchemy import select, and_
import platform
import time
import os
import xlsxwriter
init()


class Calculadora(object):
    '''
    Realiza el subneteo tomando como base una
    dirección IP.
    '''

    def __init__(self):
        '''
        Constructor de la clase.
        '''
        self.recursos = Recursos()
        self.subredes = list()
        self.opciones = {"1": self.nuevoProyecto,
                         "2": self.abrirExistente,
                         "3": self.desplegarAyuda,
                         "4": self.abrirExistente,
                         "5": self.salir
                         }

    def desplegarMenu(self):
        '''
        Muestra el menú principal del programa.
        '''
        self.recursos.mostrarEncabezado()
        # Convierte la cadena de texto al color de la tabla ANSI.
        print(Back.BLACK + Style.BRIGHT + Fore.CYAN +
              "Seleccione una de las siguientes opciones:")
        print(Fore.WHITE + "1. Nuevo Proyecto")
        print("2. Abrir existente")
        print("3. Mostrar Ayuda")
        print("4. Exportar Proyecto")
        print("5. Salir")

    def iniciarCalculadora(self):
        '''
        Comienza a pedirle los datos al usuario para hacer
        el subneteo correspondiente.
        '''
        ip = list(input('Dirección IP: '))
        self.ipBase = DireccionIP(self.segmentarIP(ip))

        print("Host Disponibles Actualmente: {0}".format(2 ** (32 - self.ipBase.mascara) - 2))
        cantidadSubredes = int(input('Numero de subredes: '))
        print(Style.RESET_ALL)
        print(Back.BLACK)
        for x in range(1, cantidadSubredes + 1):
            subred = Subred()
            subred.solicitarDatos(x)
            self.subredes.append(subred)

        self.ordenarSubredes()

        ipSubred1 = self.calcularIpSubred(self.ipBase)

        self.asignarSubredes(ipSubred1)

        for x in range(len(self.subredes)):
            self.subredes[x].guardarSubneteo(self.nombreProyecto, x + 1)
            self.subredes[x].mostrarDetalles(x + 1)

        print(Style.RESET_ALL)
        input("PRESIONE ENTER PARA REGRESAR...")

    def verificarProyectoExiste(self, nombre):
        '''
        Verifica si un proyecto determinado existe en la
        base de datos.

        Parámetros:
        nombre => el nombre del proyecto a buscar.
        '''
        connection = engine.connect()
        seleccionar = select([tabla_proyectos.c.nombre],
                             and_(tabla_proyectos.c.nombre == nombre))
        resultado = connection.execute(seleccionar)

        proyecto_existe = [dict(row) for row in resultado]

        connection.close()

        if not proyecto_existe:
            return True
        else:
            return None

    def salir(self,opcion):
        '''
        Cierra el programa.
        '''
        os.system(self.limpiar())
        print("¡Gracias por utilizar la Calculadora de Subneteo!")
        exit()

    def abrirExistente(self,opcion):
        '''
        Opción del menú que llama a los métodos para
        mostrar los proyectos existentes y abre el solicitado.
        '''
        os.system(self.limpiar())
        print(Style.RESET_ALL + "PROYECTOS EXISTENTES")
        print(Back.BLACK)
        exis = self.listarProyectos()

        print(Style.RESET_ALL)
        eleccion = input('Ingrese el nombre del proyecto: ')
        eleccion = eleccion.lower()
        if eleccion in exis:
            if opcion == 2:
                self.mostrarProyecto(eleccion)
            else:
                self.exportarProyecto(eleccion)
        else:
            print(Back.BLACK)
            print(Style.BRIGHT + Fore.RED +
                  "¡El proyecto -{0}- no existe!".format(eleccion.upper()))
            print(Style.RESET_ALL)
            time.sleep(2)
            os.system(self.limpiar())

    def listarProyectos(self):
        '''
        Despliega una lista de los proyectos existentes en la
        base de datos.
        '''
        connection = engine.connect()
        seleccionar = select([tabla_proyectos])
        resultado = connection.execute(seleccionar)

        registros = [dict(row) for row in resultado]
        contador = 0
        existentes = list()
        for x in range(len(registros)):
            if registros[x]['idSubred'] == '1':
                contador += 1
                existentes.append(registros[x]['nombre'])
                print(Back.BLACK)
                print(Style.BRIGHT + Fore.CYAN + "{}.{}"
                      .format(contador, registros[x]['nombre'].upper()))

        connection.close()
        return existentes

    def exportarProyecto(self, nombreProyecto):
        '''
        Exporta los detalles de un proyecto específico en un archivo de excel

        Parámetros:
        nombreProyecto => el nombre del proyecto a abrir.
        '''
        nombreArchivo = '{}.xlsx'.format(nombreProyecto)
        workbook = xlsxwriter.Workbook(nombreArchivo)
        worksheet = workbook.add_worksheet("Subredes")

        os.system(self.limpiar())
        connection = engine.connect()
        seleccionar = select([tabla_proyectos],
                             and_(tabla_proyectos.c.nombre == nombreProyecto))
        resultado = connection.execute(seleccionar)
        registros = [dict(row) for row in resultado]

        worksheet.write(0, 0, "LISTADO DE SUBREDES")

        worksheet.write(1, 0, "Id Subred")
        worksheet.write(1, 1, "Etiqueta")
        worksheet.write(1, 2, "Id Subred")
        worksheet.write(1, 3, "Host Solicitador")
        worksheet.write(1, 4, "Host Disponibles")
        worksheet.write(1, 5, "Bits De Red")
        worksheet.write(1, 6, "Mascara De Subred")
        worksheet.write(1, 7, "Primera IP Asignable")
        worksheet.write(1, 8, "Última IP Asignable")
        worksheet.write(1, 9, "Broadcast")

        for x in range(len(registros)):
            worksheet.write(x+2, 0,registros[0]['idSubred'])
            worksheet.write(x+2, 1, registros[x]['etiqueta'])
            worksheet.write(x+2, 2, registros[x]['ipSubred'])
            worksheet.write(x+2, 3, registros[x]['hostSolicitados'])
            worksheet.write(x+2, 4, registros[x]['hostDisponibles'])
            worksheet.write(x+2, 5, registros[x]['bitsRed'])
            worksheet.write(x+2, 6, registros[x]['mascara'])
            worksheet.write(x+2, 7, registros[x]['primeraAsignable'])
            worksheet.write(x+2, 8, registros[x]['ultimaAsignable'])
            worksheet.write(x+2, 9, registros[x]['broadcast'])
        workbook.close()
        connection.close()
        print(Style.RESET_ALL + "SE GENERÓ EL ARCHIVO " + nombreArchivo)
        input("PRESIONE ENTER PARA REGRESAR...")

    def mostrarProyecto(self, nombreProyecto):
        '''
        Muestra los detalles de un proyecto específico.
        Despliega todos los cálculos de subneteo.

        Parámetros:
        nombreProyecto => el nombre del proyecto a abrir.
        '''
        os.system(self.limpiar())
        connection = engine.connect()
        seleccionar = select([tabla_proyectos],
                             and_(tabla_proyectos.c.nombre == nombreProyecto))
        resultado = connection.execute(seleccionar)

        registros = [dict(row) for row in resultado]

        print(Back.BLACK)
        print(Style.BRIGHT + Fore.YELLOW +
              "PROYECTO: {0}".format(nombreProyecto.upper()))
        print()

        for x in range(len(registros)):
            print(Back.BLACK)
            print(Style.BRIGHT + Fore.CYAN +
                  "Subred {0}".format(registros[x]['idSubred']))
            print(Fore.WHITE + "Etiqueta:             {0}".format(registros[x]['etiqueta']))
            print("Dirección de Subred:  {0}".format(registros[x]['ipSubred']))
            print("Host Solicitados:     {0}".format(registros[x]['hostSolicitados']))
            print("Host Disponibles:     {0}".format(registros[x]['hostDisponibles']))
            print("Bits de Red:          {0}".format(registros[x]['bitsRed']))
            print("Mascara Subred:       {0}".format(registros[x]['mascara']))
            print("Primera Asignable:    {0}".format(registros[x]['primeraAsignable']))
            print("Última asignable:     {0}".format(registros[x]['ultimaAsignable']))
            print("Broadcast:            {0}".format(registros[x]['broadcast']))
            print(Style.RESET_ALL)
            print("")

        connection.close()
        print(Style.RESET_ALL)
        input("PRESIONE ENTER PARA REGRESAR...")

    def nuevoProyecto(self,opcion):
        '''
        Crea un nuevo proyecto.
        '''
        while len(self.subredes) > 0:
            self.subredes.pop()

        print(Back.BLACK)
        print(Style.BRIGHT + Fore.WHITE)
        os.system(self.limpiar())
        self.nombreProyecto = input('Nombre del proyecto: ')
        self.nombreProyecto = self.nombreProyecto.lower()

        if self.verificarProyectoExiste(self.nombreProyecto) is not None:
            self.iniciarCalculadora()
        else:
            print(Back.BLACK)
            print(Style.BRIGHT + Fore.RED)
            print("¡El proyecto ya existe!")
            time.sleep(2)

    def desplegarAyuda(self,opcion):
        '''
        Muestra el manual de uso del programa.
        '''
        self.recursos.desplegarAyuda()

    def calcularIpSubred(self, ip):
        '''
        Retorna la dirección de la red la que pertenece
        una dirección IP dada..

        Parámetros:
        ip => la dirección IP donde buscar la subred.
        '''
        bits = ""
        listaBits = list()
        binario = ip.ipBinario()

        for x in range(len(binario)):
            bits += binario[x]

        listaBits = list(bits)
        return self.transformarSubred(listaBits, ip.mascara)
        '''
        '''

    def transformarSubred(self, ipBinaria, bitsRed):
        '''
        Recibe una lista con los bits en 1 ó 0 de una
        dirección IP determinada y retorna la dirección
        de la red la que pertenece.

        Parámetros:
        ipBinaria => lista con los bits de la IP.
        bitsRed   => el numero de bits utilizados para la red.
        '''
        for x in range(len(ipBinaria)):
            if x >= bitsRed:
                ipBinaria[x] = '0'

        octetoBinario = ""
        nuevaIP = list()
        for x in range(len(ipBinaria)):
            if x != 0 and x % 8 == 0:
                nuevaIP.append(int(octetoBinario, 2))
                octetoBinario = ipBinaria[x]
            else:
                octetoBinario += ipBinaria[x]

        nuevaIP.append(int(octetoBinario, 2))

        return nuevaIP

    def asignarSubredes(self, ipSubred1):
        '''
        Método auxiliar de subneteo que permite asignar
        la ip base de las subredes a partir de la cual se
        realizará el subneteo.

        Parámetros:
        ipSubred1 => dirección ip base de la subred.
        '''
        for x in range(len(self.subredes)):
            if x == 0:
                self.subredes[x].direccionIP.setIP(ipSubred1, self.subredes[x].mascara)
                self.subredes[x].subnetear(ipSubred1)
            else:
                nuevaIP = DireccionIP()
                nuevaIP.setIP(self.subredes[x - 1].broadcast.lista(), self.subredes[x].mascara)
                nuevaIP.agregar(1)
                self.subredes[x].direccionIP.setIP(nuevaIP.lista(), nuevaIP.mascara)
                self.subredes[x].subnetear(self.subredes[x].direccionIP.lista())

    def calcularNuevaMascara(self, numeroHosts):
        '''
        Calcula la máscara necesaria para un número
        determinado de host.

        Parámetros:
        numeroHosts => cantidad de host a encontrar.
        '''
        mascara = 0
        for bits in range(2, 30):
            if (2 ** bits) - 2 >= numeroHosts:
                mascara = 32 - bits
                return mascara

        return mascara

    def segmentarIP(self, listaIP):
        '''
        Toma una dirección IP en formato lista y la
        recorre para concatenar los caracteres que
        están separados por punto (.) y pleca (/)
        y así formar otra lista con 4 octetos y una
        máscara de red en enteros.
        '''
        octeto = ""
        ip = list()
        for x in range(len(listaIP)):
            if listaIP[x] != ".":
                if listaIP[x] != "/":
                    octeto += listaIP[x]
                else:
                    ip.append(int(octeto))
                    if len(listaIP) - x > 2:
                        ip.append(int(listaIP[x + 1] + listaIP[x + 2]))
                    elif len(listaIP) - x > 1:
                        ip.append(int(listaIP[x + 1]))
                    else:
                        print(Back.BLACK)
                        print(Style.BRIGHT + Fore.RED + "¡IP inválida! Sin máscara.")
                        print(Style.RESET_ALL)
                        time.sleep(2)
                        os.system(self.limpiar())
                        self.iniciarCalculadora()

            else:
                ip.append(int(octeto))
                octeto = ""

        return ip

    def limpiar(self):
        '''
        Evalúa el sistema operativo sobre el que se ejecutará
        el programa y devuelve el comando correcto para limpiar
        la pantalla.
        '''
        limpiar = "cls"
        plataforma = platform.system()
        if plataforma == 'Linux' or plataforma == 'Darwin':
            limpiar = "clear"

        return limpiar

    def ordenarSubredes(self):
        '''
        Ordena las subredes de mayor a menor según
        el número de host solicitados.
        '''
        for numPasada in range(len(self.subredes) - 1, 0, -1):
            for i in range(numPasada):
                if self.subredes[i].hostSolicitados < self.subredes[i + 1].hostSolicitados:
                    temp = self.subredes[i]
                    self.subredes[i] = self.subredes[i + 1]
                    self.subredes[i + 1] = temp

    def run(self):
        '''
        Inicia el programa.
        '''
        while True:
            os.system(self.limpiar())
            self.desplegarMenu()
            opcion = str(input("R=> "))
            accion = self.opciones.get(opcion)
            if accion:
                accion(opcion)
            else:
                print(Back.BLACK)
                print(Style.BRIGHT + Fore.RED +
                      "¡{0} no es una opción válida!".format(opcion))
                print(Style.RESET_ALL)
                # Hace una pausa antes de ejecutar la siguiente instrucción.
                time.sleep(2)
                os.system(self.limpiar())


if __name__ == '__main__':
    calculadoraSubneteo = Calculadora()
    calculadoraSubneteo.run()
