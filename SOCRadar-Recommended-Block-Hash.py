#!/usr/bin/python3

import requests
import json
import hashlib
import os
import logging
import logging.handlers


log_file_path = os.environ.get('logfile', '/data/splunk/var/log/splunk')

def setup_logger(level):
    logger = logging.getLogger('my_search_command')
    logger.propagate = False  # Prevent the log messages from being duplicated in the python.log file
    logger.setLevel(level)
    file_handler = logging.handlers.RotatingFileHandler(log_file_path+"/socradar_intel_feed.log",maxBytes=25000000, backupCount=5)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger

logger = setup_logger(logging.INFO)


folderpath= os.environ.get('thfolder', '/data/splunk/etc/apps/thintell/appserver/static/')
chk=os.path.exists(f'{folderpath}')
domain="https://platform.socradar.com/api/threat/intelligence/feed_list/"
list="8742cab86cc4414092217f87298e94a1.csv"
host=domain+list
key="?key=" ## you must enter you company api key
file=folderpath+list

if chk != True:
    logger.info('msg: Please create a directory with  necessary permission under '+folderpath)
    exit()
else:
    pass

def file_as_bytes(file):
    with file:
        return file.read()
try:
    oldhash=hashlib.sha256(file_as_bytes(open(file, 'rb'))).hexdigest()
except:
    oldhash = "1"



def socradar(host):
    resp = requests.get(host+key,timeout=15)
    logger.info(resp)
    response1 = resp.content
    response = resp.content.decode("utf-8", "ignore")
    hsh=hashlib.sha256(response1).hexdigest()
    return hsh,response




def main():
    response=socradar(host)
    newhash=response[0]
    logger.info('msg: the new hash is '+newhash)
    logs=logger
    if oldhash == "1":
        with open(f'{folderpath}'+list, 'w', newline='') as socfile2:
            socfile2.write(response[1])
            logs.info(socfile2)
    elif oldhash !=newhash:
        with open(f'{folderpath}'+list, 'w', newline='') as socfile2:
            socfile2.write(response[1])
            logs.info(socfile2)

    else:
        logs.info("true")



if __name__=="__main__":
    main()