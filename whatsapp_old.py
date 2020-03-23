from threading import Thread
import tkinter as tk
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


WW_URL = 'https://web.whatsapp.com/'
HEADLESS_MODE = False


def show_qr_code(qr_code_base64):
	root = tk.Tk()
	im = tk.PhotoImage(data=qr_code_base64)
	tk.Label(root, image=im).pack()
	root.mainloop()
	return root  # return root so we can later destroy it. maybe we cant


def wait_for_log_in(driver):
	"Waits for user to scan the qr code. displays qr code in a tkinter window if in headless mode"
	if driver.current_url != WW_URL:
		driver.get(WW_URL)
	time.sleep(2)  # let the page load
	# if HEADLESS_MODE or 1:  # doesnt work well
	# 	# try: goto chrome developer console > right click > Copy > Copy XPath
	# 	qr_code_base64 = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div/img').get_attribute('src').split(',')[1]
	# 	# Thread(target=show_qr_code(qr_code_base64)).start()  # show qr code (using tkinter) if we're in headless mode
	while 1:
		if "connected" in driver.page_source:
			# if HEADLESS_MODE or 1:
				# root.quit()
				# pass
			break
		time.sleep(2)  # lower the value if you need


def open_chat(recipient, driver):
	input_box = driver.find_element_by_xpath('//*[@id="side"]//input')
	input_box.send_keys(recipient)
	input_box.send_keys(Keys.ENTER)
	# There must be a better way to deal with name conflicts
	# current_chat = driver.find_element_by_css_selector('span._19RFN._1ovWX._F7Vk').text
	# if current_chat.lower() != recipient.lower():
	# 	raise ValueError("Ambigious Name: there is a name conflict! try entering the full name of the recipient.")


def get_all_chats(driver):
	if driver.current_url != WW_URL:
		driver.get(WW_URL)
	arr = driver.find_elements_by_xpath('//*[@id="side"]//*[@class="_3H4MS"]')
	chats = [e.find_element_by_tag_name('span').text for e in arr]
	return chats


def send_to(recipient, msg, driver):
	# there must be a better way to do this: open chat
	# current_chat = driver.find_element_by_xpath(//*[@id="main"]/header/div[2]/div[1]/div/span).text
	# if current_chat != recipient:
		# open_chat(recipient)
	open_chat(recipient, driver)
	input_box = driver.find_element_by_xpath('//*[@id="main"]//*[@class="_3u328 copyable-text selectable-text"]')
	input_box.send_keys(msg)
	input_box.send_keys(Keys.ENTER)


def send_to_all(msg, driver):
	for recipient in get_all_chats(driver):
		send_to(recipient, msg, driver)


def send_to_anurag(msg, driver):
	# what if there is no anurag in the chats!
	return send_to('anurag', msg, driver)


def init(driver):
	wait_for_log_in(driver)


def main():
	options = Options()
	options.headless = HEADLESS_MODE
	driver = webdriver.Chrome(chrome_options=options)
	driver.get('https://web.whatsapp.com/')

	wait_for_log_in(driver)
	print('logged in')

	# send_to_anurag()
	# send_to_all("TESTing", driver)
	send_to("Shakti Agarwal", "HEllo sir.", driver)
	for i in range(1, 11):
		send_to("Shakti Agarwal", f"{2} * {i:2} = {2*i:2}", driver)
	time.sleep(10)


if __name__ == '__main__':
	main()
