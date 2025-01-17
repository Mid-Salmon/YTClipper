import requests,re
import os,argparse,subprocess
from datetime import timedelta

def clipTime(s,e):
    time = " -ss "+s+" -to "+e+" "
    return time


parser = argparse.ArgumentParser()
parser.add_argument("--url", help="video url",type=str)
args = parser.parse_args()

url = args.url

payload={}
headers = {}
response = requests.request("GET", url, headers=headers, data=payload)

pattern=r'("startTimeMs.*"endTimeMs":"[0-9]+")'
timeConfig=re.search(pattern,response.text)
time=re.findall(r"\d+\.?\d*",timeConfig.group(0))


cmd="yt-dlp -g --youtube-skip-dash-manifest -S \"ext\" --no-warnings "+args.url
r = os.popen(cmd)  
urlOutput = r.read()  
r.close()
urls=urlOutput.split('\n',1)


start=str(timedelta(milliseconds=int(time[0])))
end=str(timedelta(milliseconds=int(time[1])))

trimCmd="ffmpeg"+clipTime(start,end)+"-i \""+urls[0].replace('\n', '').replace('\r', '')+"\""
if(len(urls[1])>0):
    trimCmd+=clipTime(start,end)+"-i "+"\""+urls[1].replace('\n', '').replace('\r', '')+"\""
trimCmd+="  output.mp4"
print(trimCmd)
subprocess.run(trimCmd,shell=True)

