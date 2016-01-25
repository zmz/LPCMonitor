#coding:utf-8

import json
import datetime
from django.http import HttpResponse
from django.shortcuts import render
from LPC.integration.DateTimeUtil import DateTimeUtil
from LPC.integration.MongoEngineUtil import MongoEngineUtil
from LPC.models import project, instances, volumes

__author__ = 'teddy'


def perf_project_init(request):
    proList=project.objects.all().using('keystone').filter(enabled='1')
    resultList=[]
    tmpDict={}
    for pro in proList:
        tmpDict['id']=pro.id
        tmpDict['name']=pro.name
        resultList.append(tmpDict)
        tmpDict={}

    return HttpResponse(json.dumps(resultList))


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
