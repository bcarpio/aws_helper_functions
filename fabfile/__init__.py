from boto.iam.connection import IAMConnection
from fabric.api import *
from fabric.operations import local
from fabric.colors import *
from config import *

def get_config():
    parser = SafeConfigParser()
    config = os.path.join(os.path.dirname(__file__),"../conf/config.ini")
    parser.read(config)
    access_key = parser.get('aws', 'access_key')
    secret_key = parser.get('aws', 'secret_key')
    return {'access_key':access_key,'secret_key':secret_key}

def get_region():
    config = get_config()
    cmd_parser = argparse.ArgumentParser(description='Get Instance List')
    cmd_parser.add_argument('-r', '--region', dest='region', help='AWS Region', required=True)
    args = cmd_parser.parse_args()
    return {'region':args.region,'access_key':config['access_key'],'secret_key':config['secret_key']}

def ec2_connect(region):
    config = get_config()
    conn = connect_to_region(region,aws_access_key_id=config['access_key'],aws_secret_access_key=config['secret_key'])
    return conn

@task
def get_instance_list(region):
    conn = ec2_connect(region)
    instances = conn.get_all_instances()
    for instance in instances:
        if 'Name' in instance.instances[0].__dict__['tags']:
            name = instance.instances[0].__dict__['tags']['Name']
        if 'Environment' in instance.instances[0].__dict__['tags']:
            environment = instance.instances[0].__dict__['tags']['Environment']
        elif 'environment' in instance.instances[0].__dict__['tags']:
            environment = instance.instances[0].__dict__['tags']['environment']
        else:
            environment = "None"
        print name+","+environment

@task
def get_iam_users():
    config = get_config()
    conn = IAMConnection(config['access_key'],config['secret_key'])
    users = conn.get_all_users()
    for user in users['list_users_response']['list_users_result']['users']:
        print user['user_name']+","+user['create_date']

@task
def get_host_name(region,id):
    conn = ec2_connect(region)
    instances = conn.get_all_instances()
    for instance in instances:
        if id == instance.instances[0].id:
            print instance.instances[0].__dict__['tags']['Name']
            break
