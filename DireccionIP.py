# -*- coding: utf-8-spanish -*-
'''
Autor:  Abdias Alvarado
Fecha:  19/Nov/2017
Script: DireccionIP.py
'''


class DireccionIP(object):
    '''
    Clase que permite construir una dirección IP como
    tal, mediante una lista con octetos y máscara.
    '''

    def __init__(self, listaIP=[0, 0, 0, 0, 24]):
        '''
        Constructor de la clase.
        '''
        if self.ipValida(listaIP):
            self.octeto1 = listaIP[0]
            self.octeto2 = listaIP[1]
            self.octeto3 = listaIP[2]
            self.octeto4 = listaIP[3]
            self.mascara = listaIP[4]
        else:
            print("La dirección IP =>", listaIP, "es incorrecta.")
            self.octeto1 = 0
            self.octeto2 = 0
            self.octeto3 = 0
            self.octeto4 = 0
            self.mascara = 0

    def mostrarDecimal(self):
        '''
        Retorna un string mostrando la dirección IP en formato
        decimal.
        '''
        return str(self.octeto1)+"."+str(self.octeto2)+"."+str(self.octeto3)+"."+str(self.octeto4)+"/"+str(self.mascara)

    def ipBinario(self):
        '''
        Convierte la ip a binario y la retorna como lista.
        '''
        ipBinarioLista = list()
        ipBinarioLista.append(self.convertirABinario(self.octeto1))
        ipBinarioLista.append(self.convertirABinario(self.octeto2))
        ipBinarioLista.append(self.convertirABinario(self.octeto3))
        ipBinarioLista.append(self.convertirABinario(self.octeto4))

        return ipBinarioLista

    def ipValida(self, ipLista):
        '''
        Verifica si una ip dada es o no válida.

        Parámetros:
        ipLista => dirección ip en formato de lista.
        '''
        contador = 0
        for x in range(len(ipLista)):
            if x != 4:
                if ipLista[x] >= 0 and ipLista[x] < 256:
                    contador += 1
                else:
                    print("¡Error! Octeto incorrecto =>", ipLista[x])
            else:
                if ipLista[x] < 31 and ipLista[x] > 0:
                    contador += 1
                else:
                    print("Máscara erronea.")

        if contador == len(ipLista):
            return True
        else:
            return False

    def setIP(self, listaIP, mask):
        '''
        Inserta en la IP una lista con con octetos
        de la ip a modificar.

        Parámetros:
        listaIP => dirección ip en formato de lista.
        mask => un entero con la máscara dada.
        '''
        if self.ipValida(listaIP):
            self.octeto1 = listaIP[0]
            self.octeto2 = listaIP[1]
            self.octeto3 = listaIP[2]
            self.octeto4 = listaIP[3]
            self.mascara = mask
        else:
            print("La dirección IP =>", listaIP, "es incorrecta.")
            self.octeto1 = 0
            self.octeto2 = 0
            self.octeto3 = 0
            self.octeto4 = 0
            self.mascara = 0

    def agregar(self, cantidad):
        '''
        Suma una cantidad dada a un octeto de la
        dirección ip.

        Parámetros:
        cantidad => cantidad a aumentar.
        '''
        if cantidad > 0:
            if self.octeto4 + cantidad > 255:
                if self.octeto3 + 1 > 255:
                    if self.octeto2 + 1 > 255:
                        if self.octeto1 + 1 > 255:
                            print("¡LA IP HA SOBREPASADO EL LÍMITE!")
                        else:
                            self.octeto1 += 1
                            self.octeto2 = 0
                            self.octeto3 = 0
                            self.octeto4 = 0
                    else:
                        self.octeto2 += 1
                        self.octeto3 = 0
                        self.octeto4 = 0
                else:
                    self.octeto3 += 1
                    self.octeto4 = 0
            else:
                self.octeto4 += cantidad
        else:
            if self.octeto4 + cantidad > 0:
                self.octeto4 += cantidad
            elif self.octeto3 + cantidad > 0:
                self.octeto3 += cantidad
                self.octeto4 = 254
            elif self.octeto2 + cantidad > 0:
                self.octeto2 += cantidad
                self.octeto3 = 255
                self.octeto4 = 254
            elif self.octeto1 + cantidad > 0:
                self.octeto1 += cantidad
                self.octeto2 = 255
                self.octeto3 = 255
                self.octeto4 = 254


    def lista(self):
        '''
        Retorna la ip en formato lista.
        '''
        ipDec = list()
        ipDec.append(self.octeto1)
        ipDec.append(self.octeto2)
        ipDec.append(self.octeto3)
        ipDec.append(self.octeto4)
        return ipDec

    def convertirABinario(self, numero):
        '''
        Convierte un número del sistema decimal al sistema binario.

        Parámetros:
        numero => numero a convertir.
        '''
        numeroEnBinario = []
        numeroString = ""
        residuo = 0

        if numero == 0:
            numeroString = "00000000"
            return numeroString

        while numero > 0:
            residuo = numero % 2
            numeroEnBinario.append(residuo)
            numero = int(numero / 2)

        while len(numeroEnBinario) < 8:
            numeroEnBinario.append(0)

        numeroEnBinario.reverse()
        for x in range(len(numeroEnBinario)):
            numeroString += str(numeroEnBinario[x])

        return numeroString
