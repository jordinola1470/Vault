import pandas as pd

import ssl
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from functions.funciones_secundarias import barra_carga,scroll_down,scroll_down_times


def ManagerDriverFacebook(facebookURL,username,password,GroupURL,ProfileURL):

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
    driver.get(facebookURL)
    barra_carga(10,'PAGE CORRECT LOADED\n')

# ================================

    # Encuentra los campos de entrada para el nombre de usuario y la contraseña
    username_input = driver.find_element(By.ID, value = "email")
    password_input = driver.find_element(By.ID, value = "pass")

    # Ingresa tus credenciales de inicio de sesión
    username_input.send_keys(username)
    password_input.send_keys(password)

    # Envía el formulario de inicio de sesión
    password_input.send_keys(Keys.RETURN)

    # Espera un momento para el inicio de sesión
    barra_carga(10,'ACCESS SUCCESFULL\n')

# ================================

    if GroupURL is not None :

        driver.get(GroupURL)
        driver.maximize_window()

        barra_carga(10,'PROFILE ACCESS GRANTED\n')
        scroll_down_times(driver,3)
                         
        main_container = "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[4]/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div["
        user_div       = "]/div/div/div/div/div/div/div/div/div/div[13]/div/div/div[2]/div"
        text_span      = "]/div/div/div/div/div/div/div/div/div/div[13]/div/div/div[3]/div[1]/div/div/div/div/span"

#"/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[4]/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div["]/div/div/div/div/div/div/div/div/div/div[13]/div/div/div[2]/div
#"/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[4]/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div[7]/div/div/div/div/div/div/div/div/div/div[13]/div/div/div[2]/div"
#" /html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[4]/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div[12]/div/div/div/div/div/div/div/div/div/div[13]/div/div/div[3]/div[1]/div/div/div/div/span"
        centinela      = True
        publication_inter  = 2

        xlxs_data_base = pd.DataFrame()  

        while centinela == True: 

            scroll_down_times(driver,1)
            barra_carga(4,' ')
            try: 
                user_container = driver.find_element(By.XPATH, value = f"{main_container}{publication_inter}{user_div}")

            ###SCRAP DATA

                #00# MAIN TEXT
                try:

                  ###VER MAS    
                    try:
                        try: 
                            publication_body = driver.find_element(By.XPATH, value = f"{main_container}{publication_inter}{text_span}")
                            # Busca el botón "Ver más" en el contenedor actual
                            button_ver_mas   = publication_body.find_element(By.XPATH, ".//div[@role='button' and text()='Ver más']").click()
                            print("\nEl botón 'Ver más' está presente en el contenedor.")
                            barra_carga(4,'click performed\n')
                        
                        except:
                            publication_body = driver.find_element(By.XPATH, value = f"{main_container}{publication_inter}{text_span}")
                            print("\nEl botón 'Ver más' no está presente en este contenedor.")
                            barra_carga(4,'\n')

                        publication_text_body = publication_body.text
                        print(publication_text_body)
                        barra_carga(5,f'publication : {publication_inter} complete \n')

                    except :
                        print("contenent has no text, is photo,video or post withoout text")
                        publication_inter  = publication_inter + 1


                #01## METADATA
                    try:

                        reactions_list = []

                        meta_span = "]/div/div/div/div/div/div/div/div/div/div[13]/div/div/div[4]/div/div/div[1]/div/div[1]/div/div[1]/span"

                        container_mdata = driver.find_element(By.XPATH,value = f"{main_container}{publication_inter}{meta_span}")
                        reactions_data  = container_mdata.find_elements(By.XPATH,".//div[@aria-label]")
                        reactions_text = [element.get_attribute("aria-label") for element in reactions_data]

                        for reactions in reactions_text:
                            print(reactions)
                            reactions_list.append(reactions)

                        #crear funcion auxiliar para separar la reaccion del numero, esto lo podemos hacer en funciones primarias y aplicarla
                        #aqui para poder crear una variable que sea la lista o tupla de la reaccion con su numero.

                        barra_carga(5,f'publication : {publication_inter} complete \n')

                    except Exception as e:
                        reactions_list = [" - "]
                        # print(f"NO REACTIONS {e}")
                        barra_carga(3,f'publication : {publication_inter} complete \n')

                        pass

                #01### COMMENTS
                    try:
                        
                        comm_body = "]/div/div/div/div/div/div/div/div/div/div[13]/div/div/div[4]/div/div/div["
                        comm_div  = "]/div/div/div[2]/div[1]/div[1]/div/div/div"
                        comm_int  = 3
                        data_comment = pd.DataFrame()

                        while True:
                            
                            try:

                                comm_text = driver.find_element(By.XPATH,value=f"{main_container}{publication_inter}{comm_body}{comm_int}{comm_div}").text
                            
                                temporal_data_comment = pd.DataFrame(data={"level":2,"publication":publication_text_body,"comments":comm_text},index=[comm_int])
                                data_comment          = pd.concat([data_comment,temporal_data_comment]) 

                                comm_int = comm_int + 1
                                barra_carga(3,f"\n {comm_text} \n")
                        
                            except Exception as e:
                                # print(e)
                                break

                    except Exception as e:
                        barra_carga(3,f'Level 2 comments : {publication_inter} complete \n {e}')
                        pass

                    temporal_data_publication  = pd.DataFrame(data = {"level":1,"publication":publication_text_body,"reactions":", ".join(reactions_list)},index=[publication_inter])
                    xlxs_data_base             = pd.concat([xlxs_data_base,temporal_data_publication,data_comment],ignore_index=True)

                    xlxs_data_base.to_excel('test.xlsx',index=False)

                    publication_inter  = publication_inter + 1
                
                except:
                    print("contenent has no text, is photo,video or post withoout text")
                    publication_inter  = publication_inter + 1

            except NoSuchElementException as e:
                
                print(f"NO MORE PUBLICATIONS IN THE GROUP \n {e}")
                break

                # try:
                #     publication_text_body = driver.find_element(By.XPATH, value = f"{main_container}{publication_inter}{text_span}").text
                #     print("\nEl botón 'Ver más' no está presente en este contenedor.")
                #     barra_carga(3,'\n')
                #     scroll_down_times(driver,3)

                #     print(publication_text_body)
                #     barra_carga(5,f'publication : {publication_inter} complete \n')


                # #02### METADATA
                #     try:

                #         reactions_list = []

                #         meta_span = "]/div/div/div/div/div/div/div/div/div/div[13]/div/div/div[4]/div/div/div[1]/div/div[1]/div/div[1]/span"

                #         container_mdata = driver.find_element(By.XPATH,value = f"{main_container}{publication_inter}{meta_span}")
                #         reactions_data  = container_mdata.find_elements(By.XPATH,".//div[@aria-label]")
                #         reactions_text = [element.get_attribute("aria-label") for element in reactions_data]

                #         for reactions in reactions_text:
                #             print(reactions)

                #         #crear funcion auxiliar para separar la reaccion del numero, esto lo podemos hacer en funciones primarias y aplicarla
                #         #aqui para poder crear una variable que sea la lista o tupla de la reaccion con su numero.

                #         barra_carga(5,f'publication : {publication_inter} complete \n')

                #     except Exception as e:
                #         reactions_list = [" - "]
                #         # print(f"NO REACTIONS {e}")
                #         barra_carga(3,f'publication : {publication_inter} complete \n')
                #         pass

                # #02### COMMENTS
                #     try:

                #         comm_body = "]/div/div/div/div/div/div/div/div/div/div[13]/div/div/div[4]/div/div/div["
                #         comm_div  = "]/div/div/div[2]/div[1]/div[1]/div/div/div"
                #         comm_int  = 3

                #         data_comment = pd.DataFrame()

                #         while True:
                            
                #             try:

                #                 comm_text = driver.find_element(By.XPATH,value=f"{main_container}{publication_inter}{comm_body}{comm_int}{comm_div}").text
                            
                #                 temporal_data_comment = pd.DataFrame(data={"level":2,"publication":publication_text_body,"comments":comm_text},index=[comm_int])
                #                 data_comment          = pd.concat([data_comment,temporal_data_comment]) 

                #                 comm_int = comm_int + 1
                #                 barra_carga(3,f"\n {comm_text} \n")
                        
                #             except Exception as e:
                #                 # print(e)
                #                 break

                #     except Exception as e:
                #         barra_carga(3,f'Level 2 comments : {publication_inter} complete \n {e}')
                #         pass

                #     temporal_data_publication  = pd.DataFrame(data = {"level":1,"publication":publication_text_body,"reactions":", ".join(reactions_list)},index=[publication_inter])
                #     xlxs_data_base             = pd.concat([xlxs_data_base,temporal_data_publication,data_comment],ignore_index=True)

                #     xlxs_data_base.to_excel('test.xlsx',index=False)

                #     publication_inter  = publication_inter + 1

        
                # except Exception as e:
                #     # Captura cualquier otra excepción inesperada y detiene el bucle
                #     print(f"Unexpected Error - Video instead of text detected: {e}") 
                    

                #     # # html_inicial = driver.page_source
                    
                #     # # scroll_down_times(driver,3)
                #     # # barra_carga(4,"verificando DOM\n")

                #     # # html_posterior = driver.page_source

                #     # # if html_inicial != html_posterior:

                #     barra_carga(1,f'publication : {publication_inter} was video : complete \n')
                #     publication_inter  = publication_inter + 1

                #     # # else:
                #     #     print("No se ha cargado nuevo contenido.")
                #     #     print("DOM COMPLETE - No more publications on the page")
                        

                        


    elif ProfileURL is not  None :

        pass


    else: print("Cannot proceed: URL is None")




















#     centinela    = True
#     commt_inter  = 1
#     commt_exter  = 1
#     maxim_inter  = 3   

#     while centinela == True: 

#         try:
#             # Intentar encontrar el elemento usando el XPath
#             elemento = driver.find_element(By.XPATH, value=f"{bloque_post}{commt_exter}]/div[{commt_inter}]/a")

#             # Extraer el atributo href del elemento
#             href = elemento.get_attribute('href')

#             # Si el href está vacío o es None, extraer el texto
#             if href is None or href == "":
#                 # Extraer el texto visible del enlace
#                 texto_visible = elemento.text
#                 print(f'Texto visible: {texto_visible}')
#             else:
#                 print(f'URL del post bloque:{commt_exter} - post:{commt_inter}: {href}')# Usa href aquí para imprimir el URL

#             commt_inter = commt_inter + 1
#             time.sleep(3)  # Esperar para ver el resultado
            
#             if commt_inter > maxim_inter:
#                 commt_inter = 1  # Reiniciar el contador interno
#                 commt_exter += 1  # Pasar al siguiente grupo externo
#                 scroll_down_times(driver,1)    

#         except Exception as e:
#             print(f'Error: {e}')
#             scroll_down_times(driver,2)
#             time.sleep(5)
#             continue
#             # centinela = False






