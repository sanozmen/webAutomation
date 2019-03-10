#a script to get information about all license,prelicense owners of energy facilities
#the script is not fully automated. It requires manual confirmation of google recaptcha in an estimated max. duration of 3 min.
#then the script does the rest to get info and write it to a txt file. 

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException

#initiate the .txt file on which the data will be written
f = open('all_PL_degerlendirmede.txt', 'w+')

#define the path to the driver either gecko or chrome and then run it
driver = webdriver.Firefox(executable_path='C:/Users/ozmens/Desktop/1st/GreenFieldTest/EPDK_License_PreLicense/webscrape/drivers/geckodriver.exe')
driver.get('LINK TO THE PAGE')



#select evaluation status for the project
yururluktePath= '//*[@id="elektrikUretimOnLisansOzetForm:lisansDurumu_INPUT"]/option[2]'
selectYururlukte=driver.find_element_by_xpath(yururluktePath)
selectYururlukte.click()


#select one city or all of them
ilPath='//*[@id="elektrikUretimOnLisansOzetForm:il_INPUT"]/option[1]'
selectIl=driver.find_element_by_xpath(ilPath)
selectIl.click()

#select type of plant
ruzgarPath='//*[@id="elektrikUretimOnLisansOzetForm:j_idt32"]/option[3]'
selectRuzgar=driver.find_element_by_xpath(ruzgarPath)
selectRuzgar.click()


#waiting before the user tries manually passing recaptcha of google, sometimes fails. Requires repetitive action
time.sleep(220)


#click 50 to view max of 50 records per page
fiftyPath='//*[@id="elektrikUretimOzetSorguSonucu:list_rppDD"]/option[5]'
selectFifty=driver.find_element_by_xpath(fiftyPath)
selectFifty.click()


time.sleep(5)

#get the total number of rows
row_count = len(driver.find_elements_by_xpath('//*[@id="elektrikUretimOzetSorguSonucu:list_data"]/tr'))

print('Bu sayfa icin gösterilen toplam ÖNlisans sayısı:', row_count)

row = 0


#check the number of total pages
#get total number for FOR loop and set it up

#starts from 2 since we are viewing the first page
for mainPage in range(2, 7):

    for row in range(row, row_count):
        print(row+1, '.satir kutucugu')
        #time.sleep(3)
        #since j_idt143 changes to j_idt152 sometimes, check which one exists
        buttonPopup = None
        while not buttonPopup:
            try:
                buttonPopup = driver.find_element_by_xpath('//*[@id="elektrikUretimOzetSorguSonucu:list:' + str(row) + ':j_idt58"]/span[1]')
                buttonPopup.click()
                time.sleep(10)
                popup_rowCount = len(driver.find_elements_by_xpath('//*[@id="elektrikKoordinatViewDataTable_data"]/tr'))

            except NoSuchElementException:
                otherButtonPopup=driver.find_element_by_xpath('//*[@id="elektrikUretimOzetSorguSonucu:list:' + str(row) + ':j_idt152"]/span[1]')
                otherButtonPopup.click()
                time.sleep(10)
                popup_rowCount = len(driver.find_elements_by_xpath('//*[@id="elektrikKoordinatViewDataTable_data"]/tr'))

                break

        if popup_rowCount < 10:

            for eachRow in range(0, popup_rowCount):
                print('Number of rows:', popup_rowCount)
                for column in range(2, 19):
                    genelBilgiler = driver.find_elements_by_xpath('// *[ @ id = "elektrikUretimOzetSorguSonucu:list_data"] / tr['+str((row%50)+1)+']'+' / td['+str(column)+']')
                    for value1 in genelBilgiler:
                        f.write(value1.text)
                        f.write('   ')
                        print (value1.text)
                for column2 in range(3, 5):
                    koordinatlar = driver.find_elements_by_xpath('//*[@id="elektrikKoordinatViewDataTable_data"]/tr['+str(eachRow+1)+']'+' / td['+str(column2)+']')
                    for value2 in koordinatlar:
                        f.write(value2.text)
                        f.write('   ')
                        print (value2.text)
                f.write('\n')

        #the case when number of rows appeared in popup window equal to 10
        elif  popup_rowCount==10:
            #click to see all the 50 records
            driver.find_element_by_xpath('//*[@id="elektrikKoordinatViewDataTable_rppDD"]/option[5]').click()
            #then re-define the number of rowCount appeared in the popup window
            time.sleep(5)
            popup_rowCount = len(driver.find_elements_by_xpath('//*[@id="elektrikKoordinatViewDataTable_data"]/tr'))

            #get all data if the results shown are less then 50
            print(popup_rowCount)
            if popup_rowCount<49:

                print ('Number of rows:', popup_rowCount)
                for eachRow in range(0, popup_rowCount):
                    print('Number of rows:', popup_rowCount)
                    for column in range(2, 19):
                        genelBilgiler = driver.find_elements_by_xpath(
                            '// *[ @ id = "elektrikUretimOzetSorguSonucu:list_data"] / tr[' + str(
                                (row % 50) + 1) + ']' + ' / td[' + str(column) + ']')
                        for value1 in genelBilgiler:
                            f.write(value1.text)
                            f.write('   ')
                    for column2 in range(3, 5):
                        koordinatlar = driver.find_elements_by_xpath(
                            '//*[@id="elektrikKoordinatViewDataTable_data"]/tr[' + str(
                                eachRow + 1) + ']' + ' / td[' + str(column2) + ']')
                        for value2 in koordinatlar:
                            f.write(value2.text)
                            f.write('   ')
                    f.write('\n')

            # print company info + one row from popup
            elif popup_rowCount == 50:
                print ('icteki 50yi uyguluyor')
                print ('Number of rows:', popup_rowCount)
                #close and reopen it
                driver.find_element_by_xpath('//*[@id="elektrikKoordinatViewDialog"]/div[1]/a[1]/span').click()
                time.sleep(7)
                #this part is for reopening
                button2Popup = None
                while not button2Popup:
                    try:
                        button2Popup = driver.find_element_by_xpath(
                            '//*[@id="elektrikUretimOzetSorguSonucu:list:' + str(row) + ':j_idt58"]/span[1]')
                        button2Popup.click()
                        time.sleep(4)
                        popup_rowCount = len(
                            driver.find_elements_by_xpath('//*[@id="elektrikKoordinatViewDataTable_data"]/tr'))
                        print(popup_rowCount)

                        break

                    except NoSuchElementException:
                        driver.find_element_by_xpath(
                            '//*[@id="elektrikUretimOzetSorguSonucu:list:' + str(row) + ':j_idt152"]/span[1]').click()
                        time.sleep(7)
                        popup_rowCount = len(
                            driver.find_elements_by_xpath('//*[@id="elektrikKoordinatViewDataTable_data"]/tr'))
                        print(popup_rowCount)
                        break

                for eachRow in range(0, popup_rowCount):
                    for column in range(2, 19):
                        genelBilgiler = driver.find_elements_by_xpath('// *[ @ id = "elektrikUretimOzetSorguSonucu:list_data"] / tr[' + str((row%50)+1) + ']' + ' / td[' + str(column) + ']')
                        for value1 in genelBilgiler:
                            f.write(value1.text)
                            f.write('   ')
                    for column2 in range(3, 5):
                        koordinatlar = driver.find_elements_by_xpath(
                            '   //*[@id="elektrikKoordinatViewDataTable_data"]/tr[' + str(eachRow + 1) + ']' + ' / td[' + str(
                        column2) + ']')
                        for value2 in koordinatlar:
                            f.write(value2.text)
                            f.write('   ')
                    f.write('\n')
                    time.sleep(3)


                #if there are other pages after completing the first page
                # if there are other pages after completing the first page
                nexttoPage = None
                while not nexttoPage:
                    try:
                        for try2Page in range(2, 17):
                            nexttoPage = driver.find_element_by_xpath('//*[@id="elektrikKoordinatViewDataTable_paginator_bottom"]/span[4]/span['+str(try2Page)+']')
                            nexttoPage.click()
                            time.sleep(10)
                            popup_rowCount = len(driver.find_elements_by_xpath('//*[@id="elektrikKoordinatViewDataTable_data"]/tr'))
                            print('n')
                            for eachRow in range(0, popup_rowCount):
                                for column in range(2, 19):
                                    genelBilgiler = driver.find_elements_by_xpath('// *[ @ id = "elektrikUretimOzetSorguSonucu:list_data"] / tr[' + str((row%50) + 1) + ']' + ' / td[' + str(column) + ']')
                                    for value1 in genelBilgiler:
                                        f.write(value1.text)
                                        f.write('   ')
                                for column2 in range(3, 5):
                                    koordinatlar = driver.find_elements_by_xpath('//*[@id="elektrikKoordinatViewDataTable_data"]/tr[' + str(eachRow + 1) + ']' + ' / td[' + str(column2) + ']')
                                    for value2 in koordinatlar:
                                        f.write(value2.text)
                                        f.write('   ')
                                f.write('\n')
                                print('finished')


                    except NoSuchElementException:
                        text = 'not found any other page'
                        print(text)
                        break

        #once clicked down for expanding the results for the first popup, all following will be shown as already expanded, that's why
        #this will be the loop that is going to be mostly used if the numver of coordinates are less than 50
        elif popup_rowCount > 10 and popup_rowCount != 50:

            print ('Row Count is:', popup_rowCount)
            for eachRow in range(0,popup_rowCount):
                for column in range(2, 19):
                    genelBilgiler = driver.find_elements_by_xpath(
                        '// *[ @ id = "elektrikUretimOzetSorguSonucu:list_data"] / tr[' + str(
                            (row%50) + 1) + ']' + ' / td[' + str(column) + ']')
                    for value1 in genelBilgiler:
                        f.write(value1.text)
                        f.write('   ')
                for column2 in range(3, 5):
                    koordinatlar = driver.find_elements_by_xpath('//*[@id="elektrikKoordinatViewDataTable_data"]/tr['+str(eachRow+1)+']'+' / td['+str(column2)+']')
                    for value2 in koordinatlar:
                        f.write(value2.text)
                        f.write('   ')
                f.write('\n')
        elif popup_rowCount == 50:

            print('Number of rows:', popup_rowCount)
            for eachRow in range(0, popup_rowCount):
                for column in range(2, 19):
                    genelBilgiler = driver.find_elements_by_xpath('// *[ @ id = "elektrikUretimOzetSorguSonucu:list_data"] / tr[' + str((row%50) + 1) + ']' + ' / td[' + str(column) + ']')
                    for value1 in genelBilgiler:
                        f.write(value1.text)
                        f.write('   ')
                for column2 in range(3, 5):
                    koordinatlar = driver.find_elements_by_xpath('//*[@id="elektrikKoordinatViewDataTable_data"]/tr['+str(eachRow+1)+']'+' / td['+str(column2)+']')
                    for value2 in koordinatlar:
                        f.write(value2.text)
                        f.write('   ')
                f.write('\n')

            time.sleep(5)

           # if there are other pages after completing the first page
            nextPage = None
            while not nextPage:
                try:
                    for tryPage in range(2, 17):
                        nextPage = driver.find_element_by_xpath('//*[@id="elektrikKoordinatViewDataTable_paginator_bottom"]/span[4]/span['+str(tryPage)+']')
                        nextPage.click()
                        time.sleep(11)
                        popup_rowCount = len(driver.find_elements_by_xpath('//*[@id="elektrikKoordinatViewDataTable_data"]/tr'))
                        for eachRow in range(0, popup_rowCount):
                            for column in range(2, 19):
                                genelBilgiler = driver.find_elements_by_xpath('// *[ @ id = "elektrikUretimOzetSorguSonucu:list_data"] / tr[' + str((row%50) + 1) + ']' + ' / td[' + str(column) + ']')
                                for value1 in genelBilgiler:
                                    f.write(value1.text)
                                    f.write('   ')
                            for column2 in range(3, 5):
                                koordinatlar = driver.find_elements_by_xpath(
                                    '//*[@id="elektrikKoordinatViewDataTable_data"]/tr[' + str(
                                    eachRow + 1) + ']' + ' / td[' + str(column2) + ']')
                                for value2 in koordinatlar:
                                    f.write(value2.text)
                                    f.write('   ')
                            f.write('\n')

                    break

                except NoSuchElementException:
                    text = 'not found any other page'
                    print(text)
                    break


        #close the popup window
        driver.find_element_by_xpath('//*[@id="elektrikKoordinatViewDialog"]/div[1]/a[1]/span').click()
        #time.sleep(2)

    followingPages = driver.find_element_by_xpath('//*[@id="elektrikUretimOzetSorguSonucu:list_paginator_bottom"] / span[4]/ span['+str(mainPage)+']')
    followingPages.click()
    time.sleep(10)

    row = row_count
    row_count = row_count+50

    print('now you should be on the second page')
