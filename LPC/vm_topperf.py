import json
import datetime
from django.http import HttpResponse
from django.shortcuts import render
from LPC.integration.DateTimeUtil import DateTimeUtil
from LPC.integration.MongoEngineUtil import MongoEngineUtil
from LPC.integration.api_proxy import OpenStackPrdRequester
from LPC.models import project

__author__ = 'teddy'



def findPerfStatics(request):

    counter_name='cpu_util'
    if request.GET.has_key('counter_name'):
        counter_name=request.GET['counter_name'];
    if   request.POST.has_key('counter_name'):
        counter_name=request.POST['counter_name'];
    print counter_name
    #paging prepare
    page=1
    if request.GET.has_key('page'):
        page=request.GET['page'];
    if   request.POST.has_key('page'):
        page=request.POST['page'];
    rows=10
    if request.GET.has_key('rows'):
        rows=request.GET['rows'];
    if   request.POST.has_key('rows'):
        rows=request.POST['rows'];


    str = '2016-01-11'
    timestamp = datetime.datetime.strptime(str,'%Y-%m-%d')
    # counter_name='cpu_util'

    #get record count
    count=MongoEngineUtil.findStaticsCountByTimestampAndCounter_name(timestamp,counter_name)
    staticsList=MongoEngineUtil.findLimitStaticsByTimestampAndCounter_name(timestamp,counter_name,10)
    perfList=[]
    tmpStat={}
    for stat in staticsList:
        tmpStat['resource_name']=stat.resource_id.resource_name
        tmpStat['counter_name']=stat.counter_name
        tmpStat['counter_name']=stat.counter_name
        tmpStat['resource_id']=stat.resource_id.id
        tmpStat['timestamp']=datetime.datetime.strftime(stat.timestamp,'%Y-%m-%d %H:%M:%S')
        tmpStat['avg']=stat.avg
        tmpStat['unit']=stat.unit
        tmpStat['count']=stat.count
        tmpStat['max']=stat.max
        tmpStat['user_id']=stat.user_id
        tmpStat['val']=stat.val
        tmpStat['min']=stat.min
        tmpStat['sum']=stat.sum
        tmpStat['period_start']=datetime.datetime.strftime(stat.period_start,'%Y-%m-%d %H:%M:%S')
        tmpStat['period_end']=datetime.datetime.strftime(stat.period_end,'%Y-%m-%d %H:%M:%S')
        perfList.append(tmpStat)
        tmpStat={}
    result={}
    result["total"]=count;
    result["rows"]=perfList;
    # print(json.dumps(result))
    return HttpResponse(json.dumps(result))


def findTopPerfStatics(request):

    tmpDate=DateTimeUtil.dayBefore(7);
    str=DateTimeUtil.datetime_toString(tmpDate,"%Y-%m-%d")
    # str = '2016-01-11'
    timestamp = datetime.datetime.strptime(str,'%Y-%m-%d')

    counter_name='cpu_util'
    if request.GET.has_key('counter_name'):
        counter_name=request.GET['counter_name'];
    if   request.POST.has_key('counter_name'):
        counter_name=request.POST['counter_name'];
    print counter_name

    #get record count
    staticsList=MongoEngineUtil.findLimitStaticsByTimestampAndCounter_name(timestamp,counter_name,10)
    perfList=[]
    tmpStat={}
    for stat in staticsList:
        res=MongoEngineUtil.findResourcesById(stat.resource_id)
        tmpStat['resource_name']=res.resource_name
        tmpStat['counter_name']=stat.counter_name
        tmpStat['counter_name']=stat.counter_name
        tmpStat['resource_id']=res.id
        tmpStat['timestamp']=datetime.datetime.strftime(stat.timestamp,'%Y-%m-%d %H:%M:%S')
        tmpStat['avg']=stat.avg
        tmpStat['unit']=stat.unit
        tmpStat['count']=stat.count
        tmpStat['max']=stat.max
        tmpStat['user_id']=stat.user_id
        tmpStat['val']=stat.val
        tmpStat['min']=stat.min
        tmpStat['sum']=stat.sum
        tmpStat['period_start']=datetime.datetime.strftime(stat.period_start,'%Y-%m-%d %H:%M:%S')
        tmpStat['period_end']=datetime.datetime.strftime(stat.period_end,'%Y-%m-%d %H:%M:%S')
        perfList.append(tmpStat)
        tmpStat={}
    result={}
    result["total"]=result.__len__();
    result["rows"]=perfList;

    # print(json.dumps(result))
    return HttpResponse(json.dumps(result))


def vmtopperf_index(request):
    # context_instance          = {}
    # context_instance['hello'] = 'Hello World!'
    # return render(request, 'vmlist.html', context_instance=RequestContext(request))
    # context          = {}
    # context['hello'] = 'Hello World!'
    return render(request, 'vm_top_perf.html')
