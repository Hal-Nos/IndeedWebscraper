from selenium import webdriver
from bs4 import BeautifulSoup as soup
from datetime import datetime
import pandas as pd
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException

position = input('Input a Job Position: ')
where = input('input a location: ')
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
url = f'https://ph.indeed.com/jobs?q={position}&l={where}'
driver.get(url)
jobtitle = []
company = []
location = []
jobdate = []
link = []
today = datetime.today().strftime('%Y-%m-%d')
content = driver.page_source
bs = soup(content, 'html.parser')

while True:

    for job_card in bs.findAll(attrs='jobsearch-SerpJobCard'):
        name = job_card.find('a')
        if name not in jobtitle:
            jobtitle.append(name.get('title'))

        company_name = job_card.find('span', 'company')
        if company_name not in company:
            company.append(company_name.text.strip())

        company_location = job_card.find('div', 'recJobLoc')
        if company_location not in location:
            location.append(company_location.get('data-rc-loc'))

        date = job_card.find('span', 'date')
        if date not in jobdate:
            jobdate.append(date.text)

        joblink = job_card.find('a')
        if joblink not in link:
            link.append('https://www.indeed.com' + joblink.get('href'))

    try:
        driver.find_element_by_xpath('//a[@aria-label="Next"]').click()
    except NoSuchElementException:
        break
    except ElementNotInteractableException:
        driver.find_element_by_id('popover-x').click()
        continue

driver.quit()
df = pd.DataFrame(
    {'Job Position': jobtitle, 'Company': company, 'Location': location, 'Job Date': jobdate, 'Date': today, 'Job Link': link})
df.to_csv(f'{position}.csv', index=False, encoding='utf-8')

