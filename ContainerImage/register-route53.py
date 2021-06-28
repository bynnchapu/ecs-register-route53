import json
import os
import boto3
import schedule
import time


def get_task_arn(client):
    response = client.list_tasks(
        cluster=os.getenv('CLUSTER'),
        serviceName=os.getenv('SERVICE'),
        desiredStatus='RUNNING'
    )
    taskArn = response['taskArns'][0]
    
    return taskArn


def get_task_eni(client, taskArn):
    response = client.describe_tasks(
        cluster=os.getenv('CLUSTER'),
        tasks=[taskArn]
    )
    eniId = response['tasks'][0]['attachments'][0]['details'][1]['value']
    
    return eniId


def get_publicip_eni(eniId):
    eniInfo = boto3.resource('ec2', region_name=os.getenv('REGION')).NetworkInterface(eniId)
    
    return eniInfo.association_attribute['PublicIp']


def scheduled_routine(client):
    taskArn = get_task_arn(client)
    print('taskArn: ' + taskArn)
    
    eniId = get_task_eni(client, taskArn)
    print('eniId: ' + eniId)
    
    publicIp = get_publicip_eni(eniId)
    print('Public IP: ' + publicIp)



def main():
    print('Process Started.')
    client = boto3.client('ecs', region_name=os.getenv('REGION'))
    schedule.every().hour.do(scheduled_routine, client=client)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()