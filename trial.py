from flask import Flask, render_template, request, json 
app = Flask(__name__)

import newspaper, json

news = ''
topic = ''
category = ''

@app.route('/')
def main():
	return render_template('abc.html')

@app.route('/Calculate', methods=['POST'])
def Calculate():
	try:
		news = request.form['inputNews'].lower()
		topic = request.form['inputTopic']
		category = request.form['inputCategory']

		print news + "\t" + topic + "\t" + category
		
		from havenondemand.hodindex import HODClient
		client = HODClient(apikey='6b1f8438-56c7-45e0-98a6-6742c1be0d65', apiversiondefault=1)

		"""def get_bias(url):
			print "Hello"
			data = {'url': url}
			r = client.post('analyzesentiment', data)
			sentiment = r.json()['aggregate']['sentiment']
			score = r.json()['aggregate']['score']
			print url + " | " + sentiment + " | " + str(score)
			return score"""

		paper = newspaper.build("http://" + news + ".com", language='en', memoize_articles=False)

		url = []

		for article in paper.articles:
			url.append(article.url)

		cumulative_score = 0.0
		countNegative = 0
		countPositive = 0
		countNeutral = 0

		"""import multiprocessing as mp

		p = mp.Pool(3)
		res = p.map(get_bias, url)"""

		print newspaper.category

		for u in url:
			data = {'url': u}
			r = client.post('analyzesentiment', data)
			sentiment = r.json()['aggregate']['sentiment']
			score = r.json()['aggregate']['score']
			print u + " | " + sentiment + " | " + str(score)
			cumulative_score += score
			if sentiment == 'positive':
				countPositive += 1
			elif sentiment == 'negative':
				countNegative += 1
			elif sentiment == 'neutral':
				countNeutral += 1				

		print cumulative_score
		print cumulative_score/len(url)

	except Exception as e:
		return json.dumps({'error':str(e)})

	return news + topic + category
 
if __name__ == "__main__":
	app.run(debug = True, host='0.0.0.0', port=8080, passthrough_errors=True)

