#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from datetime import date, timedelta
from multiprocessing import Pool, Queue
import requests as rq, os, re, time, wget, queue, sys

def get_GIDs(date):
    
        try:
            url = 'https://gd2.mlb.com/components/game/mlb/year_'+str(date.year)+'/month_'+str(date.month).zfill(2)+'/day_'+str(date.day).zfill(2)
            r = rq.get(url, timeout=3.05, allow_redirects = True)
            date_string = r.text

            gid_rx = "\s{1}\w+_[0-9]{4}_[0-9]{2}_[0-9]{2}_\w+_\w+_[0-9]"

            match = re.finditer(gid_rx, date_string)
            
#            while(q.qsize > 1000):
#                time.sleep(5)

            for m in match:
                q.put((m.group()).strip())
            #print(str(date)+ " done.")
            
            
        except:
            pass

        
def process_GIDs(q):
    
    while True:
        try:
            gid = q.get_nowait()
            date_rx = '\d{2,4}'
            gid_date = re.findall(date_rx, gid)
            file_path = directory+'/MLB/'+gid

            url = 'https://gd2.mlb.com/components/game/mlb/year_'+str(gid_date[0])+'/month_'+str(gid_date[1])+'/day_'+str(gid_date[2])+'/'+gid

            if not (os.path.exists(directory+'/MLB/')):
                os.mkdir(directory+'/MLB/')
            if not (os.path.exists(directory+'/MLB/'+ gid +'/')):
                os.mkdir(directory+'/MLB/'+ gid +'/')
            if not (os.path.isfile(directory+'/MLB/'+ gid +'/players.xml')):
                wget.download(url+'/players.xml', file_path+'/players.xml')
            if not(os.path.isfile(directory+'/MLB/'+ gid +'/inning/inning_hit.xml')):
                wget.download(url+'/inning/inning_hit.xml', file_path +'/inning_hit.xml')
            if not(os.path.isfile(directory+'/MLB/'+ gid +'/inning/inning_all.xml')):
                wget.download(url+'/inning/inning_all.xml', file_path +'/inning_all.xml')
        except queue.Empty:
            break



if(__name__=="__main__"):
    
    num_threads = int(sys.argv[1])
    directory = str(sys.argv[2])
    
    start_time = time.time()
        
    date = date(2019, 9, 1)
    today = date.today()
     
    q = Queue()
    dates = [] 
        
    while(date <= today):
        dates.append(date)
        date += timedelta(1)
        
        
    print("Getting game IDs...\n")
    
    pool_GIDs = Pool(num_threads)
    pool_GIDs.map(get_GIDs, dates)
    
    elapse_1 = time.time() - start_time
    print("Finished getting game IDs.")
    print("Time Elapsed: {0} seconds.".format(round(elapse_1, 2)))
    print("Working on processing game IDs...\n")
    
    pool_process = Pool(num_threads, process_GIDs, (q,))
    
    pool_GIDs.close()
    pool_GIDs.join()
    pool_process.close()
    pool_process.join()
    
    elapse_2 = time.time() - start_time
    print("\nFinished processing game IDs.")
    print("Time Elapsed: {0} seconds.".format(round(elapse_2, 2)))

