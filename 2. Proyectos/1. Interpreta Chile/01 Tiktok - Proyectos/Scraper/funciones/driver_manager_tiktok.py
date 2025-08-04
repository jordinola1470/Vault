import pandas as pd

import time
import pyautogui
import os
import random

from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from funciones.utils_tiktok import scroll_page
# from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

from funciones.utils_tiktok import procesar_comentarios



def ManagerDriverTiktok(VideoURL):


    # # List of User-Agent strings
    # user_agents = [
    #     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    #     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    #     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    #     "Mozilla/5.0 (iPhone14,3; U; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19A346 Safari/602.1"
    #     # Add more User-Agent strings as needed
    # ]


    # # Choose a random User-Agent from the list
    # random_user_agent = random.choice(user_agents)
   
    chrome_options = Options()
    # chrome_options.add_argument(f"--user-agent={random_user_agent}")
    chrome_options.add_argument("--incognito")  # Modo incógnito
    chrome_options.add_argument("--disable-cache")  # Deshabilitar la caché
    chrome_options.add_argument("--disable-application-cache")  # Deshabilitar caché de aplicaciones
    chrome_options.add_argument("--disable-gpu")  # Deshabilitar GPU (opcional en algunos casos)
    chrome_options.add_argument("--disable-dev-shm-usage")  # Para evitar problemas en entornos Linux
    chrome_options.add_argument("--no-sandbox")  # Para evitar problemas de permisos en Linux
    chrome_options.add_argument("--disable-features=NetworkService,NetworkServiceInProcess")  # Más control sobre caché

    chrome_options.add_argument("--start-maximized")  # Abre la ventana en pantalla completa
    # Crear la instancia del WebDriver con las opciones configuradas
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()



    # # Ruta manual de geckodriver
    # geckodriver_path = r"C:\Users\Dell\.cache\selenium\geckodriver\win64\0.36.0\geckodriver.exe"

    # # Configuración del servicio de Firefox
    # service = Service(geckodriver_path)

    # # Opciones de Firefox
    # firefox_options = Options()
    # firefox_options.set_preference("browser.privatebrowsing.autostart", True)  
    # firefox_options.profile = profile
    # # firefox_options.add_argument("-private")  # Modo incógnito

    # # Crear instancia de WebDriver con el servicio configurado
    # driver = webdriver.Firefox(service=service, options=firefox_options)

    if VideoURL is not None :

        time.sleep(3)
        driver.get(VideoURL)

    
        try:
            time.sleep(4)
            
            # Espera a que el botón sea clickeable
            boton = driver.find_element(By.XPATH, value="/html/body/div[1]/div[2]/div[2]/div/div[2]/div[2]/div[2]/div[1]/div[2]/div[1]/button/div/div/span/div/div").click()
            
            print("⌛ Esperando 15 segundos para resolver CAPTCHA...")
            time.sleep(15)

            # Move mouse with a smooth transition
            pyautogui.moveTo(1800, 500, duration=0.5)  # Moves in 1.5 seconds
           
            for _ in range(20):  # Repeat 4 times
                pyautogui.click() 
                pyautogui.scroll(-800)  # Scroll up by 500
                time.sleep(0.5)  # Short delay to mimic human behavior


            print("⌛ Esperando antes de iniciar la extracción de datos...")
            time.sleep(5)  # 🔥 Damos tiempo al scroll para que avance primero

            # Comentarios CSS
            comentarios        = driver.find_elements(By.CSS_SELECTOR,"div.css-1k8xzzl-DivCommentContentWrapper") #CLASE DEL CONTENEDOR DE NOMBRE DE USUARIO, COMENTARIO, HORA Y REACCIONES
    
            textos_comentarios = [comentario.text for comentario in comentarios]
            procesados          = procesar_comentarios(lista=textos_comentarios)

            # Convertir la lista a un DataFrame
            TiktokCommentCSS = pd.DataFrame([
                {
                    "URL": VideoURL,  # URL fija para todas las filas
                    "Username": fila[0],
                    "Level": 1,  # Nivel fijo
                    "Comment": fila[1],
                    "Date": fila[2],
                    "Likes": fila[3] if fila[3] else "0"  # Si Likes está vacío, poner "0"
                }
                for fila in procesados
            ])


            timestamp        = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename_comment = f'data/data_{timestamp}.xlsx'
            # filename_video   = f'data/data_video_{timestamp}.xlsx'

            TiktokCommentCSS.to_excel(filename_comment,index=False)
            print("🔥 Proceso finalizado.")
            
            driver.quit()
            

        except:    
            
            print("⌛ Esperando 15 segundos para resolver CAPTCHA...")
            time.sleep(15)
            scroll_page(driver)

            print("⌛ Esperando antes de iniciar la extracción de datos...")
            time.sleep(10)  # 🔥 Damos tiempo al scroll para que avance primero

            # TIKTOK VIDEO STATS SCRAPPER
            VideoUserName = '/html/body/div[1]/div[2]/div[2]/div/div[2]/div[1]/div[1]/div[2]/div[1]/div/a[2]/span[1]'
            VideoLikes    = '/html/body/div[1]/div[2]/div[2]/div/div[2]/div[1]/div[1]/div[1]/div[4]/div[2]/button[1]/strong'
            VideoComments = '/html/body/div[1]/div[2]/div[2]/div/div[2]/div[1]/div[1]/div[1]/div[4]/div[2]/button[2]/strong'
            VideoSaves    = '/html/body/div[1]/div[2]/div[2]/div/div[2]/div[1]/div[1]/div[1]/div[4]/div[2]/button[3]/strong'
            VideoShares   = '/html/body/div[1]/div[2]/div[2]/div/div[2]/div[1]/div[1]/div[1]/div[4]/div[2]/button[4]/strong'

            VideoMusic = '/html/body/div[1]/div[2]/div[2]/div/div[2]/div[1]/div[1]/div[2]/div[2]/h4/a/div'

            try:
                video_username = driver.find_element(By.XPATH, value = f'{VideoUserName}').text
                video_song     = driver.find_element(By.XPATH, value = f'{VideoMusic}').text
                video_likes    = driver.find_element(By.XPATH, value = f'{VideoLikes}').text
                video_comment  = driver.find_element(By.XPATH, value = f'{VideoComments}').text 
                video_saves    = driver.find_element(By.XPATH, value = f'{VideoSaves}').text 
                video_shares   = driver.find_element(By.XPATH, value = f'{VideoShares}').text     
            
                print (f"Likes:{video_likes}, Comments & Replies:{video_comment}, Shares:{video_shares}, Saves:{video_saves}, Music:{video_song}\n")
                
                VideoDataStats = pd.DataFrame([{    "URL": VideoURL,  "Username": video_username,
                                                    "Song": video_song,
                                                    "Likes": video_likes,
                                                    "Comments": video_comment,
                                                    "Saves" : video_saves, 
                                                    "Shares": video_shares}])
            
            except Exception as e:
                
                video_username = 0
                video_song     = 0
                video_likes    = 0
                video_comment  = 0
                video_saves    = 0
                video_shares   = 0
            
                print (f"Likes:{video_likes}, Comments & Replies:{video_comment}, Shares:{video_shares}, Saves:{video_saves}, Music:{video_song}\n")
                
                VideoDataStats = pd.DataFrame([{    "URL": VideoURL,  "Username": video_username,
                                                    "Song": video_song,
                                                    "Likes": video_likes,
                                                    "Comments": video_comment,
                                                    "Saves" : video_saves, 
                                                    "Shares": video_shares}])

            ##COMENTARIOS LOOP            
            DivCommentContentWraper   = '/html/body/div[1]/div[2]/div[2]/div/div[2]/div[1]/div[2]/div[2]/div['
            UserName                  = ']/div[1]/div[2]/div[1]/div[1]/div/a'
            CommentLevel_1            = ']/div[1]/div[2]/span'  
            CommentLevel_1_Date       = ']/div[1]/div[2]/div[2]/div/span[1]'
            CommentLevel_1_Likes      = ']/div[1]/div[2]/div[2]/div/div'  
            
            Centinela         = True
            NumberUserInterno = 1

            TiktokCommentBase = pd.DataFrame(columns=["Username","Level", "Comment", "Date", "Likes"])

            while Centinela == True: 
                    
                    try:
                        username_thread = driver.find_element(by=By.XPATH,value= f'{DivCommentContentWraper}{NumberUserInterno}{UserName}').get_attribute('href')
                        main_comment    = driver.find_element(By.XPATH, value = f'{DivCommentContentWraper}{NumberUserInterno}{CommentLevel_1}').text  
                        date_comment    = driver.find_element(By.XPATH, value = f'{DivCommentContentWraper}{NumberUserInterno}{CommentLevel_1_Date}').text  
                        likes_comment   = driver.find_element(By.XPATH, value = f'{DivCommentContentWraper}{NumberUserInterno}{CommentLevel_1_Likes}').text  

                        TemporalDataRow    = pd.DataFrame([{"URL":VideoURL,"Username": username_thread,"Level": 1,"Comment": main_comment,"Date": date_comment, "Likes": likes_comment}])
                        TiktokCommentBase     = pd.concat([TiktokCommentBase,TemporalDataRow]) 

                        print(f"Data {NumberUserInterno}: {username_thread};{main_comment};{date_comment};{likes_comment}")

                        NumberUserInterno  = NumberUserInterno + 1

                    except Exception as e:
                        # print(e)

                        timestamp        = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename_comment = f'data/data_{timestamp}.xlsx'
                        filename_video   = f'data/data_video_{timestamp}.xlsx'


                        TiktokCommentBase.to_excel(filename_comment,index=False)
                        VideoDataStats.to_excel(filename_video,index=False)
                        
                        driver.quit()
                        
                        print("🔥 Proceso finalizado.")


                        break


