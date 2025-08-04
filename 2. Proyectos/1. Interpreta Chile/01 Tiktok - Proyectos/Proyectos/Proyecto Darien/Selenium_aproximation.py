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
URL = r'https://www.tiktok.com/@medicossinfronteras/video/7164445151929093382'
driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()))
driver.get(URL)
print("Esperando aparición y resolución de Captcha....")
barra_carga(15)
# Entramos a la página principal:
# Recorrido externo comments
comentarios_recorridos = list()
centinela = True
comment_externo = 1
comment_interno = 1
base_final = pd.DataFrame()
seccion_comments = '/html/body/div[1]/div[3]/div[2]/div/div[2]/div[1]/div[3]/div[2]/div/div['
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
def comments_disponibles(pos_interna, pos_externa):
  print(pos_interna)
  if pos_interna > 0:
    try:
      display_name = driver.find_element(By.XPATH, value = seccion_comments + str(pos_externa) + "]/div[2]/div[" + str(pos_interna) + "]/div[1]/a")
    except:
      comments_disponibles(pos_interna-1, pos_externa)
  else:
    pos_interna = 1
  return pos_interna
scroll_down(5,1,1080)
def validacion(seccion_comments, primer_usuario, driver):
  try:
    driver.find_element(By.XPATH, value = seccion_comments + '1]')
    print('Sección de comments encontrada')
  except:
    print('No pudo seleccionar la sección de comments')
  try:
    driver.find_element(By.XPATH, value = primer_usuario).text
  except:
    print('No pudo capturar el primer username del primer comment')
  return None
try:
  validacion(seccion_comments,'/html/body/div[1]/div[3]/div[2]/div/div[2]/div[1]/div[3]/div[2]/div/div[1]/div/div[1]/a/span',driver)
except:
  print('El bot no pasa las validaciones para correr')
  sys.exit(1)



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
