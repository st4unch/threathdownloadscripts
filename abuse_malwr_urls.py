#!/usr/bin/python3

import csv
import os
import json
import  requests
import logging.handlers
import hashlib


file_path = os.environ.get('logfile', '/data/splunk/var/log/splunk/')
os.makedirs(file_path, exist_ok=True)
folderpath= os.environ.get('thfolder', '/data/splunk/etc/apps/thintell/appserver/static')



logger=logging.getLogger('commands')
logger.propagate = False  # Prevent the log messages from being duplicated in the python.log file
logger.setLevel(logging.DEBUG)
file_handler = logging.handlers.RotatingFileHandler(file_path+"abuse_onlineurls_debug.log",maxBytes=25000000, backupCount=5)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

try:
    with open(f'{folderpath}/abuse_onlineurls.csv','rb') as file:
        f=file.read()
        try:
            oldhash=hashlib.sha256(f).hexdigest()
            logging.info('msg: current hash is '+oldhash)
        except:
            pass
except:
    oldhash = "1"
    logging.info('file does not exists going to create')

ch=os.path.exists(f'{folderpath}')

if ch == False:
    exit()
    logger.info('Please_Create_Directory')
else:
    pass
host='https://urlhaus.abuse.ch/downloads/csv_online/'
try:
    file = requests.get(host, timeout=15)
except:
    logger.info('msg: '+' the '+host+' is unreachable')
    file="none"
    exit()

logger.info(file)
hcheck=file.content
hash=hashlib.sha256(hcheck).hexdigest()
if oldhash==hash:
    logger.info('hashes are same '+oldhash+" "+hash)
    exit()
else:
    logger.info('hash is diffrent now downloading urls sha256_hash:'+hash)
    pass
data=file.content.decode('utf-8','ignore')
try:
    file= open (f'{folderpath}/abuse_onlineurls.csv','w',newline='')
    logger.info('msg'+f'{folderpath}/abuse_onlineurls.csv file opened for writing')
    logger.info(file)
    write=file.write(data)
    logger.info('urls writed to file lines writed to  file ')
    cl=file.close()
    logger.info('file is closed')
except:
    logger.info('msg: please check the file permission')

