import requests
import re
import sys
import time
import math
from multiprocessing.dummy import Pool as ThreadPool


if len(sys.argv) != 3:
	print "wrong number of arguments"
	sys.exit(0)

C = int(sys.argv[2])

pool = ThreadPool(C)

nb = int(sys.argv[1])

s = requests.Session()

def getUrl(url):
	r = s.get(url)

t1 = time.time()

r = s.get('http://<HOST>/autocombine/?nbImages=' + str(nb))

result = r.text

matches = re.findall(r'\ssrc="([^"]+)"', result)

url = "http://<HOST>/autocombine/combine.php?"

matches.append("Xenotron.ttf")
matches.append("bootstrap.min.css")
matches.append("jquery-2.1.4.min.js")

nbMatches = len(matches)
nbFilesPerRequest = math.ceil(float(nbMatches) / float(C))
curNbFiles = 0
urls = []

for m in matches:
	url += "files[]=" + m + "&"

	curNbFiles += 1

	if curNbFiles >= nbFilesPerRequest:
		urls.append(url)
		
		curNbFiles = 0
		url = "http://<HOST>/autocombine/combine.php?"
		

if curNbFiles > 0:
	urls.append(url)

results = pool.map(getUrl, urls)
	
print C, nb, time.time() - t1
