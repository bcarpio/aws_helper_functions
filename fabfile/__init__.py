from boto.iam.connection import IAMConnection
from fabric.api import *
from fabric.operations import local
from fabric.colors import *
from config import *

@task
def get_instance_list(region):
    """ Requires: Region"""
    conn = ec2_connect(region)
    instances = conn.get_all_instances()
    for instance in instances:
        if 'Name' in instance.instances[0].__dict__['tags']:
            print instance.instances[0].__dict__['tags']['Name']

@task
def get_iam_users():
    """Requires: none """
    config = get_config()
    conn = IAMConnection(config['access_key'],config['secret_key'])
    users = conn.get_all_users()
    for user in users['list_users_response']['list_users_result']['users']:
        print user['user_name']+","+user['create_date']

@task
def get_host_name(region,id):
    """ Requires: region and instance_id """
    conn = ec2_connect(region)
    instances = conn.get_all_instances()
    for instance in instances:
        if id == instance.instances[0].id:
            print instance.instances[0].__dict__['tags']['Name']
            break
