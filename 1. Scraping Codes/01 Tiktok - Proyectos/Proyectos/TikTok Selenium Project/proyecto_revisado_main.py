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
from funciones_primarias import validacion, comments_disponibles
from funciones_secundarias import barra_carga,scroll_down

'''Protocolos SSL'''
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE



'''-------------------------------------------------------------------------------------------------------'''

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

#Navegador Firefox con el perfil configurado
driver = webdriver.Firefox(options=firefox_profile)

#Instancia driver -  Acceso a la URL
PAGINA_URL = 'https://www.tiktok.com/@mariannycorderoo/video/7234287154828938501?_r=1&_t=8eux31EZrok'
driver.get(PAGINA_URL)


'''-------------------------------------------------------------------------------------------------------'''

''' 
VALIDACION 
  - Funcionamiento de acceso a la URL, navegacion y captura de segmentos del en X.Path
  - Prueba del Scroll y de la Estrategia de Espera para la carga de mensajes
'''
seccion_comments = '/html/body/div[1]/div[2]/div[2]/div/div[2]/div[1]/div[2]/div[2]/div/div['

#Ejecucion de las pruebas de validacion, comentarlas cuando se aplique la aplicacion general

barra_carga(20)
scroll_down(5,1,1080,driver)
validacion(driver,seccion_comments)

'''-------------------------------------------------------------------------------------------------------'''


'''PROGRAMA WEB SCRAPING TIK-TOK'''

#VARIABLES PARA EL SCRAPING
comentarios_recorridos = list()
centinela = True
comment_externo = 1
comment_interno = 1
base_final = pd.DataFrame()


#BOT - CODIGO DE EJECUCION GENERAL

'''
El codigo tiene como punto de referencia el container del comentario, accede a los datos del usuario por medio de un loop,
en el cual se extraen los datos basicos, incluidos el numero de replies y likes, para posteriormente 
ingresar al contenedor de las respuestas de su comentario. Repitiendo un la misma logida de recuperacion de datos que el proceso anterior
'''

while centinela == True:
  try:
    ##Validacion de acceso a la URL
    try:
      driver.find_element(By.XPATH, value= '/html/body/div[1]/div[2]/div[2]/div/div[2]/div[1]/div[2]/div[2]/div/div[1]')
      print('Hay captcha ... INICIO')
      time.sleep(20)
    except:
      pass

    ##NAVEGACION Y DATOS PRINCIPALES    
    # Level 1 comment principal
    level = 1
    # Detectar el display name del usuario (i)
    try:
      display_name = driver.find_element(By.XPATH, value = seccion_comments + str(comment_externo) + "]/div[1]/div[1]/a/span").text
      print(display_name)
    except:
      centinela = False
      break
    # 01 Detectar nombre de usuario
    username_thread = driver.find_element(by=By.PARTIAL_LINK_TEXT,value=display_name).get_attribute("href")
    # 02 Detectar comment principal
    comment = driver.find_element(By.XPATH, value = seccion_comments + str(comment_externo) + "]/div[1]/div[1]/p[1]/span").text
    # 03 Detectar fecha
    fecha = driver.find_element(By.XPATH, value = seccion_comments + str(comment_externo) + "]/div[1]/div[1]/p[2]/span[1]").text
    # 04 Detectar número de likes
    likes = driver.find_element(By.XPATH, value = seccion_comments + str(comment_externo) + "]/div[1]/div[1]/p[2]/div/span").text
    # 05 Detectar el número de respuestas al comentario (answers)
    try:
      
      if comment_externo != 1:
        answers = driver.find_element(By.XPATH, value = seccion_comments + str(comment_externo) + "]/div[2]/div/p").text
        result = int(''.join([char for char in answers if char.isdigit()]))

        print(f'Numero de Respuestas {answers} {username_thread}')

      else: 
        answers = driver.find_element(By.XPATH, value = seccion_comments + str(comment_externo) + "]/div[2]/div[2]/p").text
        result = int(''.join([char for char in answers if char.isdigit()]))

        print(f'Numero de Respuestas {answers} {username_thread}')

    except:
      traceback.print_exc
      try:
        scroll_down(3, 1, 1030)
        answers = driver.find_element(By.XPATH, value = seccion_comments + str(comment_externo) + "]/div[2]/div/[2]p").text
        # result = answers[answers.find('(')+1:answers.find(')')]
        result = int(''.join([char for char in answers if char.isdigit()]))
        print(f'Numero de Respuestas Excepcional {answers}')
        
      except:
        answers = 0
        result = 0

    answers = result
    print(f'Validacion Respuestas {answers}')
    
    d = {"level": level, "display_name": display_name, "username":username_thread, "comment":comment, "fecha": fecha, "likes":likes, "replies":answers, "Thread_author": username_thread}
    
    base_temporal = pd.DataFrame(data=d,index=[comment_externo])
    base_final = pd.concat([base_final, base_temporal], ignore_index=True)

    # VALIDACIONES DATOS BASICOS 

    # print(base_final)
    # base_final.to_excel('Base_tiktok_medicossinfronteras.xlsx')- 

##################################################################################################################

    ## RESPUESTAS A LOS COMENTARIOS 
    # Respuestas del comentarios (i)

    seccion_replies = '/html/body/div[1]/div[2]/div[2]/div/div[2]/div[1]/div[2]/div[2]/div/div['

    # APERTURA
    # total de las respuestas - (veces que debemos de hacer click para aperturar el contenedor y tener todo en el DOM)
    times_click = math.ceil(answers/3)
    lista_click = [1] + [x+3 for x in range(answers) if (x % 3 == 1)]
    lista_click = lista_click[:len(lista_click)-1]

    print(lista_click)

    if times_click != 0:
      level = 2
      for t in lista_click:
        if t == 1:
          try:

            if comment_externo != 1:
              driver.find_element(By.XPATH, value = seccion_replies + str(comment_externo) + "]/div[2]/div/p").click()
            else: 
              driver.find_element(By.XPATH, value = seccion_replies + str(comment_externo) + "]/div[2]/div[2]/p").click()
                                                
          except:
            # Fallamos por poco, scrolldown a little
            scroll_down(3, 1, 1000,driver)
            try:
              driver.find_element(By.XPATH, value= '/html/body/div[7]/div/div[1]/div[2]/div')
              print('Hay captcha ... t=1 Mini Scroll Respuesta Comentarios')
              time.sleep(20)
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
            scroll_down(3, 1, 1000,driver)
            try:
              driver.find_element(By.XPATH, value= '/html/body/div[7]/div/div[1]/div[2]/div')
              print('Hay captcha ... t!=1 Mini Scroll Respuesta Comentarios')
              time.sleep(20)
            except:
              pass
            try:
              driver.find_element(By.XPATH, value = seccion_replies + str(comment_externo) + "]/div[2]/div/p").click()
            # El botón pudo desaparecer para este momento
            except:
              continue
            #fin del loop IF  

##################################################################################################################
  
        #Estrategia de tiempo, una vez terminada la apertura de replies por medio de los puntos de referencia del ciclo for, 
        #se espera la carga en el DOM para comenzar con la recopilacion de la inforamcion de los replies

        scroll_down(3, 1, 850,driver)
        try:
          driver.find_element(By.XPATH, value= '/html/body/div[7]/div/div[1]/div[2]/div')
          print('Hay captcha ... Fin de Iteracion Respuesta a Comentarios')
          time.sleep(20)
        except:
          pass

      
      # RECOPILACION      
      # De las replies

        #valore para desde el comentario 02 hacia adelante
      if comment_externo > 1:
        valor_alcanzable = comments_disponibles(answers, comment_externo,seccion_comments,driver)
        if valor_alcanzable == 0:
          answers = 1
          valor_alcanzable = answers
      else:
        #valor para el primer comentario
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

            d = {"level": level, "display_name": display_name, "username":username, "comment":comment, "fecha": fecha, "likes":likes, "replies":reply, "Thread_author":username_thread}
            
            base_temporal = pd.DataFrame(data=d,index=[comment_externo])
            base_final = pd.concat([base_final, base_temporal], ignore_index=True)
          
          except:
            continue

    comentarios_recorridos.append(comment_externo)

    comment_externo = comment_externo + 1
    
##################################################################################################################

    ##  REPORTE POR PANTALLA DEL PROGRESO DEL BOT
    print("Acabé el comment " + str(comment_externo - 1) + ' perteneciente al usuario: ' + str(display_name))
    if comment_externo % 15 == 1:
      scroll_down(10, 1, 1080,driver)
      try:
        driver.find_element(By.XPATH, value= '/html/body/div[7]/div/div[1]/div[2]/div')
        print('Hay captcha...')
        time.sleep(30)
      except:
        pass

  except Exception as e:
    traceback.print_exc()
    time.sleep(50)
    scroll_down(3, 1, 850,driver)

    with open('progreso.txt', 'w') as fp:
      fp.write(str(comentarios_recorridos[-1]))
    print(f'Error {type(e)}: e')
    base_final.to_excel('base_rental_tiktok.xlsx')

base_final.to_excel('base_rental_prueba_tiktok.xlsx')