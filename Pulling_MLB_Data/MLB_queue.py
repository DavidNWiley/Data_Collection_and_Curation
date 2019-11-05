#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

"""

# Importing necessary libraries
from datetime import date, timedelta
from multiprocessing import Pool, Queue
import requests as rq, os, re, time, wget, queue, sys

# The function will get all of the game IDs for a date
def get_GIDs(date):
    
        try:
            # Defining a 'url' variable where the only thing that changes is the year, month, day
            url = 'https://gd2.mlb.com/components/game/mlb/year_'+str(date.year)+'/month_'+str(date.month).zfill(2)+'/day_'+str(date.day).zfill(2)
            # Getting the text of the url page to be able to search for the game ID
            r = rq.get(url, timeout=3.05, allow_redirects = True)
            date_string = r.text
            
            # setting the regular expression to be searched
            gid_rx = "\s{1}\w+_[0-9]{4}_[0-9]{2}_[0-9]{2}_\w+_\w+_[0-9]"
            
            # finding all matches of the regex
            match = re.finditer(gid_rx, date_string)
            
            #putting each instance of the game IDs from the date into the queue
            for m in match:
                q.put((m.group()).strip())
            #print(str(date)+ " done.")
            
        except:
            pass

# this function will create the necessary directories as well as download the files required
def process_GIDs(q):
    
    while True:
        try:
            # pulling from the queue if there is anything in it, if not it throws an exception queue.Empty
            gid = q.get_nowait()
            # setting regex variable for 2 or 4 digits
            date_rx = '\d{2,4}'
            # finding all instances of regex within the game ID itself
            gid_date = re.findall(date_rx, gid)
            # filepath variable to be used for downloading files
            file_path = './MLB/'+gid
            
            # as before, recreating the url where the date is the only thing that changes, this time dates are from the game ID
            url = 'https://gd2.mlb.com/components/game/mlb/year_'+str(gid_date[0])+'/month_'+str(gid_date[1])+'/day_'+str(gid_date[2])+'/'+gid

            # looking for the directories required, if it doesn't exist it creates it
            if not (os.path.exists('./MLB/')):
                os.mkdir('./MLB/')
            if not (os.path.exists('./MLB/'+ gid +'/')):
                os.mkdir('./MLB/'+ gid +'/')
                
            # same as the directories, if it doesn't find the file, it downloads it and saves it appropriately
            if not (os.path.isfile('./MLB/'+ gid +'/players.xml')):
                wget.download(url+'/players.xml', file_path+'/players.xml')
            if not(os.path.isfile('./MLB/'+ gid +'/inning/inning_hit.xml')):
                wget.download(url+'/inning/inning_hit.xml', file_path +'/inning_hit.xml')
            if not(os.path.isfile('./MLB/'+ gid +'/inning/inning_all.xml')):
                wget.download(url+'/inning/inning_all.xml', file_path +'/inning_all.xml')
        except queue.Empty:
            break



if(__name__=="__main__"):
    
    
    # allows user to set the number of threads and directory where files are to be saved
    num_threads = int(sys.argv[1])
    directory = str(sys.argv[2])
    
    start_time = time.time()
    
    # setting the start date
    date = date(2019, 9, 1)
    today = date.today()
    
    # creating empty queue
    q = Queue()
    dates = [] 
    
    # populating the empty array above with the dates required
    while(date <= today):
        dates.append(date)
        date += timedelta(1)
        
        
    print("Getting game IDs...\n")
    
    # running pools with the functions created above
    gid_pool = Pool(num_threads)
    gid_pool.map(get_GIDs, dates)
    gid_pool.close()
    gid_pool.join()
    
    elapse_1 = time.time() - start_time
    print("Finished getting game IDs.")
    print("Time Elapsed: {0} seconds.".format(round(elapse_1, 2)))
    print("Working on processing game IDs...\n")
    
    process_pool = Pool(num_threads, process_GIDs, (q,))
    process_pool.close()
    process_pool.join()
    elapse_2 = time.time() - start_time
    print("Finished processing game IDs.")
    print("Time Elapsed: {0} seconds.".format(round(elapse_2, 2)))
