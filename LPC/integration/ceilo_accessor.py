__author__ = 'zhangxg'

import pymongo
from datetime import datetime as dt
import json
from dateutil import tz
import time


class CeiloAccessor:
    COUNTER_NAME_CPU = 'cpu_util'
    COUNTER_NAME_MEMORY = 'memory.usage'
    COUNTER_NAME_VOLUME_READ = 'volume.read.bytes.rate'
    COUNTER_NAME_VOLUME_WRITE = 'volume.write.bytes.rate'
    COUNTER_NAME_DISK_READ = 'disk.read.requests.rate'
    COUNTER_NAME_DISK_WRITE = 'disk.write.requests.rate'
    COUNTER_NAME_NETWORK_IN = 'network.incoming.bytes.rate'
    COUNTER_NAME_NETWORK_OUT = 'network.outgoing.bytes.rate'

    config = {
        'ip': '10.120.20.1',
        'port': 30001,
        'username': 'ceilometer',
        'password': 'ZOJwyj7O',
        'db_name': 'ceilometer'
    }

    fields = {
        'resource_id': 1,
        'counter_name': 1,
        'counter_unit': 1,
        'counter_volume': 1,
        'timestamp': 1,
        'resource_metadata': 1
    }

    ceilo_collection = {}

    def __init__(self):
        pass

    @staticmethod
    def get_resource_ts(resource_id, time_start, time_end, counter_name, resource_id_operator):
        if not CeiloAccessor.ceilo_collection:
            CeiloAccessor.__init_mongo_connector()
        query = CeiloAccessor.__create_query_string(resource_id, time_start, time_end, counter_name,
                                                    resource_id_operator)
        cur = ceilo_collection.find(query, CeiloAccessor.fields)
        return CeiloAccessor.__populate_result(cur)

    @staticmethod
    def __init_mongo_connector():
        global ceilo_collection
        mongo_client = pymongo.MongoClient(CeiloAccessor.config['ip'], CeiloAccessor.config['port'])
        db = mongo_client[CeiloAccessor.config['db_name']]
        if not db.authenticate(CeiloAccessor.config['username'], CeiloAccessor.config['password']):
            raise Exception("Connect to mongodb error,please check user name and password!")
        ceilo_collection = db['meter']

    @staticmethod
    def __populate_result(cursor):
        points = {}
        for c in cursor:
            if c['resource_id'] in points:
                points.__getitem__(c['resource_id']).append({
                    'timestamp': c['timestamp'].replace(tzinfo=tz.tzutc()).astimezone(tz.tzlocal()).strftime(
                        '%Y-%m-%d %H:%M:%S'),
                    'volume': c['counter_volume'],
                    'unit': c['counter_unit']
                })
            else:
                points.__setitem__(c['resource_id'], [])
        return points

    @staticmethod
    def __create_query_string(resource_id, time_start, time_end, counter_name, resource_id_operator):
        date_range = CeiloAccessor.__local_to_utc(time_start, time_end)
        query = {'$and': [
            {'timestamp': {'$gt': date_range[0]}},
            {'timestamp': {'$lt': date_range[1]}},
            {'counter_name': counter_name},
        ]}

        if resource_id_operator == 'equal':
            query["$and"].append({"resource_id": resource_id})
        elif resource_id_operator == 'like':
            query["$and"].append({"resource_id": {'$regex': resource_id}})
        return query

    @staticmethod
    def __local_to_utc(date_start_str, date_end_str):
        date_start_converted = dt.strptime(date_start_str, '%Y-%m-%d %H:%M:%S').replace(tzinfo=tz.tzlocal()).astimezone(
            tz.tzutc())
        date_end_converted = dt.strptime(date_end_str, '%Y-%m-%d %H:%M:%S').replace(tzinfo=tz.tzlocal()).astimezone(
            tz.tzutc())
        return date_start_converted, date_end_converted

    @staticmethod
    def batch_get_resource_ts(resource_ids, time_start, time_end, counter_names):
        date_range = CeiloAccessor.__local_to_utc(time_start, time_end)
        query = {'$and': [
            {'timestamp': {'$gt': date_range[0]}},
            {'timestamp': {'$lt': date_range[1]}},
            {'counter_name': {'$in': counter_names}},
            {'resource_id': {'$in': resource_ids}}
        ]}

        print(query)

        if not CeiloAccessor.ceilo_collection:
            CeiloAccessor.__init_mongo_connector()
        cur = ceilo_collection.find(query, CeiloAccessor.fields)
        return CeiloAccessor.__batch_populate_result(cur)

    @staticmethod
    def __batch_populate_result(cursor):
        points = {}
        for c in cursor:
            resource_id = c['resource_id']
            if resource_id not in points:
                points.__setitem__(resource_id, {})

            counter_name = c['counter_name']

            if counter_name not in points.__getitem__(resource_id).keys():
                points.__getitem__(resource_id).__setitem__(counter_name, [])

            points.__getitem__(resource_id).__getitem__(counter_name).append({
                'timestamp': c['timestamp'].replace(tzinfo=tz.tzutc()).astimezone(tz.tzlocal()).strftime(
                    '%Y-%m-%d %H:%M:%S'),
                'volume': c['counter_volume'],
                'unit': c['counter_unit'],
                'allocated': CeiloAccessor.__get_allocated(counter_name, c)
            })
        return points

    @staticmethod
    def __get_allocated(counter_name, c):
        if counter_name == CeiloAccessor.COUNTER_NAME_CPU:
            return c['resource_metadata']['vcpus']
        elif counter_name == CeiloAccessor.COUNTER_NAME_MEMORY:
            return c['resource_metadata']['memory_mb']
        else:
            return 0


if __name__ == '__main__':
    accessor = CeiloAccessor()

    t0 = '2015-07-14 9:0:0'
    t1 = '2015-07-14 10:0:0'
    ids = [
        'd80c228d-cd52-4979-b436-bd7974027c7f',
        'a6c2c658-24b7-47db-953d-9e5fbf0c2b68',
        # 'ab0806bb-8ede-4079-8ee0-9df07d984085',
        # 'd82e76ad-58d8-44f8-89d3-00b07be634b5',
        # '364efa14-eb8b-4320-afe9-93e4457c7eed',
        # 'f820ff7f-3080-4f5f-bd29-9564f6182b86',
        # '81ce6c14-ff0b-4882-930d-bef4b1f0d308',
        # '8de6ef06-4f02-40e4-8df9-baf4711cc198',
        # 'b236baaf-d318-47f1-841f-3f1a34ab5341',
        # '6879a932-5f5e-41f0-a3e8-88da08e8e2b4',
        'instance-00001391-860ce103-4b5e-417b-92c8-81d498d38c70-tap5354d801-e5',
        'instance-00001337-f6d6f9b7-e184-4756-b905-8857e41c9e78-tapb2bab17f-bb',

    ]

    counter_names = ['cpu_util', 'memory.usage']
    # counter_names = ['network.incoming.bytes.rate', 'network.outgoing.bytes.rate']
    # counter_names = ['volume.read.bytes.rate', 'volume.write.bytes.rate']

    points = accessor.batch_get_resource_ts(ids, t0, t1, counter_names)
    print(json.dumps(points, indent=2))
    # index = 0
    # t = time.time()
    # points = accessor.get_resource_ts('instance-00001391-860ce103-4b5e-417b-92c8-81d498d38c70-tap5354d801-e5', t0, t1, 'network.incoming.bytes.rate', 'equal')
    # print('Equal : ' + str(time.time() - t) + ': count_num: ' + str(index))
    # for r_id in ids:
    #     points = accessor.get_resource_ts(r_id, t0, t1, 'cpu_util', 'equal')

    # for r_id in ids:
    #     points = accessor.get_resource_ts(r_id, t0, t1, 'memory_usage', 'equal')
    #     index += points.keys().__len__()
    # print('single processing: ' + str(time.time() - t) + ': count_num: ' + str(index))

    # t = time.time()
    # points = accessor.get_resource_ts('instance-00001391-860ce103-4b5e-417b-92c8-81d498d38c70', t0, t1, 'network.incoming.bytes.rate', 'like')
    # print('lIKE : ' + str(time.time() - t) + ': count_num: ' + str(index))

    # t = time.time()
    # points = accessor.batch_get_resource_ts(ids, t0, t1, ['cpu_util', 'memory_usage'])
    # print('batch processing: ' + str(time.time() - t) + ': count_num: ' + str(points.keys().__len__()))

    # print(json.dumps(accessor.get_resource_ts(, t0, t1, 'network.incoming.bytes.rate', 'like')))
    # print(json.dumps(accessor.get_resource_ts(ids, t0, t1, 'cpu_util', 'equal')))
