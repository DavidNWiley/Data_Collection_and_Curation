#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""
import os, wget, re, sys
from pathlib import Path

from zipfile import ZipFile

if (__name__ == "__main__"):
        
    directory = str(sys.argv[1])
    
    if not (os.path.exists(directory + '/Retrosheets/')):
        os.mkdir(directory + '/Retrosheets/')
    
    os.chdir(directory + '/Retrosheets')
    wget.download('https://www.retrosheet.org/retroID.htm', 'player.csv')
    
    if not (os.path.exists(directory + '/Retrosheets/Events/')):
        os.mkdir(directory + '/Retrosheets/Events/')
    if not (os.path.exists(directory + '/Retrosheets/Teams/')):
        os.mkdir(directory + '/Retrosheets/Teams/')
    if not (os.path.exists(directory + '/Retrosheets/Rosters/')):
        os.mkdir(directory + '/Retrosheets/Rosters/')
    
    for year in range(1900, 2020):
        
        try:
            wget.download('https://www.retrosheet.org/events/'+str(year)+'eve.zip')
            
            zf = ZipFile(str(year)+'eve.zip', 'r')
            zf.extractall()
            zf.close()
    
            r_event = '\d+\w+.EVN'
            r_rost = '\d+\w+.ROS'
            r_team = 'TEAM\d+'
            r_eva = '\d+\w+.EVA'
            r_zip = '\d+\w+.zip'
            r_eda = '\d+\w+.EDA'
            r_edn = '\d+\w+.EDN'
    
    
            for file in os.listdir():
                if(re.search(r_event, file)):
                    os.rename(file, directory + '/Retrosheets/Events/'+str(file))
                if(re.search(r_rost, file)):
                    os.rename(file, directory +'/Retrosheets/Rosters/'+str(file))
                if(re.search(r_team, file)):
                    os.rename(file, directory +'/Retrosheets/Teams/'+str(file))
                elif(re.search(r_eva, file) or re.search(r_zip, file) or re.search(r_eda, file) or re.search(r_edn, file)):
                    os.remove(file)
        except:
            pass
        
    print('The current working directory was: {}'.format(os.getcwd()))
    os.chdir(Path(os.getcwd()).parent)
    print('Now the current working directory is: {}'.format(os.getcwd()))
