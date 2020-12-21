from selenium import webdriver # ASU class table is JS rendered
from selenium.webdriver.common.keys import Keys # keys
from bs4 import BeautifulSoup # beautiful soup for scraping web data
import time # used for sleep

CURRENT_TERM = "2211"   # Spring 2020, Fall 2019, ect.

chrome_prefs = {}
options = webdriver.ChromeOptions()
options.add_argument("--headless") # reduces overhead
options.add_argument("--log-level=3")
options.add_argument("--silent")

# disable image loading to reduce load times
options.experimental_options["prefs"] = chrome_prefs
chrome_prefs["profile.default_content_settings"] = {"images": 2}
chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}

driver = webdriver.Chrome('C:/Users/carlo/Desktop/chromedriver.exe', options=options)

# this function scrapes the number of available seats
def scrape_seats(classNumber):

    # URL that is being scrapped with loaded parameters of term and number
    URL = "https://webapp4.asu.edu/catalog/classlist?t=" + CURRENT_TERM + "&k=" + classNumber + "&k=" + classNumber + "&hon=F&promod=F&e=all&page=1"
    driver.get(URL)
    
    classSeatResults = list()

    try:
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, 'lxml') # loads the source page

        # available seat search
        findSeats = soup.find("td", {"class": "availableSeatsColumnValue"}) # searches seats table column
        seats = findSeats.div.span.text # nav to html span where seat number is held

        classSeatResults.extend([classNumber, seats]) # add scrape data to result list
        return classSeatResults # returns list of course # and seats available

    except AttributeError:
        print("Class not found. Is the course number correct?")

# this function scrapes the class information including instructor and course name
def scrape_class_info(classNumber):

     # URL that is being scrapped with loaded parameters of term and number
    URL = "https://webapp4.asu.edu/catalog/classlist?t=" + CURRENT_TERM + "&k=" + classNumber + "&k=" + classNumber + "&hon=F&promod=F&e=all&page=1"
    driver.get(URL)

    classInfoResults = list()

    try:
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, 'lxml') # loads the source page

        # course search
        findCourse = soup.find("td", {"class": "subjectNumberColumnValue"}) # searches course table column
        course = findCourse.text # nav to html span where course is held
        course = "".join(line.strip() for line in course.split("\n")) # remove whitespace

        # instructor search
        findInstructor = soup.find("td", {"class": "instructorListColumnValue"}) # searches instructor table column
        instructor = findInstructor.span.text # nav to html span where instructor is held
        instructor = "".join(line.strip() for line in instructor.split("\n")) # remove whitespace

        classInfoResults.extend([course, instructor]) # add scrape data to result list
        return classInfoResults # returns list of course name and instructor

    except AttributeError:
        print("Class not found. Is the course number correct?")

# function to close chrome driver
def closeDriver():
    driver.close()