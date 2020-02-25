from selenium import webdriver

URL='https://stackoverflow.com/questions/12323403/how-do-i-find-an-element-that-contains-specific-text-in-selenium-webdriver-pyth?rq=1'
TEXT = '<div>My Button</div>'


def search_text(text,element):
    try:
        return True if ( (text in element.text) or (text in element.get_attribute('innerText')) ) else False
    except:
        return False

driver=webdriver.Chrome()
driver.get(URL)
elements=driver.find_elements_by_xpath('//*')
for element in elements:
    if search_text(TEXT,element) is True:
        print(element.get_attribute("id"),'--->',element.text)
driver.close()

