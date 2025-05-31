
import sys
from selenium.webdriver.common.by import By


#Ubicacion del primer comentario (en instagram el primer comentario
#son los titulos del post) y del usuario de ese primer comentarios

#VALIDACION - FUNCION
def validacion_instagram(driver,seccion_comments):

    '''Busqueda del contenedor que contiene los datos del primer comentario : usuario, datos,
    y el comentario'''

    try:
        driver.find_element(By.XPATH, value = seccion_comments +'1]')
        print('SeccionComentario Encontrada')
    except: print('nada')

    '''este segundo xpath corresponde al nombre del usuario dentro
    del bloque de comentarios, si el primer xpath no funciona, es decir no se ubica el 
    contenedor de comentario, se busca ubicar el contenedor tomando el nombre del usuario
    como punto de referencia'''

    try:
        driver.find_element(By.XPATH, value = '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[2]/div/div[1 ]/div/div[2]/div/span/div/div/span[1]/div/a/div/div/span').text
        print('UserName Encontrado')
    except Exception as e:
        print('UserName NO Encontrado', str(e))
    
    return None
