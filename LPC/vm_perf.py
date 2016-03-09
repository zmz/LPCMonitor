#coding:utf-8
import decimal

import json
import datetime
from bson import json_util
from django.db.models.base import ModelState
from django.http import HttpResponse
from django.shortcuts import render
from LPC.integration.DateTimeUtil import DateTimeUtil
from LPC.integration.MongoEngineUtil import MongoEngineUtil
from LPC.models import project, instances, volumes, images

__author__ = 'teddy'


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            if obj.utcoffset() is not None:
                obj = obj - obj.utcoffset()
                return obj.strftime('%Y-%m-%d %H:%M:%S.%f')
            return str(obj)
        elif hasattr(obj, 'isoformat'):
            return obj.isoformat()
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        elif isinstance(obj, ModelState):
            return None
        else:
            return json.JSONEncoder.default(self, obj)

def perf_project_init(request):
    proList=project.objects.all().using('keystone').filter(enabled='1')
    resultList=[]
    tmpDict={}
    for pro in proList:
        tmpDict['id']=pro.id
        tmpDict['name']=pro.name
        tmpDict['name_lower_case']=pro.name.lower()

        resultList.append(tmpDict)
        tmpDict={}

    return HttpResponse(json.dumps(resultList))


def perf_searchResource(request):
    resource_id=''
    if request.GET.has_key('resource_id'):
        resource_id=request.GET['resource_id'];
    if   request.POST.has_key('resource_id'):
        resource_id=request.POST['resource_id'];
    insList=instances.objects.all().filter(uuid=resource_id)
    resultList=[]
    instance={}
    '''
    {"total":7,"rows":[
	{"name":"Name","value":"Bill Smith","group":"ID Settings","editor":"text"},
	{"name":"Address","value":"","group":"ID Settings","editor":"text"},
	{"name":"Age","value":"40","group":"ID Settings","editor":"numberbox"},
	{"name":"Birthday","value":"01/02/2012","group":"ID Settings","editor":"datebox"},
	{"name":"SSN","value":"123-456-7890","group":"ID Settings","editor":"text"},
	{"name":"Email","value":"bill@gmail.com","group":"Marketing Settings","editor":{
		"type":"validatebox",
		"options":{
			"validType":"email"
		}
	}},
	{"name":"FrequentBuyer","value":"false","group":"Marketing Settings","editor":{
		"type":"checkbox",
		"options":{
			"on":true,
			"off":false
		}
	}}
]}
    '''
    for inst in insList:
        instance['name']='display_name'
        instance['value']=inst.display_name
        instance['group']=inst.display_name
        resultList.append(instance)

        instance={}
        instance['name']='vcpus'
        instance['value']=inst.vcpus
        instance['group']=inst.display_name
        resultList.append(instance)

        instance={}
        instance['name']='memory_mb'
        instance['value']=inst.memory_mb
        instance['group']=inst.display_name
        resultList.append(instance)

        instance={}
        instance['name']='launched_at'
        instance['value']=inst.launched_at
        instance['group']=inst.display_name
        resultList.append(instance)

        instance={}
        instance['name']='scheduled_at'
        instance['value']=inst.scheduled_at
        instance['group']=inst.display_name
        resultList.append(instance)

        instance={}
        instance['name']='root_gb'
        instance['value']=inst.root_gb
        instance['group']=inst.display_name
        resultList.append(instance)

        instance={}
        instance['name']='vm_state'
        instance['value']=inst.vm_state
        instance['group']=inst.display_name
        resultList.append(instance)

        instance={}
        instance['name']='user_id'
        instance['value']=inst.user_id
        instance['group']=inst.display_name
        resultList.append(instance)

        instance={}
        instance['name']='host'
        instance['value']=inst.host
        instance['group']=inst.display_name
        resultList.append(instance)



        instance={}
        proList=project.objects.all().using('keystone').filter(id=inst.project_id)
        if proList:
            instance['name']='project_name'
            instance['value']=proList[0].name
            instance['group']=inst.display_name
            resultList.append(instance)

        instance={}
        instance['name']='image'
        print(inst.image_ref)
        image=images.objects.all().using('glance').filter(id=inst.image_ref)
        print(image)
        if image:
            instance['value']=image[0].name
        else:
            instance['value']='null'

        instance['group']=inst.display_name
        resultList.append(instance)


        instance={}

    print resultList

    result={}
    result["total"]=len(resultList);
    result["rows"]=resultList;

    return HttpResponse(json.dumps(result,cls = DateTimeEncoder))


def perf_searchNetworkStatic(request):
    resource_id=''
    if request.GET.has_key('resource_id'):
        resource_id=request.GET['resource_id'];
    if   request.POST.has_key('resource_id'):
        resource_id=request.POST['resource_id'];

    counter_name='cpu_util'
    if request.GET.has_key('counter_name'):
        counter_name=request.GET['counter_name'];
    if   request.POST.has_key('counter_name'):
        counter_name=request.POST['counter_name'];

    print(counter_name)

    tmpDate=DateTimeUtil.dayBefore(7);

    result={}
    catagories=[]
    series=[]
    tmpMax={}
    tmpMaxList=[]
    # tmpMin={}
    # tmpMinList=[]
    # tmpAvg={}
    # tmpAvgList=[]

    statList=MongoEngineUtil.findNetworkStaticsByTimestampAndCounter_nameAndResourceId(tmpDate,counter_name,resource_id)
    for stat in statList:
        str=DateTimeUtil.datetime_toString(stat.timestamp,"%Y-%m-%d")
        catagories.append(str)
        tmpMaxList.append(stat.max)

    tmpMax['data']=tmpMaxList
    tmpMax['type']='line'
    tmpMax['name']='max'
    series.append(tmpMax)

    result['categories']=catagories
    result['series']=series


    # print(staticsList)
    return HttpResponse(json.dumps(result))



def perf_searchVolumeStatic(request):
    resource_id=''
    if request.GET.has_key('resource_id'):
        resource_id=request.GET['resource_id'];
    if   request.POST.has_key('resource_id'):
        resource_id=request.POST['resource_id'];

    counter_name='cpu_util'
    if request.GET.has_key('counter_name'):
        counter_name=request.GET['counter_name'];
    if   request.POST.has_key('counter_name'):
        counter_name=request.POST['counter_name'];

    print(counter_name)

    tmpDate=DateTimeUtil.dayBefore(7);

    result={}
    catagories=[]
    series=[]
    tmpMax={}
    tmpMaxList=[]
    # tmpMin={}
    # tmpMinList=[]
    # tmpAvg={}
    # tmpAvgList=[]

    #find volumes by instanceid
    volumeList=volumes.objects.all().using('cinder').filter(instance_uuid=resource_id)

    print(volumeList)
    tmpVolumeIds=[]
    for vol in volumeList:
        tmpVolumeIds.append(vol.id)

    statList=MongoEngineUtil.findStaticsByTimestampAndCounter_nameAndResourceId(tmpDate,counter_name,tmpVolumeIds)
    for stat in statList:
        str=DateTimeUtil.datetime_toString(stat.timestamp,"%Y-%m-%d")
        catagories.append(str)
        tmpMaxList.append(stat.max)

    tmpMax['data']=tmpMaxList
    tmpMax['type']='line'
    tmpMax['name']='max'
    series.append(tmpMax)

    result['categories']=catagories
    result['series']=series


    # print(staticsList)
    return HttpResponse(json.dumps(result))

def perf_searchStaticByVm(request):
    resource_id=''
    if request.GET.has_key('resource_id'):
        resource_id=request.GET['resource_id'];
    if   request.POST.has_key('resource_id'):
        resource_id=request.POST['resource_id'];

    print(resource_id)

    tmpDate=DateTimeUtil.dayBefore(7);

    counter_name='cpu_util'
    if request.GET.has_key('counter_name'):
        counter_name=request.GET['counter_name'];
    if   request.POST.has_key('counter_name'):
        counter_name=request.POST['counter_name'];

    print(counter_name)

    #staticsList=mongoUtil.findStaticsByTimestampAndCounter_name(timestamp,counter_name,0,10)
    # staticsList=mongoUtil.findLimitStaticsByTimestampAndCounter_name(timestamp,counter_name,1)

    # resource_id='7dcc77ae-6bc6-44fe-a24b-f6580f9fcce1'
    # res=MongoEngineUtil.findResourcesById('7dcc77ae-6bc6-44fe-a24b-f6580f9fcce1')
    # print(res)
    resList=[resource_id]
    staticsList=MongoEngineUtil.findStaticsByTimestampAndCounter_nameAndResourceId(tmpDate,counter_name,resList)

    result={}
    catagories=[]
    series=[]
    tmpMax={}
    tmpMaxList=[]
    tmpMin={}
    tmpMinList=[]
    tmpAvg={}
    tmpAvgList=[]

    for stat in staticsList:
        str=DateTimeUtil.datetime_toString(stat.timestamp,"%Y-%m-%d")
        catagories.append(str)
        tmpMaxList.append(stat.max)
        tmpMinList.append(stat.min)
        tmpAvgList.append(stat.avg)
    tmpMax['data']=tmpMaxList
    tmpMax['type']='line'
    tmpMax['name']='max'

    tmpMin['data']=tmpMinList
    tmpMin['type']='line'
    tmpMin['name']='min'

    tmpAvg['data']=tmpAvgList
    tmpAvg['type']='line'
    tmpAvg['name']='avg'

    series.append(tmpMax)
    series.append(tmpMin)
    series.append(tmpAvg)



    # result['legends']=['ggg']
    # result['categories']=[1,2,3]
    # result['series']=[55,2,45]
    # for stat in staticsList:

    result['categories']=catagories
    result['series']=series


    # print(staticsList)
    return HttpResponse(json.dumps(result))

def perf_searchVmByProject(request):
    project_id=''
    if request.GET.has_key('project_id'):
        project_id=request.GET['project_id'];
    if   request.POST.has_key('project_id'):
        project_id=request.POST['project_id'];
    print('--------------'+project_id)
    instancesList=instances.objects.filter(project_id=project_id,deleted=0)
    resultList=[]
    instance={}
    for inst in instancesList:
        instance['uuid']=inst.uuid
        instance['display_name']=inst.display_name
        resultList.append(instance)
        instance={}
    print resultList
    return HttpResponse(json.dumps(resultList))


def vmperf_byhost(request):
    # context_instance          = {}
    # context_instance['hello'] = 'Hello World!'
    # return render(request, 'vmlist.html', context_instance=RequestContext(request))
    # context          = {}
    # context['hello'] = 'Hello World!'
    return render(request, 'vm_perf_byhost.html')

def perf_searchVmByHost(request):
    host=''
    if request.GET.has_key('host'):
        host=request.GET['host'];
    if   request.POST.has_key('host'):
        host=request.POST['host'];
    print('--------------'+host)
    instancesList=instances.objects.filter(host=host,deleted=0)
    resultList=[]
    instance={}
    for inst in instancesList:
        instance['uuid']=inst.uuid
        instance['display_name']=inst.display_name
        resultList.append(instance)
        instance={}
    print resultList
    return HttpResponse(json.dumps(resultList))




def vmperf_index(request):
    # context_instance          = {}
    # context_instance['hello'] = 'Hello World!'
    # return render(request, 'vmlist.html', context_instance=RequestContext(request))
    # context          = {}
    # context['hello'] = 'Hello World!'
    return render(request, 'vm_perf.html')

def mysqldbtest(request):
    # context_instance          = {}
    # context_instance['hello'] = 'Hello World!'
    # return render(request, 'vmlist.html', context_instance=RequestContext(request))
    # context          = {}
    # context['hello'] = 'Hello World!'
    print('ggggggggg')
    volume=volumes.objects.all().using('cinder').first()
    print(volume)
    return HttpResponse(json.dumps(volume))

if __name__ == '__main__':
        insList=instances.objects.all().using('nova').filter(uuid='dbd7e993-2af4-4e7a-a5fe-dc47fe5bf360')
        print(instances)
