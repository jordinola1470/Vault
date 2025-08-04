
import sys
from selenium.webdriver.common.by import By


#VALIDACION - FUNCION
def validacion(driver,seccion_comments):
    try:
        driver.find_element(By.XPATH, value = seccion_comments +'1]')
        print('SeccionComentario Encontrada')
    except: print('SeccionComentario NO ENCONTRADA')

    try:
        driver.find_element(By.XPATH, value = '/html/body/div[1]/div[2]/div[2]/div/div[2]/div[1]/div[2]/div[2]/div/div[1]/div/div[1]/a/span').text
        print('UserName Encontrado')
    except:
        print('UserName NO ENCONTRADO')
    
    return None


#COMENTARIOS DISPONIBLES - FUNCION
def comments_disponibles(pos_interna, pos_externa,driver, seccion_comments):
  if pos_interna > 0:
    try:
      display_name = driver.find_element(By.XPATH, value = seccion_comments + str(pos_externa) + "]/div[2]/div[" + str(pos_interna) + "]/div[1]/a")
    except:
      comments_disponibles(pos_interna-1, pos_externa,driver,seccion_comments)
  else:
    pos_interna = 1
  return pos_interna