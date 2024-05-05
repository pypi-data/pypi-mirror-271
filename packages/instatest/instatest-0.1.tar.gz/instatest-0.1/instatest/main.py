from bs4 import BeautifulSoup
from urllib.request import urlopen
import cloudscraper
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

class Download:
    def __init__(self,url):
        self.url = url
        self.option = webdriver.FirefoxOptions() 
        self.option.add_argument("--headless")
        self.option.add_argument("--no-sandbox")
        self.driver = webdriver.Firefox(options=self.option)
        self.driver.delete_all_cookies()
        self.driver.implicitly_wait(13)
    def facebook(self):
        data = {
                'URLz': self.url,
                }        
        try:       
            scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance
            response = scraper.post('https://fdown.net/download.php',  data=data)
            download_soup = BeautifulSoup(response.text,"html.parser")
            downlaod_hdlink = download_soup.find("a",id="hdlink" )
            downlaod_sdlink = download_soup.find("a",id="sdlink" )
            downlaod_imgs = download_soup.find_all("img",class_="lib-img-show")
            downlaod_description = download_soup.find_all("div",class_='lib-row lib-desc')
            try:
                img = downlaod_imgs[0]["src"] if downlaod_imgs else None
            except :
                img = downlaod_imgs[0]["data-cfsrc"] if downlaod_imgs else None
            res={
                        'hdlink':downlaod_hdlink['href'] if downlaod_hdlink else None,
                        'sdlink':downlaod_sdlink["href"] if downlaod_sdlink else None,
                        'fb_img':img,
                        'description': downlaod_description[0].text.strip() if downlaod_description else None,
                        'duration': downlaod_description[1].text.strip() if downlaod_description else None,
                        'status_code': 200,
            }
        except Exception as e:
            res={
            'status_code': 302,
            'message': "Uh-Oh! This video might be private and not public ",
                }  
        return res
    
    def youtube(self):
        return "download link from youtube"
    def instagram(self):
        try:
            print(self.url)
            self.driver.get("https://snapinsta.app/")
            print("start get ")
            #sleep(20)
            self.driver.find_element(By.XPATH,'/html/body/main/div[1]/form/div/input[1]').send_keys('https://www.instagram.com/reel/C6bHQRir3Er/?igsh=MzRlODBiNWFlZA==')
            self.driver.find_element(By.XPATH,'/html/body/main/div[1]/form/button').click()
            try:
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "download-bottom")))
                print("Page loaded successfully!")
                new_page_html = self.driver.page_source

                # Use BeautifulSoup to parse the HTML content
                new_page_soup = BeautifulSoup(new_page_html, 'html.parser')
                download_btn = new_page_soup.find("div",class_='download-bottom')
                print(download_btn.find("a")["href"]) 
                rr =  download_btn.find("a")["href"]
            except TimeoutException:
                rr = "Page didn't load within 10 seconds."
            try:
                # Wait for the cookies widget to appear (replace "cookies_widget_xpath" with the actual XPath)
                close_button = WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[2]/button")))

                # Close or hide the cookies widget (replace "close_button_xpath" with the XPath for the close button)
                #close_button = cookies_widget.find_element(By.XPATH, "close_button_xpath")
                close_button.click()

                # Continue with other actions on the page
            except TimeoutException:
                # Cookies widget did not appear, continue with other actions on the page
                pass
    
            self.driver.quit()
            #download_video(video_url, download_directory)
        except Exception as e:
            rr=e
                
        res={
            'status_code': 200,
            'message': str(rr),
                } 
        return res
    
    def tiktok(self):
        return "download link from tiktok"