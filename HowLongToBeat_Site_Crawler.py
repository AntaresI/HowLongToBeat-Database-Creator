
import re
import requests
from bs4 import BeautifulSoup
import time
import numpy as np

class HowLongToBeat_Crawler:
    
   def __init__(self,url_num=0):
       self.url_num = url_num
       self.check_response = True
       time.sleep(2)
       
       url = 'https://howlongtobeat.com/game/'+str(url_num)  #
       
       headers = {
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0', 'Accept': 'application/json'
       }
       
       response = requests.get(url, headers=headers)
       
       if response.status_code == 404:
           print("PAGE 404 ERROR")
           self.check_response = False
       self.soup = BeautifulSoup(response.text, "html.parser")
       
   def scrape(self):
       
       if self.check_response == False:
           return None
       
       game_info = {}
       
       game_info['title'] = self.get_title(self.soup)
       game_info['log_statistics'] = self.get_log_statistics(self.soup)
       
       game_durations, online = self.get_time_spent_playing(self.soup)
       game_info['durations'] = game_durations
       game_info['online'] = online
       
       other_info = self.get_info(self.soup)
   
       game_info['description'] = other_info[0]
       game_info['platforms'] = other_info[1].split(", ")
       game_info['genres'] = other_info[2].split(", ")
       game_info['developers'] = other_info[3].split(", ")
       game_info['publishers'] = other_info[4].split(", ")
       game_info['releases'] = other_info[5]
       
       return game_info
   
   def get_title(self,soup):
       
       title = soup.find("div", class_='GameHeader_profile_header__q_PID shadow_text').get_text(strip=True)
       
       return title

   def get_log_statistics(self,soup):
       
       stats = soup.find_all("div", class_='GameHeader_profile_details__oQTrK')[0].find_all("li")
       
       game_statistics = []
       
       for i in range(len(stats)):
           
           stat = self.number_cleaner(stats[i].get_text().split()[0])
           game_statistics.append(stat)
           
       return game_statistics

   def get_time_spent_playing(self,soup):
       # durations = soup.find_all("li", class_=re.compile("GameStats_short__tSJ6I time_\d+$"))
       durations = soup.find_all("li", class_=re.compile("GameStats_(long|short)__(tSJ6I|h3afN) time_\d+$"))
       off_or_on = "Offline"
       game_durations = []
       
       for i in range(len(durations)):
           if i == 4:   #Sometimes there are 2 sets of durations for different platforms, but they pretty much don't differ at all, so I want only one set which is at most 4 elements
               break
        
           duration = self.array_cleaner(durations[i].find("h5").get_text().split())
           
           if duration[1] == "Minutes":   #In case the units are minutes instead of usual hours, convert it to hours
               duration[0]=str(float(duration[0])/10/6)
               
           list_of_durations = []   #For averaging intervals, should there be some as duration instead of one number, example is Star Wars: The Old Republic
         
           for tup in duration:
               try:
                   list_of_durations.append(float(tup))
               except ValueError:
                   pass
               
           
           duration = np.mean(list_of_durations)
           
           game_durations.append(duration)
           
       if len(game_durations)<4:
           off_or_on = "Online"
           game_durations_dictionary = {}
           game_durations_dictionary['Vs.'] = game_durations[:-1]
           game_durations_dictionary['Co-Op'] = game_durations[:-2]
           if len(game_durations)<3:
               game_durations_dictionary['Single-Player'] = None
           else:
               game_durations_dictionary['Single-Player'] = game_durations[:-3]
           game_durations_dictionary['Main Story'] = None
           game_durations_dictionary['Main + Extras'] = None
           game_durations_dictionary['Completionist'] = None
           game_durations_dictionary['All Styles'] = None
       else:
           game_durations_dictionary = {}
           game_durations_dictionary['Vs.'] = None
           game_durations_dictionary['Co-Op'] = None
           game_durations_dictionary['Single-Player'] = None
         
           game_durations_dictionary['Main Story'] = game_durations[0]
           game_durations_dictionary['Main + Extras'] = game_durations[1]
           game_durations_dictionary['Completionist'] = game_durations[2] 
           game_durations_dictionary['All Styles'] = game_durations[3]
           
       return game_durations_dictionary, off_or_on


   def get_info(self,soup):
       info = soup.find_all("div", class_=re.compile("GameSummary_profile_info__HZFQu(,?.*)"))
       
       info_arr = []
       
       desc = info[0].get_text(strip=True)
       if "...Read More" in desc:     #Sometimes there might be a span element which hides some text and user must click Read More, BeautifulSoup reads both Read More and the hidden text, but ties it together, so the ...Read More has to be removed
          desc = self.replace_word(desc,"...Read More")
       
       info_arr.append(desc)  
       
       if "How long is" in info[1].get_text(strip=True):   #Sometimes there can be a How long is... element, I don't want anything from it, but it messes up the iteration so I have to remove it
           info.remove(info[1])
           
       platforms = info[1].get_text(strip=True)   
       platforms = re.sub(r'(Platforms|Platform):',"",platforms)
       info_arr.append(platforms)
       
       genres = info[2].get_text(strip=True)
       genres = re.sub(r'(Genres|Genre):',"",genres)
       info_arr.append(genres)
       
       devs = info[3].get_text(strip=True)
       devs = re.sub(r'(Developers|Developer):',"",devs)
       info_arr.append(devs)
       
       publishers = info[4].get_text(strip=True)
       publishers = re.sub(r'(Publishers|Publisher):',"",publishers)
       info_arr.append(publishers)
       
       releases = {}
       for j in range(5,8):
           if "Updated" in info[j].get_text(strip=True):
               break
           release = info[j].get_text(strip=True)
           releases[release[0:2]] = release[3:]
           # NA_release = replace_word(NA_release, "NA:")
           # info_arr.append(NA_release)
           
           # EU_release = info[6].get_text(strip=True)
           # EU_release = replace_word(EU_release, "EU:")
           # info_arr.append(EU_release)
       if 'EU' not in releases.keys():
           releases['EU'] = None
       if 'NA' not in releases.keys():
           releases['NA'] = None
       if 'JP' not in releases.keys():
           releases['JP'] = None    
       info_arr.append(releases)
       return info_arr

   def replace_word(self,string, word):
       if type(word) != str:
           print("Word must be a string!")
           return string
              
       else: 
           return string.replace(word,"")
   def array_cleaner(self,array):
       
       for i in range(len(array)):
           
           array[i] = self.number_cleaner(array[i]) 
       return array

   def number_cleaner(self,string):
       
       if '%' in string:
           string = string.replace('%','')   #I don't want percents
           
       if 'K' in string:
           string = string.replace('K','')   #Convert K's to thousands, so I need to temporarily turn the string into a number and then back into a string
           string = int(float(string)*1000)
           string = str(string)
           
       if '½' in string:
           string = string.replace('½','.5')
           
       if '--' in string:
           string = '0'
           
       return string            
       
    
