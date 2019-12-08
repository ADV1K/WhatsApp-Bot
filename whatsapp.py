# TODO:
# Exceptions:
#   - no internet connection
#   - no user with that name in open_user
#   - etc.

from threading import Thread
import tkinter as tk
import time
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class WhastsApp:
	def __init__(self, headless=False):
		self.WW_URL = 'https://web.whatsapp.com/'
		self.is_headless = headless

		options = Options()
		options.headless = headless
		options.add_argument("user-agent=User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36")
		# options.add_argument("--window-size=1366x768")

		chrome_driver = os.path.join(os.getcwd(), "chromedriver.exe")

		self.driver = webdriver.Chrome(options=options, executable_path=chrome_driver)
		self.driver.get('https://web.whatsapp.com/')

		# self.driver.save_screenshot('woops1.png')
		self.wait_for_log_in()

	def show_qr_code(self):
		"Displays the QR Code if chrome is running in headless mode"
		self.tkroot = tk.Tk()
		im = tk.PhotoImage(data=self.qr_code_base64)
		tk.Label(self.tkroot, image=im).pack()
		self.tkroot.mainloop()

	def wait_for_log_in(self):
		"Waits for user to scan the qr code. displays qr code in a tkinter window if in headless mode"
		if self.driver.current_url != self.WW_URL:
			self.driver.get(self.WW_URL)

		if self.is_headless:
			# wait untill the qr code is loaded and then grab it
			qr_image = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div/img')))
			self.qr_code_base64 = qr_image.get_attribute('src').split(',')[1]
			Thread(target=self.show_qr_code).start()  # show qr code (using tkinter) if we're in headless mode

		while 1:
			if "connected" in self.driver.page_source:
				if self.is_headless:
					self.tkroot.quit()  # it doesnt work. why?
				break
			time.sleep(2)  # lower the value if you need

	def open_chat(self, recipient):
		"opens a chat so we can send messages. Sometimes opens wrong chats"
		input_box = self.driver.find_element_by_xpath('//*[@id="side"]//input')
		input_box.send_keys(recipient)
		input_box.send_keys(Keys.ENTER)
		# There must be a better way to deal with name conflicts
		# current_chat = driver.find_element_by_css_selector('span._19RFN._1ovWX._F7Vk').text
		# if current_chat.lower() != recipient.lower():
		# 	raise ValueError("Ambigious Name: there is a name conflict! try entering the full name of the recipient.")

	def send_msg(self, recipient, msg):
		"send msg to the recipient"
		# there must be a better way to a open chat to send messages
		# current_chat = driver.find_element_by_xpath(//*[@id="main"]/header/div[2]/div[1]/div/span).text
		# if current_chat != recipient:
		# 	open_chat(recipient)
		self.open_chat(recipient)
		input_box = self.driver.find_element_by_xpath('//*[@id="main"]//*[@class="_3u328 copyable-text selectable-text"]')
		input_box.send_keys(msg)
		input_box.send_keys(Keys.ENTER)

	def send_to(self, recipients, msg):
		"send a message to *multiple* people or just *one*"
		if isinstance(recipients, (list, tuple, set)):  # if there are multiple recipients. e.g, a list of recipients
			for recipient in recipients:
				self.send_msg(recipient, msg)
		else:
			self.send_msg(recipients, msg)

	def send(self, to, msg):
		"An alias for send_to"
		return self.send_to(to, msg)

	def send_to_all(self, msg):
		for recipient in self.get_all_chats(self.driver):
			self.send_to(recipient, msg)

	def get_all_chats(self):
		if self.driver.current_url != self.WW_URL:
			self.driver.get(self.WW_URL)
		arr = self.driver.find_elements_by_xpath('//*[@id="side"]//*[@class="_3H4MS"]')
		chats = [e.find_element_by_tag_name('span').text for e in arr]
		return chats


def main():
	print('[*] waiting for user to log in')
	w = WhastsApp(headless=True)  # automatically waits for log in
	print('[*] successfully logged in')
	w.send_to([f'selenium testing {i}' for i in range(1, 4)], 'hello')


if __name__ == '__main__':
	main()

# try: goto chrome developer console > right click > Copy > Copy XPath
# https://some-random-api.ml/
# theysaidso.com
# https://www.guru99.com/xpath-selenium.html#1
