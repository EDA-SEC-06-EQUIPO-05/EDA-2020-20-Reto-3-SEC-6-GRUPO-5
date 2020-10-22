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
import config
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import map as m
import datetime
assert config

"""
En este archivo definimos los TADs que vamos a usar,
es decir contiene los modelos con los datos en memoria


"""

# -----------------------------------------------------
# API del TAD Catalogo de accidentes
# -----------------------------------------------------


# Funciones para agregar informacion al catalogo
def newAnalyzer():
    """ Inicializa el analizador

    Crea una lista vacia para guardar todos los crimenes
    Se crean indices (Maps) por los siguientes criterios:
    -Fechas

    Retorna el analizador inicializado.
    """
    analyzer = {'accidents': None,
                'dateIndex': None
                }

    analyzer['accidents'] = lt.newList('ARRAY_LIST', compareIds)
    analyzer['dateIndex'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)
    return analyzer

def addAccident(analyzer, accident):
    """
    """
    lt.addLast(analyzer['accidents'], accident)
    updateDateIndex(analyzer['dateIndex'], accident)
    return analyzer

def updateDateIndex(map, accident):
    """
    Se toma la fecha del crimen y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de crimenes
    y se actualiza el indice de tipos de crimenes.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de crimenes
    """
    occurreddate = accident['Start_Time']
    accidentdate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    entry = om.get(map, accidentdate.date())
    if entry is None:
        datentry = newDataSeverityEntry(accident)
        om.put(map, accidentdate.date(), datentry)
    else:
        datentry = me.getValue(entry)
    addDateIndex(datentry, accident)
    return map

def addDateIndex(datentry, accident):
    """
    Actualiza un indice de tipo de crimenes.  Este indice tiene una lista
    de crimenes y una tabla de hash cuya llave es el tipo de crimen y
    el valor es una lista con los crimenes de dicho tipo en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    lst = datentry['lstaccidents']
    lt.addLast(lst, accident)
    severityIndex = datentry['severityIndex']
    seventry = m.get(severityIndex, accident['Severity'])
    if (seventry is None):
        entry = newSeverityEntry(accident['Severity'], accident)
        lt.addLast(entry['lstaccidents'], accident)
        m.put(severityIndex, accident['Severity'], entry)
    else:
        entry = me.getValue(seventry)
        lt.addLast(entry['lstaccidents'], accident)
    return datentry

def newDataSeverityEntry(accident):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'severityIndex': None, 'lstaccidents': None}
    entry['severityIndex'] = m.newMap(numelements=30,
                                     maptype='PROBING',
                                     comparefunction=compareSeverity)
    entry['lstaccidents'] = lt.newList('ARRAY_LIST', compareDates)
    return entry

def newSeverityEntry(clasificacion, accident):
    """
    Crea una entrada en el indice por tipo de crimen, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    acentry = {'severidad': None, 'lstaccidents': None}
    acentry['severidad'] = clasificacion
    acentry['lstaccidents'] = lt.newList('ARRAY_LIST', compareSeverity)
    return acentry

# ==============================
# Funciones de consulta
# ==============================
def crimesSize(analyzer):
    """
    Número de libros en el catago
    """
    return lt.size(analyzer['crimes'])

def accidentsSize(analyzer):
    """
    Número de libros en el catago
    """
    return lt.size(analyzer['accidents'])

def indexHeight(analyzer):
    """Numero de autores leido
    """
    return om.height(analyzer['dateIndex'])


def indexSize(analyzer):
    """Numero de autores leido
    """
    return om.size(analyzer['dateIndex'])


def minKey(analyzer):
    """Numero de autores leido
    """
    return om.minKey(analyzer['dateIndex'])


def maxKey(analyzer):
    """Numero de autores leido
    """
    return om.maxKey(analyzer['dateIndex'])

def getAccidentsByRange(analyzer, initialDate, finalDate):
    """
    Retorna el numero de accidentes en un rago de fechas.
    """
    lst = om.values(analyzer['dateIndex'], initialDate, finalDate)
    #print(lst)
    lstiterator = it.newIterator(lst)
    totaccidents = 0
    lst1 = 0
    lst2 = 0
    lst3 = 0
    lst4 = 0
    #n = abs(finalDate-initialDate).days
    #print(n)
    while (it.hasNext(lstiterator)):
        lstdate = it.next(lstiterator)
        i = 0
        while i<lt.size(lstdate['lstaccidents'])-1:
            if lstdate['lstaccidents']['elements'][i]['Severity'] == '1':
                lst1 += 1
            elif lstdate['lstaccidents']['elements'][i]['Severity'] == '2':
                lst2 += 1
            elif lstdate['lstaccidents']['elements'][i]['Severity'] == '3':
                lst3 += 1
            elif lstdate['lstaccidents']['elements'][i]['Severity'] == '4':
                lst4 += 1
            i += 1
        totaccidents += lt.size(lstdate['lstaccidents'])
        
    #print(lstdate)
    #print('i = '+str(i))
    total = [lst1,lst2,lst3,lst4]

    if max(total) == lst1:
        r = '1'
    elif max(total) == lst2:
        r = '2'
    elif max(total) == lst3:
        r = '3'
    elif max(total) == lst4:
        r = '4'    
    if totaccidents == 0:
        res = 'No hubo accidentes en el rango de fechas'
    else:    
        res = "\nTotal de accidentes en el rango de fechas: " + str(totaccidents) +'\nLa severidad de accidentes más reportada en este rango de fechas fue: ' + str(r)

    return res

def getAccidentsByHourRange(analyzer, initialHour, finalHour):
    """
    Retorna el numero de accidentes en un rago de horas.
    """
    lst = om.values(analyzer['dateIndex'], initialHour, finalHour)
    lstiterator = it.newIterator(lst)
    totaccidents = 0
    i = 0
    lst1 = 0
    lst2 = 0
    lst3 = 0
    lst4 = 0
    
    while (it.hasNext(lstiterator)):
        lstdate = it.next(lstiterator)
        totaccidents += lt.size(lstdate['lstaccidents'])
        if lstdate['lstaccidents']['elements'][i]['Severity'] == '1':
            lst1 += 1
        elif lstdate['lstaccidents']['elements'][i]['Severity'] == '2':
            lst2 += 1
        elif lstdate['lstaccidents']['elements'][i]['Severity'] == '3':
            lst3 += 1
        elif lstdate['lstaccidents']['elements'][i]['Severity'] == '4':
            lst4 += 1
        i += 1
    total = [lst1,lst2,lst3,lst4]

    if max(total) == lst1:
        r = '1'
    elif max(total) == lst2:
        r = '2'
    elif max(total) == lst3:
        r = '3'
    elif max(total) == lst4:
        r = '4'    
    if totaccidents == 0:
        res = 'No hubo accidentes en el rango de fechas'
    else:    
        res = "\nTotal de accidentes en el rango de fechas: " + str(totaccidents) +'\nLa severidad de accidentes más reportada en este rango de fechas fue: ' + str(r)
    return res
    
def getAccidentsByRangeSeverity(analyzer, Date):
    """
    Para una fecha determinada, retorna el numero de accidentes de diferentes severidades.
    """
    a = 0
    b = 0
    c = 0
    accidentdate = om.get(analyzer['dateIndex'], Date)

    if accidentdate == None:
        return 'No hubo accidentes en esta fecha'
    if accidentdate['key'] is not None:
        offensemap = me.getValue(accidentdate)['severityIndex']
        #s =  bs.size(offensemap)
        numoffenses = m.get(offensemap, '1')
        numoffenses2 = m.get(offensemap, '2')
        numoffenses3 = m.get(offensemap, '3')
        numoffenses4 = m.get(offensemap, '4')
        if numoffenses is not None:
            a = m.size(me.getValue(numoffenses)['lstaccidents'])
        if numoffenses2 is not None:
            b = m.size(me.getValue(numoffenses2)['lstaccidents'])
        if numoffenses3 is not None:
            c = m.size(me.getValue(numoffenses3)['lstaccidents'])
        if numoffenses4 is not None:
            d = m.size(me.getValue(numoffenses4)['lstaccidents'])
            return 'Total de accidentes de severidad 1: ' + ' ' + str(a) + '\nTotal de accidentes de severidad 2:' + ' ' + str(b) + '\nTotal de accidentes de severidad 3:' + ' ' + str(c) + '\nTotal de accidentes de severidad 4:' + ' ' + str(d) + '\nTotal de accidentes de la fecha:' + ' ' + str(c+a+b+d)
        return 0

def getAccidentsbyState(analyzer,initialDate,finalDate):

    lst = om.values(analyzer['dateIndex'], initialDate, finalDate)
    lstiterator = it.newIterator(lst)
    maximoEstado= ""
    maximoEstadoNum= 0
    maximaFechaNum= 0
    maximaFecha= ""
    i= 0
    diccFecha= {}
    diccEstado= {}

    while (it.hasNext(lstiterator)):
        lstdate = it.next(lstiterator)
        if lstdate is not None:
            state= lstdate['lstaccidents']['elements'][i]['State']
            if state not in diccEstado:
                diccEstado[state]= 0
            diccEstado[state]+= 1
            fechaEnt= lstdate['lstaccidents']['elements'][i]['Start_Time']
            date= str(datetime.datetime.strptime(fechaEnt, "%Y-%m-%d %H:%M:%S"))
            if date not in diccFecha:
                diccFecha[date]= 0
            diccFecha[date]+= 1
        i+= 1

    for estado in diccEstado:
        if diccEstado[estado]>maximoEstadoNum:
            maximoEstadoNum= diccEstado[estado]
            maximoEstado= estado

    for fecha in diccFecha:
        if diccFecha[fecha]>maximaFechaNum:
            maximaFechaNum= diccFecha[fecha]
            maximaFecha= fecha

    return (maximoEstado, maximoEstadoNum, maximaFecha, maximaFechaNum)

# ==============================
# Funciones de Comparacion
# ==============================

def compareIds(id1, id2):
    """
    Compara dos crimenes
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1


def compareDates(date1, date2):
    """
    Compara dos ids de libros, id es un identificador
    y entry una pareja llave-valor
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1


def compareOffenses(offense1, offense2):
    """
    Compara dos ids de libros, id es un identificador
    y entry una pareja llave-valor
    """
    offense = me.getKey(offense2)
    if (offense1 == offense):
        return 0
    elif (offense1 > offense):
        return 1
    else:
        return -1

def compareSeverity(severity1, severity2):
    """
    Compara dos ids de libros, id es un identificador
    y entry una pareja llave-valor
    """
    severity = me.getKey(severity2)
    if (severity1 == severity):
        return 0
    elif (severity1 > severity):
        return 1
    else:
        return -1
