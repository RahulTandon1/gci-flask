'''
About
A python program/script/module that stores the functions
that are used throughout the the application to interact with the user

-----

Functions included:

1. storeFiles - stores the file to db and returns a status accordingly.
2. getTextByTitle - returns the text of a file given it's assigned title.
3. getListOfTitles - returns a list of all the titles of all the documents.
'''


# importing pymongo
import pymongo

# getting connection string from file.
# You might find this file empty for security reasons.
f = open('connectionString', 'r')
connectionString = f.read()
f.close()


# getting the client
client = pymongo.MongoClient(connectionString)

# selecting the db
db = client.testDb

# getting the required collection
storedFiles = db.storedFiles


# stores the 'file' in the form of a mongodb document.
# takes input of the title and the binaryContent extracted from the file
# [By default a file on reading returns binary data, which this
# function converts an ASCII string]
# returns a 'status'.
# the only logical error is the case of the title already being used,
# in which case we return the appropriate 'status'
def storeFile(title, binaryContent):

    # object which will eventually be stored in mongodb
    obj = {
        # converting binary to ascii string
        'text': binaryContent.decode('ascii'),

        # the title acts as the unique id
        '_id': title
    }

    try:
        # storing in the db
        res = storedFiles.insert_one(obj)
        # if we come across no errors, return 'okay' status
        return 'okay'

    # if we do come across the error of the 'title' already being used.
    except pymongo.errors.DuplicateKeyError:
        return 'duplicateKeyError'


# takes input of title
# returns the stored content of the text file corresponding to the title
def getTextByTitle(title):

    # filter that will be used to get the correct document
    tempFilter = {'_id': title}

    # filter for returning the write pieces of information
    # here, '_id=0' means that the 'id' i.e. 'title' won't be returned
    # and 'text:1' means that the text content WILL be returned
    tempReturnDict = {'_id': 0, 'text': 1}

    # getting the file content
    res = storedFiles.find_one(tempFilter, tempReturnDict)

    # returning the file content
    return res


# returns a list of titles
# takes no input
def getListOfTitles():
    
    # search with no query to get all the records
    # return _id, which is actually the unique title
    # getting all the monogodb documents in the form of  Cursor object
    # which can be iterated over
    res = storedFiles.find({}, {'_id': 1})

    # initialising an empty list, which will finally be returned
    listOfTitles = []

    # iterating through the dictionary
    for i in res:
        # appending the 'title' of the current document to the list
        listOfTitles.append(i.get('_id'))

    # returning the list of titles
    return listOfTitles
