import os
import constants as const
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

''' Set these variables as you want '''

#Path of download
current_loc = os.path.join(os.path.abspath(os.curdir), const.directory)
#directory = const.directory
directory = current_loc

def run(delivery_type, start_year, start_month, start_day, end_year, end_month, end_day):

    ''' Path of FireFox Web Driver'''
    os.environ['PATH'] += const.webdriver_path

    firefox_options = webdriver.FirefoxOptions()
    firefox_options.set_preference("browser.download.folderList", 2)
    firefox_options.set_preference("browser.download.manager.showWhenStarting", False)
    firefox_options.set_preference("browser.helperApps.alwaysAsk.force", False)
    firefox_options.set_preference("browser.download.dir", directory)
    #firefox_options.add_argument('--no-sandbox')
    #firefox_options.add_argument('--headless')
    #firefox_options.add_argument('--disable-gpu')
    driver = webdriver.Firefox(firefox_options)
    #driver = webdriver.Firefox()

    print(str(start_day)+"/"+str(start_month)+"/"+str(start_year)+" - "+str(end_day)+"/"+str(end_month)+"/"+str(end_year))

    url = const.web_url
    driver.get(url)
    driver.implicitly_wait(5)   #if the browser or the server is slow we can increase the waiting time (3sec)

    delivery_period = Select(driver.find_element(By.NAME, 'ctl00$InnerContent$ddlPeriod'))
    delivery_period.select_by_visible_text(delivery_type)

    driver.find_element(By.NAME, "ctl00$InnerContent$calFromDate$txt_Date").click()

    select_start_year = Select(driver.find_element(By.ID, "scwYears"))
    select_start_year.select_by_visible_text(start_year)
    driver.implicitly_wait(5)
    select_start_month = Select(driver.find_element(By.ID, "scwMonths"))
    select_start_month.select_by_visible_text(start_month)
    driver.implicitly_wait(5)

    start_date = driver.find_element(By.XPATH, '//*[@id="scwCells"]')
    for row in start_date.find_elements(By.CSS_SELECTOR, "tr"):
        for cell in row.find_elements(By.CSS_SELECTOR, 'td'):
            if(cell.text == start_day):
                cell.click()

    driver.find_element(By.NAME, "ctl00$InnerContent$calToDate$txt_Date").click()
    end_start_year = Select(driver.find_element(By.ID, "scwYears"))
    end_start_year.select_by_visible_text(end_year)
    driver.implicitly_wait(5)
    end_start_month = Select(driver.find_element(By.ID, "scwMonths"))
    end_start_month.select_by_visible_text(end_month)
    driver.implicitly_wait(5)

    end_date = driver.find_element(By.XPATH, '//*[@id="scwCells"]')
    for row in end_date.find_elements(By.CSS_SELECTOR, "tr"):
        for cell in row.find_elements(By.CSS_SELECTOR, 'td'):
            if(cell.text == end_day):
                cell.click()

    try:
        update_report = driver.find_element(By.ID, "ctl00_InnerContent_btnUpdateReport")
        update_report.click()

        driver.implicitly_wait(5)   #if the browser or the server is slow we can increase the waiting time (3sec)
        save_button = driver.find_element(By.ID, "ctl00_InnerContent_reportViewer_ctl05_ctl04_ctl00_ButtonLink")
        save_button.click()

        excel_element = driver.find_element(By.LINK_TEXT, 'Excel')
        excel_element.click()
    except:
        pass

    driver.get('about:downloads')
    WebDriverWait(driver, 5000).until(EC.presence_of_element_located((By.CLASS_NAME, 'downloadIconShow')))
    driver.close()
    driver.quit()