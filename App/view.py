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


accidentsfile = 'us_accidents_dis_2016.csv'

# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de accidentes")
    print("3- Requerimiento 1")
    print("4- Requerimiento 2")
    print('5- Requerimiento 3')
    print('6- Requerimiento 4')
    print('7- Requerimiento 5')
    print("0- Salir")
    print("*******************************************")


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()

    elif int(inputs[0]) == 2:
        print("\nCargando información de crimenes ....")
        controller.loadData(cont, accidentsfile)
       
    elif int(inputs[0]) == 3:
        print("\nRequerimiento No 1 del reto 3: ")
        print("\nBuscando accidentes según severidad en una fecha: ")
        initialDate = input("Fecha (YYYY-MM-DD): ")
        numoffenses = controller.getAccidentsByRangeSeverity(cont, initialDate)
        print(numoffenses)

    elif int(inputs[0]) == 5:
        print("\nRequerimiento No 3 del reto 3: ")
        print("\nBuscando accidentes en un rango de fechas: ")
        initialDate = input("Rango Inicial (YYYY-MM-DD): ")
        finalDate = input("Rango Final (YYYY-MM-DD): ")
        total = controller.getAccidentsByRange(cont, initialDate, finalDate)
        print(total)

    elif int(inputs[0]) == 7:
        print("\nRequerimiento No 5 del reto 3: ")
        print("\nBuscando accidentes en un rango de horas: ")
        initialHour = input("Rango Inicial (HH:MM): ")
        finalHour = input("Rango Final (HH:MM): ")
        total = controller.getAccidentsByHourRange(cont, initialHour, finalHour)
        print(total)
    else:
        sys.exit(0)
sys.exit(0)
