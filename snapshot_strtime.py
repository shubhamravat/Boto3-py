import boto3
import csv
aws_mag_console=boto3.session.Session()
ec2_con_cli=aws_mag_console.client("ec2")
count=1
filt1={
            'Name': 'status',
            'Values': [
                'completed',
            ]
        }
response = ec2_con_cli.describe_snapshots(Filters=[filt1],OwnerIds=["532102821576"])   
print(response)
for each_in in response['Snapshots']:
        #print(each_in)
        print(each_in['StartTime'])
        print(count,each_in['SnapshotId'],each_in['VolumeId'],each_in['VolumeSize'])