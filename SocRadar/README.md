# SOC Radar Feed Download Scripts

<p>It Creates Files in defined in csv file</p>

<p><b>SocRadarCheckHash.py</b></p>

<p>the script checks hashes form content and download if any changed also it calls  <b>SocRadarFeedListCreate.py</b> for creating not existed files. </p>


<p>if you want you can use <b>SocRadarFeedListCreate.py</b> script separately</p>

<p>  before using feed script please configure csv file with your api definition the api call has 3 part</p><p><b>1:domain=https://platform.socradar.com/api/threat/intelligence/feed_list/</b></p><p><b>2:feed file=8742cab86cc4414092217f87298e94a1.csv</b></p><p><b>3:key=apikey you need to generate this</b></p>
