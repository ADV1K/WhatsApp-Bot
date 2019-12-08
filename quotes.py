from selenium import webdriver
from whatsapp import *
import requests

# they said so

driver = webdriver.Chrome()
init(driver)

while 1:
	joke = '---\n' + get_random_joke('Dark', flags=[''])
	# send_to_anurag(joke, driver)
	# send_to('Techno', joke, driver)
	time.sleep(30)
