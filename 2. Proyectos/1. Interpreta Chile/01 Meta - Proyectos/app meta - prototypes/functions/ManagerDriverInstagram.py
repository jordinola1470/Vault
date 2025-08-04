
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import ssl
import time



class DriverInstagramManager:
    def __init__(self, paginaURL, username, password):
        # Configurar SSL
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        # Opciones del navegador Firefox
        firefox_profile = webdriver.FirefoxOptions()
        firefox_profile.set_preference("browser.download.folderList", 2)
        firefox_profile.set_preference("browser.download.dir", 'descargas')
        firefox_profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")

        # Inicializar WebDriver
        self.driver = webdriver.Firefox(options=firefox_profile)
        
        # Navegar a la página de inicio de sesión de Instagram
        self.driver.get(paginaURL)
        time.sleep(3)  # Esperar a que cargue la página (se puede mejorar con WebDriverWait)
        
        # Realizar el inicio de sesión
        self.login(username, password)

    def login(self, username, password):
        # Encontrar los campos de usuario y contraseña e iniciar sesión
        username_input = self.driver.find_element(By.XPATH, "//input[@name='username']")
        password_input = self.driver.find_element(By.XPATH, "//input[@name='password']")
        
        # Ingresar credenciales
        username_input.send_keys(username)
        password_input.send_keys(password)
        
        # Enviar formulario
        password_input.send_keys(Keys.RETURN)
        time.sleep(5)  # Esperar a que el inicio de sesión sea exitoso
        
    def acceder_perfil(self, perfilURL):
        # Navegar al perfil especificado
        self.driver.get(perfilURL)
        time.sleep(3)  # Esperar a que cargue el perfil
        
    def extraer_comentarios(self):
        # Aquí iría la lógica para extraer comentarios de las publicaciones del perfil
        # Por ejemplo, encontrar los elementos HTML de los comentarios y extraer su contenido.
        comentarios = self.driver.find_elements(By.CLASS_NAME, "comentario_clase")  # Ajustar selector según sea necesario
        lista_comentarios = [comentario.text for comentario in comentarios]
        return lista_comentarios
    
    def cerrar(self):
        # Cerrar el navegador cuando hayas terminado
        self.driver.quit()


    