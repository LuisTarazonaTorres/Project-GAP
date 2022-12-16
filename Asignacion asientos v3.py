# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 17:04:49 2022

@author: le.tarazona
"""

import openpyxl as opxl              #Leer datos de excel
import datetime                      #Manejo de fechas
import math      
import pandas as pd
import numpy as np
from time import time
import xlsxwriter 
import random
from random import randint
from time import time
import matplotlib.pyplot as plt
#leer el archivo
book=opxl.load_workbook('BD SEAT.xlsx',data_only = True)
#fijar hoja
hoja = book.active

celdas = hoja['A2':'J55601']

Record_list  = []
for fila in celdas:
    Record = ([celda.value for celda in fila])
    Record_list.append(Record)


df = pd.DataFrame(Record_list, columns=['RecordLocator','PassengerID', 'UnitDesignator', 'BookingBookDate', 'DepartureDate', 'FlightNumber', 'DepartureStation', 'ArrivalStation', 'SeatBookDate', 'SeatBookDateTime'])
print(df)


#%%Instancia

Num_vuelo = df['FlightNumber']
Fecha_vuelo = df['DepartureDate']    


Num_vuelo = Num_vuelo.drop_duplicates()
Num_vuelo.index = range(0,len(Num_vuelo))
Fecha_vuelo = Fecha_vuelo.drop_duplicates()
Fecha_vuelo.index = range(0,len(Fecha_vuelo))

ID = []
Asig_ini = []
Verificador = []

## Escoja las instancias 
vuelo = 3 #0 a 50
fecha = 28 #0 a 29

##
for i in range(0,len(df['RecordLocator'])):
    if Num_vuelo[vuelo] == df['FlightNumber'][i] and Fecha_vuelo[fecha] == df['DepartureDate'] [i]:
        ID.append(df['PassengerID'][i])
        Asig_ini.append(df['UnitDesignator'][i])
        Verificador.append((df['SeatBookDateTime'][i]))

print("Numero de vuelo: ", Num_vuelo[vuelo])    
print("Fecha de vuelo: ", Fecha_vuelo[fecha])

#%% Matriz de precios
import pandas as pd
Matriz = pd.read_fwf('Datos.txt', header = None, delim_whitespace = True, skipinitialspace = True )

#%% Función Costo perdido por asignación
def ASIG(Matriz, Asignacion):
    Costo_venta = []
    for j in range(0,len(Asig_ini)):
        for i in range(0,len(Matriz[0])):
            if Asig_ini[j] == Matriz[0][i] and Verificador[j] == 0:
                asig = Matriz[2][i]
                Costo_venta.append(asig)
    return Costo_venta

def SEAT(Matriz, Asignación):
    a_asignar = []
    for i in range(0,len(Matriz[0])):
        for j in range(0,len(Asig_ini)):
            if Matriz[0][i] == Asig_ini[j] and Verificador[j] == 0:
                asig2 = Matriz[0][i]
                a_asignar.append(asig2)
    return a_asignar

def VENTA(Matriz, Asignación):
    vendido = []
    for i in range(0,len(Matriz[0])):
        for j in range(0,len(Asig_ini)):
            if Matriz[0][i] == Asig_ini[j] and Verificador[j] == 1:
                asig3 = Matriz[0][i]
                vendido.append(asig3)
    return vendido

#%%
Costoinicial = ASIG(Matriz,Asig_ini)
print(sum(Costoinicial))

asig_ini2 = SEAT(Matriz,Asig_ini)
print(asig_ini2)
print(len(asig_ini2))
vendido = VENTA(Matriz,Asig_ini)    


#%% Asientos disponibles
Matrix = Matriz
for i in range(0,len(Matriz[0])):
    for j in range(0,len(vendido)):
        if vendido[j] == Matrix[0][i]:
            Matrix.remove(Matrix[0][i])
    

#%% BUSQUEDA LOCAL
#SOLUCIÓN INICIAL
control = time() 
Asig_ini3 = []

for i in range(0,len(asig_ini2)):
    Asig_ini3.append(Matriz[0][i])  
    
Costo_inicial = 0
for j in range(0,len(Asig_ini3)):
    for i in range(0,len(Matriz[0])):
        if Asig_ini3[j] == Matriz[0][i]: #and Asig_ini[3] != vendido[t]:
            asig = Matriz[2][i]
            Costo_inicial += asig
    

##APLICACIÓN DE BÚSQUEDA LOCAL

Asig_ini4 = Asig_ini3
Costonuevo = Costo_inicial
Costonuevo2 = Costonuevo
k = 0
FOset = []

for k in range(0,1):
    for i in range(0,len(Matriz[2])):
        for j in range(0,len(Asig_ini4)):
            Costonuevo = Costonuevo2
            pos1 = randint(0,len(Matriz[2])-1)
            pos2 = randint(0,len(Asig_ini4)-1)
            
            Asig_ini4[pos2] = Matriz[0][pos1]
            Asig_ini5 = Asig_ini4
               
            Costonuevo2 = 0
            for h in range(0,len(Asig_ini4)):
                for g in range(0,len(Matriz[0])):
                    for t in range(0,len(vendido)):
                        if Asig_ini4[h] == Matriz[0][g] and Asig_ini4[h] != vendido[t]:
                            asig = Matriz[2][g]
                            Costonuevo2 += asig
               
            if Costonuevo < Costonuevo2:
                Asig_ini5 = Asig_ini3
                Asig_ini4[pos2] = Asig_ini4[pos2]
                Costonuevo2 = Costonuevo
                FOset.append(Costonuevo2)
                print(Costonuevo)
    k = k + 1     
times = time() - control 
print(times)

#%%
plt.scatter(range(0,len(FOset)), FOset, color = 'purple')
plt.title('FO Instancia 01') #cambiar nombre a instancia
plt.xlabel('Iterations')
plt.ylabel('Objective')
plt.show()    

#%% constructivo

asientos = Matriz[0]

col = [0]* len(asientos)

#asigna los asientos a los que ya compraron
for k in range(0,len(asientos)):
    for i in range(0,len(vendido)):
        if vendido[i] == asientos[k]:
            col[k] = 1

#%%asigna asientos a los que no compraron
pasajeros_por_asignar = list(range(0,len(asig_ini2)))
pas = pasajeros_por_asignar
for k in range(0,len(asientos)):
    for i in range(0,len(pas)):
        if col[k] == 0:
            pas[i] = 1
            col[k] = pas[i]
            pas.remove(pas[i])
     
            
asientos_asignados = {'asientos': asientos, 'asignacion': col}
df = pd.DataFrame(data=asientos_asignados)


columnas = 6
filas = len(df.asignacion) // columnas

a = np.reshape(np.asarray(df.asignacion[0: filas * columnas]), (filas, columnas))

np.savetxt('Inst01.txt', a) ###cambiar numero de instancia


#%%
#Costos de asignación
costos = []
costos_disponibles = []
for k in range(0,len(df['asientos'])):
    if df['asignacion'][k] == 1:
        costos.append(Matriz[2][k])
    if df['asignacion'][k] == 0:
        costos_disponibles.append(Matriz[2][k])

costosnuevo = sum(costos)   
monto_disponible = sum(costos_disponibles) 
print(costosnuevo)

#%% ventas

ventas = []

for l in range(0,len(df['asientos'])):
    for j in range(0,len(vendido)):
        if vendido[j] == df['asientos'][l]:
            ventas.append(Matriz[2][l])
                
ventas_inicial = sum(ventas)

Costoini= sum(Costoinicial) 
print(Costoini)
costosnuevo = sum(costos)-ventas_inicial
print (costosnuevo)
    


