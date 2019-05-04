import pymongo

class DataBase:

    def __init__(self, dbname, username, password):
        self.dbname = dbname
        self.username = username
        self.password = password
        self._initializeDB()
        self._initializeCollections()

    def _initializeDB(self):
        connection = pymongo.MongoClient()
        self.db = connection[self.dbname]
        self.db.authenticate(self.username, self.password)

    def _initializeCollections(self):
        self.defaultSchedule = self.db.defaultSchedule
        self.specialRings = self.db.specialRings
        self.currentSchedule = self.db.currentSchedule
        self.logs = self.db.logs
        self.holidayData = self.db.holidayData
