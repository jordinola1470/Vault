import sys
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By



def barra_carga(tiempo,alerta):
    sys.stdout.flush()   
    sys.stdout.write("\b" * (tiempo+1))
    for i in range(tiempo):
        time.sleep(1) # do real work here
        # update the bar
        sys.stdout.write(f'{1+i}')
        sys.stdout.flush()
    sys.stdout.write(f" ---- 100% {alerta}")    
    return


# #SCROLL - ESTRATEGIA DE ACTUALIZACION DEL DOM DE LA PAGINA
# def scroll_down(load_time, times, bottom,driver):
#   i = 0
#   # Get scroll height
#   # Altura actual de la pagina web
#   last_height = driver.execute_script("return document.body.scrollHeight")
#   # Altura actual del navegador
#   browser_window_height = driver.get_window_size(windowHandle='current')['height']
#   # Posicion actual vertical del desplazamiento del navegador 
#   current_position = driver.execute_script('return window.pageYOffset')
  
#   scrolling = times
#   while i <= times:
#     if bottom == 1080:
#       # Scroll down to bottom
#       driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#       # Wait to load page
#       barra_carga(load_time,None)
#     else:
#       while (last_height - current_position > browser_window_height) & scrolling > 0:
#         driver.execute_script(f"window.scrollTo({current_position}, {browser_window_height + current_position - bottom});")
#         current_position = driver.execute_script('return window.pageYOffset')
#         print('Voy a bajar a: ' + str(browser_window_height + current_position - bottom) + ' estando en: ' + str(current_position))
#         scrolling -= 1
#         barra_carga(load_time,None)

#     # Calculate new scroll height and compare with last scroll height
#     new_height = driver.execute_script("return document.body.scrollHeight")
#     if new_height == last_height:
#         break
#     last_height = new_height
#     i = i + 1
#   return 


def scroll_down(driver):
    # Obtener la altura total de la página
    total_height = driver.execute_script("return document.body.scrollHeight")
    
    # Obtener la altura de la ventana del navegador
    window_height = driver.get_window_size(windowHandle='current')['height']
    
    # Calcular el porcentaje de desplazamiento (20% de la altura de la ventana)
    scroll_amount = window_height * 0.2
    
    # Inicializar la posición actual del scroll
    current_position = 0
    
    while current_position < total_height:
        # Hacer scroll hacia abajo
        driver.execute_script(f"window.scrollTo(0, {current_position + scroll_amount});")
        
        # Esperar un momento para que el contenido cargue
        time.sleep(1)
        
        # Actualizar la posición actual del scroll
        current_position += scroll_amount
        
        # Actualizar la altura total de la página
        total_height = driver.execute_script("return document.body.scrollHeight")

        # Imprimir la posición actual
        print(f"Desplazado a: {current_position} de {total_height}")

    print("Fin del scroll")

# # Ejemplo de uso
# if __name__ == "__main__":
#     # Configurar el driver de Selenium (asegúrate de tener el controlador adecuado)
#     # driver = webdriver.Chrome()  # O usa el controlador que necesites
#     # Firefox Options
#     firefox_profile = webdriver.FirefoxOptions()
#     firefox_profile.set_preference("browser.download.folderList", 2)
#     firefox_profile.set_preference("browser.download.dir", 'descargas')
#     firefox_profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")

#     # Firefox navigator with proper profile configurated
#     driver = webdriver.Firefox(options=firefox_profile)
#     driver.get("https://www.elcomercio.pe/")  # Reemplaza con la URL que deseas

#     # Llamar a la función de scroll
#     scroll_down(driver)

    # Cerrar el navegador
    

# def scroll_down_times(driver, num_scrolls):
#     # Obtener la altura de la ventana del navegador
#     window_height = driver.get_window_size(windowHandle='current')['height']
    
#     # Calcular el porcentaje de desplazamiento (20% de la altura de la ventana)
#     scroll_amount = window_height * 0.4
    
#     # Inicializar la posición actual del scroll
#     current_position = 0

#     for scroll in range(num_scrolls):
#         # Hacer scroll hacia abajo
#         driver.execute_script(f"window.scrollTo(0, {current_position + scroll_amount});")
        
#         # Esperar un momento para que el contenido cargue
#         time.sleep(1)
        
#         # Actualizar la posición actual del scroll
#         current_position += scroll_amount

#         # Imprimir la posición actual
#         print(f"Scroll {scroll + 1}/{num_scrolls}: desplazado a {current_position}")


def scroll_down_times(driver, num_scrolls):
    # Obtener la altura inicial de la página
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    for scroll in range(num_scrolls):
        # Hacer scroll hacia abajo
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Esperar un momento para que el contenido cargue
        time.sleep(2)  # Aumentar el tiempo si es necesario

        # Comprobar la nueva altura de la página
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        # Si la altura no ha cambiado, salir del bucle
        if new_height == last_height:
            print("No hay más contenido para cargar. Deteniendo el scroll.")
            break
        
        last_height = new_height  # Actualizar la altura para la siguiente iteración
        print(f"Scroll {scroll + 1}/{num_scrolls}: desplazado a {new_height}")
