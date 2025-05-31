#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 19:08:34 2021

@author: diegoalejandrobermudezsierra
"""
import pandas as pd
import re
import string
import numpy as np


def limpieza_base(df):
    '''
    Definimos una función que va a limpiar la base con los tweets
    '''
    #numero corresponde a la posición donde se encuentran los nombres de las columnas
    #numero=int(input('Escriba la fila donde se encuentran los nombres de las columnas - '))
    numero = 5
    #Eliminamos las primeras filas del df que tienen información que no necesitamos y 
    #la primera columna que es un conteo dado por brandwatch
    df=df.iloc[numero:len(df),1:]
    #Tomamos la primera fila como nombre de las columnas
    column_names=df.iloc[0,:].tolist()
    #Cambiamos los espacios por _
    column_names=[re.sub('\\s', '_', x) for x in column_names]
    #Renombramos las columnas
    df.columns=column_names
    #Eliminamos la fila que tomamos como nombre de las columnas
    df=df.iloc[1:,:]
    #Hacemos un reset al index
    df=df.reset_index(drop=True)
    return df

def search_autor(df, autores):
    """
    Retorna una pequeña DataFrame en donde todas las filas tienen almenos una mención de medios o policía
    """
    return df[np.logical_or.reduce([df['Snippet'].str.contains(autor) for autor in autores])]

def label_base(df, autores):
    """
    Retorna una pequeña DataFrame en donde todas las filas tienen almenos una mención de medios o policía
    """
    df['Cita_medios'] = np.logical_or.reduce([df['Snippet'].str.contains(autor) for autor in autores])
    return df
