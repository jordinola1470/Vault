import ssl
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from functions.funciones_secundarias import barra_carga,scroll_down,scroll_down_times


def ManagerDriverInstagram(paginaURL,username,password,links):

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE 

    # Firefox Options
    firefox_profile = webdriver.FirefoxOptions()
    firefox_profile.set_preference("browser.download.folderList", 2)
    firefox_profile.set_preference("browser.download.dir", 'descargas')
    firefox_profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")

    # Firefox navigator with proper profile configurated
    driver = webdriver.Firefox(options=firefox_profile)
    driver.get(paginaURL)
    barra_carga(10,'PAGINA CARGADA\n')

# ================================

    # Encuentra los campos de entrada para el nombre de usuario y la contraseña
    username_input = driver.find_element(By.XPATH, value = "//input[@name='username']")
    password_input = driver.find_element(By.XPATH, value = "//input[@name='password']")

    # Ingresa tus credenciales de inicio de sesión
    username_input.send_keys(username)
    password_input.send_keys(password)

    # Envía el formulario de inicio de sesión
    password_input.send_keys(Keys.RETURN)

    # Espera un momento para el inicio de sesión
    barra_carga(10,'ACCESO EXITOSO\n')

# ================================
    driver.get(links)
    barra_carga(10,'ACCESO PERFIL EXITOSO\n')
    scroll_down_times(driver,3)
# ================================


    # bloque_post = "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/div[2]/div/div[1]/div[1]/a" 
    
    # /html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/div[2]/div/div[ 1 ]/div[ 1 ]/a
    # /html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/div[2]/div/div[ 1 ]/div[ 2 ]/a
    # /html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/div[2]/div/div[ 1 ]/div[ 3 ]/a

    # /html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/div[2]/div/div[ 2 ]/div[ 1 ]/a
    # /html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/div[2]/div/div[ 2 ]/div[ 2 ]/a
    # /html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/div[2]/div/div[ 2 ]/div[ 3 ]/a


    bloque_post = "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/div[2]/div/div["

    centinela    = True
    commt_inter  = 1
    commt_exter  = 1
    maxim_inter  = 3   

    while centinela == True: 

        try:
            # Intentar encontrar el elemento usando el XPath
            elemento = driver.find_element(By.XPATH, value=f"{bloque_post}{commt_exter}]/div[{commt_inter}]/a")

            # Extraer el atributo href del elemento
            href = elemento.get_attribute('href')

            # Si el href está vacío o es None, extraer el texto
            if href is None or href == "":
                # Extraer el texto visible del enlace
                texto_visible = elemento.text
                print(f'Texto visible: {texto_visible}')
            else:
                print(f'URL del post bloque:{commt_exter} - post:{commt_inter}: {href}')# Usa href aquí para imprimir el URL

            commt_inter = commt_inter + 1
            time.sleep(3)  # Esperar para ver el resultado
            
            if commt_inter > maxim_inter:
                commt_inter = 1  # Reiniciar el contador interno
                commt_exter += 1  # Pasar al siguiente grupo externo
                scroll_down_times(driver,1)
                time.sleep(3)    

        except Exception as e:
            print(f'Error: {e}')
            scroll_down_times(driver,2)
            time.sleep(5)
            continue
            # centinela = False





# PaginaURL = "https://www.instagram.com/"
# UserName  = "j.alonsoordinola@gmail.com"
# PassWord  = "Libertad5%"


