#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
\
"""

import os, wget, sys
from zipfile import ZipFile
from pathlib import Path

if (__name__ == "__main__"):
    
    directory = str(sys.argv[1])

    if not (os.path.exists(directory + '/Lahman/')):
        os.mkdir(directory + '/Lahman/')
    
    os.chdir(directory + '/Lahman/')
    
    print('Downloading the file...\n')
    wget.download('http://seanlahman.com/files/database/baseballdatabank-master_2018-03-28.zip')
    
    print('Extracting the file to Lahman...\n')
    file = ZipFile('baseballdatabank-master_2018-03-28.zip', 'r')
    file.extractall()
    file.close()
    
    print('Removing unecessary zip file...\n')
    os.remove('baseballdatabank-master_2018-03-28.zip')
    
    print('\nThe file was downloaded to: \n{}'.format(os.getcwd()))
    os.chdir(Path(os.getcwd()).parent)
    print('Now the current working directory is: {}'.format(os.getcwd()))