# get list of ec2 details  like ID , its state and when it was launched

import boto3
aws_mag_console=boto3.session.Session()
ec2_con_cli=aws_mag_console.client("ec2")
response=ec2_con_cli.describe_instances()['Reservations']
for each_item in response:
    for each_instances in each_item['Instances']:
        print(each_instances['PlatformDetails'])
        #print(each_instances['InstanceId'])
        #print(each_instances['State'])
        #print(each_instances['LaunchTime'])
        print("instance id is :{}\n state of instance is:{}\n launch time of instance is:{}".format(each_instances['InstanceId'],each_instances['State']['Name'],each_instances['LaunchTime']))