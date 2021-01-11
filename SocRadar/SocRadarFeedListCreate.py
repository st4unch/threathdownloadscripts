import requests
import json
import csv
import hashlib
import os
import logging
import logging.handlers


folderpath= os.environ.get('thfolder', '/data/splunk/etc/apps/thintell/appserver/static/')
domain = "https://platform.socradar.com/api/threat/intelligence/feed_list/"
key = "?key=asdasdasdasdasdasda&v=2" ## you must add your key
fname="SocRadarfeed_list.csv"

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


def readfile(fname):
    file=open(fname, 'r')
    readedfile=csv.DictReader(file)
    return readedfile

def checkfilesstatus(row):
    chkdescription=row['newdescription']+".csv"
    chkfilename = row['newfilename']
    nexsistfiles=[]
    chkdescriptionpt = os.path.exists(f'{folderpath}' + chkdescription)
    if chkdescriptionpt == True:
        nexsistfiles.append({'exfilename':chkfilename,'exdescription':chkdescription})
    else:
        x=chkfilename
        z=chkdescription
        nexsistfiles.append({'notexsitfilename':x,'notexsitdescription':z})
    return nexsistfiles



def getnotexsitsfile(domain,notexsitfilename,key):
    newlydownloadedfilehash=[]
    responsefornonexfile=requests.get(domain+notexsitfilename+key)
    readcontentfromresp=responsefornonexfile.content
    hsh = hashlib.sha256(readcontentfromresp).hexdigest()
    newlydownloadedfilehash.append({'newhash':hsh,'newfilename':notexsitfilename})
    return newlydownloadedfilehash,readcontentfromresp


def checkknotexistsfile(texfile):
    y = checkfilesstatus(texfile)
    for exfilname in y:
        t=exfilname.get('notexsitfilename')
        tsa = exfilname.get('notexsitdescription')
        if t != None:
            nonfile=t
            nondesc=tsa
            return nonfile,nondesc


def createfile(feedname,respon): #write file to location
    socfile2=open(f'{folderpath}' + feedname, 'wb')
    x = socfile2.write(respon)


def craeteifnotexsist():
    for i in readfile(fname):  # for loop for open file
        ya=checkknotexistsfile(i)
        if ya != None:
            nohvefile=ya[0]
            nohvedesc = ya[1]
            reqtosocradar=getnotexsitsfile(domain,nohvefile,key)
            getbody=reqtosocradar[1]
            createfile(nohvedesc,getbody)



def main():
    tas=craeteifnotexsist()



if __name__=="__main__":
    main()
