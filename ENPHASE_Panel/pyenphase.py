# Description : Get Home Solar EnPhase System Info , webscraps local EnPhase Envoy network enphase device
# Date : 07/18/2020
# Author : mcalyer
# Notes : 
# url may change if system needs to be rebooted 
# Alternate method : Scrap data from enphase website , requires internet , login
# Alternate method : Use enphase API , requires internet , login , API key
# Using BeautifulSoup makes it easy , more challenging for embbeded devices 
# Example of webpage :   <tr><td>Lifetime generation</td>    <td> 29.6 MWh</td></tr><tr><td>Currently generating</td>    <td> 1.97 kW</td></tr>

import requests
from bs4 import BeautifulSoup
import sys


enphase_local_ip = 'http://192.168.1.160'

enphase_webpage_07_2020 = [
'Lifetime generation'             ,
'Currently generating'            ,
'Last connection to website'      ,
'Number of Microinverters'        ,
'Number of Microinverters Online' ,
'Current Software Version'        ,
'Software Build Date'             ,
'Database Size'                   ,
'Current Timezone'                ,
'Envoy IP Address'                ,
'Envoy Mac Address'               ,
'Wi-Fi MAC Address'               ,
'Envoy Power Line Device' ]

enphase_data = [
'Lifetime generation'             ,
'Currently generating'            ,
'Last connection to website'      ,
'Number of Microinverters'        ,
'Number of Microinverters Online' ,
'Current Software Version'        ,
'Software Build Date'             ,
'Database Size'                   ,
'Current Timezone'                ,
'Envoy IP Address'                ,
'Envoy Mac Address'               ,
'Wi-Fi MAC Address'               ,
'Envoy Power Line Device'         ]

class EnPhase_Solar():
    def __init__(self,url,web_page_ids):
        self.url = url
        self.web_page_ids = web_page_ids
        self.num_micro_invert_str = 0
        self.num_micro_invert_online_str = 0
        self.microinvert_status = False
        self.last_data = None
        
    def get_data(self):
        page = requests.get(self.url)
        if 200 != page.status_code: 
            return 1 , 'http request Failed'   
        soup = BeautifulSoup(page.text, 'html.parser')
        self.last_data = {}      
        for i, id in enumerate(self.web_page_ids):    
            q = soup.find('td' , string = id)
            if q == None:
                self.last_data = {}    
                return 1 , 'Invalid data'                    
            v = q.find_next()
            s = v.string  
            self.last_data[enphase_data[i]] = s           
        return 0 ,  self.last_data       
 
    def energy_generation(self):
        return self.last_data['Currently generating']        
        
    def panel_status(self):
        num_inv = int(self.last_data['Number of Microinverters'])     
        num_inv_online = int(self.last_data['Number of Microinverters Online']) 
        num_inv_good = num_inv - num_inv_online      
        status = 'All Panels On Line'  
        if 0 != num_inv_good:       
            status = str(num_inv_online) + '/' +  str(num_inv) + '  Panels On Line'                   
        return status   

    def connect_status(self):
        return self.last_data['Last connection to website']   
        
enphase = EnPhase_Solar(enphase_local_ip,enphase_webpage_07_2020) 

def main():
    #enphase = EnPhase_Solar(enphase_local_ip,enphase_webpage_07_2020)   
    result , data = enphase.get_data()
    if result:
        print(result)
        sys.exit(0)
    for key,value in data.items():       
        sp = 40 - len(key) 
        print(key + sp * ' '  + value)
    
    
if __name__ == "__main__":
    main()
