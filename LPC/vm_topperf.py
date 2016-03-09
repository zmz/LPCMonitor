import decimal
import json
import datetime
from django.db.models.base import ModelState
from django.http import HttpResponse
from django.shortcuts import render
from LPC.integration.DateTimeUtil import DateTimeUtil
from LPC.integration.MongoEngineUtil import MongoEngineUtil
from LPC.integration.api_proxy import OpenStackPrdRequester
from LPC.models import project, instances, images, volumes

__author__ = 'teddy'


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            if obj.utcoffset() is not None:
                obj = obj - obj.utcoffset()
                return obj.strftime('%Y-%m-%d %H:%M:%S')
            return str(obj)
        elif hasattr(obj, 'isoformat'):
            return obj.isoformat()
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        elif isinstance(obj, ModelState):
            return None
        else:
            return json.JSONEncoder.default(self, obj)

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

    bdt=str
    if request.GET.has_key('bdt'):
        bdt=request.GET['bdt'];
    if   request.POST.has_key('bdt'):
        bdt=request.POST['bdt'];


    edt=str
    if request.GET.has_key('edt'):
        edt=request.GET['edt'];
    if   request.POST.has_key('edt'):
        edt=request.POST['edt'];


    counter_name='cpu_util'
    if request.GET.has_key('counter_name'):
        counter_name=request.GET['counter_name'];
    if   request.POST.has_key('counter_name'):
        counter_name=request.POST['counter_name'];

    order='aesc'
    if request.GET.has_key('order'):
        order=request.GET['order'];
    if   request.POST.has_key('order'):
        order=request.POST['order'];

    sortby='avg'
    if request.GET.has_key('sortby'):
        sortby=request.GET['sortby'];
    if   request.POST.has_key('sortby'):
        sortby=request.POST['sortby'];

    limit=10
    if request.GET.has_key('limit'):
        limit=request.GET['limit'];
    if   request.POST.has_key('limit'):
        limit=request.POST['limit'];


    print counter_name
    print order
    print sortby
    print limit


    # str = '2016-01-11'
    bdtime = datetime.datetime.strptime(bdt,'%Y-%m-%d')
    edtime = datetime.datetime.strptime(edt,'%Y-%m-%d')


    #get record count
    staticsList=MongoEngineUtil.findLimitStaticsByTimestampAndCounter_name(bdtime,edtime,counter_name,int(limit),order,sortby)
    perfList=[]
    tmpStat={}
    for stat in staticsList:


        #counter name is network.incoming.bytes.rate
        # instance-0000322e-3f6c30d6-e029-49c6-ab20-aa502fdbe557-tape7c7968e-bf
        uuid = stat.resource_id
        if counter_name.__contains__('network'):
            uuid=stat.resource_id[18:54]
        elif counter_name.__contains__('volume'):
            volList=volumes.objects.all().using('cinder').filter(id=stat.resource_id)
            if volList:
                uuid=volList[0].instance_uuid

        # print(uuid)
        res=MongoEngineUtil.findResourcesById(uuid)
        #get instance info
        insList=instances.objects.all().filter(uuid=uuid)
        if insList:
            tmpStat['vm_state']=insList[0].vm_state
            tmpStat['launched_at']=insList[0].launched_at
            tmpStat['scheduled_at']=insList[0].scheduled_at
            tmpStat['terminated_at']=insList[0].terminated_at
            tmpStat['vcpus']=insList[0].vcpus
            tmpStat['memory_mb']=insList[0].memory_mb
            tmpStat['host']=insList[0].host
            tmpStat['root_gb']=insList[0].root_gb

            image=images.objects.all().using('glance').filter(id=insList[0].image_ref)
            print(image)
            if image:
                tmpStat['image']=image[0].name
            else:
                tmpStat['image']='null'


            proList=project.objects.all().using('keystone').filter(id=insList[0].project_id)
            if proList:
                tmpStat['project_name']=proList[0].name

        tmpStat['resource_name']=res.resource_name
        tmpStat['counter_name']=stat.counter_name
        tmpStat['counter_name']=stat.counter_name
        tmpStat['resource_id']=stat.resource_id
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
    return HttpResponse(json.dumps(result,cls = DateTimeEncoder))


def vmtopperf_index(request):
    # context_instance          = {}
    # context_instance['hello'] = 'Hello World!'
    # return render(request, 'vmlist.html', context_instance=RequestContext(request))
    # context          = {}
    # context['hello'] = 'Hello World!'
    return render(request, 'vm_top_perf.html')
