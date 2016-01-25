__author__ = 'zhangxg'

import MySQLdb as mdb
import json
import time


# config = {
#     'ip': '10.120.64.51',
#     'username': 'test',
#     'password': 'test',
#     'db_name': '',
#     'port':3307
# }

config = {
    'ip': '10.120.20.1',
    'username': 'root',
    'password': 'lenovo1qaz2wsx,./',
    'db_name': '',
    'port':33060
}


connection = {}


def initialize_connection():
    global connection
    try:
        connection = mdb.connect(config['ip'], config['username'], config['password'],config['db_name'], config['port'])
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
    # finally:
    #     if connection:
    #         connection.close()


def get_cpu(date_start, date_end):
    if not connection:
        initialize_connection()

    cursor = connection.cursor(mdb.cursors.DictCursor)
    sql_string = 'select * from cpu_util where timestamp between \'' + date_start + '\' and \'' + date_end + '\''
    cursor.execute(sql_string)
    rows = cursor.fetchall()

    result = []
    for row in rows:
        record = {
            'id': row['_id'],
            'tenant_id': row['tenant_id'],
            'vm_id': row['vm_id'],
            'tenant_name': row['tenant_name'],
            'count_unit': row['count_unit'],
            'timestamp': row['timestamp'].strftime('%Y-%m-%d'),
            'core': row['core'],
            'avg_core': row['avg_core'],
            'max': row['max'],
            'count': row['count'],
            'name': row['name']
        }
        result.append(record)

    return result


def get_memory(date_start, date_end):
    if not connection:
        initialize_connection()

    cursor = connection.cursor(mdb.cursors.DictCursor)
    sql_string = 'select * from memory_usage where timestamp between \'' + date_start + '\' and \'' + date_end + '\''
    cursor.execute(sql_string)
    rows = cursor.fetchall()

    result = []
    for row in rows:
        record = {
            'id': row['_id'],
            'tenant_id': row['tenant_id'],
            'vm_id': row['vm_id'],
            'tenant_name': row['tenant_name'],
            'count_unit': row['count_unit'],
            'timestamp': row['timestamp'].strftime('%Y-%m-%d'),
            'ram': row['ram'],
            'avg_mem': row['avg_mem'],
            'max': row['max'],
            'rate': row['rate'],
            'count': row['count'],
            'name': row['name']
        }
        result.append(record)

    return result


def get_disk_read(date_start, date_end):
    if not connection:
        initialize_connection()

    cursor = connection.cursor(mdb.cursors.DictCursor)
    sql_string = 'select * from disk_read where timestamp between \'' + date_start + '\' and \'' + date_end + '\''
    cursor.execute(sql_string)
    rows = cursor.fetchall()

    result = []
    for row in rows:
        record = {
            'id': row['_id'],
            'resource_id': row['resource_id'],
            'display_name': row['display_name'],
            'vm_id': row['vm_id'],
            'vm_name': row['vm_name'],
            'tenant_id': row['tenant_id'],
            'tenant_name': row['tenant_name'],
            'timestamp': row['timestamp'].strftime('%Y-%m-%d'),
            'count_unit': row['count_unit'],
            'avg_read': row['avg_read'],
            'max_read': row['max_read'],
            'count': row['count']
        }
        result.append(record)

    return result


def get_disk_write(date_start, date_end):
    if not connection:
        initialize_connection()

    cursor = connection.cursor(mdb.cursors.DictCursor)
    sql_string = 'select * from disk_write where timestamp between \'' + date_start + '\' and \'' + date_end + '\''
    cursor.execute(sql_string)
    rows = cursor.fetchall()

    result = []
    for row in rows:
        record = {
            'id': row['_id'],
            'resource_id': row['resource_id'],
            'display_name': row['display_name'],
            'vm_id': row['vm_id'],
            'vm_name': row['vm_name'],
            'tenant_id': row['tenant_id'],
            'tenant_name': row['tenant_name'],
            'timestamp': row['timestamp'].strftime('%Y-%m-%d'),
            'count_unit': row['count_unit'],
            'avg_write': row['avg_write'],
            'max_write': row['max_write'],
            'count': row['count']
        }
        result.append(record)

    return result


def get_network_in(date_start, date_end):
    if not connection:
        initialize_connection()

    cursor = connection.cursor(mdb.cursors.DictCursor)
    sql_string = 'select * from network_in where timestamp between \'' + date_start + '\' and \'' + date_end + '\''
    cursor.execute(sql_string)
    rows = cursor.fetchall()

    result = []
    for row in rows:
        record = {
            'id': row['_id'],
            'resource_id': row['resource_id'],
            'tap_name': row['tap_name'],
            'vm_id': row['vm_id'],
            'vm_name': row['vm_name'],
            'tenant_id': row['tenant_id'],
            'tenant_name': row['tenant_name'],
            'timestamp': row['timestamp'].strftime('%Y-%m-%d'),
            'count_unit': row['count_unit'],
            'avg_in': row['avg_in'],
            'max_in': row['max_in'],
            'count': row['count']
        }
        result.append(record)

    return result


def get_network_out(date_start, date_end):
    if not connection:
        initialize_connection()

    cursor = connection.cursor(mdb.cursors.DictCursor)
    sql_string = 'select * from network_out where timestamp between \'' + date_start + '\' and \'' + date_end + '\''
    cursor.execute(sql_string)
    rows = cursor.fetchall()

    result = []
    for row in rows:
        record = {
            'id': row['_id'],
            'resource_id': row['resource_id'],
            'tap_name': row['tap_name'],
            'vm_id': row['vm_id'],
            'vm_name': row['vm_name'],
            'tenant_id': row['tenant_id'],
            'tenant_name': row['tenant_name'],
            'timestamp': row['timestamp'].strftime('%Y-%m-%d'),
            'count_unit': row['count_unit'],
            'avg_out': row['avg_out'],
            'max_out': row['max_out'],
            'count': row['count']
        }
        result.append(record)

    return result


def get_tenants_statistics(start_date, end_date):

    sql_cpu = 'select tenant_id, tenant_name, sum(core) as allocated, count_unit, (avg_core)/count(vm_id) as avg, max(max) as max, count(vm_id) as vm_num ' \
              'from cpu_util where timestamp between \'' + start_date + '\' and \'' + end_date + '\' group by tenant_id'

    sql_memory = 'select tenant_id, tenant_name, sum(ram) as allocated, count_unit, sum(avg_mem)/sum(ram) as avg, max(max) as max, count(vm_id) as vm_num' \
                 ' from memory_usage where timestamp between \'' + start_date + '\' and \'' + end_date + '\' group by tenant_id'

    sql_disk_read = 'select tenant_id, tenant_name, count_unit, sum(avg_read)/count(vm_id) as avg, max(max_read) max, count(vm_id) as vm_num ' \
                    'from disk_read where timestamp between \'' + start_date + '\' and \'' + end_date + '\' group by tenant_id'

    sql_disk_write = 'select tenant_id, tenant_name, count_unit, sum(avg_write)/count(vm_id) as avg, max(max_write) as max, count(vm_id) as vm_num ' \
                     'from disk_write where timestamp between \'' + start_date + '\' and \'' + end_date + '\' group by tenant_id'

    sql_network_in = 'select tenant_id, tenant_name, count_unit, sum(avg_in)/count(vm_id) as avg, max(max_in) as max, count(vm_id) as vm_num ' \
                     'from network_in where timestamp between \'' + start_date + '\' and \'' + end_date + '\' group by tenant_id'

    sql_network_out = 'select tenant_id, tenant_name, count_unit, sum(avg_out)/count(vm_id) as avg, max(max_out) as max, count(vm_id) as vm_num ' \
                      'from network_out where timestamp between \'' + start_date + '\' and \'' + end_date + '\' group by tenant_id'

    if not connection:
        initialize_connection()

    cursor = connection.cursor(mdb.cursors.DictCursor)

    cursor.execute(sql_cpu)

    print(sql_cpu)

    cpu_result = cursor.fetchall()

    cursor.execute(sql_memory)
    memory_result = cursor.fetchall()

    cursor.execute(sql_disk_read)
    disk_read_result = cursor.fetchall()

    cursor.execute(sql_disk_write)
    disk_write_result = cursor.fetchall()

    cursor.execute(sql_network_in)
    network_in_result = cursor.fetchall()

    cursor.execute(sql_network_out)
    network_out_result = cursor.fetchall()

    stats = {}
    for row in cpu_result:
        key = row['tenant_id']
        if not stats.get(key):
            record = __create_tenant_stat_record()
            record['tenant_id'] = key
            record['tenant_name'] = row['tenant_name']
            stats.__setitem__(key, record)

        record = stats.__getitem__(key)
        record['cpu']['core'] = int(row['allocated'])
        record['cpu']['unit'] = row['count_unit']
        record['cpu']['avg'] = round(row['avg'], 2)
        record['cpu']['max'] = round(row['max'], 2)
        record['cpu']['vm_num'] = int(row['vm_num'])

    for row in memory_result:
        key = row['tenant_id']
        if not stats.get(key):
            record = __create_tenant_stat_record()
            record['tenant_id'] = key
            record['tenant_name'] = row['tenant_name']
            stats.__setitem__(key, record)

        record = stats.__getitem__(key)
        record['memory']['ram'] = int(row['allocated'])
        record['memory']['unit'] = row['count_unit']
        record['memory']['avg'] = round(row['avg'], 2)
        record['memory']['max'] = round(row['max'], 2)
        record['memory']['vm_num'] = int(row['vm_num'])

    for row in disk_read_result:
        key = row['tenant_id']
        if not stats.get(key):
            record = __create_tenant_stat_record()
            record['tenant_id'] = key
            record['tenant_name'] = row['tenant_name']
            stats.__setitem__(key, record)

        record = stats.__getitem__(key)
        record['disk_read']['unit'] = row['count_unit']
        record['disk_read']['avg'] = round(row['avg']/1024.0, 2)
        record['disk_read']['max'] = round(row['max']/1024.0, 2)
        record['disk_read']['vm_num'] = int(row['vm_num'])

    for row in disk_write_result:
        key = row['tenant_id']
        if not stats.get(key):
            record = __create_tenant_stat_record()
            record['tenant_id'] = key
            record['tenant_name'] = row['tenant_name']
            stats.__setitem__(key, record)

        record = stats.__getitem__(key)
        record['disk_write']['unit'] = row['count_unit']
        record['disk_write']['avg'] = round(row['avg']/1024.0, 2)
        record['disk_write']['max'] = round(row['max']/1024.0, 2)
        record['disk_write']['vm_num'] = int(row['vm_num'])

    for row in network_in_result:
        key = row['tenant_id']
        if not stats.get(key):
            record = __create_tenant_stat_record()
            record['tenant_id'] = key
            record['tenant_name'] = row['tenant_name']
            stats.__setitem__(key, record)

        record = stats.__getitem__(key)
        record['network_in']['unit'] = row['count_unit']
        record['network_in']['avg'] = round(row['avg']/1024.0, 2)
        record['network_in']['max'] = round(row['max']/1024.0, 2)
        record['network_in']['vm_num'] = int(row['vm_num'])

    for row in network_out_result:
        key = row['tenant_id']
        if not stats.get(key):
            record = __create_tenant_stat_record()
            record['tenant_id'] = key
            record['tenant_name'] = row['tenant_name']
            stats.__setitem__(key, record)

        record = stats.__getitem__(key)
        record['network_out']['unit'] = row['count_unit']
        record['network_out']['avg'] = round(row['avg']/1024.0, 2)
        record['network_out']['max'] = round(row['max']/1024.0, 2)
        record['network_out']['vm_num'] = int(row['vm_num'])

    record_list = []
    for key in stats.keys():
        record_list.append(stats[key])

    return record_list

    # print(json.dumps(record_list))


def get_tenant_vm_statistic():

    sql_search = 'select timestamp, count(tenant_id) as tenant_count, ' \
                 'sum(vm_all_count) as total, sum(vm_current_count) as current, ' \
                 'sum(vm_active_count) as active from tenant group by timestamp order by timestamp asc'

    if not connection:
        initialize_connection()

    cursor = connection.cursor(mdb.cursors.DictCursor)

    cursor.execute(sql_search)
    results = cursor.fetchall()
    converted_list = []
    for row in results:
        stat = {
            'timestamp': row['timestamp'].strftime('%Y-%m-%d'),
            'tenant_count': str(row['tenant_count']),
            'vm_total': str(row['total']),
            'vm_current': str(row['current']),
            'vm_active': str(row['active'])
        }
        converted_list.append(stat)

    # cursor.execute(sql_vm_search)
    # vm_result = cursor.fetchall()
    #
    # index = 0
    # converted_list = []
    # for row in tenant_result:
    #     stat = {
    #         'timestamp': key,
    #         'tenant_count': tenant_vm_stats[key]['tenant_count'],
    #         'vm_total': tenant_vm_stats[key]['total_vm'],
    #         'vm_current': tenant_vm_stats[key]['current_vm'],
    #         'vm_active':tenant_vm_stats[key]['active_vm']
    #     }
    #
    #
    # tenant_vm_stats = {}
    # for row in tenant_result:
    #     tenant_vm_stats.__setitem__(row['timestamp'].strftime('%Y-%m-%d'), {
    #         'tenant_count': str(row['tenant_count'])
    #     })
    #
    # for row in vm_result:
    #     s = tenant_vm_stats.get(row['timestamp'].strftime('%Y-%m-%d'))
    #     s.__setitem__('total_vm', str(row['total']))
    #     s.__setitem__('current_vm', str(row['current']))
    #     s.__setitem__('active_vm', str(row['active']))
    #
    # converted_list = []
    # for key in tenant_vm_stats:
    #     stat = {
    #         'timestamp': key,
    #         'tenant_count': tenant_vm_stats[key]['tenant_count'],
    #         'vm_total': tenant_vm_stats[key]['total_vm'],
    #         'vm_current': tenant_vm_stats[key]['current_vm'],
    #         'vm_active':tenant_vm_stats[key]['active_vm']
    #     }
    #     converted_list.append(stat)

    return converted_list

def findAllHostByZone(zone):
    return ''
def findAllZones():
    return ''

# create by zmz 2016-1-18
def findVmsByVnameHostnameForCount(vname,hostname):
    print 'findvm:'+vname+hostname
    # print(str(vname).__len__())
    sql_search = 'SELECT  count(*) count from ' \
                     '(SELECT ni.id FROM  	nova.instances ni,  	keystone.project kp,  	nova.instance_types nit  ' \
                     'WHERE  	ni.project_id = kp.id  AND ni.deleted = 0  AND ni.instance_type_id = nit.id  ' \

    # sql_search='select * from nova.instances ni'
    if str(vname).__len__()!=0:
        sql_search = sql_search+' and  ni.hostname like "%'+vname+'%" '
    if str(hostname).__len__()!=0:
        sql_search = sql_search+' and  ni.host ="'+hostname+'"'

    sql_search=sql_search+' GROUP BY  	ni.user_id,  	project_id ' \
                     'order by ni.updated_at desc) tt'

    print(sql_search);

    if not connection:
        initialize_connection()

    cursor = connection.cursor(mdb.cursors.DictCursor)

    cursor.execute(sql_search)
    results = cursor.fetchall()
    return results[0]['count']

# create by zmz 2016-1-18
def findVmsByVnameHostname(vname,hostname,offset,rows):
    print 'findvm:'+vname+hostname
    # print(str(vname).__len__())
    sql_search = 'SELECT  ni.uuid,  ni.hostname,  ni.display_name,  ni.display_description, ni.user_id, ' \
                     'ni.availability_zone,  ni.`host`,  ni.vm_state,  ni.project_id,  kp.`name` project_name,  nit.root_gb,  nit.memory_mb,  nit.vcpus  ' \
                     'FROM  	nova.instances ni,  	keystone.project kp,  	nova.instance_types nit  ' \
                     'WHERE  	ni.project_id = kp.id  AND ni.deleted = 0  AND ni.instance_type_id = nit.id  ' \

    # sql_search='select * from nova.instances ni'
    if str(vname).__len__()!=0:
        sql_search = sql_search+' and  ni.hostname like "%'+vname+'%" '
    if str(hostname).__len__()!=0:
        sql_search = sql_search+' and  ni.host ="'+hostname+'"'

    sql_search=sql_search+' GROUP BY  	ni.user_id,  	project_id ' \
                     'order by ni.updated_at desc'+' limit '+str(offset)+','+str(rows)

    print(sql_search);

    if not connection:
        initialize_connection()

    cursor = connection.cursor(mdb.cursors.DictCursor)

    cursor.execute(sql_search)
    results = cursor.fetchall()
    converted_list = []
    for row in results:
        stat = {
            'uuid': str(row['uuid']),
            'vname': str(row['hostname']),
            'project_id': str(row['project_id']),
            'project_name': str(row['project_name']),
            'user_id': str(row['user_id']),
            'vcpus': str(row['vcpus']),
            'memory_mb': str(row['memory_mb']),
            'root_gb': str(row['root_gb']),
            'host': str(row['host']),
            'vm_state': str(row['vm_state']),
        }
        converted_list.append(stat)
    return converted_list

def __create_tenant_stat_record():
    return {
        'tenant_id': '',
        'tenant_name': '',
        'cpu': {
            'core': 0,
            'unit': '',
            'avg': 0,
            'max': 0,
            'vm_num': 0
        },
        'memory': {
            'ram': 0,
            'unit': '',
            'avg': 0,
            'max': 0,
            'vm_num': 0
        },
        'disk_read': {
            'unit': '',
            'avg': 0,
            'max': 0,
            'vm_num': 0
        },
        'disk_write': {
            'unit': '',
            'avg': 0,
            'max': 0,
            'vm_num': 0
        },
        'network_in': {
            'unit': '',
            'avg': 0,
            'max': 0,
            'vm_num': 0
        },
        'network_out': {
            'unit': '',
            'avg': 0,
            'max': 0,
            'vm_num': 0
        }
    }



if __name__ == '__main__':

    # converted_list=get_tenant_vm_statistic();
    # result={}
    # result["total"]=converted_list.__len__();
    # result["rows"]=converted_list;
    #
    # print(json.dumps(result))

    #test findVmsByVnameHostname
    # result=findVmsByVnameHostname('11','node-1.domain.tld');
    count=findVmsByVnameHostnameForCount('','');
    print('aaaaaaaaaaaaaaa'+str(count))
    result=findVmsByVnameHostname('','',0,2);

    for vm in result:
        print(vm)

# get_tenants_statistics('2015-06-16')

# disk_r = get_disk_read('2015-06-08', '2015-06-20')
# print(disk_r.__len__())
# disk_w = get_disk_write('2015-06-08', '2015-06-20')
# print(disk_w.__len__())
#
# net_in = get_network_in('2015-06-08', '2015-06-20')
# print(net_in.__len__())
# net_out = get_network_out('2015-06-08', '2015-06-20')
# print(net_out.__len__())


# r = get_memory('2015-06-08', '2015-06-20')
# print(json.dumps(r))
# i = 0
# for row in rows:
#     i += 1
#     if i < 13:
#         print(row)
#         print(row['_id'], row['tenant_name'])