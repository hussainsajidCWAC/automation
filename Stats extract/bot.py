from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from time import sleep

import re

#gets firmstep login details and date parameters
from secrets import username, password

class statsBot():
    def __init__(self):
        self.driver = webdriver.Edge()
        self.startDate = '01/04/2021'
        self.endDate =  '31/03/2022'
        self.resume = False
        self.startingService = ''
        self.startingReason = ''
        self.startingType = ''

    #clicks on a button
    def clickButton(self, xPath):
        btn = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, xPath)))
        btn.click()
    
    #inputs a value in an input field
    def input(self, xPath, input):
        field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xPath))
        )
        #selects and deletes the existing text
        field.send_keys(Keys.COMMAND, "a")
        field.send_keys(Keys.BACKSPACE)
        field.send_keys(input)
    
    #gets a select field
    def getSelect(self, xPath):
        field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xPath))
        )
        return Select(field)
    
    #goes through the table and gets the phone number stat
    def getPhoneTeamNumber(self):
        result = '0'
        found = False

        #table = self.driver.find_element_by_xpath('//*[@id="transactionsByChannel"]')
        table = self.driver.find_element(by=By.XPATH, value='//*[@id="transactionsByChannel"]')
        rows = table.find_elements(By.TAG_NAME, "tr")
        
        #goes through each row of the table
        for row in rows:
            columns = row.find_elements(By.TAG_NAME, "td")

            #goes through each column to find the correct row
            for column in columns:
                if column.text == 'Phone Team':
                    found = True
                elif found:
                    result = column.text
                    break
            
            if found:
                break
            
        return result
    
    def start(self):
        file = open("stats.csv", "a")
        file.close()

        file = open("stats.csv", "r")

        data = re.split("\n", file.read())

        if (len(data) <= 2):
            file.close()

            file = open("stats.csv", "a")
            file.write('Service, Reason, Type, Amount\n')
            file.close()
        else:
            lastEntry = data[-2].split(',')
            self.startingService = lastEntry[0]
            self.startingReason = lastEntry[1].strip()
            self.startingType = lastEntry[2].strip()
            file.close()
            self.resume = True

        self.login()
    
    #navigates through the login screen
    def login(self):
        self.driver.get('https://qwest.achieveservice.com/')

        self.clickButton('/html/body/div/div/div/div/div[1]/a')

        self.input('//*[@id="username"]', username)
        self.input('//*[@id="password"]', password)

        self.clickButton('/html/body/div/div/div/form/fieldset/div[3]/button')

        self.goToTransactions()
    
    #navigates the self site to transaction page
    def goToTransactions(self):
        self.clickButton('//*[@id="close-cookie-message"]')
        self.clickButton('//*[@id="reports"]')

        self.clickButton('/html/body/div/div[5]/div/div/div/ul/li[6]/a')

        self.input('/html/body/div[1]/div[5]/div/div/div/div/div/div[6]/div/div[1]/div/div/form/div[4]/input', self.startDate)
        self.input('/html/body/div[1]/div[5]/div/div/div/div/div/div[6]/div/div[1]/div/div/form/div[5]/input', self.endDate)
        self.clickButton('//*[@id="tab-transactions"]/div/div[1]/div/div/form/div[6]/button')

        self.getStats()

    #goes through each SRT and saves the value
    def getStats(self):
        services = self.getSelect('//*[@id="TransactionsService"]')

        for service in services.options:
            serviceLabel = service.get_attribute('value')
            
            if ((self.resume and self.startingService == serviceLabel) or self.resume == False):
                services.select_by_value(serviceLabel)
                
                sleep(1)

                reasons = self.getSelect('//*[@id="TransactionsReason"]')
                for reason in reasons.options:
                    reasonLabel = reason.get_attribute('value')

                    if ((self.resume and self.startingReason == reasonLabel) or self.resume == False):
                        reasons.select_by_value(reasonLabel)
                    
                        sleep(1)

                        types = self.getSelect('//*[@id="TransactionsType"]')
                        for type in types.options:
                            typeLabel = type.get_attribute('value')

                            if (self.resume and self.startingType == typeLabel):
                                self.resume = False

                            elif (self.resume == False):
                                types.select_by_value(typeLabel)
                        
                                sleep(1)
                        
                                self.clickButton('//*[@id="tab-transactions"]/div/div[1]/div/div/form/div[6]/button')

                                sleep(5)

                                value = self.getPhoneTeamNumber()

                                file = open("stats.csv", "a")
                                file.write(serviceLabel + ', ' + reasonLabel + ', ' + typeLabel + ', ' + value + '\n')
                                file.close()


bot = statsBot()
bot.start()