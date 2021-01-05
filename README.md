# threathdownloadscripts
diffrent type of threatfeeed download scripts
abuse_malware_hash.py > 
the script file download  json file from https://bazaar.abuse.ch/  and convert it to a csv file that contain file_hash(sha256) file_name and signature value.  i'm using this file for splunk you can chose to change file location with changing "folderpath" and you can change the log lile location changing with "file_path". if you want to get last 100 item you need to change "selector" in data variable.
