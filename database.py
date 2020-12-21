import pymongo
from pymongo import MongoClient

# connect to our cluster and setup client and collection
client = pymongo.MongoClient("Enter Database Here")
db = client["seatnotify"]
collection = db["users"]

# insert a new user into our database
# classArray - string array of classes user wants to track
def insertUser(classArray, phoneNumber):
    user = {"classes": classArray, "phone": phoneNumber}
    collection.insert_one(user)

# gets all the classes within the database, duplicates are ignored
def getClasses():
    results = collection.distinct("classes") # finds all collections classes
    return results # returns list of classes

# gets the phone number of all collections that have the inputed class number
def getPhone(classNumber):
    results = db.users.find({"classes":classNumber}) # find collections with specified class number
    return results.distinct("phone") # returns a list of phone numbers

# removes every instance of classNumber in our database
def removeClass(classNumber):
    db.users.update( { }, { "$pull": { "classes": classNumber } }, multi=True )
