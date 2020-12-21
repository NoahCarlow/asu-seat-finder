import requests # requests for getting html of URL
from requests.exceptions import ConnectionError # catch errors when website can't connect
from bs4 import BeautifulSoup # beautiful soup for scraping web data

CURRENT_TERM = "2211"   # Spring 2020, Fall 2019, ect.

# this function scrapes the number of available seats
def scrape_seatsv2(classNumber):

    # URL that is being scrapped with loaded parameters of term and number
    URL = "https://webapp4.asu.edu/catalog/myclasslistresults?t=" + CURRENT_TERM + "&k=" + classNumber + "&k=" + classNumber + "&hon=F&promod=F&e=all&page=1"

    # sets up requests with a user agent so it is not blocked by ASU servers
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'}
    driver = requests.get(URL, headers=headers)
    #print(driver) # prints the html response (200, 403, ect.) can be useful for error checking

    try:
        classSeatsResults = list()
        soup = BeautifulSoup(driver.text, 'lxml') # loads the source page

        # available seat search
        findSeats = soup.find("td", {"class": "availableSeatsColumnValue"}) # searches seats table column
        seats = findSeats.div.span.text # nav to html span where seat number is held

        driver.close() # close connection

        classSeatsResults.extend([classNumber, seats]) # add scrape data to result list
        return classSeatsResults # returns list of course, instructor, class #, and seats available

    except AttributeError:
        print("Class not found. Is the course number correct?")

    except ConnectionError:
        print("Connection Error")

def scrape_infov2(classNumber):

    # URL that is being scrapped with loaded parameters of term and number
    URL = "https://webapp4.asu.edu/catalog/myclasslistresults?t=" + CURRENT_TERM + "&k=" + classNumber + "&k=" + classNumber + "&hon=F&promod=F&e=all&page=1"

    # sets up requests with a user agent so it is not blocked by ASU servers
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'}
    driver = requests.get(URL, headers=headers)
    #print(driver) # prints the html response (200, 403, ect.) can be useful for error checking

    try:
        classInfoResults = list()
        soup = BeautifulSoup(driver.text, 'lxml') # loads the source page

        # course search
        findCourse = soup.find("td", {"class": "subjectNumberColumnValue"}) # searches course table column
        course = findCourse.text # nav to html span where course is held
        course = "".join(line.strip() for line in course.split("\n")) # remove whitespace

        # instructor search
        findInstructor = soup.find("td", {"class": "instructorListColumnValue"}) # searches instructor table column
        instructor = findInstructor.span.text # nav to html span where instructor is held
        instructor = "".join(line.strip() for line in instructor.split("\n")) # remove whitespace

        driver.close() # close connection

        classInfoResults.extend([course, instructor]) # add scrape data to result list
        return classInfoResults # returns list of course, instructor, class #, and seats available

    except AttributeError:
        print("Class not found. Is the course number correct?")

    except ConnectionError:
        print("Connection Error")