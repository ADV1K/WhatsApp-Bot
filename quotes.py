from selenium import webdriver
from whatsapp_old import *
import requests

# they said so

driver = webdriver.Chrome()
init(driver)

while 1:
	quote = "A quote here"
	# send_to_anurag(joke, driver)
	# send_to('Techno', joke, driver)
	time.sleep(30)
