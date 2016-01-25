#coding:utf-8
from json import JSONEncoder

__author__ = 'teddy'
class Series(JSONEncoder):

    name=''
    type=''
    data=[int]
class EchartData(JSONEncoder):
    #数据分组
    legends=[]
    #横坐标
    category=[]
    #纵坐标
    series=[Series]
