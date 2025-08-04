#MODULOS DE SELENIUM
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime

#MODULOS SECUNDARIOS
import pandas as pd
import numpy as np
import os
import time
import ssl
import sys
import traceback
import pyautogui


#MODULO ALERTAS DESACTIVADAS
import warnings
warnings.filterwarnings('ignore')

#MODULO PROPIOS
from utils import modelamiento


def ManagerFaceBookScrapper (url,medio):

    driver = webdriver.Firefox()
    driver.get(url)

# Publicacion Multimedia - Video (No Reel)
    try:
        
        time.sleep(2)
        # Espera a que el botón sea clickeable
        boton = driver.find_element(By.XPATH, value="/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/div").click()
  
    # Detener el video    
        ## Coordenadas
        x = 83
        y = 256
        ## Duración del movimiento en segundos
        duracion = 0.5
        pyautogui.moveTo(x, y, duration=duracion)
        pyautogui.click()
        
        time.sleep(1)
        print('video detenido')

    # Todos los comentarios
        try:
            # Seleccion de "Todos los comentarios"
            time.sleep(1)
            # Espera a que el botón sea clickeable
            boton = driver.find_element(By.XPATH, "//div[@role='button' and contains(., 'Más pertinentes')]")
            boton.click()

            time.sleep(2)
            boton = driver.find_element(By.XPATH, "//span[contains(text(), 'Todos los comentarios')]")
            boton.click()


            # Comenzar scroll de contenedor de comentarios y click boton "Ver Mas"
            time.sleep(2)
            boton = driver.find_element(By.XPATH, "//span[contains(text(), 'Ver más comentarios')]")
            boton.click()
            print('click ver mas')

            pyautogui.moveTo(x=1261, y=374, duration=0.5)
            pyautogui.click()

            for _ in range(3):
                pyautogui.scroll(-300)
                time.sleep(2.5)


##
            intentos = 0
            max_intentos = 8
            intentos_sin_boton = 0
            seguir = True  # variable de control para el bucle

            while seguir and intentos < max_intentos:
                try:
                    boton = driver.find_element(By.XPATH, "//span[contains(text(), 'Ver más comentarios')]")
                    boton.click()
                    time.sleep(1)
                    intentos_sin_boton = 0  # reinicia el contador si encuentra el botón
                except:
                    for _ in range(3):
                        pyautogui.scroll(-500)
                        time.sleep(1)
                    intentos += 1
                    intentos_sin_boton += 1

                    # Si no encuentra el botón 1 veces seguidas, termina el bucle cambiando la variable
                    if intentos_sin_boton >= 1:
                        print("No se encontró el botón en 1 intentos consecutivos. Saliendo del bucle.")
                        seguir = False

            if intentos == max_intentos:
                print("No se encontró el botón después de 8 intentos.")


        except Exception as e:
            pass


# Contenedor de Comentarios

        comentarios = driver.find_elements(By.CSS_SELECTOR,"div.xv55zj0.x1vvkbs.x1rg5ohu.xxymvpz") #CLASE DEL CONTENEDOR DE NOMBRE DE USUARIO, COMENTARIO, HORA Y REACCIONES
        print(comentarios)

### div.xv55zj0.x1vvkbs.x1rg5ohu.xxymvpz CLASE EN LOS VIDEOS


# Publicacion sin Multimedia (Post/Imagen)
    except:
        try:
            # Seleccion de "Todos los comentarios"
            time.sleep(1)
            # Espera a que el botón sea clickeable
            boton = driver.find_element(By.XPATH, "//div[@role='button' and contains(., 'Más pertinentes')]")
            boton.click()

            time.sleep(2)
            boton = driver.find_element(By.XPATH, "//span[contains(text(), 'Todos los comentarios')]")
            boton.click()

            pyautogui.moveTo(x=785, y=879, duration=0.5)
            pyautogui.click()
            for _ in range(80):
                pyautogui.scroll(-300)
                time.sleep(2.5)


        except Exception as e:
            pass
            # print("no_button")
            # print("Ocurrió un error:", e)

        time.sleep(10)

        # Encontrar todos los elementos con la clase específica
        classCSScomentarios_ = "div.xv55zj0.x1vvkbs.x1rg5ohu.xxymvpz"

        comentarios = driver.find_elements(By.CSS_SELECTOR,classCSScomentarios_) #CLASE DEL CONTENEDOR DE NOMBRE DE USUARIO, COMENTARIO, HORA Y REACCIONES

## Extraer los textos de los comentarios
 
    textos_comentarios = [comentario.text for comentario in comentarios]

    try:
        print("Iniciando procesamiento de textos_comentarios...")
        procesados = [modelamiento(texto) for texto in textos_comentarios]
        # print(f"Procesados: {procesados}")

        flattened_data = [item for sublist in procesados for item in sublist]
        print(f"Datos aplanados: {flattened_data}")

        print("Creando DataFrame...")
        df = pd.DataFrame(flattened_data, columns=["Usuario", "Comentario", "Hora", "Reacciones"])
        print(f"DataFrame creado con {len(df)} filas")

        df["url_facebook"] = url
        print(f"Columna 'url_facebook' añadida con valor: {url}")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'data/data_{medio}_{timestamp}.xlsx'
        print(f"Guardando archivo Excel en: {filename}")

        df.to_excel(filename, index=False)
        print("Archivo guardado correctamente.")

    except Exception as e:
        print(f"Error detectado: {e}")



    driver.quit()
    print("Excel generado con éxito 🎉")   
    

def main(url):
    comentarios = ManagerFaceBookScrapper(url,medio=None)


if __name__ == "__main__":

    list_url = [
    # "https://www.facebook.com/adncl/posts/pfbid0dimR8jJYrbtkjZ7Vq2kufnMpa5r1Xty38mohvTWT7ssvJnQVDtgYDhTQ8EDiy3KZl",
    # "https://www.facebook.com/laterceracom/posts/pfbid02RqYJnUGiV66iGV4NfjDfUda5SixnBL9qQJoaJBZXz4789Xp8nKk29MomF72EVkNel",
    "https://www.facebook.com/thecliniccl/posts/pfbid02sVRG7cnEbHE8fxhDS18sf6dmNs5HcejpKw58x511c3DT1qqPwPeoVZ15LjQDgPw1l",
    "https://www.facebook.com/thecliniccl/posts/pfbid0uvCLbWU43SnqcvtNQEg8sxbag7chVHY4NN3ccFse1fFrM43EGAyWjn5qDR21GWFl",
    "https://www.facebook.com/thecliniccl/posts/pfbid038H9wE8q4Ag5BsD7emEogPKbHtbvXG6XYaZCHoeMaJt53X4KJqPqqWoecodPsQGjml"
]
    for url in list_url:
        main(url)