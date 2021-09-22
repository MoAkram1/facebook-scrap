#
# Facebook group posts scrapper
# By Mahmoud Mustafa  @2021
#
import os,json,csv
import io
import time
from time import gmtime, strftime 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.command import Command
import urllib.request
from PyQt5.QtWidgets import QApplication,QLineEdit,QWidget,QFormLayout,QPushButton,QLabel
from PyQt5.QtGui import QIntValidator,QDoubleValidator,QFont,QIcon
from PyQt5.QtCore import Qt,pyqtSlot,QSize
import sys

class Qt(QWidget):
        def __init__(self,parent=None):
                super().__init__(parent)
                self.e1 = QLineEdit()
                self.e2 = QLineEdit()
                self.e2.setEchoMode(QLineEdit.Password)
                self.e3 = QLineEdit()
                self.button = QPushButton()
                self.button.setText("Scrape")
                self.button.clicked.connect(self.scrape)
                self.flo = QFormLayout()
                self.flo.addRow("email",self.e1)
                self.flo.addRow("Password",self.e2)
                self.flo.addRow("group link",self.e3)
                self.flo.addRow("   ",self.button)
                app =QIcon()

                app.addFile("logo.png",QSize(24,24))


                self.setWindowIcon(app)
                self.setLayout(self.flo)
                self.setWindowTitle("facebook scrapper")
                self.setGeometry(500, 400, 480, 80)


        def scrape(self):


        	email= self.e1.text()
        	password = self.e2.text()
        	group= self.e3.text()
        	if "https://www.facebook.com/groups/" not in group:
        		self.label= QLabel()
        		self.label.setText("Please enter a valid FB group link such as https://www.facebook.com/groups/1355209068185656")
        		self.flo.addRow("",self.label)

        	else:
        		scrape_fb(group,email,password)




def browser_init():
	opt = Options()
	opt.add_argument("--disable-infobars")
	opt.add_argument("start-maximized")
	opt.add_argument("--disable-extensions")
	# Pass the argument 1 to allow and 2 to block
	opt.add_experimental_option("prefs", { \
	    "profile.default_content_setting_values.media_stream_mic": 2, 
	    "profile.default_content_setting_values.media_stream_camera": 2,
	    "profile.default_content_setting_values.geolocation": 2, 
	    "profile.default_content_setting_values.notifications": 2 
	  })
	browser = webdriver.Chrome(options=opt, executable_path="chromedriver.exe")
	return browser




def FB_summer21(browser,group,FB_email="",FB_password=""):
	posts_array=[]

	try:

		cwd=os.getcwd()
		current_time=strftime("%a,%d-%b-%Y,%H-%M-%S ", gmtime())
		img_dir=f"Images[{current_time}]"
		path = os.path.join(cwd, img_dir)
		os.mkdir(path,0o666)
	except:
		print("OS error")

	try:
		
		if FB_email != "" and FB_password != "":
			browser.get("https://facebook.com")
			time.sleep(2)
			browser.find_element_by_xpath("//input[@class='inputtext _55r1 _6luy']").send_keys(FB_email)
			browser.find_element_by_xpath("//input[@class='inputtext _55r1 _6luy _9npi']").send_keys(FB_password)
			browser.find_element_by_xpath("//button[@class='_42ft _4jy0 _6lth _4jy6 _4jy1 selected _51sy']").click()
			time.sleep(5)

		browser.get(group)

	except:
		print("connection error ")
		return

	time.sleep(2)
	count =0
	while count < 200:
		count += 1
		browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")
		time.sleep(2)
	posts = browser.find_elements_by_xpath("//div[@class='du4w35lb k4urcfbm l9j0dhe7 sjgh65i0']")

	counter =1
	for post in posts:

		print(f"post {counter}")
		# try:
		# 	owner= post.find_element_by_xpath(".//span[@class='nc684nl6']/a/strong")
		# except:
		# 	owner= post.find_element_by_xpath(".//span[@class='nc684nl6']/a/span")
		browser.execute_script("arguments[0].scrollIntoView(true);", post);
		try:
			owner = post.find_element_by_xpath(".//h2[@class='gmql0nx0 l94mrbxd p1ri9a11 lzcic4wl aahdfvyu hzawbc8m']").text
			# --- post date
			date =post.find_element_by_xpath(".//span[@class='tojvnm2t a6sixzi8 abs2jz4q a8s20v7p t1p8iaqh k5wvi7nf q3lfd5jv pk4s997a bipmatt0 cebpdrjk qowsmv63 owwhemhu dp1hu0rb dhp61c6y iyyx5f41']/a/span").text
		except:
			owner=""
			date=""
			print("retrieve error")


		try:
			body= post.find_element_by_xpath(".//div[@class='kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql ii04i59q']/div").text
		except:
			body=""
			print("Post has no text")
		try:
			likes= post.find_element_by_xpath(".//span[@class='pcp91wgn']").text
		except:
			likes="0"
			print("post has no likes")

		try:
			no_comments_shares= post.find_element_by_xpath(".//div[@class='bp9cbjyn j83agx80 pfnyh3mw p1ueia1e']").text
		except:
			no_comments_shares="0"
			print("post has no comments or shares")

		Post_comments=[]

		try:
			comment_section =post.find_elements_by_xpath(".//div[@class='tw6a2znq sj5x9vvc d1544ag0 cxgpxx05']")
		except:
			print("no comments found")
		for cs in comment_section:
			commentor = cs.find_element_by_xpath(".//span[@class='pq6dq46d']/span")
			try:
				comment_body = cs.find_element_by_xpath(".//div[@class='kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql']/div")
				Post_comments.append({"user":commentor.text,"comment":comment_body.text})
			except:
				comment_body= "Comment is an image or GIF"
				Post_comments.append({"user":commentor.text,"comment":comment_body})

		

		post_json= {"post_owner":owner,
		"date":f"{date}",
		"body":body,
		"likes":likes,
		"number of comments":no_comments_shares,
		"comments":Post_comments
		}

		posts_array.append(post_json)

		with io.open('post.json', 'w',encoding="utf-8") as json_file:
			# if os.stat('post.txt').st_size ==0 :
			json.dump(posts_array, json_file,indent=4,ensure_ascii = False)


		try:
			img = post.find_element_by_xpath(".//div[@class='pmk7jnqg kr520xx4']/img").get_attribute("src")
			urllib.request.urlretrieve(img,f"{img_dir}/Post{counter}.jpg")
		except:
			print("post may not have an image")
		print("#################")
		counter +=1

		

def scrape_fb(group,FB_email,FB_password):

	FB_summer21(browser_init(),group,FB_email,FB_password)
	try:
		with io.open('post.json','r',encoding="utf-8") as json_file:
		 	jsondata=( json.load(json_file))
		data_file = io.open('jsonoutput.csv', 'w', newline='',encoding="utf-8")
		csv_writer = csv.writer(data_file)
		count = 0
		csv_writer.writerow(jsondata[0].keys())
		while count < len(jsondata):
			csv_writer.writerow(jsondata[count].values())
			count+=1
		data_file.close()
	except:
		print("file not found")

	print("finished scraping")


if __name__ == "__main__":
	app = QApplication(sys.argv)
	win = Qt()
	win.show()
	sys.exit(app.exec_())
