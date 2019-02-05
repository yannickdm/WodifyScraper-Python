#!/usr/bin/env python
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

display = Display(visible=0, size=(1920, 1080))
display.start()

def outsystems_is_inactive(driver):
    isactive = driver.execute_script('return outsystems.internal.$.active;')
    print 'isactive=', isactive
    return isactive == 0
    
class WodifyScraper(object):
    def __init__(self, username, password):
	options = webdriver.ChromeOptions()
	options.add_argument("--no-sandbox")
        options.add_argument("--disable-impl-side-painting")
        options.add_argument("--disable-setuid-sandbox")
        options.add_argument("--disable-seccomp-filter-sandbox")
        options.add_argument("--disable-breakpad")
        options.add_argument("--disable-client-side-phishing-detection")
        options.add_argument("--disable-cast")
        options.add_argument("--disable-cast-streaming-hw-encoding")
        options.add_argument("--disable-cloud-import")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-session-crashed-bubble")
        options.add_argument("--disable-ipv6")
        options.add_argument("--allow-http-screen-capture")
        options.add_argument("--start-maximized")

        self.url = 'http://app.wodify.com'
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome(chrome_options=options)

    def login(self):
        username_elem = self.driver.find_element_by_id('wtLayoutLogin_SilkUIFramework_wt8_block_wtUsername_wtUsername_wtUserNameInput')
        password_elem = self.driver.find_element_by_id('wtLayoutLogin_SilkUIFramework_wt8_block_wtPassword_wtPassword_wtPasswordInput')

        username_elem.send_keys(self.username)
        password_elem.send_keys(self.password)

        login_elem = self.driver.find_element_by_id('wtLayoutLogin_SilkUIFramework_wt8_block_wtAction_wtAction_wtLoginButton')
        login_elem.click()

        def logged_in(driver):
            try:
                elem = driver.find_element_by_link_text('WOD')
                return elem.is_displayed()
            except NoSuchElementException:
                return False

        wait = WebDriverWait(self.driver, 3)
        wait.until(logged_in)


    def scrape(self):
        self.driver.get(self.url)
        self.login()

	self.driver.get('https://app.wodify.com/Membership/Attendance.aspx')
        list = self.driver.find_element_by_id('AthleteTheme_wt8_block_wtMainContent_wt15_wtUserClassLoginTable_Wrapper').text
 	print list


if __name__ == '__main__':
    scraper = WodifyScraper('wodifyuser','wodifypassword')
    scraper.scrape()
