from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.common.keys import Keys
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import random
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


def crtl_a(navegador):
    action = ActionChains(navegador)
    action.key_down(Keys.CONTROL).send_keys('A').key_up(Keys.CONTROL).perform()

def Try_find_xp(navegador,elemento,timee):
    found=False
    for t in range(1,timee):
        
        try:
            myElem = WebDriverWait(navegador,3).until(EC.presence_of_element_located((By.XPATH, elemento)))
            found=True
            return found
        except TimeoutException:
            found=False
            time.sleep(1)
    if not found:
        print(elemento+' not found')
    return found

def click_xp(navegador,elemento):
    boo = False
    err1 = 0
    while err1 < 5:
        try:
            myElem = WebDriverWait(navegador,3).until(EC.presence_of_element_located((By.XPATH, elemento)))
            navegador.find_element(By.XPATH,elemento).click()
            boo = True
            break
        except:
            err1+=1
            print ("Loading took too much time!" + str(elemento))
            time.sleep(1)
    if not boo:
        1/0 #forçar error
        return boo    

def by_xpath(navegador,elemento,loop=4,error=False):
    boo = False
    err1 = 0
    while err1 < loop:
        try:
            myElem = WebDriverWait(navegador,3).until(EC.presence_of_element_located((By.XPATH, elemento)))
            navegador.find_element(By.XPATH,elemento).click()
 
            print('Found')
            boo = True
            break
        except:
            err1+=1
            print ("Loading took too much time!" + str(elemento))
            time.sleep(0.5)
    if error: return boo # antecipar o retorno quando eu quiser
    if not boo: 1/0 #forçar error
    return boo
            
def send_k(navegador,elemento,snd):
    boo = False
    if snd==None:
        click_xp(elemento)
        crtl_a()
        navegador.find_element(By.XPATH,elemento).send_keys(Keys.DELETE)
        boo=True
    else:
        try:
            click_xp(elemento)
            crtl_a()
            navegador.find_element(By.XPATH,elemento).send_keys(snd)
            boo = True
        except:
            print("Key not sent" + str(elemento))
    if not boo: 1/0 #forçar erro
    return boo

def include_k(navegador,elemento,snd):
    boo = False
    if snd!=None:
        try:
            click_xp(elemento)
            navegador.find_element(By.XPATH,elemento).send_keys(snd)
            boo = True
        except:
            print("Key not sent" + str(elemento))
    if not boo: 1/0 #forçar erro
    return boo

def get_text(navegador,elemento):

    a = navegador.find_element(By.XPATH,elemento).text
    
    return a

def click_in_list(navegador,elemento,string):
    err=True
    loop=0
    while loop<5:
        for i in navegador.find_elements(By.XPATH, elemento):
            try:
                if string in i.text:
                    a=i.text
                    i.click()
                    err=False
                    break
            except: 1
        if not err:
            break
        time.sleep(1)
        loop+=1
    return err

def send_xpath(navegador,elemento,snd,loop=4,error=False):
    boo = False
    err1 = 0
    while err1 < loop:
        try:
            myElem = WebDriverWait(navegador,3).until(EC.presence_of_element_located((By.XPATH, elemento)))
            navegador.find_element(By.XPATH,elemento).send_keys(snd)
 
            print('Found')
            boo = True
            break
        except:
            err1+=1
            print ("Loading took too much time!" + str(elemento))
            time.sleep(1)
    if error: return boo
    if not boo: 1/0 #forçar error
    return boo



