import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument("--disable-infobars")
import selenium.webdriver.common.keys

#defining the driver to be used in process
driver = webdriver.Chrome(executable_path='/Users/apple/Desktop/gdrive/webscrape/drivers/chromedriver',chrome_options=chrome_options)
#access to the page
driver.get('https://sonuc.ysk.gov.tr/sorgu')

time.sleep(8)
#Clicking on "Secim adı ile sorgula"
selectQuery=driver.find_element_by_xpath('//*[@id="collapsePanelTwo"]/div/div/div[3]/button/div/div')
selectQuery.click()
time.sleep(2)

#selecting the name of election
dropdownElectionName= driver.find_element_by_xpath('//*[@id="collapsePanelThree"]/div[1]/div/div/form/div[1]/div/div/ng-select/div/div/div[2]/input')
dropdownElectionName.click()
#as each single element in dropdownlist has randomly created id's, I have to follow more manual,visual way.
#after clicking expanding the dropdown, down arrow 5 times and then push  enter to proceed
i=1
for i in range(1,6):
    dropdownElectionName.send_keys(Keys.DOWN)
dropdownElectionName.send_keys(Keys.ENTER)

#now selecting the type of election

dropdownElectionType=driver.find_element_by_xpath('//*[@id="collapsePanelThree"]/div[1]/div/div/form/div[1]/div[2]/div/ng-select/div/div/div[2]/input')
dropdownElectionType.send_keys(Keys.ENTER)
dropdownElectionType.send_keys(Keys.ENTER)
time.sleep(3)
#click on "Devam et"
buttonDevam=driver.find_element_by_xpath('//*[@id="collapsePanelThree"]/div[1]/div/div/form/div[2]/div/div/button[1]')
buttonDevam.click()
time.sleep(3)

dropdownCity=driver.find_element_by_xpath('//*[@id="collapsePanelFour"]/div[1]/div/div/fieldset/form/div[1]/div[2]/div[1]/ng-select/div/div/div[2]/input')
dropdownCity.send_keys(Keys.ENTER)
dropdownCity.send_keys(Keys.ENTER)

buttonSorgula=driver.find_element_by_xpath('//*[@id="collapsePanelFour"]/div[1]/div/div/fieldset/form/div[2]/div/div/button')
buttonSorgula.click()

time.sleep(2)
saveTable=driver.find_element_by_xpath('//*[@id="collapsePanelFour"]/div[1]/div/div/app-yurtici-ilce-listesi/fieldset/div[2]/div/button')
saveTable.click()

agreeButton=driver.find_element_by_xpath('/html/body/ngb-modal-window/div/div/div[2]/div/button[1]')
agreeButton.click()

a=1
#for 81 cities of Turkey
for a in range(1,82):
    #at each return the down key should be applied as many as the corresponding city in the order
    for a in (0,a):
        dropdownCity.send_keys(Keys.DOWN)
        time.sleep(2)
    dropdownCity.send_keys(Keys.ENTER)
    buttonSorgula.click()
    time.sleep(5)
    #needed to reintroduce the variables initiated above
    saveTable = driver.find_element_by_xpath('//*[@id="collapsePanelFour"]/div[1]/div/div/app-yurtici-ilce-listesi/fieldset/div[2]/div/button')
    saveTable.click()
    time.sleep(1)
    agreeButton = driver.find_element_by_xpath('/html/body/ngb-modal-window/div/div/div[2]/div/button[1]')
    agreeButton.click()