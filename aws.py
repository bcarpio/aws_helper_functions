import boto
from boto.ec2 import *
import argparse
import sys, os
from ConfigParser import SafeConfigParser

def get_config():
    parser = SafeConfigParser()
    config = os.path.join(os.path.dirname(__file__),"./config.ini")
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

def ec2_connect():
    config = get_region()
    conn = connect_to_region(config['region'],aws_access_key_id=config['access_key'],aws_secret_access_key=config['secret_key'])
    return conn

def get_instance_list():
    conn = ec2_connect()
    instances = conn.get_all_instances(max_results='1000')
    print len(instances)
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

if __name__ == "__main__":
    get_instance_list()
