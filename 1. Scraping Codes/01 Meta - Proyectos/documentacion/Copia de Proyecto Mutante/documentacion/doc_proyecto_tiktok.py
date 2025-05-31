#MODULOS DE SELENIUM
from selenium import webdriver
from selenium.webdriver.common.by import By

#MODULOS SECUNDARIOS
import pandas as pd
import numpy as np
import os
import re
import time
import ssl
import sys
import math
import traceback

#MODULO ALERTAS DESACTIVADAS
import warnings
warnings.filterwarnings('ignore')

#MODULO PROPIOS
from funciones_primarias import validacion
from funciones_secundarias import barra_carga,scroll_down

'''Protocoloes SSL'''
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

'''
OBJETO DRIVER 
- OPCIONES 
- URL 
'''

#Opciones Firefox
firefox_profile = webdriver.FirefoxOptions()
firefox_profile.set_preference("browser.download.folderList", 2)
firefox_profile.set_preference("browser.download.dir", 'descargas')
firefox_profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")

# Navegador Firefox con el perfil configurado
driver = webdriver.Firefox(options=firefox_profile)

#Instancia driver -  Acceso a la URL
PAGINA_URL = 'https://www.tiktok.com/@mariannycorderoo/video/7234287154828938501?_r=1&_t=8eux31EZrok'
driver.get(PAGINA_URL)

'''-------------------------------------------------------------------------------------------------------'''
#
#
#
''' VALIDACION 

Funcionamiento de acceso a la URL, navegacion y captura de segmentos del en X.Path
Prueba del Scroll y de la Estrategia de Espera para la carga de mensajes

'''
seccion_comments = '/html/body/div[1]/div[2]/div[2]/div/div[2]/div[1]/div[2]/div[2]/div/div['

barra_carga(20)
scroll_down(5,1,1080,driver)
validacion(driver,seccion_comments)

'''-------------------------------------------------------------------------------------------------------'''
#
#
#


#VARIABLES PARA EL SCRAPING
comentarios_recorridos = list()
centinela = True
comment_externo = 1
comment_interno = 1
base_final = pd.DataFrame()


while centinela == True:
  try:
    try:
      driver.find_element(By.XPATH, value= '/html/body/div[7]/div/div[1]/div[2]/div')
      print('Hay captcha...')
      time.sleep(30)
    except:
      pass
    # Level 1 comment principal
    level = 1
    # Detectar el display name del usuario
    try:
      display_name = driver.find_element(By.XPATH, value = seccion_comments + str(comment_externo) + "]/div[1]/div[1]/a/span").text
      print(display_name)
    except:
      centinela = False
      break
    # Detectar nombre de usuario
    username_thread = driver.find_element(by=By.PARTIAL_LINK_TEXT,value=display_name).get_attribute("href")
    # Detectar comment principal
    comment = driver.find_element(By.XPATH, value = seccion_comments + str(comment_externo) + "]/div[1]/div[1]/p[1]/span").text
    # Detectar fecha
    fecha = driver.find_element(By.XPATH, value = seccion_comments + str(comment_externo) + "]/div[1]/div[1]/p[2]/span[1]").text
    # Detectar número de likes
    likes = driver.find_element(By.XPATH, value = seccion_comments + str(comment_externo) + "]/div[1]/div[1]/p[2]/div/span").text


    # Detectar el número de respuestas
    try:
      answers = driver.find_element(By.XPATH, value = seccion_comments + str(comment_externo) + "]/div[2]/div/p").text
      result = answers[answers.find('(')+1:answers.find(')')]
    except:
      traceback.print_exc
      try:
        scroll_down(3, 1, 1030)
        answers = driver.find_element(By.XPATH, value = seccion_comments + str(comment_externo) + "]/div[2]/div/p").text
        result = answers[answers.find('(')+1:answers.find(')')]
      except:
        answers = 0
        result = 0
    answers = int(result)
    

    d = {"level": level, "display_name": display_name, "username":username_thread, "comment":comment, "fecha": fecha, "likes":int(likes), "replies":answers, "Thread_author": username_thread}
    base_temporal = pd.DataFrame(data=d,index=[comment_externo])
    base_final = pd.concat([base_final, base_temporal], ignore_index=True)
    
    # Ahora entramos a las respuestas del comentario
    seccion_replies = '/html/body/div[1]/div[3]/div[2]/div/div[2]/div/div[4]/div[2]/div/div['
    # Veces que debemos de hacer click para obtener replies
    times_click = math.ceil(answers/3)
    lista_click = [1] + [x+3 for x in range(answers) if (x % 3 == 1)]
    lista_click = lista_click[:len(lista_click)-1]
    if times_click != 0:
      level = 2
      for t in lista_click:
        if t == 1:
          try:
            driver.find_element(By.XPATH, value = seccion_replies + str(comment_externo) + "]/div[2]/div/p").click()

            #verificasi si esta el boton de respuestas, si es verdadero sumar un numero a la casilla general de comment externo, dado que el HTML del siguiente boton sera ese,
            #tenemos que empezar con 3 dado que el primer comentario es el titulo, el segundo label es el primer coment y el 3 es el primer Ver Respuesta, y de ahi dos en dos

          except:
            # Fallamos por poco, scrolldown a little
            scroll_down(3, 1, 1000)
            try:
              driver.find_element(By.XPATH, value= '/html/body/div[7]/div/div[1]/div[2]/div')
              print('Hay captcha...')
              time.sleep(30)
            except:
              pass
            try:
              driver.find_element(By.XPATH, value = seccion_replies + str(comment_externo) + "]/div[2]/div/p").click()
            except:
              continue
        else:
          try:
            driver.find_element(By.XPATH, value = seccion_replies + str(comment_externo) + "]/div[2]/div[" + str(t) + "]/p[1]").click()
          except:
            # Fallamos por poco, scrolldown a little
            scroll_down(3, 1, 1000)
            try:
              driver.find_element(By.XPATH, value= '/html/body/div[7]/div/div[1]/div[2]/div')
              print('Hay captcha...')
              time.sleep(30)
            except:
              pass
            try:
              driver.find_element(By.XPATH, value = seccion_replies + str(comment_externo) + "]/div[2]/div/p").click()
            # El botón pudo desaparecer para este momento
            except:
              continue
        scroll_down(3, 1, 850)
        try:
          driver.find_element(By.XPATH, value= '/html/body/div[7]/div/div[1]/div[2]/div')
          print('Hay captcha...')
          time.sleep(30)
        except:
          pass
      # Recopilamos las replies
      if comment_externo > 1:
        valor_alcanzable = comments_disponibles(answers, comment_externo)
        if valor_alcanzable == 0:
          answers = 1
          valor_alcanzable = answers
      else:
        valor_alcanzable = answers+1
      if answers != 0:
        for j in range(1, valor_alcanzable+1):
          # Detectar el display name del usuario
          try:
            display_name = driver.find_element(By.XPATH, value = seccion_replies + str(comment_externo) + "]/div[2]/div[" + str(j) + "]/div[1]/a").text
            # Detectar nombre de usuario
            username = driver.find_element(by=By.PARTIAL_LINK_TEXT,value=display_name).get_attribute("href")
            # Detectar comment principal
            comment = driver.find_element(By.XPATH, value = seccion_replies + str(comment_externo) + "]/div[2]/div[" + str(j) + "]/div[1]/p[1]").text
            # Detectar fecha
            fecha = driver.find_element(By.XPATH, value = seccion_replies + str(comment_externo) + "]/div[2]/div["+ str(j) + "]/div[1]/p[2]/span[1]").text
            # Detectar número de likes
            likes = driver.find_element(By.XPATH, value = seccion_replies + str(comment_externo) + "]/div[2]/div["+ str(j) + "]/div[1]/p[2]/div/span").text
            # Detectar el número de respuestas
            reply = 0
            d = {"level": level, "display_name": display_name, "username":username, "comment":comment, "fecha": fecha, "likes":int(likes), "replies":reply, "Thread_author":username_thread}
            base_temporal = pd.DataFrame(data=d,index=[comment_externo])
            base_final = pd.concat([base_final, base_temporal], ignore_index=True)
          except:
            continue


    comentarios_recorridos.append(comment_externo)
    comment_externo = comment_externo + 1
    print("Acabé el comment " + str(comment_externo - 1) + ' perteneciente al usuario: ' + str(display_name))
    if comment_externo % 15 == 1:
      scroll_down(10, 1, 1080)
      try:
        driver.find_element(By.XPATH, value= '/html/body/div[7]/div/div[1]/div[2]/div')
        print('Hay captcha...')
        time.sleep(30)
      except:
        pass
      
  except Exception as e:
    traceback.print_exc()
    time.sleep(50)
    scroll_down(3, 1, 850)
    with open(r'C:\Users\JOSE\Desktop\Trabajo\BX\Tiktok\progreso.txt', 'w') as fp:
      fp.write(str(comentarios_recorridos[-1]))
    print(f'Error {type(e)}: e')
    base_final.to_excel('Base_tiktok_medicossinfronteras.xlsx')
    
base_final.to_excel('Base_tiktok_medicossinfronteras.xlsx')   