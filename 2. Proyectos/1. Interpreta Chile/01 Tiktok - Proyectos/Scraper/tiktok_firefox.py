import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By

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


def extract_data(driver):
    """Extrae datos con un pequeño retraso para permitir el scroll inicial."""

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

        VideoDataStats = pd.DataFrame([{ "Username": video_username,
                                            "Song": video_song,
                                            "Likes": video_likes,
                                            "Comments": video_comment,
                                            "Saves" : video_saves, 
                                            "Shares": video_shares}])
        
       
    
    except Exception as e:
        print("No video stats")
        pass

    time.sleep(3)
    
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
                
                
                TemporalDataRow    = pd.DataFrame([{ "Username": username_thread,"Level": 1,"Comment": main_comment,"Date": date_comment, "Likes": likes_comment}])
                TiktokCommentBase     = pd.concat([TiktokCommentBase,TemporalDataRow]) 

                print(f"Data {NumberUserInterno}: {username_thread};{main_comment};{date_comment};{likes_comment}")

                NumberUserInterno  = NumberUserInterno + 1

                
            except Exception as e:
                print(e)
                TiktokCommentBase.to_excel('data/coments_data.xlsx',index=False)
                VideoDataStats.to_excel('data/stats_data.xlsx',index=False)
                break


def Async_ManagerDriverTiktok(VideoURL):
    driver = webdriver.Firefox()
    driver.get(VideoURL)

    print("⌛ Esperando 15 segundos para resolver CAPTCHA...")
    time.sleep(15)

    scroll_page(driver)  # 🔽 Primero hace el scroll hasta el final
    extract_data(driver)  # 🔍 Luego extrae los datos de manera síncrona


    # driver.quit()
    print("🔥 Proceso finalizado.")


if __name__ == "__main__":
    VideoURL = "https://www.tiktok.com/@nightsoline/video/7341084291478179077?q=boone%20benson&t=1741536291369"
    Async_ManagerDriverTiktok(VideoURL)