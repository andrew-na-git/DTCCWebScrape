from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC

import time
import requests
from bs4 import BeautifulSoup

import os
import glob
import zipfile
import numpy as np

obj = 'Rates'

path = r".\chromedriver_win32\chromedriver.exe"
website = 'https://pddata.dtcc.com/gtr/dashboard.do'
download_path = r'.\Data'
download = download_path + '\\' + obj

## retrieve iframe src
sess = requests.Session()
req = sess.get(website)
soup = BeautifulSoup(req.content, 'html.parser')
src = soup.select_one('#cumulativeSliceFrame').attrs['src']
print(src)

## retrieving data
option = Options()
option.headless = True
for i in np.arange(0, 30):
    with wd.Chrome(path, options=option) as brws:
        brws.command_executor._commands['send_command'] = ('POST', '/session/$sessionId/chromium/send_command')
        params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download}}
        command_result = brws.execute("send_command", params)
        wait = WebDriverWait(brws, 10)
        brws.get(src)
        brws.find_element_by_link_text(obj).click()
        if obj == 'Rates':
            x_path = '//*[@id="ratesSwapsData"]'+'/table[2]/tbody/tr['+str(int(i+1))+']/td[1]/a'
        if obj == 'Credits':
            x_path = '//*[@id="creditSwapsData"]'+'/table[2]/tbody/tr['+str(int(i+1))+']/td[1]/a'
        if obj == 'Equities':
            x_path = '//*[@id="equitiesSwapsData"]'+'/table[2]/tbody/tr['+str(int(i+1))+']/td[1]/a'
        #waiter.find_element(brws, x_path, XPATH).click()
        WebDriverWait(brws, 5).until(
        EC.presence_of_element_located((By.XPATH, x_path))).click()
        file_count = lambda x: len(x("{0}/*.zip*".format(download))) == i+1
        try:
            WebDriverWait(glob.glob, 300).until(file_count)
        except:
            continue
        finally:
            brws.quit()