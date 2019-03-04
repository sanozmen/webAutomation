#a little script to get all the lottery results published on 
#web page of Turkish lottery organization

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException


f = open('loto.txt', 'w+')

#call the drive and open up the page

driver = webdriver.Chrome(executable_path='/Users/apple/Desktop/gdrive/webscrape/drivers/chromedriver')
driver.get('LINK TO THE PAGE')

time.sleep(5)

#total number of elements where all the draw results were linked
allDropdown = len(driver.find_elements_by_xpath('//*[@id="sayisal-tarihList"]/option'))
#just to check how many in total
print(allDropdown)

#then looping
for hafta in range(1,allDropdown+1):


    #first select the week you would like to look at
    selectHafta = driver.find_element_by_xpath('//*[@id="sayisal-tarihList"]/option['+str(hafta)+']')
    selectHafta.click()
    time.sleep(1)
    date = driver.find_element_by_xpath('//*[@id="sayisal-tarihList"]/option[' + str(hafta) + ']')
    f.write(date.text)
    f.write(',')

    altiBilen = driver.find_element_by_xpath('//*[@id="sayisal-bilenkisisayisi-6_BILEN"]')
    besBilen=driver.find_element_by_xpath('//*[@id="sayisal-bilenkisisayisi-5_BILEN"]')
    dortBilen = driver.find_element_by_xpath('//*[@id="sayisal-bilenkisisayisi-4_BILEN"]')
    ucBilen = driver.find_element_by_xpath('//*[@id="sayisal-bilenkisisayisi-3_BILEN"]')

    f.write(altiBilen.text)
    f.write(',')
    f.write(besBilen.text)
    f.write(',')
    f.write(dortBilen.text)
    f.write(',')
    f.write(ucBilen.text)
    f.write('\n')

