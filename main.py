import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#introduction
print("Connection BOT -\n"
      "1. Must have Google Chrome\n"
      "2. Works with People Only\n"
      "3. Enter your Linkedin Credentials\n"
      "4. Search for types of people (Eg: recruiter facebook)\n"
      "5. Hit Enter\n")


#Entering details
username = input("Enter LinkedIn Username: ")
password = input("Enter LinkedIn Password: ")
searchText = input("Enter Search Text: ")
messageNote = input("Enter your message to connections: ")


#opening the driver
driver = webdriver.Chrome('./chromedriver.exe')

#urls
baseUrl = 'https://www.linkedin.com/login'
feedUrl = 'https://www.linkedin.com/feed'

#filling in the login form
driver.get(baseUrl)
usr = driver.find_element_by_id('username')
usr.send_keys(username)
pwd = driver.find_element_by_id('password')
pwd.send_keys(password)
pwd.send_keys(Keys.RETURN)

#wait for feed to load
time.sleep(1)

#search in the global search bar
globalSearch = driver.find_element_by_class_name(
    "search-global-typeahead__input")
globalSearch.send_keys(searchText)
globalSearch.send_keys(Keys.RETURN)
time.sleep(2)

#gets only people
onlyPeople= driver.find_element_by_xpath('//button[@aria-label="View only People results"]')
onlyPeople.send_keys(Keys.RETURN)

time.sleep(2)


#bool value to check if the search page is the last ne
end=True

#if not
while end:

    #get all the lists of profile
    #omits LinkedIn cards and filler stuff
    connects = driver.find_elements_by_xpath('//div[@data-test-search-result="PROFILE"]')
    time.sleep(1)

    #Repeated PAGE DOWNs to load the profiles of the connections 
    body= driver.find_element_by_tag_name('body')
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(1)
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(1)
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(1)
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(2)


    #after the complete page load, get all the profiles
    for i in connects:

        #try except block to catch the connections who are either premium members or private
        try:

            #click the action button for each profile 
            #could be CONNECT / FOLLOW
            #MESSAGE action is not being handled here
            connec=i.find_element_by_class_name('search-result__action-button')
            connec.send_keys(Keys.RETURN)
            addANote = driver.find_element_by_xpath('//button[@aria-label="Add a note"]')
            addANote.send_keys(Keys.RETURN)
            time.sleep(1)   

            #writes a custom message to the connection   
            message = driver.find_element_by_id('custom-message')
            message.send_keys(messageNote)
            time.sleep(1)

            #send the connection request to the person
            done = driver.find_element_by_xpath('//button[@aria-label="Done"]')
            done.send_keys(Keys.RETURN)
            

            #this block of code was used for testing purpose
            #dismiss = driver.find_element_by_xpath('//button[@aria-label="Dismiss"]')
            #dismiss.send_keys(Keys.RETURN)

            time.sleep(1)
        except:

            #if there is no CONNECT or FOLLOW buttons or any exception that occurs
            #this will list out the names of the connections left to connect
            name = i.find_element_by_class_name('actor-name')
            print ("Could not find an action button for this person:  "+name.text)
    
    #checks for the next button in the search list
    buttonNext = driver.find_element_by_xpath('//button[@aria-label="Next"]')
    time.sleep(1)

    #if it is the last search page, the next button is disabled
    #check if the button is disabled
    end = buttonNext.is_enabled()

    #if not, move to the next page
    if end:
        buttonNext.send_keys(Keys.RETURN)

    #else, change the value of end and exit the loop
    time.sleep(1)

print("The bot has done its job! Have a great network ahead!")