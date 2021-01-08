import requests
import  gzip
import shutil
import logging
from logging import  handlers
import os

folderpath= os.environ.get('thfolder', '/data/splunk/etc/apps/thintell/appserver/static/')

def setup_logger(level):
    logger = logging.getLogger('message')
    logger.propagate = False  # Prevent the log messages from being duplicated in the python.log file
    logger.setLevel(level)
    log_file_path = os.environ.get('logfile', '/data/splunk/var/log/splunk')
    file_handler = logging.handlers.RotatingFileHandler(log_file_path+"/phistank_intel_feed.log",maxBytes=25000000, backupCount=5)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


logger = setup_logger(logging.INFO)


def req(host,file):
    resp=requests.get(host+file,allow_redirects=True)
    re=str(resp)
    logger.info("msg: the phisthank response is "+re)
    return  resp


def unzip():
    fil = "online-valid.csv.gz"
    host="https://data.phishtank.com/data/"
    response=req(host,fil)
    if response.status_code<400 :
        writefile = open(fil, 'wb').write(response.content)
        wf=str(writefile)
        logger.info("phistank status is ",wf)
        return fil, writefile
    else:
        writefile="False"
        logger.info('msg: domain response fail please check domain ')
        return writefile


def main():
    uz=str(unzip())
    f=str(uz[0])
    f2=uz[1]
    if type(f2) is str:
        logger.info('msg:file response is lower than expected')
        f2=1
    if uz != "False" and f2>9999:
        file = f
        file2 = file.strip('.gz')
        with gzip.open(file, 'rb') as filein:
            with open(f'{folderpath}'+file2, 'wb') as fileout:
                print(shutil.copyfileobj(filein, fileout))
        checkfile = os.path.getsize(file2)
        chekthz = str(os.path.exists(file))
        if chekthz == "False":
            logger.info("msg: " + file + " deleted")
        if checkfile > 1:
            logger.info("msg: file created successfully")
    else:
        if uz == "False":
            logger.info("the unzip response is  false please check the domain ")
            exit()


if __name__ == "__main__":
    main()
