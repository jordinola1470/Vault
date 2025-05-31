import sys
import time


#BARRA DE CARGA / ESTRATEGIA DE ESPERA
def barra_carga(tiempo):
    sys.stdout.flush()
    sys.stdout.write("\b" * (tiempo+1))
    for i in range(tiempo):
        time.sleep(1) # do real work here
        # update the bar
        sys.stdout.write(f'{1+i}')
        sys.stdout.flush()
    sys.stdout.write("-------------]\n")    
    return



#SCROLL - ESTRATEGIA DE ACTUALIZACION DEL DOM DE LA PAGINA
def scroll_down(load_time, times, bottom,driver):
  i = 0
  # Get scroll height
  # Altura actual de la pagina web
  last_height = driver.execute_script("return document.body.scrollHeight")
  # Altura actual del navegador
  browser_window_height = driver.get_window_size(windowHandle='current')['height']
  # Posicion actual vertical del desplazamiento del navegador 
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
  return 


