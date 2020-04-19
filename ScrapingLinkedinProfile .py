#Author: WEB SCRAPING MAROC
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import getpass
import csv
from parsel import Selector

writer = csv.writer(open('LinkedInProfiles.csv', 'w')) # preparing csv file to store parsing result later
writer.writerow(['name', 'job_title', 'schools', 'location', 'ln_url'])

class LinkedinBot:
    def __init__(self, username, password):
        """ Initialized Chromedriver, sets common urls, username and password for user """
	
        self.driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')

        self.base_url = 'https://www.linkedin.com'
        self.login_url = self.base_url + '/login'
        self.google_url = 'https://www.google.com'


        self.username = username
        self.password = password

    def _nav(self, url):
        self.driver.get(url)
        time.sleep(3)

    def login(self, username, password):
        """ Login to LinkedIn account """
        self._nav(self.login_url)
        self.driver.find_element_by_id('username').send_keys(self.username)
        self.driver.find_element_by_id('password').send_keys(self.password)
        self.driver.find_element_by_xpath("//button[contains(text(), 'S’identifier')]").click()
	
  

    #def post(self, text):
       # """ Make a text post """
        #self.driver.find_element_by_class_name('share-box__open').click()
        #self.driver.find_element_by_class_name('mentions-texteditor__content').send_keys(text)
        #self.driver.find_element_by_class_name('share-actions__primary-action').click()
    
    def search(self, text, connect=False):
        """ Search execeuted from home screen """
        self._nav(self.google_url)

        search_input = self.driver.find_element_by_name('q')
        #search_input.send_keys(text)
	# let google find any linkedin user with keyword "python developer" and "San Francisco"
        search_input.send_keys(text)
        search_input.send_keys(Keys.RETURN)
        # grab all linkedin profiles from first page at Google
        profiles = self.driver.find_elements_by_xpath('//*[@class="r"]/a[1]')
        profiles = [profile.get_attribute('href') for profile in profiles]
        # visit each profile in linkedin and grab detail we want to get
        for profile in profiles:
            self.driver.get(profile)

            try:
                sel = Selector(text=self.driver.page_source)
                name = sel.xpath('//title/text()').extract_first().split(' | ')[0]
                job_title = sel.xpath('//h2/text()').extract_first().strip()
                schools = ', '.join(sel.xpath('//*[contains(@class, "pv-entity__school-name")]/text()').extract())
                location = sel.xpath('//*[@class="t-16 t-black t-normal inline-block"]/text()').extract_first().strip()
                ln_url = self.driver.current_url
                """
                you can add another logic in case parsing is failed, ie because no job title is found
                because the linkedin user isn't add it
                """
       	    except:
                print('failed')

            # print to console for testing purpose
            print('\n')
            print(name)
            print(job_title)
            print(schools)
            print(location)
            print(ln_url)
            print('\n')

            writer.writerow([name, job_title, schools, location, ln_url])

	#driver.quit()
    
        # Waiting for search results to load
        time.sleep(3)
      	

        if connect:
            self._search_connect()

    def _search_connect(self):
        """ Called after search method to send connections to all on page """

        connect = self.driver.find_element_by_class_name('search-result__action-button')
        connect.click()
        time.sleep(2)
        self.driver.find_element_by_class_name('ml1').click()


if __name__ == '__main__':

    username = input("Username:")
    password = getpass.getpass("Password:")
    post_text = 'TEST'
    search_text = input("Search Text:")

    bot = LinkedinBot(username, password)
    bot.login(username, password)
    #bot.post(post_text)
    bot.search(search_text, connect=True)


