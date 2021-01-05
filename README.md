# Diffrent type of threatfeeed download scripts

<p><b>abuse_malware_hash.py</b></p>
<p></p>
<p>the script file download  json file from hxxps://bazaar_abuse_ch/  and convert it to a csv file that contain file_hash(sha256) file_name and signature value.  i'm using this file for splunk. so  you can easly change  download location  changing with "folderpath" and you can change the log lile location changing with "file_path". if you want to get last 100 item you need to change "selector" in data variable.</p>


<p><b>abuse_malwr_urls.py</b></p>

<p>the script file download csv from "hxxps://urlhaus_abuse_ch/downloads/csv_online/"  it contain malware feed online URLs only. </p>
<p>if you want to change folder you can easly change  download location  changing with "folderpath" and you can change the log lile location changing with "file_path" <p>
  
  
