from selenium import webdriver
from whatsapp_old import *
import requests

sent_jokes = []


def get_random_joke(category='Any', flags=['nsfw']):
	url = f'https://sv443.net/jokeapi/category/{category}/'
	params = {
		'blacklistFlags': ','.join(*flags)
	}
	with requests.get(url=url, params=params) as r:
		d = r.json()
		if d['id'] in sent_jokes:
			return get_random_joke(category, flags)
		sent_jokes.append(d['id'])
		if d['type'] == 'single':
			return d['joke']
		else:
			return d['setup'] + '\n' + d['delivery']


driver = webdriver.Chrome()
init(driver)

while 1:
	joke = '---\n' + get_random_joke('Dark', flags=[''])
	send_to_anurag(joke, driver)
	send_to('Techno', joke, driver)
	time.sleep(30)
