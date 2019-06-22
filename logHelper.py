import time  
import datetime
import math

def ExecuteWithLogs(func_desc, log_file_path, func_to_measure):   
    start_tmstmp = time.time()
    start_datetime = datetime.datetime.fromtimestamp(start_tmstmp).strftime("%d-%m-%Y, %H:%M:%S")    
    with open(log_file_path, 'a') as log_file:
        log_file.write("{0} started at {1}.\n".format(func_desc, start_datetime))
    result = func_to_measure()
    end_tmstmp = time.time()
    end_datetime = datetime.datetime.fromtimestamp(end_tmstmp).strftime("%d-%m-%Y, %H:%M:%S")
    duration = end_tmstmp - start_tmstmp
    hours = math.floor(duration / 3600)
    minutes = math.floor((duration - (hours * 3600)) / 60)
    seconds = int(duration - (hours * 3600) - (minutes * 60))
    with open(log_file_path, 'a') as log_file:
        log_file.write("{0} ended at {1} and lasted {2}h {3}m {4}s.\n".format(func_desc, end_datetime, hours, minutes, seconds))
    return result