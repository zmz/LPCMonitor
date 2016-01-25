import datetime
import  time
__author__ = 'teddy'

# coding=utf-8

class DateTimeUtil:

    def __init__(self):
        pass

    #date to string
    @staticmethod
    def datetime_toString(dt,formatStr):
        # return dt.strftime("%Y-%m-%d-%H")
        return dt.strftime(formatStr)




    #string to date
    @staticmethod
    def string_toDatetime(string,formatStr):
        # return datetime.strptime(string, "%Y-%m-%d-%H")
        return time.strptime(string, formatStr)




    #string to datetime
    # @staticmethod
    # def string_toTimestamp(strTime):
    #     return datetime.time.mktime(string_toDatetime(strTime).timetuple())


    #datetime to string
    @staticmethod
    def timestamp_toString(stamp):
        return datetime.time.strftime("%Y-%m-%d-%H", datetime.time.localtime(stamp))



    @staticmethod
    def datetime_toTimestamp(dateTim):
        return datetime.time.mktime(dateTim.timetuple())

    # day defore
    @staticmethod
    def dayBefore(dateNum):

        start = datetime.datetime.now()
        i = dateNum
        end = start - datetime.timedelta(i)
        return end;

if __name__ == '__main__':
     #test dateutil
    tmpDate=DateTimeUtil.dayBefore(7);
    str=DateTimeUtil.datetime_toString(tmpDate,"%Y-%m-%d")
    tmpStr=DateTimeUtil.string_toDatetime(str,'%Y-%m-%d')
    print(tmpStr)