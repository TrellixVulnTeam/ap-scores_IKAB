from bs4 import BeautifulSoup
from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

@app.route('/api/scores', methods=['POST'])
def get_scores():
	login_url = 'https://account.collegeboard.org/login/authenticateUser'
	scores_url = 'https://apscore.collegeboard.org/scores/view-your-scores'
	
	form = {
		'forgotPWUrl': 'forgotPassword%3FappId%3D287%26DURL%3Dhttps%25253A%25252F%25252Fapscore.collegeboard.org%25252Fscores%25252Fview-your-scores%26idp%3DECL',
		'forgotUNUrl': 'forgotUsername%3FappId%3D287%26DURL%3Dhttps%25253A%25252F%25252Fapscore.collegeboard.org%25252Fscores%25252Fview-your-scores%26idp%3DECL',
		'signUpUrl': 'signUp%3FappId%3D287%26idp%3DECL%26DURL%3Dhttps%25253A%25252F%25252Fapscore.collegeboard.org%25252Fscores%25252Fview-your-scores',
		'DURL': 'https%3A%2F%2Fapscore.collegeboard.org%2Fscores%2Fview-your-scores',
		'appId': '287',
		'LOGINURL': 'https%3A%2F%2Faccount.collegeboard.org%2Fprofessional%2Fdashboard',
		'person.userName': request.form['username'],
		'person.password': request.form['password'],
		'__checkbox_rememberMe': 'false'
	}
	
	print(request.form['username'])
	
	session = requests.session()
	response = session.post(login_url, data=form)
	
	soup = BeautifulSoup(session.get(scores_url).content, 'html.parser')
	exams_container = soup.findAll('div', {'class': 'span5'})
	
	exams = []
	scores = []
	for tag in exams_container:
		hTag = tag.find_all('h4')
		for tag in hTag:
			exams.append(tag.text)
		sTag = tag.find_all('em')
		for tag in sTag:
			scores.append(tag.text)
			
	return json.dumps(dict(zip(exams, scores)))
	
@app.route('/')
def index():
	return render_template('main.html')