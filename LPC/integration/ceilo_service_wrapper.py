__author__ = 'zhangxg'

from ceilo_accessor import CeiloAccessor
from redis_accessor import *
import json


class MongoServiceWrapper:
    def __init__(self):
        self.ceilo_accessor = CeiloAccessor()
        self.redis_accessor = RedisAccessor()

    def get_all_matrix_ts(self, vm_ids, counter_name_list, time_start, time_end):
        vms = self.redis_accessor.get_item(RedisKeyConstants.API_RAW_VMS)['servers']
        all_vms = {}
        for vm in vms:
            all_vms[vm['id']] = vm

        all_ts_matrix = {}
        counter_names = []
        t = time.time()
        retrieve_cpu_or_memory = False
        if 'CPU' in counter_name_list:
            retrieve_cpu_or_memory = True
            counter_names.append(CeiloAccessor.COUNTER_NAME_CPU)
        if 'Memory' in counter_name_list:
            retrieve_cpu_or_memory = True
            counter_names.append(CeiloAccessor.COUNTER_NAME_MEMORY)

        if "Disk" in counter_name_list:
            retrieve_cpu_or_memory = True
            counter_names.append(CeiloAccessor.COUNTER_NAME_DISK_READ)
            counter_names.append(CeiloAccessor.COUNTER_NAME_DISK_WRITE)

        if retrieve_cpu_or_memory:
            all_ts_matrix = self.ceilo_accessor.batch_get_resource_ts(vm_ids, time_start, time_end, counter_names)
        print('cpu, memory and disk: ' + str(time.time() - t))

        if 'Volume' in counter_name_list:
            self.__get_volume_ts_series(all_ts_matrix, vm_ids, time_start, time_end)

        if 'Network' in counter_name_list:
            self.__get_network_ts_series(all_ts_matrix, vm_ids, time_start, time_end)

        return all_ts_matrix

    def __get_volume_ts_series(self, all_ts_matrix, vm_ids, time_start, time_end):
        vm_volumes = self.redis_accessor.get_item(RedisKeyConstants.API_PROCESSED_VM_VOLUMES)
        volume_ids = []
        volume_vm_index = {}
        for vm_id in vm_ids:
            if vm_volumes.get(vm_id):
                volumes = vm_volumes.get(vm_id)['volumes']
                if volumes:
                    for volume in volumes:
                        volume_ids.append(volume['id'])
                        volume_vm_index.__setitem__(volume['id'], vm_id)
            else:
                print("vm: " + vm_id + " has no volume.")

        volume_points = self.ceilo_accessor.batch_get_resource_ts(volume_ids, time_start, time_end,
                                                                  [CeiloAccessor.COUNTER_NAME_VOLUME_READ,
                                                                   CeiloAccessor.COUNTER_NAME_VOLUME_WRITE])
        if volume_points:
            for vm_id in vm_ids:
                if not all_ts_matrix.get(vm_id):
                    all_ts_matrix.__setitem__(vm_id, {})
                all_ts_matrix.get(vm_id).__setitem__(CeiloAccessor.COUNTER_NAME_VOLUME_READ, {})
                all_ts_matrix.get(vm_id).__setitem__(CeiloAccessor.COUNTER_NAME_VOLUME_WRITE, {})

        for r_id in volume_points.keys():
            disk_read_points = volume_points.get(r_id).get(CeiloAccessor.COUNTER_NAME_VOLUME_READ)
            disk_write_points = volume_points.get(r_id).get(CeiloAccessor.COUNTER_NAME_VOLUME_WRITE)

            if disk_read_points:
                all_ts_matrix.get(volume_vm_index.get(r_id))[CeiloAccessor.COUNTER_NAME_VOLUME_READ].__setitem__(r_id,
                                                                                                               disk_read_points)

            if disk_write_points:
                all_ts_matrix.get(volume_vm_index.get(r_id))[CeiloAccessor.COUNTER_NAME_VOLUME_WRITE].__setitem__(
                    r_id, disk_write_points)

    def __get_network_ts_series(self, all_ts_matrix, vm_ids, time_start, time_end):
        vm_taps = self.redis_accessor.get_item(RedisKeyConstants.API_PROCESSED_VM_PORTS)
        tap_ids = []
        tap_vm_index = {}
        for vm_id in vm_ids:
            taps = vm_taps.get(vm_id)
            if taps:
                for tap in taps:
                    tap_ids.append(tap)
                    tap_vm_index.__setitem__(tap, vm_id)

        t = time.time()
        net_work_points = self.ceilo_accessor.batch_get_resource_ts(tap_ids, time_start, time_end,
                                                                    [CeiloAccessor.COUNTER_NAME_NETWORK_IN,
                                                                     CeiloAccessor.COUNTER_NAME_NETWORK_OUT])
        print('network-search:' + str(time.time() - t))

        t = time.time()
        if net_work_points:
            for vm_id in vm_ids:
                if vm_id not in all_ts_matrix:
                    all_ts_matrix.__setitem__(vm_id, {})
                all_ts_matrix.get(vm_id).__setitem__(CeiloAccessor.COUNTER_NAME_NETWORK_IN, {})
                all_ts_matrix.get(vm_id).__setitem__(CeiloAccessor.COUNTER_NAME_NETWORK_OUT, {})

        for resource_id in net_work_points.keys():
            network_in_points = net_work_points.get(resource_id).get(CeiloAccessor.COUNTER_NAME_NETWORK_IN)
            network_out_points = net_work_points.get(resource_id).get(CeiloAccessor.COUNTER_NAME_NETWORK_OUT)

            if network_in_points:
                all_ts_matrix.get(tap_vm_index.get(resource_id))[CeiloAccessor.COUNTER_NAME_NETWORK_IN].__setitem__(
                    resource_id, network_in_points)

            if network_out_points:
                all_ts_matrix.get(tap_vm_index.get(resource_id))[CeiloAccessor.COUNTER_NAME_NETWORK_OUT].__setitem__(
                    resource_id, network_out_points)
        print('network-post-search:' + str(time.time() - t))

    def get_vm_trend(self, time_range, counter_names, vm_ids):
        """ get the time series points for assigned vm_ids, counter_names between the time range"""
        time_range_boundary = time_range.split('-')
        time_start = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(time_range_boundary[0][:10])))
        time_end = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(time_range_boundary[1][:10])))

        l = vm_ids.split('|')
        vm_list = l[:l.__len__() - 1]

        c = counter_names.split('|')
        counter_name_list = c[:c.__len__() - 1]

        all_points = self.get_all_matrix_ts(vm_list, counter_name_list, time_start, time_end)

        import pdb
        pdb.set_trace()
        print(json.dumps(all_points, indent=2))

        return all_points

        # return self.get_all_matrix_ts(vm_list, counter_name_list, time_start, time_end)


if __name__ == '__main__':
    tr = '1436832000000-1436918400000'
    cn = 'CPU|Memory|Volume|Network|'
    # cn = 'Network|'
    # ids = '6519af65-91d4-4bde-ac2b-49ab3d8d080a|d8ee29ff-ae20-4495-bce9-667dfdf793b8|d7d32866-c409-48f2-ad49-ec8ad849c7fb|5bf3065e-aaf0-4d95-b1d1-d126b5998bf2|79dea409-72da-4363-ae2a-d03b7236dc19|cd94ddde-1cc5-4396-9933-f2691585d90f|f3022e9b-d133-4961-9144-b5a1b0434b03|b5c4f9a4-c7cc-4912-a923-4a5b418429ee|e3843192-dc94-4f2c-9c63-c0a59ad591da|a89a4ef5-fce0-4601-9106-654a4b13b50e|d4d0e31b-e882-408e-bf02-a2b40859ed77|fa467a50-6ca1-40a0-9226-f6a83bdbc2cd|cf15bc2d-7efc-4a3e-8b66-b9407c72d5b2|dc3d7375-160c-48a2-b2d3-d1f787ef7989|28878564-43a5-462b-8ec4-ed22aff18a6e|8da853b2-4a28-4947-9373-7251f8bb6954|2414b6a1-a8d5-4f39-b64a-ce7cce79bc84|568374e8-3a09-421d-addd-758cd5dc1a3f|831294c6-923d-4ec6-8a5a-b2bf17500d64|71fd6b31-ed3d-41d5-8897-5b20c83601c3|011cf21f-573d-4996-88ed-f58a8e64f47c|bb99cdb5-7653-41b4-bd8c-3c35e4b5db0e|bb57a033-2a05-4022-820b-06bc60b234b1|d4e16ebd-adac-404d-a159-4fca03ae7386|ea5fed84-5d1f-4246-ab5f-be24e3ed1c39|87bb37e0-c0af-4703-9eaa-48236d24e258|cedece60-c57e-45e4-b277-c81120e9962b|483fb477-93c4-4ef4-b645-0e69049444fd|2d50709e-8f38-4a3b-9382-7859dda237b3|9b0d19e4-06da-420f-bde3-5cf670599bb4|ab0806bb-8ede-4079-8ee0-9df07d984085|3150fe5c-ec49-4e3a-965a-b2fd611c0368|29d2e304-5260-47e5-bdd8-de4435f78430|78cb8f90-253f-4a8a-8ac9-e82a76efacb8|f68ca035-9dd8-4da4-a9cb-be7c073a6159|e3aad97f-8f87-4e6f-8a14-a556234d9acf|3feb3eb1-5a7e-479e-97bb-ebf125180465|807bdeb7-f2a8-4ebc-8a79-2109f267774e|fe6b57b7-27d5-4f86-b446-e237810ba220|bf2693bc-36fc-4462-acef-e9d9658c4664|e7a6f47b-2257-4a02-b130-a8bfd43f415f|86a6bc23-f008-48d6-8841-3dd8e34e1dad|343e95d1-64f1-4d9a-9b3e-0b6658a188ac|168b3e29-b1c1-46c4-909b-1dffc85db4dc|1b78c881-5c99-4ede-b2a9-95dbc754ff57|ddfcdaa6-315d-4cea-90d2-d4f91f7fbe55|dca1f948-6cbc-4be0-86b2-1278fa7ad04c|c07b238b-314b-4b3e-9ccc-be8a5af9f73c|81ce6c14-ff0b-4882-930d-bef4b1f0d308|11a609d9-b4ff-49ef-8e1f-8bd0ec0c1fcb|66dcf54a-d9ef-4da5-a3b0-193f271b77d7|'
    ids = '6a5e1bda-1382-4ee9-8e08-51df5cfc876c|74c4c5cd-a813-44e7-a06d-f5e48db8d63c|64d2bd2a-ebae-417c-a52e-49ff8c383333|79b83e10-9959-48ba-af63-a7ec4ab56ebe|18bc8a17-198c-47c0-b91a-70687c0c32b0|'

    service = MongoServiceWrapper()
    print(json.dump(service.get_vm_trend(tr, cn, ids), open('/home/zhangxg/work/temp/tenant1_all_data.json', 'w+'), indent=2))
    # service = MongoServiceWrapper()
    # print(json.dumps(service.get_all_matrix_ts(['ab0806bb-8ede-4079-8ee0-9df07d984085','040232cb-aeb8-44a1-894c-cc923afc55c5', '8ded84e7-b736-4c44-8c0d-6e32b9fe4962'], ['CPU', 'Memory', 'Network', 'Volume'], '2015-07-06 8:0:0', '2015-07-07 8:0:0'), indent=2))
