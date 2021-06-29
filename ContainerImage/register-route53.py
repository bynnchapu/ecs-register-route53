import json
import os
import boto3
import schedule
import time


class EcsTaskIp:
    ecsClient = None
    ec2Client = None
    taskArn = None
    eniId = None
    publicIp = None

    def __init__(self):
        print('Created Class instance')
        self.ecsClient = boto3.client('ecs', region_name=os.getenv('REGION'))
        self.ec2Resource = boto3.resource('ec2', region_name=os.getenv('REGION'))
    

    def GetTaskArn(self):
        print('Called GetTaskArn function')
        response = self.ecsClient.list_tasks(
            cluster=os.getenv('CLUSTER'),
            serviceName=os.getenv('SERVICE'),
            desiredStatus='RUNNING'
        )
        self.taskArn = response['taskArns'][0]
        print('taskArn: ' + self._taskArn)
    
        return self.taskArn
    

    def GetTaskEni(self):
        print('Called GetTaskEni function')
        response = self.ecsClient.describe_tasks(
            cluster=os.getenv('CLUSTER'),
            tasks=[self.taskArn]
        )
        self.eniId = response['tasks'][0]['attachments'][0]['details'][1]['value']
    
        return self.eniId


    def GetPublicIpFromEni(self):
        print('Called GetPublicIpFromEni function')
        eniInfo = self.ec2Resource.NetworkInterface(self.eniId)
        self.publicIp = association_attribute['PublicIp']
        print('PublicIp: ' + self.publicIp)

        return self.publicIp


def scheduled_routine():
    ecsTaskIp = EcsTaskIp()
    ecsTaskIp.GetTaskArn()
    ecsTaskIp.GetTaskEni()
    ecsTaskIp.GetPublicIpFromEni()


def main():
    print('Process Started.')
    schedule.every().hour.do(scheduled_routine)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()