import time
import datetime


from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.options import Options

# Create ChromeOptions
#chrome_options = Options()
#chrome_options.add_argument('--headless') 


import pandas as pd
import csv
import os
import threading

today = datetime.datetime.today()
date = datetime.datetime.strftime(today, "%Y-%m-%d")

current_time = datetime.datetime.now()
current_time_string = datetime.datetime.strftime(current_time, "%H:%M")


print("Please briefly describe your search. If more than one word, connect with an underscore.")
print("For example, addiction treatment would be addiction_treatment")
subject = input("Search subject:")

#Giving option to enter new search url or use a stored search
print("Please copy and paste a library search url to start a new search. To use an example search, type url")
user_input_url = input("Type here:")
url = "https://miami-primo.hosted.exlibrisgroup.com/primo-explore/search?query=sub,contains,well-being%20OR%20flourishing%20OR%20happiness,AND&query=any,contains,addiction%20treatment%20OR%20addiction%20recovery,AND&pfilter=pfilter,exact,articles,AND&tab=everything&search_scope=Everything&sortby=rank&vid=uml_new&facet=topic,include,Substance%20Abuse&mode=advanced&offset=0"


#need to test creating file path to store search data
user_path = os.path.expanduser('~')
file_path = user_path + '/Documents/search_buddy'
isExist = os.path.exists(file_path)
if not isExist:
	os.makedirs(file_path)
	print("New file path for search_buddy created!")


#defining location of driver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))


#calling url based on user input
if user_input_url == "url":
	driver.get(url)
	with open(file_path + "/" + 'search_log.txt', 'a') as log:
		log.write(date + '\t' + url + '\n')
else:
	driver.get(user_input_url)
	with open(file_path + "/" + 'search_log.txt', 'a') as log:
		log.write(date + '\t' + user_input_url + '\n')

#wait to load page
time.sleep(5)


results_count0 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="select_value_label_466"]/span[1]'))).text
results_count1 = results_count0.split(' ')[-2]  # Extracting the numeric part
results_count = pd.to_numeric(results_count1)


x = results_count/10
y = int(x)
logic = (x - y)

if logic != 0:
	z = (y)
else:
	z = (y - 1)

#print(z)

hrefs = [] #list for links to scrape in next function



#print(current_time_string)


# display countdown timer
def countdown(t, scrape_flag):
    while t:
        hrs, mins = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(hrs, mins)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1

    scrape_flag.set()



#estimating time to completion
est0 = ((z * 5.5) + (int(results_count) * 5))/60
t = int(est0)
print("Estimated time to completion:")
print(str(t) + " " + "minutes")

scrape_flag = threading.Event()

# Start the countdown timer in a separate thread
countdown_thread = threading.Thread(target=countdown, args=(t * 60, scrape_flag))
countdown_thread.start()

#countdown(int(t*60))

print("before scraping")
#scraping for links
for i in range(0,z):
	links = driver.find_elements(By.XPATH, '/html/body/primo-explore/div/prm-explore-main/ui-view/prm-search/div/md-content/div[2]/prm-search-result-list/div/div[1]/div/div/*/prm-brief-result-container/div[1]/div[3]/prm-brief-result/h3/a')

	#links = driver.find_elements(By.XPATH,'/html/body/primo-explore/div/prm-explore-main/ui-view/prm-search/div/md-content/div[2]/prm-search-result-list/div/div[1]/div/div[*]/prm-brief-result-container/div[1]/div[3]/prm-brief-result/h3/a')
	print(links)
	for link in links:
		hrefs.append(link.get_attribute('href'))
	print(hrefs)
	time.sleep(1.5)
	button_next = driver.find_element(By.XPATH, '//*[@id="resultsPerPage"]/div[1]/div[3]/a')
	button_next.click()
	time.sleep(4)

print(hrefs)






#scraping list of links found in previous function
headings = ["title", "1st author", "abstract", "journal info"]
articles = [] #list for holding meta-data
string = "scripti" #used to find which element has the abstract



for href in hrefs:
	driver.get(href)
	time.sleep(5)
	title = driver.find_element(By.XPATH, '//*[@id="item-details"]/div/div[1]/div[2]/div/div/div[2]/prm-highlight/span')
	author = driver.find_element(By.XPATH, '//*[@id="item-details"]/div/div[2]/div[2]/div/div[1]/div[1]/a/prm-highlight/span')
	test = driver.find_element(By.XPATH, '//*[@id="item-details"]/div/div[3]/div[1]/span').text
	if string in test:
		abstract = driver.find_element(By.XPATH, '//*[@id="item-details"]/div/div[3]/div[2]/div/div/div[2]/prm-highlight/span')
		journal = driver.find_element(By.XPATH, '//*[@id="item-details"]/div/div[4]/div[2]/div/div/div[2]/prm-highlight/span')
	else:
		abstract = driver.find_element(By.XPATH, '//*[@id="item-details"]/div/div[4]/div[2]/div/div/div[2]/prm-highlight/span')
		journal = driver.find_element(By.XPATH, '//*[@id="item-details"]/div/div[5]/div[2]/div/div/div[2]/prm-highlight/span')
	articles.append([title.text, author.text, abstract.text, journal.text])


driver.close()


with open(file_path + "/" + subject + ".csv",'w',newline='') as f:
	c = csv.writer(f)
	c.writerow(headings)
	c.writerows(articles)



print("Program finished!")
print('\a')

