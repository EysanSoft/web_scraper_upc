import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
import requests
import re
import pandas as pd
from maquina1 import *


class index(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("vistaImplementacionProyectoCorte3.ui", self)
        self.botonExtraer.clicked.connect(self.extraer)

    def extraer(self):
        cadena = self.ingresoDeEnlace.text()
        try:
            numTel = re.compile('(\+?\d{1,4}(\-|\.|\s)?)?(\(?\d\)?(\-|\.|\s)?){9}\(?\d\)?')

            corEle = re.compile('(\w|\d)(\.?(\w|\d))*@(\w|\d)(\.?(\w|\d))*(\.(\d){2,4})')

            datos = requests.get(cadena)

            numerosTelefonicos = re.findall(numTel, datos.text)
            numerosTelefonicos.sort()
            listaNumTel = []
            for i in numerosTelefonicos:
                if i not in listaNumTel:
                    listaNumTel.append(i)
            print(listaNumTel)

            correosElectronicos = re.findall(corEle, datos.text)
            correosElectronicos.sort()
            listaCorElec = []
            for i in correosElectronicos:
                if i not in listaCorElec:
                    listaCorElec.append(i)
            print(listaCorElec)

            # Filtro
            listaNumTelMex = []
            for i in listaNumTel:
                numMex = self.filtroNumMex(i)
                if numMex == "NO":
                    print("Descartado")
                else:
                    listaNumTelMex.append(numMex)
            print(listaNumTelMex)

            # Automata
            listaCorElecUni = []
            listaCarrera = []
            for i in listaCorElec:
                carrera = self.automata(i)
                if carrera == "NO":
                    print("Descartado")
                else:
                    listaCorElecUni.append(i)
                    listaCarrera.append(carrera)
            # Turing
            listaNumTelConEstados = []
            for i in listaNumTelMex:
                numTelConEstados = self.maquina(i)
                listaNumTelConEstados.append(numTelConEstados)

            # Pasarlos a CSV, estas cuatro listas
            if len(listaNumTelMex) != 0:
                print(listaNumTelMex)
            else:
                listaNumTelMex.append("No se encontraron resultados.")
                print(listaNumTelMex)

            if len(listaNumTelConEstados) != 0:
                print(listaNumTelConEstados)
            else:
                listaNumTelConEstados.append("No se encontraron resultados.")
                print(listaNumTelConEstados)

            if len(listaCorElecUni) != 0:
                print(listaCorElecUni)
            else:
                listaCorElecUni.append("No se encontraron resultados.")
                print(listaCorElecUni)

            if len(listaCarrera) != 0:
                print(listaCarrera)
            else:
                listaCarrera.append("No se encontraron resultados.")
                print(listaCarrera)

            if len(listaNumTelMex) != 1 and len(listaCorElecUni) != 1:
                tabla = pd.DataFrame({
                    "Numero Telefonico": listaNumTelMex,
                    "Estado": listaNumTelConEstados,
                    "Correo Universitario": listaCorElecUni,
                    "Carrera": listaCarrera
                })
                print(tabla)
                tabla.to_csv("datos.csv", index=False)

            elif len(listaNumTelMex) != 1:
                tabla = pd.DataFrame({
                    "Numero Telefonico": listaNumTelMex,
                    "Estado": listaNumTelConEstados
                })
                print(tabla)
                tabla.to_csv("datos.csv", index=False)

            else:
                tabla = pd.DataFrame({
                    "Correo Universitario": listaCorElecUni,
                    "Carrera": listaCarrera
                })
                print(tabla)
                tabla.to_csv("datos.csv", index=False)

            self.texto.setText("Enlace valido, los datos fueron reportados en un CSV.")

        except Exception as exception:
            self.texto.setText("Error, enlace invalido, o error de conexion.")

    def maquina(self, telefono):
        contadorCinta = 0
        cabezal = 'q1'
        cinta = self.convertirDatos(telefono)
        banderaMaquina = True
        while banderaMaquina:
            for i in range(len(datosIda)):
                if cabezal == datos[i][0] and cinta[contadorCinta] == datos[i][1]:
                    cabezal = datosIda[i][0]
                    cinta[contadorCinta] = datosIda[i][1]
                    if datosIda[i][2] == 'R':
                        contadorCinta += 1
                    elif datosIda[i][2] == 'S':
                        banderaMaquina = False
                    break
        print(cinta)
        return cinta

    def convertirDatos(self, listNum):
        cinta = []
        if listNum[0:2] == "55" or listNum[0:2] == "33" or listNum[0:2] == "81":
            lada = listNum[0:2]
        else:
            lada = listNum[0:3]
        for i in lada:
            cinta.append(i)
        cinta.append('B')
        return cinta

    def filtroNumMex(self, numTel):
        caracteresEspeciales = "-+!#$%^&*()[] "
        mensajeError = "NO"
        for caracEsp in caracteresEspeciales:
            numTel = numTel.replace(caracEsp, '')

        numeroMxLADA3 = re.compile('(52)?(449|686|612|981|961|614|844|312|618|473|747|771|311|443|777|951|222|442|983'
                                   '|444|667|662|993|834|246|228|999|492)\d\d\d\d\d\d\d$')

        numeroMxLADA2 = re.compile('(52)?(55|81|31)\d\d\d\d\d\d\d\d$')

        resultado = re.match(numeroMxLADA3, numTel)
        if resultado:
            return numTel
        else:
            resultado = re.match(numeroMxLADA2, numTel)
            if resultado:
                return numTel
            else:
                return mensajeError

    def automata(self, correo):
        pattern = "@(.*?)\."
        carrera = re.search(pattern, correo).group(1)
        AF = {
            'q0': {'i': 'q1', 'm': 'q20', 'p': 'q24'},
            'q1': {'n': 'q2', 'a': 'q10', 'b': 'q11', 'e': 'q12', 'm': 'q13', 'p': 'q14', 'd': 'q15', 't': 'q17'},
            'q2': {'d': 'q3', ' ': 'Ingeniería en Nanotecnología'},
            'q3': {'u': 'q4'},
            'q4': {'c': 'q5'},
            'q5': {'c': 'q6'},
            'q6': {'i': 'q7'},
            'q7': {'o': 'q8'},
            'q8': {'n': 'q9'},
            'q9': {' ': 'Inducción'},
            'q10': {' ': 'Ingeniería Agroindustrial'},
            'q11': {' ': 'Ingeniería Biomédica'},
            'q12': {' ': 'Ingeniería en Energía'},
            'q13': {' ': 'Ingeniería Mecatrónica'},
            'q14': {' ': 'Ingeniería Petrolera'},
            'q15': {'s': 'q16'},
            'q16': {' ': 'Ingeniería en Desarrollo de Software'},
            'q17': {'a': 'q18', 'm': 'q19'},
            'q18': {' ': 'Ingeniería en Tecnología Ambiental'},
            'q19': {' ': 'Ingeniería en Tecnologías de Manufactura'},
            'q20': {'b': 'q21', 'e': 'q22'},
            'q21': {' ': 'Maestría en Biotecnología'},
            'q22': {'r': 'q23'},
            'q23': {' ': 'Maestría en Energías Renovables'},
            'q24': {'r': 'q25', 'y': 'q28'},
            'q25': {'e': 'q26'},
            'q26': {'u': 'q27'},
            'q27': {' ': 'Preuniversitario'},
            'q28': {'m': 'q29'},
            'q29': {'e': 'q30'},
            'q30': {'s': 'q31'},
            'q31': {' ': 'Licenciatura en Administración y Gestión de PYMES'},
        }
        estadoInicial = 'q0'
        estadoFinal = ['Ingeniería en Nanotecnología', 'Inducción', 'Ingeniería Agroindustrial', 'Ingeniería Biomédica',
                       'Ingeniería en Energía', 'Ingeniería Mecatrónica', 'Ingeniería Petrolera',
                       'Ingeniería en Desarrollo de Software', 'Ingeniería en Tecnología Ambiental',
                       'Ingeniería en Tecnologías de Manufactura', 'Maestría en Biotecnología',
                       'Maestría en Energías Renovables', 'Preuniversitario',
                       'Licenciatura en Administración y Gestión de PYMES']
        texto = carrera + " "
        mensajeError = "NO"
        estadoActual = estadoInicial
        n = 0
        try:
            while len(texto) > n:
                estadoActual = AF[estadoActual][texto[n]]
                n = n + 1
                valido = estadoActual in estadoFinal
        except:
            valido = False
        if valido:
            return estadoActual
        if not valido:
            return mensajeError


if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = index()
    GUI.show()
    sys.exit(app.exec_())
