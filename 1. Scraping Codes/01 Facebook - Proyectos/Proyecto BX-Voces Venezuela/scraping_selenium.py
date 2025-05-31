# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 20:26:52 2021

@author: JOSE
"""

import os, shutil, pytrends
import re
import ssl
import sys
import time
import numpy as np
import pandas as pd
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
  "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True
  })

web_page_cabecera = 'https://www.facebook.com/'
usuario = 'comunicaciones@barometrodexenofobia.org'
password = 'barometro2021*'

def barra_carga(tiempo):
    sys.stdout.write("%s: [" % ('Esperando '+str(tiempo)+' segundos'))
    sys.stdout.flush()
    sys.stdout.write("\b" * (tiempo+1))

    for i in range(tiempo):
        time.sleep(1) # do real work here
        # update the bar
        if (round(tiempo/(i+1))%5)==0:
            sys.stdout.write("-")
            sys.stdout.flush()
    sys.stdout.write("]\n")
    return

driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
action = webdriver.ActionChains(driver)
driver.get(web_page_cabecera)

# Paso 1: Inicio sesión
user = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[1]/div/div/div/div[2]/div/div[1]/form/div[1]/div[1]/input")
user.send_keys(usuario)
contraseña = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[1]/div/div/div/div[2]/div/div[1]/form/div[1]/div[2]/div/input")
contraseña.send_keys(password)
boton_iniciar = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[1]/div/div/div/div[2]/div/div[1]/form/div[2]/button")
boton_iniciar.click()
barra_carga(5)
# TODO: Implementar un placeholder de la hora en la que se corre el código

# Paso 2: Redireccionamiento al grupo o página
# TODO: Realizar una lista de páginas o grupos para que entre como párametro y definir periodicidad para correr el código
driver.get("https://www.facebook.com/groups/2459047080785676")
for num in range(5):
    print('End número: ' + str(num))
    action.key_down(Keys.END).key_up(Keys.END).perform()
    barra_carga(6)
# Paso 3: Descargar mensajes
for mensaje in range(2,42):
    try:
        element = driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[4]/div/div/div/div/div[1]/div[2]/div[2]/div[" + str(mensaje) + "]")
    except:
        element = driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[4]/div/div/div/div/div[1]/div[2]/div/div[" + str(mensaje) + "]")
    html_del_mensaje = element.get_attribute('innerHTML')
    break
with open('readme.txt', 'w', encoding='utf-8') as f:
    f.write(html_del_mensaje)
# Paso 4: Pre-procesamiento
