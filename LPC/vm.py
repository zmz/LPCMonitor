from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from LPC.integration.DBUtil import DBUtil
from LPC.integration.api_proxy import OpenStackPrdRequester
from LPC.models import instances, project

__author__ = 'teddy'
from django.shortcuts import render, render_to_response
from integration import  mysql_connector
from django.http import HttpResponse
import json


def zone_init(request):
    requester = OpenStackPrdRequester()
    zoneList=requester.get_zone_list();
    return HttpResponse(json.dumps(zoneList))

def testDb(request):
    # instancesList=instances.objects.filter(project_id='f7ed332ed82f40a5a7b42f853399e162')
    # resultList=[]
    # instance={}
    # for inst in instancesList:
    #     instance['project_id']=inst.project_id
    #     instance['display_name']=inst.display_name
    #     resultList.append(instance)
    # print resultList

    proList=project.objects.all().using('keystone').filter(enabled='1')
    return HttpResponse(json.dumps(proList))



def vm_search(request):
    '''
    1 handle request parms
    2 select search
    3 return json
    :param request:
    :return:
    '''

    page=1
    rows=10
    vname=''
    hostname=''

    if request.GET.has_key('page'):
        page=int(request.GET['page']);
    if   request.POST.has_key('page'):
        page=int(request.POST['page']);
    if request.GET.has_key('rows'):
        rows=int(request.GET['rows']);
    if   request.POST.has_key('rows'):
        rows=int(request.POST['rows']);

    if request.GET.has_key('vname'):
            vname=request.GET['vname'];
    if   request.POST.has_key('vname'):
            vname=request.POST['vname'];

    if request.GET.has_key('hostname'):
            hostname=request.GET['hostname'];
    if   request.POST.has_key('hostname'):
            hostname=request.POST['hostname'];
    print(hostname+vname+'--------'+str(rows))

    total=0
    total=mysql_connector.findVmsByVnameHostnameForCount(vname,hostname);
    print '---------------'+str(total)+'-----'+str(page)+'----'+str(rows)

    offset = (page-1)*rows
    print '+++++++++++'+str(offset)

    # pageCount=total%rows+1
    # if page>=pageCount:
    #     offset = (page-1)*rows;
    # else:
    #     offset = (page-1)*rows;

    converted_list=mysql_connector.findVmsByVnameHostname(vname,hostname,offset,rows);

    result={}
    result["total"]=total;
    result["rows"]=converted_list;

    # print(json.dumps(result))
    return HttpResponse(json.dumps(result))

def vm_index(request):
    # context_instance          = {}
    # context_instance['hello'] = 'Hello World!'
    # return render(request, 'vmlist.html', context_instance=RequestContext(request))
    # context          = {}
    # context['hello'] = 'Hello World!'
    return render(request, 'vmlist.html')

def vm_test(request):
    # context_instance          = {}
    # context_instance['hello'] = 'Hello World!'
    # return render(request, 'vmlist.html', context_instance=RequestContext(request))
    context          = {}
    context['hello'] = 'Hello World!'
    return render(request, 'test.html', context)

def echart_demo(request):
    # context_instance          = {}
    # context_instance['hello'] = 'Hello World!'
    # return render(request, 'vmlist.html', context_instance=RequestContext(request))
    context          = {}
    context['hello'] = 'Hello World!'
    return render(request, 'echart_demo.html', context)