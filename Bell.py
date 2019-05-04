import Helper as h
from Relay import relay_off, relay_on
from datetime import datetime
import time

PIN = 21


class Bell:
    def __init__(self, db):
        self.db = db
        self.checkCurrentSchedule()
        self.isDayChecked = False
        self.updateSchedule()

    def start(self):
        relay_off(PIN)
        while True:
            currentTime = datetime.now().time().replace(microsecond=0)
            checkDay(currentTime)
            if self.isHoliday:
                time.sleep(1)
                continue
            self.updateSchedule()
            timeList, statusList = h.ScheduleToLists(self.schedule)
            if self.checkForTurn(currentTime, timeList, statusList):
                self.ring(currentTime)

    def ring(self, currentTime):
        relay_on(PIN)
        print("Relay ON")
        time.sleep(5)
        relay_off(PIN)
        print("Relay OFF")
        self.syncWithdb(currentTime)

    def updateSchedule(self):
        self.schedule = h.getSchedule(self.db.currentSchedule)

    def checkForTurn(self, currentTime, timeList, statusList):
        if currentTime in timeList:
            index = timeList.index(currentTime)
            if statusList[index] == "Not Rang":
                return True

    def syncWithdb(self, time):
        time = time.strftime("%H:%M:%S")
        self.db.currentSchedule.update(
            {"time": time}, {"$set": {"status": "Completed"}})
        self.updateSchedule()

    def checkCurrentSchedule(self):
        if len(list(self.db.currentSchedule.find())) == 0:
            for item in self.db.defaultSchedule.find({}, {"_id": 0, "tag": 0}):
                self.db.currentSchedule.insert(item)
            self.db.currentSchedule.update(
                {}, {"$set": {"status": "Not Rang"}}, multi=True)
                
    def checkDay(self,currentTime):
        midNight = "00:00:00"
        midNight = datetime.strptime(midNight,"%H:%M:%S")
	    if currentTime == midNight:
			self.isDayChecked = False
	    if not self.isDayChecked:
		    day = datetime.today().weekday()
		    holidayList = h.getHolidayList(list(holidayData.find({},{"Date":1, "_id": 0})))
		    if day == 6 or datetime.now().date() in holidayList:
			    self.isHoliday = True
			    print("Holiday!!")
		    else:
			    self.isHoliday = False
		    self.isDayChecked = True

