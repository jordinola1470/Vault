#MODULES OF SELENIUM
from selenium import webdriver
from selenium.webdriver.common.by import By

#SECONDARY LIBRARIES 
import pandas as pd
import numpy as np
import os
import re
import time
import ssl
import sys
import math
import traceback

#LIBRARY FOR DEACTIVATION OF ALERTS
import warnings
warnings.filterwarnings('ignore')


'''
------------------------------------

DRIVER OBJECT
   - OPTIONS
   - URL

------------------------------------
'''

#SSL Protocols (for secure connections)
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


#Firefox Options
firefox_profile = webdriver.FirefoxOptions()
firefox_profile.set_preference("browser.download.folderList", 2)
firefox_profile.set_preference("browser.download.dir", 'descargas')
firefox_profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")

#Firefox navigator with proper profile configurated
driver = webdriver.Firefox(options=firefox_profile)

#Driver instance -  URL Access (web page that is going to be opened)
PAGINA_URL = 'https://www.tiktok.com/@migracioncol'
driver.get(PAGINA_URL)




'''-----------------------------------------------------------------------------------------------------------------------------------

AUXILIAR FUNCTIONS

'''

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

def scroll_down(load_time, times, bottom,driver):
  i = 0
  # Get scroll height
  last_height = driver.execute_script("return document.body.scrollHeight")
  browser_window_height = driver.get_window_size(windowHandle='current')['height']
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
        print('Going to: ' + str(browser_window_height + current_position - bottom) + ' being in: ' + str(current_position))
        scrolling -= 1
        barra_carga(load_time)
    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
    i = i + 1
  return None

'''------------------------------------------------------------------------------------------------------------------------------'''




'''
------------------------------------

MAIN CODE - FUNCTION

------------------------------------
'''

print("Waiting for the resolve of the CAPTCHA....")
barra_carga(20)


i = 1 #this is the begining of the bucle (the first roung)
lista_videos = "/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div[2]/div/div[" #this is the main block of HTML (the point of reference or the body of the HMTL, the root of it) 
centinela = True
base_final = pd.DataFrame()

'''
The 'while' keyword creates a bucle based on a condition. In this case this bucle is looking for the principal data giving by the posted videos
and when there is not more videos to get information from this bucle ends, creating a excel sheet with all the possible information 
collected trought the bucle like : username , descriptions, hashtags, url video link, views.
'''

while centinela == True:
   try:
    
    #USER NAME (who publish the tik tok)
    user_name = driver.find_element(By.XPATH, value = "/html/body/div[1]/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/h1").text
    
    #DESCRIPTION (of the tik tok video) 
    '''This include the sintax of the description and the hashtags added to the description'''

    ##Getting the main description of the video (including the # in a separate column)
    try:
       description = driver.find_element(By.XPATH, value = lista_videos + str(i) + "]/div[2]").text
      #  hashtags = re.findall(r'\#\w+', description)
      #  hashtags_str = ' '.join(hashtags)
    except:
       description = 'No Description Found'

    #URL LINK OF THE VIDEO

    link = driver.find_element(By.XPATH, value = lista_videos + str(i) + "]/div/div/a").get_attribute('href')

    #DATE (of publish)
   #  date = driver.find_element(By.XPATH, value = lista_videos + str(i) + "]/div[1]/div/div/a/div/div[2]/div").text

    #VIEWS (number in text format)
    views = driver.find_element(By.XPATH, value = lista_videos + str(i) + "]/div[1]/div/div/a/div[1]/div[2]/strong").text
    
    print(str(i),"validation : ",user_name,description,link,views)
     

    d = {"description": description, "user": user_name, "link":link, "views": views}
    
    base_temporal = pd.DataFrame(data=d,index=[i])
    base_final = pd.concat([base_final, base_temporal], ignore_index=True)
   
    i += 1 #this is a very important part of the bucle, this add 1 more round to the bucle to run.   

    barra_carga(5)
    scroll_down(2,1,600,driver)
    
    try:
       driver.find_element(By.XPATH, value= "/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/div/div/div[1]")
    except:
       print('CAPTCHA - RESOLVE')

   except:
      print('Finished')
      centinela = False
      base_final.to_excel('base_feed_test_migracol_account.xlsx',index=False)
      driver.close()


  