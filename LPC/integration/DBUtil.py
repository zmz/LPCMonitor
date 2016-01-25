from LPC.models import instances

__author__ = 'teddy'

class DBUtil:
    def __init__(self):
        pass
    @staticmethod
    def findInstanceByProjectId(project_id):
        instancesList=instances.objects(project_id=project_id)
        return  instancesList

if __name__ == '__main__':
    instancesList=instances.objects.filter(project_id='f7ed332ed82f40a5a7b42f853399e162')
    resultList=[]
    instance={}
    for inst in instancesList:
        instance['project_id']=inst.project_id
        instance['display_name']=inst.display_name
        resultList.append(instance)
    print resultList