import seatscrapev2 # web scraper for course info
import database # mongodb database handling
import send_sms # twilio sms/email notifications

def main():
    
    classList = database.getClasses() # get all classes in our database

    # run seat scrape and store data into scrapedSeats list
    scrapedSeats = list()
    for classes in classList:
        scrapedSeats.append(seatscrapev2.scrape_seatsv2(classes))

    openClasses = list() # stores list of class #'s with open spots

    # runs through scrapedSeats list and finds open seats i.e. greater than 0
    for i in range (0, len(scrapedSeats)):
        if (scrapedSeats[i] != None): # condition to check if class exists
            if (int(scrapedSeats[i][1]) > 0):
                openClasses.append(scrapedSeats[i][0]) # appends open class #'s to list

    # find what phones numbers to send open seat notifications to
    for classes in openClasses:
        userPhones = database.getPhone(classes) # stores user phone #'s for each class

        classInfo = (seatscrapev2.scrape_infov2(classes)) # stores class name and instructor

        # traverses through list of phone numbers correspondent with open classes
        # sends a message to each phone number in that list (ONLY HANDLES U.S. #'s)
        for i in range(0, len(userPhones)):
            message = send_sms.client.messages.create(
                body = "{} with {} has open seats!".format(classInfo[0], classInfo[1]),
                from_ = '+123',
                to = '+1{}'.format(userPhones[i])
            )

        database.removeClass(classes) # removes every instance of open class in db


if __name__ == "__main__":
    main()