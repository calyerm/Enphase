# -*- coding: utf-8 -*-
"""
File : solar_panel.py
Date : 07/19/2020
Author : mcalyer
Description :  
              
notes : 



"""

import tkinter as tk
from PIL import ImageTk,Image 
import time , datetime
import threading
from pyenphase import enphase

class Control_Panel():
    def __init__(self,enphase):   
        # EnPhase interface
        self.enpahse = enphase
        
        # Window
        self.root = tk.Tk()     
        self.root.title("ENPHASE Solar")
        self.root.geometry("600x600")      
        self.root.resizable(False, False)    
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)     
        
        #Layout
        self.app_bg = 'lightgrey'
        self.root.configure(bg= self.app_bg)
        
        self.logo_region       = tk.Frame(self.root, background=self.app_bg  , width=600, height=100)
        
        self.blank_region      = tk.Frame(self.root, background=self.app_bg  , width=150, height=200)
        self.energy_numeric_region     = tk.Frame(self.root, background=self.app_bg   , width=250, height=200)
        self.energy_units_region       = tk.Frame(self.root, background=self.app_bg   , width=200, height=200)
        self.kw_region                 = tk.Frame(self.energy_units_region, background=  self.app_bg  , width=100, height=100)        
        self.kw_2        = tk.Frame(self.energy_units_region, background=self.app_bg   , width=100, height=100)
        self.kw_3        = tk.Frame(self.energy_units_region, background=self.app_bg   , width=100, height=100)
        self.kw_4        = tk.Frame(self.energy_units_region, background=self.app_bg   , width=100, height=100)
        
        self.blank_status_region     = tk.Frame(self.root, background=self.app_bg        , width=600, height=75)
        self.panel_status_region     = tk.Frame(self.root, background=self.app_bg        , width=600, height=75)
        self.connect_status_region   = tk.Frame(self.root, background=self.app_bg        , width=600, height=75)
        self.data_update_time_region = tk.Frame(self.root, background=self.app_bg        , width=600, height=75)
        
        self.root.columnconfigure(3, weight=1)
        self.energy_units_region.columnconfigure(2, weight=1)
        self.kw_region.grid(row=1,column=1,sticky="ew")
        self.kw_2.grid(row=2,column=2,sticky="ew")
        
        self.logo_region.grid(row=1, column=1, columnspan=3, sticky="ew")
        
        self.blank_region.grid(row=2, column=1, sticky="ew")
        self.energy_numeric_region.grid(row=2, column=2, sticky="ew")
        self.energy_units_region.grid(row=2, column=3, sticky="ew")
        
        self.blank_status_region.grid(row=3, column=1, columnspan=3, sticky="ew") 
        self.panel_status_region.grid(row=4, column=1, columnspan=3, sticky="ew")
        self.connect_status_region.grid(row=5,column=1,columnspan=3, sticky="ew")  
        self.data_update_time_region.grid(row=6,column=1,columnspan=3, sticky="ew")        
        
        # Static Elemnt , Image       
        canvas = tk.Canvas(self.logo_region, background=self.app_bg , width = 600, height = 105)  
        img = ImageTk.PhotoImage(Image.open("enphase.gif")) 
        canvas.create_image(1, 1, anchor=tk.NW,image=img)      
        canvas.pack()
        self.label = tk.Label(image=img)
        self.label.image = img         
        
        # Dynamic Elements , energy generated , energy Units
        self.energy_units = None     
        self.energy_numeric  = None
        self.update_energy('32.0  MWh')   
        
        # Dynamic elements , panel status
        self.panel_status  = None
        self.update_panel_status('Panels On Line')     
        
        # Dynamic elements , connection status
        self.connect_status  = None
        self.update_connect_status('Last connection')  

        # Dynamic elements , data time
        self.data_time  = None
        self.update_data_time(datetime.datetime.now())          

       # Start periodic update   
        self.update_timer = None     
        self.next_call = time.time()
        self.update()

    def update(self):
        # Get enphase data
        result , data =  self.enpahse.get_data()
        # Check for valid data 
        if result:
            #data not valid
            energy = '0.0 MWh'
            panel_status   = data 
            connect_status = data    
        else:            
            # update energy generation
            energy = self.enpahse.energy_generation()                       
            
            # update panel status
            panel_status = self.enpahse.panel_status()       
            
            # update connection status  
            connect_status = self.enpahse.connect_status()      
        
        # update
        self.update_energy(energy) 
        self.update_panel_status(panel_status)
        self.update_connect_status(connect_status)
        self.update_data_time(datetime.datetime.now())    
        
        # Start peroidic timer again        
        self.next_call = self.next_call + 60
        self.update_timer = threading.Timer(self.next_call - time.time(), self.update)
        self.update_timer.start()          
        
    def update_energy(self,eng_str):
        # get energy , units
        if self.energy_numeric != None:
           self.energy_numeric.destroy()    
        eng_num   = eng_str.split()[0]
        eng_units = eng_str.split()[1]    
        # update energy        
        self.energy_numeric = tk.Label(self.energy_numeric_region, bg=self.app_bg, text=eng_num , font=("bold", 80 ))
        self.energy_numeric.pack()
        # update energy units
        if self.energy_units != None:
           self.energy_units.destroy()   
        self.energy_units = tk.Label(self.kw_region, bg=self.app_bg , text=eng_units , font=("bold", 20))
        self.energy_units.pack()    
        
    def update_panel_status(self,status):
        if self.panel_status != None:
           self.panel_status.destroy()  
        color='green'              
        self.panel_status = tk.Label(self.panel_status_region,  bg=self.app_bg, fg=color, text=status , font=("bold", 20 ))
        self.panel_status.pack()
        
    def update_connect_status(self,str_message):
        if self.connect_status != None:
           self.connect_status.destroy()         
        m_str =  'Last Connection to Website ' + str_message  
        if len(str_message) > 16:
             m_str = str_message              
        color='green'     
        self.connect_status = tk.Label( self.connect_status_region, bg=self.app_bg, fg=color, text=m_str , font=("bold", 20 ))
        self.connect_status.pack()
        
    def update_data_time(self,time):
        if self.data_time != None:
           self.data_time.destroy()   
        color='black'
        time = 'Data Update ' + time.strftime("%Y-%m-%d %H:%M:%S")       
        self.data_time = tk.Label(self.data_update_time_region, bg=self.app_bg, fg=color, text=time , font=("bold", 20 ))
        self.data_time.pack()
        
    def on_closing(self): 
        print('cancel timer')
        self.update_timer.cancel()
        self.root.destroy()
        
    
        

# Create the entire GUI program
ctrl_panel = Control_Panel(enphase)

# Start the GUI event loop
ctrl_panel.root.mainloop()


