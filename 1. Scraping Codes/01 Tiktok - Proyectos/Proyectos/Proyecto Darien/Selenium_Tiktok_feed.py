import os
import re
import ssl
import sys
import math
import time
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import traceback

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
  "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True
  })
def barra_carga(tiempo):
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
def scroll_down(load_time, times, bottom):
  i = 0
  # Get scroll height
  last_height = driver.execute_script("return document.body.scrollHeight")
  browser_window_height = driver.get_window_size(windowHandle='current')['height']
  current_position = driver.execute_script('return window.pageYOffset')
  scrolling = times
  while i <= times:
    if bottom == 1080:
      # Scroll down to bottom
      driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
      # Wait to load page
      barra_carga(load_time)
    else:
      while (last_height - current_position > browser_window_height) & scrolling > 0:
        driver.execute_script(f"window.scrollTo({current_position}, {browser_window_height + current_position - bottom});")
        current_position = driver.execute_script('return window.pageYOffset')
        print('Voy a bajar a: ' + str(browser_window_height + current_position - bottom) + ' estando en: ' + str(current_position))
        scrolling -= 1
        barra_carga(load_time)
    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
    i = i + 1
  return None
def listToString(s):
 
    # initialize an empty string
    str1 = ""
 
    # traverse in the string
    for ele in s:
        str1 += ele
 
    # return string
    return str1
URL = r'https://www.tiktok.com/search?q=darien'
driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()))
driver.get(URL)
print("Esperando aparición y resolución de Captcha....")
barra_carga(15)
# Entramos a la página principal:
# Recorrido externo comments
i = 2
lista_videos = "/html/body/div[2]/div[2]/div[2]/div[2]/div[1]/div/div["
centinela = True
contador = 1
base_final = pd.DataFrame()
while centinela == True:
   try:
    lista_hashtags = list()
    #Usuario que publica
    usuario = driver.find_element(By.XPATH, value = lista_videos + str(i) + "]/div[2]/div/div[2]/a/div/p").text
    #Descripción
    try:
       hashtags_elements = driver.find_element(By.XPATH, value= lista_videos + str(i) + "]/div[2]/div/div[1]")
       hashtags_elements = hashtags_elements.find_elements(By.TAG_NAME, value='strong')
       for elem in hashtags_elements:
          if elem.text.startswith('#'):
             lista_hashtags.append(elem.text + ' ')
       hashtags = listToString(lista_hashtags)
    except:
       hashtags = ''
    try:
       descripcion = driver.find_element(By.XPATH, value = lista_videos + str(i) + "]/div[2]/div/div[1]/div/span[1]").text + ' ' + hashtags
    except:
       descripcion = '' + hashtags
    #Fecha de publicación
    fecha = driver.find_element(By.XPATH, value = lista_videos + str(i) + "]/div[1]/div/div/a/div/div[2]/div").text
    #Link del vídeo
    link = driver.find_element(By.XPATH, value = lista_videos + str(i) + "]/div[1]/div/div/a").get_attribute('href')
    #Views del vídeo
    views = driver.find_element(By.XPATH, value = lista_videos + str(i) + "]/div[2]/div/div[2]/div/strong").text
    contador += 1
    scroll_down(2,1,600)
    if contador == 12:
       contador = 1
       # Cargar mas
       driver.find_element(By.XPATH, value = "/html/body/div[2]/div[2]/div[2]/div[2]/div[2]/button").click()
       barra_carga(15)
    d = {"descripcion": descripcion, "usuario": usuario, "fecha":fecha, "link":link, "views": views}
    base_temporal = pd.DataFrame(data=d,index=[i])
    base_final = pd.concat([base_final, base_temporal], ignore_index=True)
    base_final.to_excel('Base_feed.xlsx')
    if i == 1000:
       centinela = False
    i += 1
   except Exception as e:
    print(f'Error {type(e)}: e')
    print(e)
    i += 1
    continue
