import requests
import json
import csv
import hashlib
import os
import logging
import logging.handlers




folderpath= os.environ.get('thfolder', 'C:\data\splunk\etc\\apps\\thintell\\appserver\\static\\')
domain = "https://platform.socradar.com/api/threat/intelligence/feed_list/"
key = "?key=3ad9fe099a8e49018ff98ef882b88d1c&v=2"
fname="SocRadarfeed_list.csv"

def callcreatefile():
    x=os.system('python SocRadarFeedListCreate.py')

def setup_logger(level):
    logger = logging.getLogger('message')
    logger.propagate = False  # Prevent the log messages from being duplicated in the python.log file
    logger.setLevel(level)
    log_file_path = os.environ.get('logfile', '/data/splunk/var/log/splunk')
    file_handler = logging.handlers.RotatingFileHandler(log_file_path+"/socradar_feeds.log",maxBytes=25000000, backupCount=5)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger

logger = setup_logger(logging.INFO)

def readthelocalfile(fname): #reading local "SocRadarfeed_list.csv" file
    file=open(fname, 'r')
    readedfile=csv.DictReader(file)
    return readedfile

def exfildesc(fname):#exctract filename and description from local file
    filn=[]
    for fna in readthelocalfile(fname):
        filn.append({'newfilename':fna['newfilename'],'newdescription':fna['newdescription'],'oldhash':fna['oldhash'],'newhash':'newhash'})
    return filn





def rspons(filename,description):
    downloadedfilehash=[]
    response=requests.get(domain+filename+key)
    readcontentfromresp=response.content
    hash = hashlib.sha256(readcontentfromresp).hexdigest()
    downloadedfilehash.append({'newhash':hash,'newfilename':filename,'newdescription':description})
    return downloadedfilehash,readcontentfromresp

def createresponsefile(feedname,respon): #write file to location
    socfile2=open(f'{folderpath}' + feedname+'.csv', 'wb')
    x = socfile2.write(respon)

def createfile():
    callcreatefile()
    fileenv=exfildesc(fname)
    with open(fname, 'w', newline='') as openfile:
        fieldnames = ['newfilename', 'newdescription', 'oldhash','newhash']
        writer = csv.DictWriter(openfile, fieldnames=fieldnames)
        writer.writeheader()
        # for fenv in fileenv:
        for fenv in fileenv:
            filename = fenv.get('newfilename')
            description = fenv.get('newdescription')
            currenthash = fenv.get('oldhash')
            resp=rspons(filename, description)[0]
            dumpresp=rspons(filename, description)[1]
            for rs in resp:
                newhash=rs.get('newhash')
                rsfilename=rs.get('newfilename')
                writer.writerow({'newfilename': filename, 'newdescription': description, 'oldhash': newhash, 'newhash': newhash})
            if filename == rsfilename and newhash != currenthash:
                createresponsefile(description, dumpresp)
                print(newhash)
                print(currenthash)


def main():
    createfile()





if __name__ == "__main__":
    main()