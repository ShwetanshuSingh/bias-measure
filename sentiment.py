import newspaper, json	
cnn_paper = newspaper.build('http://cnn.com', language='en', memoize_articles=False)

url = []

for article in cnn_paper.articles:
	url.append(article.url)

from havenondemand.hodindex import HODClient
client = HODClient(apikey='6b1f8438-56c7-45e0-98a6-6742c1be0d65', apiversiondefault=1)

cumulative_score = 0.0
count = 0

import multiprocessing as mp

p = mp.Pool(3)

def get_bias(url):
	data = {'url': url}
	r = client.post('analyzesentiment', data)
	sentiment = r.json()['aggregate']['sentiment']
	score = r.json()['aggregate']['score']
	print url + " | " + sentiment + " | " + str(score)
	return score

res = p.map(get_bias, url)

for record in res:
    cumulative_score += record

"""for u in url:
	try:
		data = {'url': u}
		r = client.post('analyzesentiment', data)
		sentiment = r.json()['aggregate']['sentiment']
		score = r.json()['aggregate']['score']
		count += 1
		cumulative_score += score
		print u + " | " + sentiment + " | " + str(score)
	except:
		continue"""

print (cumulative_score/len(url))