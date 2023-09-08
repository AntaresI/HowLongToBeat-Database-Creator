
import re
import requests
from bs4 import BeautifulSoup
import time
import numpy as np

class HowLongToBeat_Crawler:
    
   def __init__(self,url_num=0):
       self.url_num = url_num
       time.sleep(2)
       
       url = 'https://howlongtobeat.com/game/'+str(url_num)  #
       
       headers = {
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0', 'Accept': 'application/json'
       }
       
       response = requests.get(url, headers=headers)
       
       if response.status_code == 404:
           print("PAGE 404 ERROR")
           return None
       soup = BeautifulSoup(response.text, "html.parser")
       
   def scrape(self):
       
       
       
    
