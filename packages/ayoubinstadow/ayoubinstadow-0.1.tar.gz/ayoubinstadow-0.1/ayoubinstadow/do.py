
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
def download():
    option = webdriver.ChromeOptions() 
    option.add_argument("--headless")
    option.add_argument("--no-sandbox")
    option.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=option)
    driver.delete_all_cookies()
    driver.implicitly_wait(13)
    print('go ')
    driver.get("https://snapinsta.app/")
    #sleep(20)
    driver.find_element(By.XPATH,'/html/body/main/div[1]/form/div/input[1]').send_keys('https://www.instagram.com/reel/C6bHQRir3Er/?igsh=MzRlODBiNWFlZA==')
    driver.find_element(By.XPATH,'/html/body/main/div[1]/form/button').click()

    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "download-bottom")))
        print("Page loaded successfully!")
        new_page_html = driver.page_source

        # Use BeautifulSoup to parse the HTML content
        new_page_soup = BeautifulSoup(new_page_html, 'html.parser')
        download_btn = new_page_soup.find("div",class_='download-bottom')
        print(download_btn.find("a")["href"]) 
        rr =  download_btn.find("a")["href"]
    except TimeoutException:
        rr = "Page didn't load within 10 seconds."
    try:
        # Wait for the cookies widget to appear (replace "cookies_widget_xpath" with the actual XPath)
        close_button = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[2]/button")))

        # Close or hide the cookies widget (replace "close_button_xpath" with the XPath for the close button)
        #close_button = cookies_widget.find_element(By.XPATH, "close_button_xpath")
        close_button.click()

        # Continue with other actions on the page
    except TimeoutException:
        # Cookies widget did not appear, continue with other actions on the page
        pass

    #download_video(video_url, download_directory)

    driver.quit()
    print('fin')