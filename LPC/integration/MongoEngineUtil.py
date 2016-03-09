import datetime
import os
from bson import ObjectId
from django.utils.timezone import now
from mongoengine import connect
from LPC.MongoDBModel import Resource, Statistics300, Statistics86400
from LPC.integration.DateTimeUtil import DateTimeUtil
from LPCMonitor import settings

__author__ = 'teddy'

class MongoEngineUtil:
    def __init__(self):
        pass

    ceilo_collection = {}

    # config = {
    #     'host': '10.120.64.51',
    #     'port': 27017,
    #     'username': 'ceilometer',
    #     'password': 'aFK9prlV',
    #     'db_name': 'ceilometer'
    # }
    config = {
        'host': '10.120.20.1',
        'port': 30001,
        'username': 'ceilometer',
        'password': 'ZOJwyj7O',
        'db_name': 'ceilometer'
    }

    # @staticmethod
    # def testSave():
    #     if not MongoEngineUtil.ceilo_collection:
    #         MongoEngineUtil.__init_mongo_connector()
    #     entry=TestModel(test_key='aa')
    #     entry.test_value='aaaaaaa'
    #     entry.save()
    # @staticmethod
    # def testFind():
    #     if not MongoEngineUtil.ceilo_collection:
    #         MongoEngineUtil.__init_mongo_connector()
    #     modelList=TestModel.objects.all()
    #
    #     for model in modelList:
    #         print model.test_key;

    @staticmethod
    def __init_mongo_connector():
        global ceilo_collection
        ceilo_collection=connect(MongoEngineUtil.config['db_name'], host=MongoEngineUtil.config['host'],
                                 port=MongoEngineUtil.config['port'],
                                 username=MongoEngineUtil.config['username'],
                                 password=MongoEngineUtil.config['password'])
    @staticmethod
    def findResourcesByProject_id(project_id):
        if not MongoEngineUtil.ceilo_collection:
            MongoEngineUtil.__init_mongo_connector()
        modelList=Resource.objects(project_id=project_id);
        return  modelList
        # for model in modelList:
        #     print model.first_sample_timestamp;

    @staticmethod
    def findResourcesById(id):
        if not MongoEngineUtil.ceilo_collection:
            MongoEngineUtil.__init_mongo_connector()

        resource=Resource.objects(__raw__={'_id': id}).first()
        return  resource

    @staticmethod
    def findStaticsByResource_idAndCounter_name(resource_id,counter_name):
        if not MongoEngineUtil.ceilo_collection:
            MongoEngineUtil.__init_mongo_connector()

        modelList=Statistics300.objects(resource_id=resource_id,counter_name=counter_name);
        return modelList

    @staticmethod
    def findStaticsByProject_id(project_id,counter_name):
        if not MongoEngineUtil.ceilo_collection:
            MongoEngineUtil.__init_mongo_connector()

        modelList=Statistics300.objects(project_id=project_id,counter_name=counter_name);
        return modelList

    @staticmethod
    def findStaticsCountByTimestampAndCounter_name(timestamp,counter_name):
        if not MongoEngineUtil.ceilo_collection:
            MongoEngineUtil.__init_mongo_connector()

        count=Statistics86400.objects(timestamp__gte=timestamp,counter_name=counter_name).count();
        return count

    @staticmethod
    def findStaticsByTimestampAndCounter_name(timestamp,counter_name,page,rows):
        if not MongoEngineUtil.ceilo_collection:
            MongoEngineUtil.__init_mongo_connector()

        modelList=Statistics86400.objects(timestamp__gte=timestamp,counter_name=counter_name)[page:rows]\
            .order_by('-avg,-timestamp');
        return modelList

    # top perf 10
    @staticmethod
    def findLimitStaticsByTimestampAndCounter_name(bdt,edt,counter_name,limit,order,sortby):
        if not MongoEngineUtil.ceilo_collection:
            MongoEngineUtil.__init_mongo_connector()

        if order=='aesc':
            order_by=sortby
        elif order=='desc':
            order_by='-'+sortby

        print(order_by)
        modelList=Statistics86400.objects(timestamp__gte=bdt,timestamp__lte=edt,counter_name=counter_name)[:limit]\
                .order_by(order_by);
        return modelList

    @staticmethod
    def findStaticsByTimestampAndCounter_nameAndResourceId(timestamp,counter_name,resList):

        if not MongoEngineUtil.ceilo_collection:
            MongoEngineUtil.__init_mongo_connector()

            # resList=Resource.objects(__raw__={'_id': ''+resource_id+''})
            # print(resList[0].id)
            modelList=Statistics86400.objects.filter(timestamp__gte=timestamp,counter_name=counter_name,resource_id__in=resList)\
            .order_by('timestamp');
        return modelList

    @staticmethod
    def findNetworkStaticsByTimestampAndCounter_nameAndResourceId(timestamp,counter_name,resource_id):

        #"resource_id" : "instance-00002714-cfa690db-b36d-4441-aa44-821611cd441b-tap1af20fc2-3d",
        if not MongoEngineUtil.ceilo_collection:
            MongoEngineUtil.__init_mongo_connector()

            # resList=Resource.objects(__raw__={'_id': ''+resource_id+''})
            # print(resList[0].id)
            modelList=Statistics86400.objects.filter(timestamp__gte=timestamp,counter_name=counter_name,resource_id__icontains=resource_id)\
            .order_by('timestamp');
        return modelList

if __name__ == '__main__':
    mongoUtil=MongoEngineUtil()
    # mongoUtil.testSave();
    # mongoUtil.testFind()
    # project_id='bd78fccc0a1b48a8bf09797a9c5031a9'
    # resList=mongoUtil.findResourcesByProject_id(project_id);
    # for res in resList:
    #     print(res.resource_name)

    tmpDate=DateTimeUtil.dayBefore(7);
    str=DateTimeUtil.datetime_toString(tmpDate,"%Y-%m-%d")
    # str = '2016-01-11'
    beginTimestamp = datetime.datetime.strptime(str,'%Y-%m-%d')

    tmpDate=DateTimeUtil.dayBefore(1);
    str=DateTimeUtil.datetime_toString(tmpDate,"%Y-%m-%d")
    endTimestamp = datetime.datetime.strptime(str,'%Y-%m-%d')

    counter_name='cpu_util'
    # count=mongoUtil.findStaticsCountByTimestampAndCounter_name(timestamp,counter_name)
    # print(count)
    staticsList=mongoUtil.findLimitStaticsByTimestampAndCounter_name(beginTimestamp,endTimestamp,counter_name,50,'desc','avg')
    print(staticsList)
    for stat in staticsList:
        # print stat.avg
        print stat.max
        print stat.timestamp
    # staticsList=mongoUtil.findLimitStaticsByTimestampAndCounter_name(timestamp,counter_name,1)

    # resource_id='00002714-cfa690db-b36d-4441-aa44-821611cd441b'
    # res=mongoUtil.findResourcesById(resource_id);
    # resList=[resource_id]
    # staticsList=mongoUtil.findStaticsByTimestampAndCounter_nameAndResourceId(tmpDate,counter_name,resList)
    # for stat in staticsList:
    #     print stat.avg
    #     print stat.max

    # resource_id='cfa690db-b36d-4441-aa44-821611cd441b'
    # staticsList=mongoUtil.findNetworkStaticsByTimestampAndCounter_nameAndResourceId(tmpDate,counter_name,resource_id)
    # for stat in staticsList:
    #     print stat.avg
    #     print stat.max
        # print stat.resource
    # print(staticsList)
    # print(len(staticsList))
    # print(staticsList[0].id)

    # resource_id='aa109798-ba88-4e8f-87bf-29b2b228ea29'
    # counter_name='poll.volume'
    # staticsList=mongoUtil.findStaticsByResource_id(resource_id,counter_name)
    # print(staticsList[0].id)
    # mongoUtil.findStaticsByResource_id(resource_id)