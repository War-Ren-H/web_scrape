import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import csv
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from bs4 import BeautifulSoup


names = pd.read_excel('Tech_Aspects.xlsx', header = None)

names = list(names[0])

tech_urls = []

browser = webdriver.Safari()

browser.get('https://en.wikipedia.org/wiki/Cheese')


for name in names:

    try:
        searchBar = browser.find_element_by_id('searchInput')
        searchBar.send_keys(name)

        searchBar.send_keys(Keys.ENTER)

        wait = WebDriverWait(browser, 100)
        men_menu = wait.until(ec.visibility_of_element_located((By.XPATH, "//h1[@id='firstHeading']")))
        ActionChains(browser).move_to_element(men_menu).perform()

        soup = BeautifulSoup(browser.page_source, 'lxml')
        scope_row = soup.find_all("h1",{"id":"firstHeading"})

        for thing in scope_row:
            the_header = thing.text

        if the_header.lower() != name.lower():
            tech_urls.append(name + 'not found')

    #search = browser.find_element_by_id('searchButton')
    #print(search)
    #search.click()

        else:
            tech_urls.append(browser.current_url)
    except:
        searchBar = browser.find_element_by_id('simpleSearch')
        searchBar.send_keys(name)

        searchBar.send_keys(Keys.ENTER)

        wait = WebDriverWait(browser, 10000)
        men_menu = wait.until(ec.visibility_of_element_located((By.XPATH, "//h1[@id='firstHeading']")))
        ActionChains(browser).move_to_element(men_menu).perform()

        soup = BeautifulSoup(browser.page_source, 'lxml')
        scope_row = soup.find_all("h1",{"id":"firstHeading"})

        for thing in scope_row:
            the_header = thing.text
            print(the_header)

        if the_header != name:
            tech_urls.append(name + ' not found')

    #search = browser.find_element_by_id('searchButton')
    #print(search)
    #search.click()

        else:
            tech_urls.append(browser.current_url)


zipper = list(zip(names, tech_urls))
df = pd.DataFrame(zipper, columns = ['Aspects', 'Wikipedia Links'])

df.to_excel('Aspect_urls.xlsx', index = False)
