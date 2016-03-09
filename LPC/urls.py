from LPC.vm_perf import perf_project_init, vmperf_index, perf_searchVmByProject, perf_searchStaticByVm, \
    perf_searchVolumeStatic, mysqldbtest, perf_searchNetworkStatic, vmperf_byhost, perf_searchVmByHost, \
    perf_searchResource
from LPC.vm_topperf import  findTopPerfStatics, vmtopperf_index

__author__ = 'teddy'
from django.conf.urls import include, url
from LPC.views import index
from LPC.vm import  vm_index, vm_search, vm_test, zone_init, testDb, echart_demo

urlpatterns = [
    url(r'^index',index),
    url(r'^vm_index',vm_index),
    url(r'^vm_search',vm_search),
    url(r'^vm_test',vm_test),
    url(r'^zone_init',zone_init),
    url(r'^findTopPerfStatics',findTopPerfStatics),
    url(r'^testDb',testDb),
    url(r'^vmperf_index',vmperf_index),
    url(r'^vmtopperf_index',vmtopperf_index),
    url(r'^perf_project_init',perf_project_init),
    url(r'^perf_searchVmByProject',perf_searchVmByProject),
    url(r'^echart_demo',echart_demo),
    url(r'^perf_searchStaticByVm',perf_searchStaticByVm),
    url(r'^perf_searchVolumeStatic',perf_searchVolumeStatic),
    url(r'^perf_searchNetworkStatic',perf_searchNetworkStatic),

    url(r'^vmperf_byhost',vmperf_byhost),
    url(r'^perf_searchVmByHost',perf_searchVmByHost),
    url(r'^perf_searchResource',perf_searchResource),




    url(r'^mysqldbtest',mysqldbtest),











]