import json
import os
import boto3
import schedule
import time


class EcsTaskIp:
    _ecsClient = None
    _ec2Resource = None
    taskArn = None
    eniId = None
    publicIp = None

    def __init__(self):
        self._ecsClient = boto3.client('ecs', region_name=os.getenv('REGION'))
        self._ec2Resource = boto3.resource('ec2', region_name=os.getenv('REGION'))
    

    def _GetTaskArn(self):
        response = self._ecsClient.list_tasks(
            cluster=os.getenv('CLUSTER'),
            serviceName=os.getenv('SERVICE'),
            desiredStatus='RUNNING'
        )
        self.taskArn = response['taskArns'][0]
        print('taskArn: ' + self.taskArn)
    
        return self.taskArn
    

    def _GetTaskEni(self):
        response = self._ecsClient.describe_tasks(
            cluster=os.getenv('CLUSTER'),
            tasks=[self.taskArn]
        )
        self.eniId = response['tasks'][0]['attachments'][0]['details'][1]['value']
    
        return self.eniId


    def _GetPublicIpFromEni(self):
        eniInfo = self._ec2Resource.NetworkInterface(self.eniId)
        self.publicIp = eniInfo.association_attribute['PublicIp']
        print('PublicIp: ' + self.publicIp)

        return self.publicIp
    

    def GetPublicIp(self):
        self._GetTaskArn()
        self._GetTaskEni()
        self._GetPublicIpFromEni()


class Route53Update:
    _route53Client = None

    def __init__(self):
        self._route53Client = boto3.client('route53')
    

    def UpdateZone(self, resource):
        return self._route53Client.change_resource_record_sets(
            HostedZoneId=os.getenv('HOSTED_ZONE'),
            ChangeBatch={
                'Changes': [
                    {
                        'ACTION': 'UPSERT',
                        'ResourceRecordSet': [
                            {
                                'Name': os.getenv('RECORD_NAME'),
                                'TYPE': 'A',
                                'TTL': 300,
                                'ResourceRecords': [
                                    {
                                        'Value': resource
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        )


def scheduled_routine():
    ecsTaskIp = EcsTaskIp()
    ecsTaskIp.GetPublicIp()
    
    route53Update = Route53Update()
    route53Update.UpdateZone(ecsTaskIp.publicIp)


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