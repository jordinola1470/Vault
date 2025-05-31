
import sys
from selenium.webdriver.common.by import By


#VALIDACION - FUNCION
def validacion(driver,seccion_comments):

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
        driver.find_element(By.XPATH, value = '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-comments/ytd-item-section-renderer/div[3]/ytd-comment-thread-renderer[1]/ytd-comment-renderer/div[3]/div[2]/div[1]/div[2]/h3/a/span').text
        print('UserName Encontrado')
    except:
        print('No pudo capturar el primer username del primer comment')
    
    return None
