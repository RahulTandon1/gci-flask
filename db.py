# importing pymongo
import pymongo

# getting connection string
f = open('connectionString', 'r')
connectionString = f.read()
f.close()


# getting the client
client = pymongo.MongoClient(connectionString)

# selecting the db
db = client.testDb

# getting the required collection
storedFiles = db.storedFiles



def storeFile(title, binaryContent):

    obj = {
        # converting binary to ascii string
        'text': binaryContent.decode('ascii'),

        # the title acts as the unique id
        '_id': title
    }
    try:
        res = storedFiles.insert_one(obj)
        return 'okay'
    except pymongo.errors.DuplicateKeyError:
        return 'duplicateKeyError'


def getTextByTitle(title):
    tempFilter = {'_id': title}
    tempReturnDict = {'_id': 0, 'text': 1}

    res = storedFiles.find_one(tempFilter, tempReturnDict)
    return res


def getListOfTitles():
    # search with no query to get all the records
    # return _id, which is actually the unique title
    res = storedFiles.find({}, {'_id': 1})

    listOfTitles = []

    for i in res:
        listOfTitles.append(i.get('_id'))

    return listOfTitles
