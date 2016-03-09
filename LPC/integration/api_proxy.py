__author__ = 'zhangxg'

from abc import ABCMeta, abstractmethod
from httplib import HTTPConnection, HTTPException
from urlparse import urlparse
import json
import re


class APIEndpointsInterface:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def get_token(self):
        pass

    @abstractmethod
    def get_all_projects(self):
        pass

    @abstractmethod
    def get_all_vms(self):
        pass

    @abstractmethod
    def get_port_list(self):
        pass

    @abstractmethod
    def get_image_list(self):
        pass

    @abstractmethod
    def get_flavor_list(self):
        pass

    @abstractmethod
    def get_zone_list(self):
        pass


class OpenStackPrdRequester(APIEndpointsInterface):
    """ a class connection to production api"""
    # config = {
    #     'endpoint_port': 5000,
    #     'endpoint_ip': '10.120.64.50',
    #     'user_name': 'fopadmin',
    #     'user_password': 'YG86R-jkE',
    #     'tenant_name': 'admin'
    # }

    config = {
        'endpoint_port': 5000,
        'endpoint_ip': '10.120.20.1',
        'user_name': 'fopadmin',
        'user_password': 'YG86R-jkE1234',
        'tenant_name': 'admin'
    }

    url_root = 'http://' + config['endpoint_ip'] + ':' + str(config['endpoint_port'])

    base_header = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    def __init__(self):
        pass

    @staticmethod
    def get_token():
        url = OpenStackPrdRequester.url_root + '/v2.0/tokens'
        body = {"auth": {"tenantName": OpenStackPrdRequester.config['tenant_name'],
                         "passwordCredentials": {"username": OpenStackPrdRequester.config['user_name'],
                                                 "password": OpenStackPrdRequester.config['user_password']}}}
        return OpenStackPrdRequester.__request('POST', url, body, OpenStackPrdRequester.base_header)




    @staticmethod
    def get_zone_list():
        """
        [
        {value:''
        text:''
        group:''},{}]

        :return:
        """
        token = OpenStackPrdRequester.get_token()
        print("----------------token-----------------"+str(token))
        service_catalog = OpenStackPrdRequester.__make_service_catalog(token)
        url = service_catalog['nova']['endpoints'][0]['adminURL']
        url = OpenStackPrdRequester.__make_endpoint_ip(url) + '/os-availability-zone/detail'
        OpenStackPrdRequester.__make_base_header_token(token)
        zoneList= OpenStackPrdRequester.__request('GET', url, None, OpenStackPrdRequester.base_header)
        print(zoneList)
        zoneResult = []
        tmpDict={}
        for i, zone in enumerate(zoneList['availabilityZoneInfo']):
            print i, zone
            if zone['zoneName']=='internal':
                continue

            for  host  in  zone['hosts'].keys():
                tmpDict['group']=zone['zoneName']
                tmpDict['value']=host
                tmpDict['text']=host
                zoneResult.append(tmpDict)
                tmpDict={};


        return zoneResult


    @staticmethod
    def get_all_projects():
        token = OpenStackPrdRequester.get_token()
        service_catalog = OpenStackPrdRequester.__make_service_catalog(token)
        url = service_catalog['keystone']['endpoints'][0]['adminURL']
        url = OpenStackPrdRequester.__make_endpoint_ip(url) + '/tenants'
        OpenStackPrdRequester.__make_base_header_token(token)
        return OpenStackPrdRequester.__request('GET', url, None, OpenStackPrdRequester.base_header)

    @staticmethod
    def get_all_vms():
        token = OpenStackPrdRequester.get_token()
        service_catalog = OpenStackPrdRequester.__make_service_catalog(token)
        url = service_catalog['nova']['endpoints'][0]['adminURL']
        url = OpenStackPrdRequester.__make_endpoint_ip(url) + '/servers/detail?all_tenants=1'
        OpenStackPrdRequester.__make_base_header_token(token)
        return OpenStackPrdRequester.__request('GET', url, None, OpenStackPrdRequester.base_header)

    @staticmethod
    def get_port_list():
        token = OpenStackPrdRequester.get_token()
        service_catalog = OpenStackPrdRequester.__make_service_catalog(token)
        url = service_catalog['neutron']['endpoints'][0]['adminURL']
        url = OpenStackPrdRequester.__make_endpoint_ip(url) + '/v2.0/ports.json'
        OpenStackPrdRequester.__make_base_header_token(token)
        return OpenStackPrdRequester.__request('GET', url, None, OpenStackPrdRequester.base_header)

    @staticmethod
    def get_image_list():
        token = OpenStackPrdRequester.get_token()
        service_catalog = OpenStackPrdRequester.__make_service_catalog(token)
        url = service_catalog['nova']['endpoints'][0]['adminURL']
        url = OpenStackPrdRequester.__make_endpoint_ip(url) + '/images/detail'
        OpenStackPrdRequester.__make_base_header_token(token)
        return OpenStackPrdRequester.__request('GET', url, None, OpenStackPrdRequester.base_header)

    @staticmethod
    def get_flavor_list():
        token = OpenStackPrdRequester.get_token()
        service_catalog = OpenStackPrdRequester.__make_service_catalog(token)
        url = service_catalog['nova']['endpoints'][0]['adminURL']
        url = OpenStackPrdRequester.__make_endpoint_ip(url) + '/flavors/detail'
        OpenStackPrdRequester.__make_base_header_token(token)
        return OpenStackPrdRequester.__request('GET', url, None, OpenStackPrdRequester.base_header)

    @staticmethod
    def __make_service_catalog(token):
        """ a help method to build the service catalogue, in the format of key-value, data is from the token"""
        service_catalog = {}
        for service in token['access']['serviceCatalog']:
            service_catalog.__setitem__(service['name'], {
                'type': service['type'],
                'endpoints': service['endpoints']
            })
        return service_catalog

    @staticmethod
    def __make_endpoint_ip(url):
        """ a help method to do the ip replacement"""
        ips = re.findall('(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})', url)
        return url.replace(ips[0], OpenStackPrdRequester.config['endpoint_ip'])

    @staticmethod
    def __make_base_header_token(token):
        OpenStackPrdRequester.base_header['X-Auth-Token'] = token['access']['token']['id']

    @staticmethod
    def __get_connection(url):
        parsed_url = urlparse(url)
        return HTTPConnection(parsed_url.hostname, parsed_url.port, {'timeout': 30})

    @staticmethod
    def __request(method, url, body, header):
        connection = OpenStackPrdRequester.__get_connection(url)
        try:
            if body:
                body = json.dumps(body)
            connection.request(method, url, body, header)
            response = connection.getresponse()

            if response.status > 299:
                return False

            return json.loads(response.read())
        except HTTPException, e:
            raise e
        finally:
            connection.close()


class FileStubRequester(APIEndpointsInterface):
    data_folder = '/home/zhangxg/work/temp/OpenstackData/'

    def __init__(self):
        pass

    @staticmethod
    def get_token():
        pass

    @staticmethod
    def get_all_projects():
        file_name = FileStubRequester.data_folder + 'prod-projects-list'
        return json.load(open(file_name, 'r'))

    @staticmethod
    def get_all_vms():
        file_name = FileStubRequester.data_folder + 'prod-vm-list'
        return json.load(open(file_name, 'r'))

    @staticmethod
    def get_port_list():
        file_name = FileStubRequester.data_folder + 'prod-port-list'
        return json.load(open(file_name, 'r'))

    @staticmethod
    def get_image_list():
        file_name = FileStubRequester.data_folder + 'prod-image-list'
        return json.load(open(file_name, 'r'))

    @staticmethod
    def get_flavor_list():
        file_name = FileStubRequester.data_folder + 'prod-flavor-list'
        return json.load(open(file_name, 'r'))


if __name__ == "__main__":
    # requester = FileStubRequester()
    requester = OpenStackPrdRequester()
    # requester.get_token()
    # project_list={};
    # project_list=requester.get_all_projects()
    # for project in project_list['tenants']:
    # print(project['name'])
    # requester.get_all_vms()

    zoneList=requester.get_zone_list();
    print(zoneList)


    # projectList=requester.get_all_projects()
    # print(projectList)
    # for project in projectList['tenants']:
    #     print(project['id']+' '+project['name'])



    # zoneList = requester.get_zone_list()
    # zoneResult = {};
    # tmpList=[];
    # for i, zone in enumerate(zoneList['availabilityZoneInfo']):
    #     print i, zone
    #     zoneResult[zone['zoneName']]=zone['zoneName'];
    #     for  host  in  zone['hosts'].keys():
    #         tmpList.append(host)
    #     zoneResult[zone['zoneName']]=tmpList
    #     tmpList=[];
    # print(zoneResult)

    # for zone in zoneList['availabilityZoneInfo']:
    #     print(zone['zoneName'])
    #     zoneResult.append(zone['zoneName'])
    # print(zone['hosts'])

    # zoneResult[zone['zoneName']]=zone['zoneName']
    # for  host  in  zone['hosts'].keys():
    #     print(host)
    # zoneResult[zone['zoneName']][host]=host;
    # print(zoneResult)

    # print(json.dump(requester.get_token(), open('/home/zhangxg/work/temp/production_token.json', 'w+'), indent=2))
    # print(json.dump(requester.get_all_projects(), open('/home/zhangxg/work/temp/production_all_projects.json', 'w+'), indent=2))
    # print(json.dump(requester.get_all_vms(), open('/home/zhangxg/work/temp/production_all_vms.json', 'w+'), indent=2))
    # print(json.dump(requester.get_port_list(), open('/home/zhangxg/work/temp/production_all_port_list.json', 'w+'), indent=2))
