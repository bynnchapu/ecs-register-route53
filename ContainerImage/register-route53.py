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
        self.ecsClient = boto3.client('ecs', region_name=os.getenv('REGION'))
        self.ec2Resource = boto3.resource('ec2', region_name=os.getenv('REGION'))
    

    def GetTaskArn(self):
        response = self.ecsClient.list_tasks(
            cluster=os.getenv('CLUSTER'),
            serviceName=os.getenv('SERVICE'),
            desiredStatus='RUNNING'
        )
        self.taskArn = response['taskArns'][0]
        print('taskArn: ' + self.taskArn)
    
        return self.taskArn
    

    def GetTaskEni(self):
        response = self.ecsClient.describe_tasks(
            cluster=os.getenv('CLUSTER'),
            tasks=[self.taskArn]
        )
        self.eniId = response['tasks'][0]['attachments'][0]['details'][1]['value']
    
        return self.eniId


    def GetPublicIpFromEni(self):
        eniInfo = self.ec2Resource.NetworkInterface(self.eniId)
        self.publicIp = eniInfo.association_attribute['PublicIp']
        print('PublicIp: ' + self.publicIp)

        return self.publicIp


def scheduled_routine():
    ecsTaskIp = EcsTaskIp()
    ecsTaskIp.GetTaskArn()
    ecsTaskIp.GetTaskEni()
    ecsTaskIp.GetPublicIpFromEni()


def main():
    print('Process Started.')
    # Run at once
    scheduled_routine()

    schedule.every().hour.do(scheduled_routine)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()