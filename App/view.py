"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """

import sys
import config
from App import controller
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Ruta a los archivos
# ___________________________________________________

# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Cargar datos")
    print("2- Inicializar Analizador")
    print("3- Cargar información de accidentes")
    print("4- Requerimiento 1")
    print("5- Requerimiento 2")
    print('6- Requerimiento 3')
    print('7- Requerimiento 4')
    print('8- Requerimiento 5')
    print("0- Salir")
    print("*******************************************")


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        accidentsfile = input("Ingrese el nombre del archivo CSV: ")
        print("\nRecopilando datos....")

    elif int(inputs[0]) == 2:
        print("\nInicializando analizador....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()

    elif int(inputs[0]) == 3:
        print("\nCargando información de accidentes ....")
        controller.loadData(cont, accidentsfile)
       
    elif int(inputs[0]) == 4:
        print("\nRequerimiento No 1 del reto 3: ")
        print("\nAccidentes según severidad en una fecha: ")
        initialDate = input("Fecha (YYYY-MM-DD): ")
        numoffenses = controller.getAccidentsByRangeSeverity(cont, initialDate)
        print(numoffenses)

    elif int(inputs[0]) == 5:
        print("\nRequerimiento No 4 del reto 3: ")
        print("\nAccidentes anteriores a la fecha: ")
        initialDate = "2016-01-01"
        finalDate = input("Fecha a buscar (YYYY-MM-DD): ")
        total = controller.getAccidentsByRange(cont, initialDate, finalDate)
        print(total)

    elif int(inputs[0]) == 6:
        print("\nRequerimiento No 3 del reto 3: ")
        print("\nAccidentes en un rango de fechas: ")
        initialDate = input("Rango Inicial (YYYY-MM-DD): ")
        finalDate = input("Rango Final (YYYY-MM-DD): ")
        total = controller.getAccidentsByRange(cont, initialDate, finalDate)
        print(total)

    elif int(inputs[0]) == 7:
        print("\nRequerimiento No 4 del reto 3: ")
        print("\nAccidentes de un estado en el rango de fechas: ")
        initialDate = input("Rango Inicial (YYYY-MM-DD): ")
        finalDate = input("Rango Final (YYYY-MM-DD): ")
        tupla= controller.AccidentsbyState(cont, initialDate, finalDate)
        print("\nEntre "+str(initialDate)+" y "+str(finalDate)+" el estado con mas accidentes es "+tupla[0]+", con "+str(tupla[1])+" accidentes reportados")
        print("\nLa fecha con mas accidentes reportados en ese rango fue el "+tupla[2]+", con "+str(tupla[3])+" accidentes reportados ese dia")

    elif int(inputs[0]) == 8:
        print("\nRequerimiento No 5 del reto 3: ")
        print("\nAccidentes en un rango de horas: ")
        initialHour = input("Rango Inicial (HH:MM:SS): ")
        finalHour = input("Rango Final (HH:MM:SS): ")
        total = controller.getAccidentsByHourRange(cont, initialHour, finalHour)
        print(total)
    else:
        sys.exit(0)
sys.exit(0)
