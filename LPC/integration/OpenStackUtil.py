__author__ = 'teddy'

from openstack import connection
auth_args = {
    'auth_url': 'http://10.120.64.50:5000/v3',
    'project_name': 'admin',
    'username': 'fopadmin',
    'password': 'YG86R-jkE',
    'region_name':'RegionOne'
}

def test():
    conn = connection.Connection(**auth_args);
    projects = conn.identity.list_projects();
    for project in projects:
        print(project)

def testa():
    page=1
    rows=10
    offset = (page-1)*rows
    print offset
if __name__ == '__main__':
    testa();