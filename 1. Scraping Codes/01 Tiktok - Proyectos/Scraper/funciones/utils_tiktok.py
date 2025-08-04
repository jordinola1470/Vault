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



def scroll_page(driver):
    """Hace scroll continuo hasta que ya no haya más contenido."""
    print("🔽 Iniciando scroll...")
    
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Espera para cargar nuevo contenido

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print("✅ No hay más contenido para cargar.")
            break  # Detiene cuando la altura ya no cambia
        
        last_height = new_height

    print("✅ Scroll finalizado.")


def scroll_down_times(driver, num_scrolls,time_seconds):
    # Obtener la altura inicial de la página
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    for scroll in range(num_scrolls):
        # Hacer scroll hacia abajo
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Esperar un momento para que el contenido cargue
        time.sleep(time_seconds) #Aumentar el tiempo si es necesario

        # Comprobar la nueva altura de la página
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        # Si la altura no ha cambiado, salir del bucle
        if new_height == last_height:
            print("No more content to load. Stoping scroll.")
            break
        
        last_height = new_height  # Actualizar la altura para la siguiente iteración
        print(f"Scroll {scroll + 1}/{num_scrolls}: moving to {new_height}")


def procesar_comentarios(lista):
    resultado = []
    for dato in lista:
        partes = dato.split("\n")
        if "Responder" in partes:
            partes.remove("Responder")  # Eliminar "Responder"

        # Si no hay un cuarto elemento (likes), agregar "0"
        while len(partes) < 4:
            partes.append("0")

        resultado.append(partes)  # Añadir la lista procesada
    return resultado