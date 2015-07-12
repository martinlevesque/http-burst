import requests
import re
import time
import sys
from multiprocessing.dummy import Pool as ThreadPool

if len(sys.argv) != 2:
	print "wrong number of arguments"
	sys.exit(0)

nb = int(sys.argv[1])

s = requests.Session()

def getUrl(url):
	r = s.get(url)

t1 = time.time()

url = "http://<HOST>/autocombine/?nbImages=" + str(nb)

r = s.get(url)

result = r.text

matches = re.findall(r'\ssrc="([^"]+)"', result)

pool = ThreadPool(6)
urls = []
url1 = "http://<HOST>/autocombine/combine.php?files[]=" + "Xenotron.ttf"
url2 = "http://<HOST>/autocombine/combine.php?files[]=" + "bootstrap.min.css"
url3 = "http://<HOST>/autocombine/combine.php?files[]=" + "jquery-2.1.4.min.js"
urls.append(url1)
urls.append(url2)
urls.append(url3)

for m in matches:
	url = "http://<HOST>/autocombine/combine.php?files[]=" + m
	urls.append(url)
	
	# t = threading.Thread(target=getUrl, args = (s, url))
	# t.deamon = 

results = pool.map(getUrl, urls)

print nb, time.time() - t1
	
